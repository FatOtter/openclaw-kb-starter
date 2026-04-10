# KB Bootstrap — Update Guide

> **这是升级指南，不是初始安装。** 仅当 `skills/kb-bootstrap/` 已存在时使用此文件。
> **绝对不要删除或覆盖** `kb/` 目录下用户的知识库数据。
> **绝对不要重新运行用户问答流程（BOOTSTRAP.md 的 Step 2）。**

---

## Step 1: 版本检测

读取当前已安装的版本和新版本：

```
当前版本: cat ~/.openclaw/workspace/skills/kb-bootstrap/VERSION
新版本: cat <解压路径>/skills/kb-bootstrap/VERSION
```

向用户报告：
```
检测到 KB Bootstrap 已安装（当前版本: [旧版本]）。
新版本: [新版本]
将执行升级，你的知识库数据（kb/ 目录）不会受影响。
```

如果版本号相同，告诉用户 "已是最新版本，无需更新" 并停止。

---

## Step 2: 备份当前配置

在升级前记录当前状态：

1. 读取 `kb/KB_CONFIG.md` — 记住用户的配置（名称、来源、语言等）
2. 读取 `kb/KB_INDEX.md` — 记住当前主题列表
3. 记录已安装的 cron 任务：`openclaw cron list`（查找 `kb-maintain`）

---

## Step 3: 覆盖技能文件

用新版本覆盖 `skills/kb-bootstrap/` 下的所有文件：

```bash
cp -r <解压路径>/skills/kb-bootstrap/* ~/.openclaw/workspace/skills/kb-bootstrap/
```

这会更新：SKILL.md、BOOTSTRAP.md、KB_GUIDE.md、KB_MAINTAIN.md、VERSION、UPDATE.md、scripts/

---

## Step 4: 迁移 kb/ 结构

按顺序检查以下迁移项，**只执行适用的**：

### 4a: KB_GUIDE.md（操作手册更新）

如果 `kb/KB_GUIDE.md` 存在：
- 用新版本覆盖：`cp skills/kb-bootstrap/KB_GUIDE.md kb/KB_GUIDE.md`
- 这个文件是操作手册，不含用户数据，直接覆盖安全。

### 4b: KB_MAINTAIN.md（维护脚本更新）

如果 `kb/KB_MAINTAIN.md` 存在：
- 用新版本覆盖：`cp skills/kb-bootstrap/KB_MAINTAIN.md kb/KB_MAINTAIN.md`
- 这个文件是维护脚本，不含用户数据，直接覆盖安全。

如果 `kb/KB_MAINTAIN.md` **不存在**（从旧版本升级）：
- 复制新版本：`cp skills/kb-bootstrap/KB_MAINTAIN.md kb/KB_MAINTAIN.md`

### 4c: topics/ 目录

如果 `kb/topics/` **不存在**（从旧版本升级）：
- 创建目录：`mkdir -p kb/topics/`
- 告诉用户新版本支持按主题分类知识，可以手动添加或等待下次维护时自动创建。

### 4d: topic 文件 wiki_node 字段

扫描 `kb/topics/` 下的所有 `.md` 文件。如果任何 topic 文件的 frontmatter **没有 `wiki_node` 字段**：
- 在 frontmatter 中追加 `wiki_node:` 空字段（在 `source:` 行之后）

### 4e: KB_CONFIG.md Tag Reference

如果 `kb/KB_CONFIG.md` 不包含 "Tag Reference" 部分：
- 在文件末尾追加：
```markdown

## Tag Reference
知识库使用 [kb:tag] 系统管理知识之间的关系：
- `[kb:topic-slug]` — 引用一个主题
- `[kb:topic-slug/concept]` — 引用一个具体概念
- `[kb:?query]` — 标记需要研究的内容
- `[kb:!warning]` — 标记重要注意事项
```

**绝对不要修改** KB_CONFIG.md 中的 Name、Purpose、Source、Language 等用户配置字段。

---

## Step 5: 更新 cron 任务

检查 `kb-maintain` cron 任务是否存在：

```bash
openclaw cron list
```

- 如果 **存在**：不做修改（保留用户可能调整过的调度频率）。
- 如果 **不存在**（从旧版本升级）：创建新的 cron 任务：
  ```bash
  openclaw cron add \
    --name "kb-maintain" \
    --every 6h \
    --session isolated \
    --message "读取并执行 kb/KB_MAINTAIN.md 中的所有维护任务。" \
    --description "KB 知识库定期维护：索引更新、标签检查、存根解析、过期审查、Wiki 同步"
  ```

---

## Step 6: 更新 MEMORY.md

检查 `MEMORY.md` 中的 KB 注册信息。如果缺少以下字段，追加到 KB 段落中：

- `**Maintenance:** kb/KB_MAINTAIN.md (cron: kb-maintain, every 6h)` — 如果缺少
- `**Tag System:** [kb:topic], [kb:topic/concept], [kb:?query], [kb:!warning]` — 如果缺少

**仅追加缺少的字段，不要删除或修改已有内容。**

---

## Step 7: Dry Run 验证

执行维护脚本的 dry run，验证升级后一切正常：

1. 读取 `kb/KB_MAINTAIN.md`
2. 以 `--dry-run` 模式执行所有任务
3. 向用户报告结果

---

## Step 8: 汇报完成

告诉用户：

```
KB Bootstrap 升级完成！ [旧版本] → [新版本]

✅ 已更新：
- 技能文件（SKILL.md、BOOTSTRAP.md、KB_GUIDE.md、KB_MAINTAIN.md）
- [列出执行的迁移项]

⏭️ 未改动：
- kb/KB_CONFIG.md（你的配置）
- kb/topics/（你的知识数据）
- kb/KB_INDEX.md（你的索引）

🔄 维护 Dry Run: [结果摘要]

如有问题请告诉我。
```
