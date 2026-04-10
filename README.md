# OpenClaw KB Starter

Give any running OpenClaw bot a persistent Knowledge Base system. Send a zip via Feishu, the bot installs itself. No existing persona or config gets touched.

## Why This Exists

Karpathy frames the modern LLM stack as a new kind of operating system. The model is the CPU — it can reason, but it forgets everything between sessions. What's missing is the rest of the OS: memory, I/O, persistence.

This project builds on that idea. An OpenClaw bot already has the "CPU" (the LLM) and "peripherals" (tools, Feishu, wiki APIs). What it lacks is a **structured knowledge layer** — a way to accumulate, index, and recall domain knowledge across sessions. That's what this starter kit adds.

### The Memory Problem

An LLM's context window is its working memory — fast but volatile. Once the session ends, everything is gone. Karpathy compares this to a person who wakes up with amnesia every morning. The fix isn't a bigger context window. It's **external memory** — files the agent reads on boot and writes to before sleep.

This kit implements a three-tier memory architecture:

```
┌─────────────────────────────────────────┐
│  Context Window (Working Memory)        │  ← Fast, volatile, limited
│  What the LLM sees right now            │
├─────────────────────────────────────────┤
│  MEMORY.md (Long-term Memory)           │  ← Curated, persisted, agent-managed
│  Distilled knowledge across sessions    │
├─────────────────────────────────────────┤
│  kb/ (Knowledge Base)                   │  ← Structured, indexed, source-linked
│  KB_CONFIG.md — what to know            │
│  KB_MEMORY.md — what it learned         │
│  KB_INDEX.md  — what it's ingested      │
└─────────────────────────────────────────┘
```

### Software That Installs Itself

The other Karpathy insight: English is the hottest new programming language. The entire install process of this kit is a markdown file (`INSTALL.md`) that the bot reads and executes. No installer binary, no setup script — just instructions written for an LLM to follow. The bot downloads the zip, reads the instructions, runs the environment check, asks you questions, and builds the KB. The "code" is prose.

This is what Karpathy calls Software 3.0 — programs written in natural language, executed by a model that can reason about what to do next.

## Quickstart

### Via Feishu (Recommended)

1. Download `openclaw-kb-starter.zip` from [Releases](https://github.com/FatOtter/openclaw-kb-starter/releases)
2. Open a chat with your OpenClaw bot in Feishu
3. Send the zip with a message: "帮我安装这个知识库工具"
4. The bot will:
   - Download and extract the zip
   - Read `INSTALL.md`
   - Run environment checks
   - Ask you step-by-step: KB name, **wiki root node**, language, indexing rules
   - Create KB files under `kb/`
   - Connect to your Feishu wiki (if you provided a root node)

### Via SSH (Manual)

```bash
git clone https://github.com/FatOtter/openclaw-kb-starter.git /tmp/kb-starter
cp -r /tmp/kb-starter/skills/kb-bootstrap/ ~/.openclaw/workspace/skills/kb-bootstrap/

# Then tell the bot in Feishu: "帮我设置知识库"
```

## How It Works

```
User sends zip → Bot extracts → Reads INSTALL.md → Env check → Interviews user → Creates kb/
```

The bot follows `BOOTSTRAP.md` step by step:

1. **Environment check** — validates LLM config, Feishu plugin, workspace access
2. **User interview** (one question at a time, waits for each answer):
   - Q1: KB name and purpose
   - Q2: **Wiki root node** — Feishu wiki URL, space ID, local path, or skip
   - Q3: Language
   - Q4: Indexing rules
3. **Create KB** — generates `kb/KB_CONFIG.md`, `kb/KB_MEMORY.md`, `kb/KB_INDEX.md` from your answers
4. **Wiki integration** — if you gave a Feishu wiki URL, creates pages under that root node
5. **Register** — appends KB reference to existing `MEMORY.md` (non-destructive)

## What's in the Zip

```
openclaw-kb-starter/
├── INSTALL.md                 ← The bot reads this (Software 3.0 installer)
├── README.md                  ← You're reading this (for humans)
├── skills/
│   └── kb-bootstrap/
│       ├── SKILL.md           ← Tells the bot when to trigger
│       ├── BOOTSTRAP.md       ← Step-by-step execution instructions
│       └── scripts/
│           └── check_env.py   ← Runtime dependency checker (Software 1.0)
└── templates/                 ← Reference only, never copied as-is
    ├── AGENTS.md
    ├── SOUL.example.md
    ├── USER.example.md
    └── IDENTITY.example.md
```

## Safety Guarantees

- **Never modifies** the bot's SOUL.md, IDENTITY.md, USER.md, or AGENTS.md
- All KB files live in `kb/` subdirectory, isolated from existing workspace
- MEMORY.md is only appended to, never overwritten

## Supported Wiki Sources

| Source | Status |
|--------|--------|
| Feishu/Lark Wiki | Supported (requires Lark plugin) |
| Local Markdown folder | Supported |
| Notion | Recorded, requires manual integration |
| Manual input | Always available |

## Requirements

- A running OpenClaw bot
- At least one LLM API key (in `env` or `models.providers`)
- Python 3.8+ (for the env checker)
- Feishu/Lark plugin (if using Feishu)

## Design Principles

**Additive, not destructive.** The kit adds a layer; it never replaces what's there. An existing bot with its own personality keeps working exactly as before.

**Files over features.** The entire KB system is markdown files. No database, no vector store, no embedding pipeline. The LLM reads the files. This is intentional — it's the simplest thing that works, and it's debuggable by a human with `cat`.

**English (and Chinese) as code.** The installer, the skill definitions, the bootstrap instructions — they're all natural language documents that an LLM executes. When the behavior is wrong, you fix it by editing prose, not by debugging a program.
