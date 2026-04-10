# KB Bootstrap Skill

Initializes the Knowledge Base system on a fresh OpenClaw bot. This skill runs automatically on first launch (triggered by BOOTSTRAP.md) and guides the user through setup.

## What it does

1. **Environment Check** — Verifies runtime dependencies:
   - Lark/Feishu plugin connectivity
   - LLM provider configuration (API keys, model availability)
   - Required OpenClaw version and plugins
   - File system write access to workspace

2. **User Interview** — Asks the user (via OpenClaw chat) for:
   - Bot name and persona basics
   - Wiki root note URL or local path (the knowledge source)
   - Preferred language(s)
   - Any custom behavioral rules

3. **KB Construction** — Based on answers, generates:
   - `SOUL.md` — Core persona from user input
   - `USER.md` — Owner profile
   - `IDENTITY.md` — Short identity card
   - `AGENTS.md` — Operating instructions (pre-filled with sensible defaults)
   - `MEMORY.md` — Empty long-term memory with structure
   - `HEARTBEAT.md` — Initial heartbeat config
   - Removes `BOOTSTRAP.md` after successful setup

## Trigger

Runs when the agent detects `BOOTSTRAP.md` in the workspace root (per AGENTS.md first-run protocol).
