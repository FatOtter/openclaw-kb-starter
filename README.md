# OpenClaw KB Starter

A structured Knowledge Base system for OpenClaw bots. Send a zip via Feishu, the bot installs itself. No existing persona or config gets touched.

## Why This Exists

Karpathy frames the modern LLM stack as a new kind of operating system. The model is the CPU — it can reason, but it forgets everything between sessions. What's missing is the rest of the OS: memory, I/O, persistence.

This project builds on that idea. An OpenClaw bot already has the "CPU" (the LLM) and "peripherals" (tools, Feishu, wiki APIs). What it lacks is a **structured knowledge layer** — a way to accumulate, categorize, link, and recall domain knowledge across sessions. That's what this starter kit adds.

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
│  Topics → Concepts → [kb:tag] links    │
│  A knowledge graph in plain markdown    │
└─────────────────────────────────────────┘
```

### Software That Installs Itself

The other Karpathy insight: English is the hottest new programming language. The entire install process of this kit is a markdown file (`INSTALL.md`) that the bot reads and executes. No installer binary, no setup script — just instructions written for an LLM to follow. The bot downloads the zip, reads the instructions, runs the environment check, asks you questions, and builds the KB. The "code" is prose.

This is what Karpathy calls Software 3.0 — programs written in natural language, executed by a model that can reason about what to do next.

## How Knowledge Is Organized

### Topics
Knowledge is organized into **topics** — each one a file in `kb/topics/`. A topic is a domain: "API Design", "Deployment Procedures", "Product Requirements". Each topic contains multiple **concepts**.

### Concepts
A **concept** is an atomic piece of knowledge — one idea, one fact, one definition. Concepts live inside topic files with metadata:

```markdown
### OAuth Token Refresh
Access tokens expire after 2 hours. Use the refresh token to obtain a new one
without re-authenticating. The refresh token itself expires after 30 days.
- **Source:** API docs v3.2
- **Links:** [kb:auth/session-management], [kb:api-design/rate-limits]
- **Confidence:** high
- **Added:** 2026-04-10
```

### The [kb:tag] System
Tags are how concepts reference each other, forming a **knowledge graph** in plain text:

| Tag | Meaning | Example |
|-----|---------|---------|
| `[kb:topic]` | References a topic | `[kb:api-design]` |
| `[kb:topic/concept]` | References a specific concept | `[kb:auth/oauth-flow]` |
| `[kb:?query]` | Needs research | `[kb:?rate-limit-policy]` |
| `[kb:!warning]` | Important caveat | `[kb:!deprecated-after-v3]` |

When the bot ingests new knowledge, it doesn't just dump text into a file. It:
1. **Classifies** — which topic does this belong to?
2. **Extracts** — what are the discrete concepts?
3. **Links** — what other concepts does this relate to?
4. **Indexes** — updates the master index for fast lookup

The result is a navigable knowledge graph where the bot can follow `[kb:tag]` links to find related information, not just keyword-match.

## Quickstart

### Via Feishu (Recommended)

1. Download `openclaw-kb-starter.zip` from [Releases](https://github.com/FatOtter/openclaw-kb-starter/releases)
2. Open a chat with your OpenClaw bot in Feishu
3. Send the zip with a message: "帮我安装这个知识库工具"
4. The bot will:
   - Download and extract the zip
   - Read `INSTALL.md`
   - Run environment checks
   - Ask you step-by-step: KB name, **wiki root node**, language, initial topics, indexing rules
   - Create KB structure under `kb/` with topic files
   - Connect to your Feishu wiki (if you provided a root node)

### Via SSH (Manual)

```bash
git clone https://github.com/FatOtter/openclaw-kb-starter.git /tmp/kb-starter
cp -r /tmp/kb-starter/skills/kb-bootstrap/ ~/.openclaw/workspace/skills/kb-bootstrap/

# Then tell the bot in Feishu: "帮我设置知识库"
```

## How It Works

### Setup Phase
```
User sends zip → Bot extracts → Reads INSTALL.md → Env check → Interviews user → Creates kb/
```

The bot follows `BOOTSTRAP.md` step by step:

1. **Environment check** — validates LLM config, Feishu plugin, workspace access
2. **User interview** (one question at a time, waits for each answer):
   - Q1: KB name and purpose
   - Q2: **Wiki root node** — Feishu wiki URL, space ID, local path, or skip
   - Q3: Language
   - Q4: Initial topics (1-5 domains to seed the KB)
   - Q5: Indexing rules
3. **Create KB** — generates full structure with topic files, operating manual, and index
4. **Wiki integration** — if you gave a Feishu wiki URL, creates pages under that root node
5. **Schedule maintenance** — creates a cron job (`kb-maintain`, every 6h) and runs a dry run to validate
6. **Register** — appends KB reference to existing `MEMORY.md` (non-destructive)

### Daily Operation

Once the KB is set up, the bot manages it continuously:

- **Adding knowledge** — Tell the bot "记住这个" or "add this to KB". It classifies, extracts concepts, tags relationships, and files it under the right topic.
- **Querying knowledge** — Ask about anything in the KB. The bot reads the index, loads relevant topics, follows [kb:tag] links to related concepts, and synthesizes an answer.
- **Scheduled self-maintenance** — A cron job (`kb-maintain`) runs every 6 hours, executing `KB_MAINTAIN.md` — a Software 3.0 maintenance script. It re-indexes sources, checks tag integrity, resolves stubs, and flags stale content. A dry run validates the setup during bootstrap.
- **Manual maintenance** — Run `openclaw cron run kb-maintain` anytime, or tell the bot "整理知识库".

## What's in the Zip

```
openclaw-kb-starter/
├── INSTALL.md                 ← The bot reads this (Software 3.0 installer)
├── README.md                  ← You're reading this (for humans)
├── skills/
│   └── kb-bootstrap/
│       ├── SKILL.md           ← Trigger definitions (setup + daily management)
│       ├── BOOTSTRAP.md       ← Step-by-step setup instructions
│       ├── KB_GUIDE.md        ← Operating manual (copied to kb/ during setup)
│       ├── KB_MAINTAIN.md     ← Maintenance script (cron runs this every 6h)
│       └── scripts/
│           └── check_env.py   ← Runtime dependency checker (Software 1.0)
└── templates/                 ← Reference only, never copied as-is
    ├── AGENTS.md
    ├── SOUL.example.md
    ├── USER.example.md
    └── IDENTITY.example.md
```

### What Gets Created in kb/

```
kb/
├── KB_CONFIG.md               ← Configuration from user interview
├── KB_GUIDE.md                ← Operating manual for the bot
├── KB_MAINTAIN.md             ← Maintenance script (cron reads this)
├── KB_INDEX.md                ← Master index of all topics
└── topics/
    ├── api-design.md          ← Example: one topic file
    ├── deployment.md          ← Each containing concepts + [kb:tags]
    └── ...
```

## Safety Guarantees

- **Never modifies** the bot's SOUL.md, IDENTITY.md, USER.md, or AGENTS.md
- All KB files live in `kb/` subdirectory, isolated from existing workspace
- MEMORY.md is only appended to, never overwritten
- No credentials or API keys are stored in KB files

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

**Knowledge as graph, not pile.** Raw text dumps are useless. Knowledge is decomposed into concepts, organized by topic, and cross-linked with `[kb:tag]` references. The bot navigates this graph to find related knowledge, not just keyword-match against a flat file.

**English (and Chinese) as code.** The installer, the skill definitions, the bootstrap instructions, the operating manual — they're all natural language documents that an LLM executes. When the behavior is wrong, you fix it by editing prose, not by debugging a program.
