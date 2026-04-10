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

### During Heartbeats or Idle Time
- Review `[kb:?...]` tags and resolve them (research or create stub topics)
- Check topic files for stale information (look at `updated` dates)
- Merge small related topics if they'd be clearer combined
- Archive topics that are no longer relevant (set status to `archived`)

### When Sources Update
If a wiki page or document that was ingested into the KB gets updated:
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
