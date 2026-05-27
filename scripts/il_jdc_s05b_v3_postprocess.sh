#!/bin/bash
# Post-process v3 fix clips and produce final_hormozi_v2.mp4
# Sequence: clip1, clip2_v2, clip3, clip4, clip5, clip6, clip7_new, clip8_new
#
# Steps:
#   1. Voice-change new clips to match voice_id i9yTCgybojAJs64RgpvX
#   2. Loudnorm all 3 new clips
#   3. Stitch full 8-clip sequence
#   4. Watermark crop
#   5. Hormozi captions

set -e
cd /home/user/aicreative
source .env 2>/dev/null || true

OUT="outputs/il_jdc_script05_b_v2"
VOICE_ID="i9yTCgybojAJs64RgpvX"

echo "=== Step 1: Verify new clips exist ==="
for f in clip2_v2 clip7_new clip8_new; do
    size=$(stat -c%s "${OUT}/${f}.mp4" 2>/dev/null || echo 0)
    if [ "$size" -lt 100000 ]; then
        echo "ERROR: ${f}.mp4 missing or too small (${size} bytes)"
        exit 1
    fi
    echo "  ${f}.mp4: ${size} bytes ✓"
done

echo ""
echo "=== Step 2: Voice-change new clips ==="
# Extract audio from each new clip
for n in 2_v2 7_new 8_new; do
    ffmpeg -y -i "${OUT}/clip${n}.mp4" -vn -ar 44100 -ac 1 "/tmp/clip${n}_audio.mp3" 2>/dev/null
    echo "  Extracted audio for clip${n}"
done

# Voice-change via ElevenLabs
.venv/bin/python - <<'PYEOF'
import os
import sys
sys.path.insert(0, '.')
from elevenlabs_client import voice_changer

VOICE_ID = "i9yTCgybojAJs64RgpvX"
clips = ["2_v2", "7_new", "8_new"]

for n in clips:
    src = f"/tmp/clip{n}_audio.mp3"
    dst = f"/tmp/clip{n}_vc.mp3"
    print(f"  voice_changer clip{n} …", flush=True)
    voice_changer(
        src,
        VOICE_ID,
        dst,
        model_id="eleven_multilingual_sts_v2",
        stability=0.5,
        similarity_boost=0.85,
    )
    size = os.path.getsize(dst)
    print(f"  clip{n} voice-changed → {size//1024}KB")
PYEOF

echo ""
echo "=== Step 3: Merge VC audio back into clips + loudnorm ==="
for n in 2_v2 7_new 8_new; do
    # Merge VC audio
    ffmpeg -y -i "${OUT}/clip${n}.mp4" -i "/tmp/clip${n}_vc.mp3" \
        -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest \
        "/tmp/clip${n}_withvc.mp4" 2>/dev/null
    # Loudnorm
    ffmpeg -y -i "/tmp/clip${n}_withvc.mp4" \
        -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
        -c:v copy -c:a aac -b:a 192k \
        "${OUT}/clip${n}_norm.mp4" 2>/dev/null
    size=$(stat -c%s "${OUT}/clip${n}_norm.mp4")
    echo "  clip${n}_norm.mp4: ${size//1024} bytes"
done

echo ""
echo "=== Step 4: Stitch 8-clip sequence ==="
# Sequence: clip1, clip2_v2, clip3, clip4, clip5, clip6, clip7_new, clip8_new
cat > /tmp/concat_v3.txt <<EOF
file '$(pwd)/${OUT}/clip1_norm.mp4'
file '$(pwd)/${OUT}/clip2_v2_norm.mp4'
file '$(pwd)/${OUT}/clip3_norm.mp4'
file '$(pwd)/${OUT}/clip4_norm.mp4'
file '$(pwd)/${OUT}/clip5_norm.mp4'
file '$(pwd)/${OUT}/clip6_norm.mp4'
file '$(pwd)/${OUT}/clip7_new_norm.mp4'
file '$(pwd)/${OUT}/clip8_new_norm.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i /tmp/concat_v3.txt -c copy "${OUT}/stitched_v3.mp4" 2>/dev/null
size=$(stat -c%s "${OUT}/stitched_v3.mp4")
echo "  stitched_v3.mp4: $((size/1024/1024))MB"

echo ""
echo "=== Step 5: Watermark crop (bottom 50px) ==="
ffmpeg -y -i "${OUT}/stitched_v3.mp4" \
    -vf "crop=720:1230:0:0" \
    -c:v libx264 -preset fast -crf 19 -c:a aac -b:a 192k \
    "${OUT}/stitched_v3_nowm.mp4" 2>/dev/null
size=$(stat -c%s "${OUT}/stitched_v3_nowm.mp4")
echo "  stitched_v3_nowm.mp4: $((size/1024/1024))MB"

echo ""
echo "=== Step 6: Hormozi captions ==="
ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY .venv/bin/python scripts/caption_hormozi3.py \
    "${OUT}/stitched_v3_nowm.mp4" \
    --out "${OUT}/final_hormozi_v2.mp4" \
    --biased "Illinois juvenile detention compensation lawyers"

size=$(stat -c%s "${OUT}/final_hormozi_v2.mp4")
echo ""
echo "=== DONE ==="
echo "Output: ${OUT}/final_hormozi_v2.mp4 ($((size/1024/1024))MB)"
