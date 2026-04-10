# KB Guide — Knowledge Base Operating Manual

> **This file is your instruction set for managing the Knowledge Base.**
> Read it on every session where you interact with the KB.
> Follow it precisely — don't improvise the structure.

---

## Core Idea

Your context window is volatile — everything is lost between sessions. This KB is your **external memory**: structured files you read on boot and write to during work. It turns you from an amnesiac into an agent with accumulating knowledge.

Three tiers of memory:

| Tier | What | Persistence | Speed |
|------|------|-------------|-------|
| Context window | What you see right now | Session only | Instant |
| MEMORY.md | Curated long-term memory | Persistent | Fast (loaded on boot) |
| kb/ | Structured knowledge base | Persistent | On-demand (read when needed) |

The KB is the deepest layer — **organized by topic, linked by tags, source-tracked**.

---

## KB Structure

```
kb/
├── KB_CONFIG.md      ← Configuration (source, language, rules)
├── KB_GUIDE.md       ← This file (operating manual)
├── KB_INDEX.md       ← Master index of all topics
└── topics/
    ├── {slug}.md     ← One file per topic
    └── ...
```

---

## Topics

A **topic** is a domain of knowledge. Each topic gets its own file in `kb/topics/`.

### Topic File Format

```markdown
---
topic: {Topic Name}
slug: {topic-slug}
tags: [kb:{related-topic}], [kb:{parent-topic}]
status: active | archived | stub
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: {where this knowledge came from}
wiki_node: {feishu node_token, empty until first wiki sync}
---

# {Topic Name}

{1-3 sentence overview of what this topic covers.}

## Concepts

### {Concept Name}
{Clear definition or explanation.}
- **Source:** {URL, document name, or "user input"}
- **Links:** [kb:{other-topic}], [kb:{other-topic}/{concept}]
- **Confidence:** high | medium | low
- **Added:** YYYY-MM-DD

### {Another Concept}
...

## Key Facts
- Fact 1. [kb:{related-topic}]
- Fact 2.

## Open Questions
- {Things not yet resolved or needing research}

## Change Log
- YYYY-MM-DD: Created topic with N concepts.
```

### Naming Rules
- **Slug:** lowercase, hyphens, no spaces. Example: `api-rate-limits`, `onboarding-flow`
- **One topic per file.** If a topic grows beyond ~200 lines, split it into sub-topics.
- **Stubs are OK.** A topic with just a name and one concept is better than no topic at all.

---

## The [kb:tag] System

Tags are how knowledge items reference each other. They create a **relationship graph** across your KB.

### Tag Syntax

| Format | Meaning | Example |
|--------|---------|---------|
| `[kb:{topic-slug}]` | References a topic | `[kb:api-design]` |
| `[kb:{topic-slug}/{concept}]` | References a specific concept | `[kb:auth/oauth-flow]` |
| `[kb:?{query}]` | Marks something that needs research | `[kb:?rate-limit-policy]` |
| `[kb:!{warning}]` | Flags important caveats | `[kb:!deprecated-after-v3]` |

### When to Tag

- A concept **depends on** another concept → link it
- A fact in one topic **contradicts or qualifies** a fact in another → link both
- A concept is mentioned but **doesn't exist yet** → use `[kb:?...]` to mark it for later
- A concept has a **known caveat** → use `[kb:!...]`

### Tag Integrity

When you create or update a topic:
1. Check that all `[kb:slug]` tags point to existing topics
2. If a referenced topic doesn't exist, either create a stub or convert to `[kb:?...]`
3. Periodically scan for orphaned `[kb:?...]` tags and resolve them

---

## Ingestion Workflow

When new knowledge arrives (from wiki, documents, user input, or any source):

### Step 1: Classify
Determine which existing topic(s) the knowledge belongs to. If none fit, create a new topic.

### Step 2: Extract Concepts
Break the knowledge into **atomic concepts** — each one a discrete, self-contained piece of understanding.

Bad: "The API has rate limits and uses OAuth and returns JSON"
Good: Three separate concepts — "Rate Limiting Policy", "OAuth Authentication Flow", "Response Format"

### Step 3: Write
Add each concept to the appropriate topic file using the format above. Set:
- **Source** to where the knowledge came from
- **Confidence** based on source reliability
- **Links** to related concepts in other topics

### Step 4: Tag
Add `[kb:tag]` references wherever concepts relate to each other. This is what makes the KB a **graph** instead of a flat list.

### Step 5: Update Index
Add or update the topic entry in `KB_INDEX.md`.

### Step 6: Sync to Wiki
If `KB_CONFIG.md` has a configured Feishu wiki source (`Source Type: feishu-wiki`):

1. Read `KB_CONFIG.md` to get the `Wiki Space ID` and `Wiki Root Node`.
2. For each **new topic** created in this ingestion:
   - Use `feishu_wiki_space_node` `create` action to create a child page under the root node.
   - Page title: topic name from frontmatter.
   - Page content: the full topic file content (convert markdown to docx format).
   - Record the created `node_token` in the topic file frontmatter as `wiki_node: {token}`.
3. For each **updated topic** that already has a `wiki_node` in its frontmatter:
   - Use `feishu_docx` tools to update the existing wiki page with the new content.
4. Update the wiki index page (the "[KB名称] — 索引" page created during bootstrap) with the current `KB_INDEX.md` content.

**If wiki sync fails** (auth error, permission denied, etc.):
- Log the failure in the topic's Change Log: `- [date]: Wiki sync failed: {error}`
- Do **not** block the local file write — local KB is always the source of truth
- Retry on next maintenance cycle

---

## Retrieval Workflow

When you need knowledge to answer a question or complete a task:

1. **Check KB_INDEX.md** — scan topic names and descriptions for relevance
2. **Read relevant topic files** — load the specific topics you need
3. **Follow [kb:tag] links** — if a concept references another topic, read that too
4. **Cite your sources** — when using KB knowledge in responses, mention where it came from

Don't load the entire KB into context. Read selectively — index first, then specific topics.

---

## Maintenance

Maintenance runs automatically via a cron job (`kb-maintain`, every 6 hours). The full procedure is defined in `kb/KB_MAINTAIN.md` — a Software 3.0 script that the bot reads and executes.

### What the Cron Job Does
1. **Source Re-indexing** — checks wiki/folder for new or updated content, ingests it
2. **Tag Integrity Check** — scans all `[kb:tag]` references, fixes broken links
3. **Stub Resolution** — attempts to fill `status: stub` topics from available sources
4. **Stale Content Review** — flags topics not updated in 90+ days for human review
5. **Index Sync** — ensures `KB_INDEX.md` matches actual topic files on disk

### Manual Trigger
Run `openclaw cron run kb-maintain` to trigger maintenance immediately.
Add `--dry-run` to the message to preview changes without writing them.

### When Sources Update (Outside of Cron)
If you notice a source has changed during a conversation:
1. Re-read the source
2. Compare with existing concepts — update changed facts, add new ones, mark removed ones
3. Update the `updated` date and change log
4. Update `KB_INDEX.md` with the new indexed date

### Confidence Decay
- Knowledge from 6+ months ago without re-verification → consider downgrading confidence
- Knowledge contradicted by newer information → update or remove
- User-corrected knowledge → always update immediately, set confidence to `high`

---

## Safety Rules

- **Never overwrite** the bot's SOUL.md, IDENTITY.md, USER.md, or AGENTS.md
- All KB files live in `kb/` — don't scatter knowledge files elsewhere
- MEMORY.md is only **appended to**, never overwritten by the KB system
- When in doubt about categorization, ask the user
- Don't ingest sensitive credentials, API keys, or passwords into topic files
