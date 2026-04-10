# KB Bootstrap — Setup Guide

> **严格按照以下步骤执行，不要跳步，不要自行发挥。**
> **绝对不要修改** workspace 根目录的 SOUL.md、IDENTITY.md、USER.md、AGENTS.md。
> **绝对不要**把 templates/ 目录下的示例文件复制为实际 KB 文件。templates/ 仅供参考。

---

## Step 1: 环境检查

运行环境检查脚本：

```
python3 skills/kb-bootstrap/scripts/check_env.py
```

读取 JSON 输出，向用户报告结果。如果有 `failed` 项，告诉用户如何修复，**等用户修复后再继续**。`warnings` 可以忽略继续。

---

## Step 2: 询问用户（必须逐个提问，等用户回答后再问下一个）

**重要：你必须逐个提问，每次只问一个问题，等用户回答后再问下一个。不要一次性把所有问题发出去。不要跳过任何问题。不要自己编造答案。**

### Q1: KB 名称和用途
向用户提问：
```
请为这个知识库起个名字，并简要说明它的用途。
例如："产品文档库 — 存放我们的内部产品文档" 或 "项目知识库 — 汇总项目相关资料"
```
**等待用户回答。**

### Q2: Wiki 根节点（核心问题）
向用户提问：
```
请提供知识库的根节点，支持以下方式：
1. 飞书 Wiki 页面链接（例如 https://xxx.feishu.cn/wiki/xxx）
2. 飞书知识空间 ID（space_id）
3. 本地文件夹路径（包含 markdown 文件）
4. 输入 "skip" 稍后配置

如果选择飞书 Wiki，我会在该节点下创建知识库的子页面结构。
```
**等待用户回答。这是最关键的一步，不要跳过。**

### Q3: 语言
向用户提问：
```
知识库主要使用什么语言？（例如：中文、英文、中英双语）
```
**等待用户回答。**

### Q4: 初始主题
向用户提问：
```
你希望知识库先覆盖哪些主题领域？请列出 1-5 个初始主题。
例如："API 设计规范"、"产品需求"、"运维手册"
输入 "无" 则创建空的知识库，后续手动添加。
```
**等待用户回答。**

### Q5: 索引规则（可选）
向用户提问：
```
有什么特殊的内容组织规则吗？输入 "无" 使用默认规则。
例如："按产品线分类"、"忽略草稿页"、"优先更新最近修改的内容"
```
**等待用户回答。**

---

## Step 3: 创建 KB 文件结构

**在收集完所有用户回答之后**，在 workspace 下创建以下文件结构：

### 3a: 创建目录

```bash
mkdir -p kb/topics
```

### 3b: 复制 KB_GUIDE.md

将 `skills/kb-bootstrap/KB_GUIDE.md` 复制到 `kb/KB_GUIDE.md`：

```bash
cp skills/kb-bootstrap/KB_GUIDE.md kb/KB_GUIDE.md
```

这是知识库的操作手册，指导你如何管理知识。**每次与 KB 相关的 session 都要先读这个文件。**

### 3c: 创建 kb/KB_CONFIG.md

用**用户的实际回答**填写，不要用模板里的占位符：

```markdown
# KB Configuration

- **Name:** [用户在 Q1 的回答]
- **Purpose:** [用户在 Q1 的回答]
- **Source:** [用户在 Q2 的回答 — wiki URL、space_id、本地路径、或 "pending"]
- **Source Type:** [feishu-wiki / local-folder / pending]
- **Language:** [用户在 Q3 的回答]
- **Indexing Rules:** [用户在 Q5 的回答，或 "default"]
- **Created:** [今天的日期]
- **Last Indexed:** Never

## Tag Reference
知识库使用 [kb:tag] 系统管理知识之间的关系：
- `[kb:topic-slug]` — 引用一个主题
- `[kb:topic-slug/concept]` — 引用一个具体概念
- `[kb:?query]` — 标记需要研究的内容
- `[kb:!warning]` — 标记重要注意事项
```

### 3d: 创建 kb/KB_INDEX.md

```markdown
# KB Index

知识库主题索引。管理知识时先查此文件，按需读取具体主题文件。

| Topic | Slug | Status | Concepts | Last Updated |
|-------|------|--------|----------|-------------|
```

**然后，对用户在 Q4 提供的每个主题：** 在索引表中添加一行，并创建对应的主题文件（见 Step 3e）。

如果用户回答 "无"，保持索引表为空。

### 3e: 为每个初始主题创建 topic 文件

对用户提供的每个初始主题，在 `kb/topics/` 下创建文件。**slug 命名规则：小写、连字符、无空格。**

每个主题文件内容：

```markdown
---
topic: [主题名称]
slug: [topic-slug]
tags:
status: stub
created: [今天的日期]
updated: [今天的日期]
source: pending
wiki_node:
---

# [主题名称]

[根据用户描述写 1-2 句话概述此主题的范围]

## Concepts

（空 — 等待首次索引或用户输入后填充）

## Key Facts

（空）

## Open Questions

（空）

## Change Log
- [今天的日期]: 主题创建，等待内容填充。
```

同时在 `KB_INDEX.md` 的表格中添加对应行：

```
| [主题名称] | [slug] | stub | 0 | [今天的日期] |
```

---

## Step 4: 飞书 Wiki 对接（如果用户在 Q2 提供了飞书链接或 space_id）

### 4a: 解析用户提供的 Wiki 信息

- 如果用户给了 **Wiki 页面链接**（如 `https://xxx.feishu.cn/wiki/xxx`）：
  - 从链接中提取 `node_token`（URL 最后一段）
  - 用 `feishu_wiki_space_node` 的 `get` action 查询该节点，获取 `space_id`
  - 记录 `space_id` 和 `node_token` 到 `kb/KB_CONFIG.md`

- 如果用户给了 **space_id**：
  - 用 `feishu_wiki_space` 查询该空间信息
  - 记录到 `kb/KB_CONFIG.md`

### 4b: 在 Wiki 根节点下创建知识库结构

使用 `feishu_wiki_space_node` 的 `create` action，在用户指定的根节点下创建：

1. 一个名为 **"[KB名称] — 索引"** 的子页面（docx 类型）
2. 将 `kb/KB_INDEX.md` 的内容写入该页面

**注意：** 如果 `create` 返回 `field validation failed`，请：
- 读取 `feishu_wiki_space_node` 的 SKILL.md 了解正确参数格式
- 检查是否缺少必填字段
- 不要重复尝试相同的错误调用

### 4c: 如果用户选了 "skip" 或本地路径

- 在 `kb/KB_CONFIG.md` 中标记 source 为 pending 或记录本地路径
- 告诉用户可以稍后配置

---

## Step 5: 注册维护定时任务

知识库需要定期自我整理。使用 OpenClaw 的 cron 系统创建一个维护任务。

### 5a: 复制维护脚本

```bash
cp skills/kb-bootstrap/KB_MAINTAIN.md kb/KB_MAINTAIN.md
```

### 5b: 创建 cron 任务

运行以下命令（注意：`--every 6h` 表示每 6 小时执行一次，可根据知识库规模调整）：

```bash
openclaw cron add \
  --name "kb-maintain" \
  --every 6h \
  --session isolated \
  --message "读取并执行 kb/KB_MAINTAIN.md 中的所有维护任务。" \
  --description "KB 知识库定期维护：索引更新、标签检查、存根解析、过期审查"
```

如果 `openclaw cron add` 失败（例如命令不可用），告诉用户手动添加，不要阻塞安装流程。

### 5c: Dry Run 验证

立即执行一次维护的 dry run，验证 KB 结构正确：

1. 读取 `kb/KB_MAINTAIN.md`
2. 按其中的步骤执行所有检查，但**加上 `--dry-run` 模式：只读不写**
3. 向用户报告 dry run 结果，例如：
   ```
   维护 Dry Run 完成 ✓
   - 索引: 0 条新内容 / 0 条更新（来源尚未配置）
   - 标签: 0 检查（尚无概念）
   - 存根: [N] 待填充
   - 索引同步: OK
   (dry run — 未写入任何变更)
   ```
4. 如果 dry run 发现问题（文件缺失、目录结构错误等），**立即修复**后再继续。

---

## Step 6: 注册到 MEMORY.md

在**现有的** `MEMORY.md` 文件**末尾追加**以下内容（使用 `echo >>` 追加，绝对不要覆盖）：

```markdown

## Knowledge Base: [用户给的名称]
- **Config:** kb/KB_CONFIG.md
- **Guide:** kb/KB_GUIDE.md (每次 KB 操作前必读)
- **Index:** kb/KB_INDEX.md
- **Topics:** kb/topics/ (每个主题一个文件)
- **Source:** [wiki URL / 本地路径 / pending]
- **Source Type:** [feishu-wiki / local-folder / pending]
- **Wiki Space ID:** [如果有]
- **Wiki Root Node:** [如果有]
- **Tag System:** [kb:topic], [kb:topic/concept], [kb:?query], [kb:!warning]
- **Maintenance:** kb/KB_MAINTAIN.md (cron: kb-maintain, every 6h)
- **Status:** Initialized, [N] topics created, awaiting content ingestion
```

---

## Step 7: 汇报完成

告诉用户：

```
KB 设置完成！

📂 文件结构：
- kb/KB_CONFIG.md — 知识库配置
- kb/KB_GUIDE.md — 操作手册（我每次操作 KB 前会读取）
- kb/KB_INDEX.md — 主题索引
- kb/topics/ — 主题文件目录 [如果有初始主题则列出]
- [如果配置了飞书 Wiki] Wiki 索引页：[链接]

🏷️ 标签系统：
知识库使用 [kb:tag] 系统管理知识间的关系，当我从来源学习新知识时，
会自动将其分解为独立的概念，归入对应主题，并用标签建立关联。

🔄 自动维护：
- 已注册定时任务 kb-maintain，每 6 小时自动执行一次
- 维护内容：索引更新、标签完整性检查、存根解析、过期内容审查
- Dry run 已通过验证 ✓

📥 下一步：
- 如果你提供了知识来源，下次维护时会自动开始索引
- 你也可以随时告诉我新的知识，我会分类归档
- 查看 kb/KB_INDEX.md 了解知识库概况
- 运行 `openclaw cron run kb-maintain` 可手动触发维护
```

---

## 常见错误处理

- **OAuth 授权弹窗**：飞书操作可能触发授权请求，这是正常的。告诉用户点击授权卡片，等待授权完成后重试。
- **field validation failed**：参数格式错误。查阅对应工具的 SKILL.md 了解正确用法，不要盲目重试。
- **权限不足**：告诉用户需要将 Bot 添加为 Wiki 空间的管理员或成员。
