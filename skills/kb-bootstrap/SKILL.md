---
name: kb-bootstrap
description: |
  Knowledge Base 管理系统。包含初始化和日常知识管理两部分功能。

  **初始化触发（一次性）：**
  (1) 用户发送了一个 zip 文件（特别是名为 openclaw-kb-starter.zip 的文件）
  (2) 用户要求设置/初始化知识库
  (3) 用户提到 "KB setup"、"知识库"、"kb-bootstrap"

  **日常管理触发（持续）：**
  (4) 用户要求添加/更新/查询知识
  (5) 用户说 "记住这个"、"归档"、"整理到知识库"
  (6) Cron 定时任务 kb-maintain 触发自动维护（每 6 小时）
  (7) 用户要求查看知识库状态或某个主题
  (8) 用户说 "维护知识库"、"kb maintain"、"整理知识库"
---

# KB Bootstrap & Management Skill

为当前 OpenClaw Bot 添加并管理知识库（KB）系统。**不会修改任何已有的 workspace 文件**（SOUL.md、IDENTITY.md、USER.md、AGENTS.md 不受影响）。

## 功能概述

### 知识库架构
三层记忆系统（灵感来自 Karpathy 的 LLM OS 概念）：
- **Context Window（工作记忆）** — 当前 session 可见内容，快但易失
- **MEMORY.md（长期记忆）** — 跨 session 的精炼记忆
- **kb/（知识库）** — 结构化知识，按主题分类，用标签建立关联

### 知识组织方式
- **主题（Topics）** — 知识的分类容器，每个主题一个文件
- **概念（Concepts）** — 原子化的知识单元，归属于主题
- **[kb:tag] 标签** — 概念之间的关系链接，形成知识图谱

## 触发方式

### 方式一：初始化（用户发送 zip 文件或要求设置）

1. 使用 `feishu_im_user_fetch_resource` 下载该文件
2. 解压到临时目录：`unzip /path/to/file.zip -d /tmp/kb-install/`
3. 检查解压内容中是否有 `INSTALL.md` 或 `skills/kb-bootstrap/`
4. 如果找到，读取 `INSTALL.md` 并按照其中的步骤执行
5. 将 `skills/kb-bootstrap/` 复制到 workspace 的 `skills/` 目录下（如果不存在）

用户说"帮我设置知识库"、"run kb-bootstrap" 等，直接读取并执行 `BOOTSTRAP.md`。

### 方式二：日常知识管理

当 `kb/` 目录已存在时，你拥有以下日常能力：

**添加知识：** 用户说"记住这个"、"把这个加到知识库" →
1. 读取 `kb/KB_GUIDE.md` 了解操作规范
2. 分类到已有主题或创建新主题
3. 提取概念，添加 [kb:tag] 链接
4. 更新 `kb/KB_INDEX.md`

**查询知识：** 用户问知识库相关问题 →
1. 读取 `kb/KB_INDEX.md` 找到相关主题
2. 读取对应的 `kb/topics/{slug}.md`
3. 沿着 [kb:tag] 链接读取关联主题
4. 综合回答

**定时维护：** Cron 任务 kb-maintain（每 6 小时）→
1. 读取并执行 `kb/KB_MAINTAIN.md` 中的维护流程
2. 从知识源索引新内容、检查标签完整性、解析存根、审查过期内容
3. 输出维护摘要报告

## 执行流程（初始化）

**严格按照** `BOOTSTRAP.md` 中的步骤顺序执行，不要跳步：

1. **环境检查** — 运行 `python3 skills/kb-bootstrap/scripts/check_env.py`，向用户报告结果
2. **逐个询问用户**（最关键的一步）：
   - Q1: KB 名称和用途
   - Q2: **Wiki 根节点**（飞书 Wiki URL / space_id / 本地路径 / skip）← 这是核心问题，不能跳过
   - Q3: 语言
   - Q4: 初始主题（1-5 个）
   - Q5: 索引规则
   - **每次只问一个问题，等用户回答后再问下一个**
3. **创建 KB 结构** — 创建 `kb/` 目录、`kb/topics/` 目录、配置文件、操作手册、初始主题文件
4. **Wiki 对接** — 如果用户提供了飞书 Wiki，在指定根节点下创建知识库页面结构
5. **注册维护定时任务** — 创建 cron 任务 `kb-maintain`（每 6h），执行 dry run 验证
6. **注册到 MEMORY.md** — 在现有 MEMORY.md 末尾追加 KB 信息（不覆盖）
7. **汇报完成** — 告诉用户 KB 已就绪

**注意：templates/ 目录下的文件仅供参考，绝对不要直接复制为 KB 文件。**

## 安全规则

- **绝不覆盖** workspace 根目录的 SOUL.md、IDENTITY.md、USER.md、AGENTS.md
- 所有 KB 文件仅在 `kb/` 子目录下创建
- 对 MEMORY.md 仅做追加操作
- 不要将敏感凭证（API Key、密码等）写入知识库文件

## 文件结构

```
skills/kb-bootstrap/
├── SKILL.md          ← 本文件（技能说明）
├── BOOTSTRAP.md      ← 初始化执行步骤
├── KB_GUIDE.md       ← 知识库操作手册（初始化时复制到 kb/）
├── KB_MAINTAIN.md    ← 维护脚本（cron 定时执行，初始化时复制到 kb/）
└── scripts/
    └── check_env.py  ← 环境检查脚本
```
