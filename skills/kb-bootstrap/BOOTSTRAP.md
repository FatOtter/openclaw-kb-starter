# KB Bootstrap — Setup Guide

> **This file is the skill's instruction set.** Read and follow it when the user asks to set up a Knowledge Base.
> **Do NOT modify any existing workspace root files (SOUL.md, IDENTITY.md, USER.md, AGENTS.md).**

---

## Step 1: Environment Check

Run the environment checker:

```
python3 skills/kb-bootstrap/scripts/check_env.py
```

Read the JSON output. If any checks **failed**, tell the user what's wrong and how to fix it. Warnings are OK to continue with.

Report results:
> **Environment Check:**
> - [PASS/FAIL] each check with detail

---

## Step 2: Ask the User for KB Info

Ask these questions **one at a time**:

### Q1: KB Purpose
> What is this Knowledge Base for? Give it a name and describe what it should know about.
>
> (Example: "Product Wiki — our internal product documentation" or "Aviation Ontology — Airbus manufacturing data")

### Q2: Wiki Root Note
> Where is the source content? This can be:
> - A Feishu/Lark wiki space URL
> - A local folder path with markdown files
> - "skip" to configure later
>
> This is the source of truth the KB will index.

### Q3: Language
> What language(s) should the KB operate in?

### Q4: Indexing Rules (Optional)
> Any rules for how content should be organized? (Type "none" for defaults)
>
> (Example: "Group by product area", "Ignore draft pages", "Prioritize recent updates")

---

## Step 3: Create KB Structure

Create a `kb/` directory in the workspace and generate these files:

### kb/KB_CONFIG.md
```markdown
# KB Configuration

- **Name:** [from Q1]
- **Purpose:** [from Q1]
- **Source:** [from Q2]
- **Language:** [from Q3]
- **Indexing Rules:** [from Q4 or "default"]
- **Created:** [today's date]
- **Last Indexed:** Never
```

### kb/KB_MEMORY.md
```markdown
# KB Memory — [name]

Knowledge extracted from the source. Updated on each indexing pass.

## Topics
(empty — will be populated after first index)

## Key Facts
(empty)

## Recent Updates
- [today's date]: KB initialized. Awaiting first indexing pass.
```

### kb/KB_INDEX.md
```markdown
# KB Index

Tracks what has been ingested and when.

| Source Path | Last Indexed | Status |
|-------------|-------------|--------|
| (none yet)  | —           | —      |
```

---

## Step 4: Wiki Integration

If the user provided a wiki source in Q2:

- **Feishu/Lark URL**: Verify the Lark plugin is active (from env check). Note the wiki space in `kb/KB_CONFIG.md`. Tell the user the KB will index on the next heartbeat.
- **Local folder**: Verify path exists. List top-level files. Note them in `kb/KB_INDEX.md`.
- **Skipped**: Note in KB_CONFIG.md that source is pending.

---

## Step 5: Register KB with the Agent

Append a non-destructive section to the **existing** `MEMORY.md` (do NOT overwrite it):

```markdown

## Knowledge Base: [name]
- **Config:** kb/KB_CONFIG.md
- **Memory:** kb/KB_MEMORY.md
- **Index:** kb/KB_INDEX.md
- **Source:** [url or path]
- **Status:** Initialized, awaiting first index
```

---

## Step 6: Summary

Tell the user:

> **KB Setup Complete!**
>
> - **Name:** [name]
> - **Source:** [source or "not configured"]
> - **Files:** `kb/KB_CONFIG.md`, `kb/KB_MEMORY.md`, `kb/KB_INDEX.md`
>
> I'll start indexing content on my next heartbeat. You can check progress in `kb/KB_INDEX.md`.

---

**Important:** This skill adds a KB layer. It never touches SOUL.md, IDENTITY.md, USER.md, or AGENTS.md.
