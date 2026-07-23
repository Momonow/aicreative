# Audio Finishing

## Order

1. Verify the retained transcript.
2. Remove leading/trailing extras by Scribe word timings.
3. Measure clip loudness, spectral balance, noise, speaker similarity, and F0.
4. Use raw audio when it is already coherent.
5. Apply voice changer only for a real continuity or cleanup benefit.
6. Assemble the full master.
7. Measure integrated loudness.
8. Apply one static gain and true-peak limiter.
9. Measure the rendered result again.

Dynamic single-pass `loudnorm` can pump short speech. For transparent finishing, measure integrated LUFS and apply one constant `volume` gain to the assembled master.

Always disable ffmpeg limiter makeup:

```text
alimiter=limit=0.794:level=disabled:asc=1
```

Choose the limit and loudness target for the format, then verify integrated LUFS and true peak. Do not trust the filter settings as proof of the output.

Use both `scripts/audio_match.py` and `scripts/voice_consistency.py`; each catches problems the other misses.
