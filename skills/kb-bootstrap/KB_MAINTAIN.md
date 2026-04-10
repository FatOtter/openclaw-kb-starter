# KB Maintenance — Scheduled Self-Arrangement

> **This file is the cron job prompt.** The bot reads and executes it on a schedule.
> It is a Software 3.0 script — natural language instructions executed by the LLM.

---

## Pre-flight

1. Read `kb/KB_CONFIG.md` — confirm the KB exists and note the source type.
2. Read `kb/KB_INDEX.md` — load the current topic inventory.
3. If either file is missing, reply `KB_MAINTAIN: KB not initialized, skipping.` and stop.

---

## Task 1: Source Re-indexing

Check if the knowledge source has new or updated content.

### If source type is `feishu-wiki`:
1. Read the wiki root node (from KB_CONFIG.md) using `feishu_wiki_space_node` `get` action.
2. List child nodes. Compare against `kb/KB_INDEX.md` entries.
3. For each **new or updated** page (compare `updated` timestamps):
   - Read the page content.
   - Follow the Ingestion Workflow in `kb/KB_GUIDE.md`: classify → extract concepts → write to topic file → add [kb:tags] → update index.
4. Update `KB_CONFIG.md` field `Last Indexed` to today's date.

### If source type is `local-folder`:
1. List files in the source path.
2. Compare modification dates against `kb/KB_INDEX.md`.
3. Ingest new/updated files using the same workflow.

### If source type is `pending`:
Skip this task.

---

## Task 2: Tag Integrity Check

Scan all topic files in `kb/topics/` for broken or dangling tags.

For each file:
1. Find all `[kb:slug]` and `[kb:slug/concept]` tags.
2. For each `[kb:slug]` — verify that `kb/topics/{slug}.md` exists.
   - If missing: convert tag to `[kb:?slug]` (marks it for research).
3. For each `[kb:slug/concept]` — verify the concept heading exists in that topic file.
   - If missing: convert to `[kb:?slug/concept]`.
4. Count total tags checked, broken tags found, and tags fixed.

---

## Task 3: Stub Resolution

Find topic files with `status: stub` in their frontmatter.

For each stub:
1. If the KB has a configured source, attempt to find content related to this topic.
2. If content is found, ingest it — add concepts, set status to `active`.
3. If no content is available, leave as `stub` — do not delete.

---

## Task 4: Stale Content Review

Find topic files where `updated` date is older than 90 days.

For each stale topic:
1. If source is available, check if source content has changed. Re-ingest if yes.
2. If no source, add an entry to the topic's `Open Questions` section:
   `- [YYYY-MM-DD] This topic hasn't been updated in 90+ days. Verify content is still accurate.`
3. Do **not** auto-archive — only flag for human review.

---

## Task 5: Index Sync

Ensure `kb/KB_INDEX.md` matches the actual state of `kb/topics/`:

1. List all `.md` files in `kb/topics/`.
2. For each file, verify it has a row in `KB_INDEX.md`. Add missing rows.
3. For each row in `KB_INDEX.md`, verify the file exists. Remove rows for deleted files.
4. Update concept counts (count `###` headings under `## Concepts` in each topic file).

---

## Task 6: Wiki Sync

**Skip this task if** `KB_CONFIG.md` source type is NOT `feishu-wiki`, or if no Wiki Space ID / Root Node is configured.

Sync local KB changes to the Feishu wiki:

1. Read `KB_CONFIG.md` to get `Wiki Space ID` and `Wiki Root Node`.
2. For each topic file in `kb/topics/`:
   - If the topic frontmatter has **no `wiki_node` field** → this topic hasn't been pushed to wiki yet.
     - Use `feishu_wiki_space_node` `create` action to create a child page under the root node.
     - Page title: topic name. Page content: full topic file content.
     - Write the returned `node_token` back into the topic frontmatter as `wiki_node: {token}`.
   - If the topic **has `wiki_node`** and its `updated` date is **newer than** the last maintenance run:
     - Use `feishu_docx` tools to update the wiki page content with the current topic file.
3. Update the wiki index page with the current `KB_INDEX.md` content.
4. If any wiki operation fails, log the error in the topic's Change Log and continue with other topics.

---

## Report

After all tasks, compose a **brief** maintenance summary (under 500 characters for Feishu):

```
KB 维护完成 ✓
- 索引: [N] 条新内容 / [N] 条更新
- 标签: [N] 检查, [N] 修复
- 存根: [N] 待填充
- 过期: [N] 需审查
- 索引同步: OK / [具体问题]
- Wiki 同步: [N] 页面创建, [N] 页面更新 / 跳过（未配置）
```

### Dry Run Mode

If the message contains `--dry-run`:
- Execute all checks (read files, scan tags, etc.)
- **Do not write any changes** to files
- Report what *would* be done instead of doing it
- End the report with: `(dry run — no changes written)`
