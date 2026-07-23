# Campaign Jobs

Use `jobs/<campaign>/<concept>/` for new campaign orchestration. This separates changing campaign
state from reusable production tools.

A job directory should contain only what is specific to that production:

- `README.md`: objective, inputs, approved copy, and resume command
- `run.py`: resumable orchestration
- `job.json`: provider task IDs, approved asset IDs, and completion state when appropriate
- `prompts/`: campaign prompt text
- `copy/`: approved scripts and ad copy

Do not duplicate general editing, anchor, caption, audio, or QA implementations inside a job.
Call the canonical utilities under `scripts/` and load the relevant skills.

Legacy campaign entry points remain under `scripts/` for reproducibility. Use
`inventory/video_workflow_catalog.md` to find and migrate them when a campaign is touched.
