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

### Q4: 索引规则（可选）
向用户提问：
```
有什么特殊的内容组织规则吗？输入 "无" 使用默认规则。
例如："按产品线分类"、"忽略草稿页"、"优先更新最近修改的内容"
```
**等待用户回答。**

---

## Step 3: 创建 KB 文件结构

**在收集完所有用户回答之后**，在 workspace 下创建 `kb/` 目录，生成以下文件：

### kb/KB_CONFIG.md
用**用户的实际回答**填写，不要用模板里的占位符：
```markdown
# KB Configuration

- **Name:** [用户在 Q1 的回答]
- **Purpose:** [用户在 Q1 的回答]
- **Source:** [用户在 Q2 的回答 — wiki URL、space_id、本地路径、或 "pending"]
- **Source Type:** [feishu-wiki / local-folder / pending]
- **Language:** [用户在 Q3 的回答]
- **Indexing Rules:** [用户在 Q4 的回答，或 "default"]
- **Created:** [今天的日期]
- **Last Indexed:** Never
```

### kb/KB_MEMORY.md
```markdown
# KB Memory — [用户给的名称]

从知识源提取的内容。每次索引更新。

## Topics
（空 — 首次索引后填充）

## Key Facts
（空）

## Recent Updates
- [今天的日期]: KB 初始化完成，等待首次索引。
```

### kb/KB_INDEX.md
```markdown
# KB Index

追踪已索引的内容。

| Source Path | Last Indexed | Status |
|-------------|-------------|--------|
| (none yet)  | —           | —      |
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
2. 将 `kb/KB_CONFIG.md` 的内容写入该页面

**注意：** 如果 `create` 返回 `field validation failed`，请：
- 读取 `feishu_wiki_space_node` 的 SKILL.md 了解正确参数格式
- 检查是否缺少必填字段
- 不要重复尝试相同的错误调用

### 4c: 如果用户选了 "skip" 或本地路径

- 在 `kb/KB_CONFIG.md` 中标记 source 为 pending 或记录本地路径
- 告诉用户可以稍后配置

---

## Step 5: 注册到 MEMORY.md

在**现有的** `MEMORY.md` 文件**末尾追加**以下内容（使用 `echo >>` 追加，绝对不要覆盖）：

```markdown

## Knowledge Base: [用户给的名称]
- **Config:** kb/KB_CONFIG.md
- **Memory:** kb/KB_MEMORY.md
- **Index:** kb/KB_INDEX.md
- **Source:** [wiki URL / 本地路径 / pending]
- **Source Type:** [feishu-wiki / local-folder / pending]
- **Wiki Space ID:** [如果有]
- **Wiki Root Node:** [如果有]
- **Status:** Initialized, awaiting first index
```

---

## Step 6: 汇报完成

告诉用户：

```
KB 设置完成！

- 名称：[名称]
- 来源：[来源]
- 文件：kb/KB_CONFIG.md, kb/KB_MEMORY.md, kb/KB_INDEX.md
- [如果配置了飞书 Wiki] Wiki 索引页：[链接]

下次 heartbeat 时我会开始从来源索引内容到知识库。
你可以随时查看 kb/KB_INDEX.md 了解索引进度。
```

---

## 常见错误处理

- **OAuth 授权弹窗**：飞书操作可能触发授权请求，这是正常的。告诉用户点击授权卡片，等待授权完成后重试。
- **field validation failed**：参数格式错误。查阅对应工具的 SKILL.md 了解正确用法，不要盲目重试。
- **权限不足**：告诉用户需要将 Bot 添加为 Wiki 空间的管理员或成员。
