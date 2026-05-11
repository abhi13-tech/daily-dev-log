# Daily Dev Log

A lightweight automation repo for keeping a legitimate daily engineering log.

This is intended for real progress tracking, not fake contribution farming. Each scheduled run creates or updates a dated Markdown note with prompts for:

- what you worked on
- what you learned
- blockers
- next steps

You can edit the generated note afterward with actual details from your day.

## Run locally

```bash
python3 scripts/update_dev_log.py
```

## GitHub Actions

The workflow runs daily and commits a dated note only when there is a real file change.
