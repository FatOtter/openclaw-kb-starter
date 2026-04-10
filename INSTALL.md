# OpenClaw KB Starter — 安装指南

> **这是给 Bot 看的安装说明。** 当用户发送这个 zip 文件时，按照以下步骤操作。

## 你收到了什么

这是一个 Knowledge Base（知识库）管理系统。它会给你添加一套结构化的知识管理能力：
- 按**主题**分类知识
- 将知识分解为**原子概念**
- 用 **[kb:tag]** 标签建立概念之间的关系
- 从飞书 Wiki、本地文件或用户输入中**持续索引**新知识

## 安装步骤

### Step 1: 安装技能文件

将解压目录中的 `skills/kb-bootstrap/` 复制到你的 workspace：

```bash
cp -r <解压路径>/skills/kb-bootstrap/ ~/.openclaw/workspace/skills/kb-bootstrap/
```

注意：`<解压路径>` 是你解压 zip 后的实际目录，例如 `/tmp/kb-starter/openclaw-kb-starter-0.1.0/`。

如果 `skills/kb-bootstrap/` 已经存在，跳过这一步。

### Step 2: 运行 KB Bootstrap

读取并执行 `skills/kb-bootstrap/BOOTSTRAP.md` 中的完整流程：

1. 运行环境检查（`python3 skills/kb-bootstrap/scripts/check_env.py`）
2. 向用户报告检查结果
3. 逐个询问用户 KB 配置信息（名称、来源、语言、**初始主题**、索引规则）
4. 生成 KB 文件结构到 `kb/` 目录（包含操作手册、主题文件、索引）
5. 在 MEMORY.md 末尾追加 KB 信息

### Step 3: 确认完成

告诉用户 KB 已设置完毕，并汇报创建了哪些文件。

**重要：安装完成后，读取 `kb/KB_GUIDE.md` — 这是你管理知识库的操作手册。**

## 重要提醒

- **不要修改** SOUL.md、IDENTITY.md、USER.md、AGENTS.md
- 所有 KB 文件放在 `kb/` 子目录下
- 对 MEMORY.md 仅追加，不覆盖
