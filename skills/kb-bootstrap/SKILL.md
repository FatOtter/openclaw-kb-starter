# KB Bootstrap Skill

A tool for setting up a Knowledge Base system on an OpenClaw bot. Does NOT modify existing persona or workspace files — it creates a new KB layer alongside whatever is already running.

## Trigger

User invokes manually: tell the bot "set up a KB" or "run kb-bootstrap".

## What it does

1. **Environment Check** — Runs `scripts/check_env.py` to verify:
   - Lark/Feishu plugin connectivity
   - LLM provider configuration
   - Workspace write access

2. **User Interview** — Asks the user:
   - KB name and purpose
   - Wiki root note (Feishu wiki URL, local folder, or skip)
   - Language preference
   - Any custom indexing rules

3. **KB Construction** — Creates files in a `kb/` subdirectory (never overwrites root files):
   - `kb/KB_CONFIG.md` — KB source config and indexing rules
   - `kb/KB_MEMORY.md` — KB-specific knowledge store
   - `kb/KB_INDEX.md` — Index of ingested content
   - Appends a KB section to the existing `MEMORY.md` (non-destructive)

## Files

- `SKILL.md` — This file
- `scripts/check_env.py` — Runtime dependency checker
- `BOOTSTRAP.md` — Standalone setup guide (for blank bots only, not used as a skill)
