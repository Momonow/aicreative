# Inventory

This directory stores campaign-specific research, copy, compliance notes, asset decisions, and
historical production learnings.

- Reusable video craft belongs in `skills/video-production`, `skills/ai-video-generation`, or
  `skills/video-post-production`.
- Reusable ad strategy belongs in `skills/admachin-video-ads`.
- Regulated campaign text belongs in a dedicated campaign skill and `config/campaigns/`.
- Provider task IDs, approved people, asset IDs, rejects, and launch state remain campaign-specific.

Generated indexes:

- `video_workflow_catalog.md` and `.json`: every Python workflow
- `skill_catalog.md`: every custom and linked skill

Regenerate them with:

```bash
.venv/bin/python scripts/catalog_video_workflows.py
```
