---
name: kb-bootstrap
description: |
  Knowledge Base 初始化工具。当用户发送 zip 文件并提到"知识库"、"KB"、"setup"、"安装"时自动触发。
  也可通过用户指令手动触发："帮我设置知识库"、"run kb-bootstrap"、"setup KB"。
  
  **当以下情况时使用此 Skill**:
  (1) 用户发送了一个 zip 文件（特别是名为 openclaw-kb-starter.zip 的文件）
  (2) 用户要求设置/初始化知识库
  (3) 用户提到 "KB setup"、"知识库"、"kb-bootstrap"
---

# KB Bootstrap Skill

为当前 OpenClaw Bot 添加知识库（KB）系统。**不会修改任何已有的 workspace 文件**（SOUL.md、IDENTITY.md、USER.md、AGENTS.md 不受影响），仅在 `kb/` 子目录下创建新文件。

## 触发方式

### 方式一：用户发送 zip 文件
当用户通过飞书发送 zip 文件时：

1. 使用 `feishu_im_user_fetch_resource` 下载该文件
2. 解压到临时目录：`unzip /path/to/file.zip -d /tmp/kb-install/`
3. 检查解压内容中是否有 `INSTALL.md` 或 `skills/kb-bootstrap/`
4. 如果找到，读取 `INSTALL.md` 并按照其中的步骤执行
5. 将 `skills/kb-bootstrap/` 复制到 workspace 的 `skills/` 目录下（如果不存在）

### 方式二：用户直接要求
用户说"帮我设置知识库"、"run kb-bootstrap" 等，直接读取并执行 `BOOTSTRAP.md`。

## 执行流程

按顺序执行 `BOOTSTRAP.md` 中的所有步骤：

1. **环境检查** — 运行 `python3 skills/kb-bootstrap/scripts/check_env.py`，向用户报告结果
2. **询问用户** — 逐个提问：KB 名称/用途、Wiki 根节点、语言、索引规则
3. **创建 KB 结构** — 在 `kb/` 子目录下生成配置文件
4. **Wiki 对接** — 如果用户提供了飞书 Wiki URL，验证 Lark 插件是否可用
5. **注册到 MEMORY.md** — 在现有 MEMORY.md 末尾追加 KB 信息（不覆盖）
6. **汇报完成** — 告诉用户 KB 已就绪

## 安全规则

- **绝不覆盖** workspace 根目录的 SOUL.md、IDENTITY.md、USER.md、AGENTS.md
- 所有 KB 文件仅在 `kb/` 子目录下创建
- 对 MEMORY.md 仅做追加操作

## 文件结构

```
skills/kb-bootstrap/
├── SKILL.md          ← 本文件（技能说明）
├── BOOTSTRAP.md      ← 详细执行步骤
└── scripts/
    └── check_env.py  ← 环境检查脚本
```
