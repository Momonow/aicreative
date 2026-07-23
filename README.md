# aicreative

Production workspace for generated video, paid-social creative, caption systems, image ads, and
AdMachin publishing.

## Start Here

1. Read `AGENTS.md`.
2. Read `CLAUDE.md`.
3. Load `video-production` and the specialist skills it routes to.
4. Read campaign memory or `inventory/` only for the active campaign.

## Repository Map

| Path | Purpose |
|---|---|
| `skills/` | Version-controlled skill mirror |
| `scripts/` | Canonical utilities and stable legacy campaign entry points |
| `jobs/` | New campaign orchestration |
| `config/campaigns/` | Exact regulated text and campaign correction maps |
| `inventory/` | Campaign research, copy, asset decisions, and generated catalogs |
| `docs/` | Historical detail and old design specs |
| `outputs/` | Generated media and resumable job artifacts |

## Workflow Catalog

```bash
.venv/bin/python scripts/catalog_video_workflows.py
```

This regenerates:

- `inventory/video_workflow_catalog.md`
- `inventory/video_workflow_catalog.json`
- `inventory/skill_catalog.md`

The catalog covers every Python workflow and every skill, while preserving legacy paths needed for
historical reruns.
