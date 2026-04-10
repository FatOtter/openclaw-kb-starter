# OpenClaw KB Starter

Drop this zip into a blank OpenClaw bot (via Feishu or any channel) to bootstrap a personalized Knowledge Base assistant.

## Quickstart

```bash
# 1. Download and unzip
git clone https://github.com/FatOtter/openclaw-kb-starter.git
cd openclaw-kb-starter

# 2. Copy everything into your OpenClaw workspace
cp -r BOOTSTRAP.md templates/ skills/ memory/ ~/.openclaw/workspace/

# 3. Copy the agent operating instructions
cp templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md

# 4. Start OpenClaw (if not already running)
openclaw start

# 5. Send any message to the bot — it will detect BOOTSTRAP.md and walk you through setup
```

Or, if using **Feishu**: just zip and send the file directly to your bot.

```bash
zip -r openclaw-kb-starter.zip . -x ".git/*" ".DS_Store"
# Upload openclaw-kb-starter.zip to the bot in Feishu
```

The bot will automatically check your environment, ask a few questions, and build your KB system.

## What's Inside

```
openclaw-kb-starter/
├── BOOTSTRAP.md              ← The bot reads this on first run and starts setup
├── templates/
│   ├── AGENTS.md             ← Operating instructions (copied to workspace)
│   ├── SOUL.example.md       ← Example persona (generated from your answers)
│   ├── USER.example.md       ← Example owner profile
│   └── IDENTITY.example.md   ← Example identity card
├── skills/
│   └── kb-bootstrap/
│       ├── SKILL.md           ← Skill documentation
│       └── scripts/
│           └── check_env.py   ← Runtime dependency checker
├── memory/
│   └── daily/                 ← Empty, ready for daily logs
└── README.md                  ← This file
```

## How to Use

### 1. Prepare a Blank OpenClaw Bot

Make sure your OpenClaw instance has:
- At least one LLM API key configured (Gemini, OpenAI, Anthropic, etc.)
- A Feishu/Lark channel configured (if using Feishu)
- The bot is running and connected

### 2. Upload the Zip

Upload `openclaw-kb-starter.zip` as a file to the bot through Feishu (or place the contents in `~/.openclaw/workspace/`).

### 3. Trigger Bootstrap

Send any message to the bot. On detecting `BOOTSTRAP.md`, the bot will:

1. **Check environment** — verify LLM config, Lark plugin, workspace access
2. **Ask you questions** — bot name, wiki source, language, preferences
3. **Generate your KB system** — persona files, memory structure, operating rules
4. **Connect to wiki** — if you provided a Feishu wiki URL or local path
5. **Clean up** — delete BOOTSTRAP.md, start operating in character

### 4. Customize

After setup, you can edit any generated file:
- `SOUL.md` — change personality, add rules
- `USER.md` — update your profile
- `AGENTS.md` — adjust operating behavior
- `MEMORY.md` — seed with knowledge

## Wiki Sources Supported

| Source | Status |
|--------|--------|
| Feishu/Lark Wiki | Supported (requires Lark channel config) |
| Local Markdown Folder | Supported |
| Notion | Noted, requires manual integration |
| Manual Input | Always available |

## Requirements

- OpenClaw (any recent version)
- Python 3.8+ (for environment checker)
- At least one LLM provider API key
- Feishu/Lark plugin (optional, for Feishu integration)
