# OpenClaw KB Starter — 安装指南

> **这是给 Bot 看的安装说明。** 当用户发送这个 zip 文件时，按照以下步骤操作。

## 你收到了什么

这是一个 Knowledge Base（知识库）初始化工具包。用户希望你帮他们设置一个知识库系统。

## 安装步骤

### Step 1: 安装技能文件

将 zip 中的 `skills/kb-bootstrap/` 目录复制到你的 workspace：

```bash
cp -r /tmp/kb-install/openclaw-kb-starter/skills/kb-bootstrap/ ~/.openclaw/workspace/skills/kb-bootstrap/
```

如果 `skills/kb-bootstrap/` 已经存在，跳过这一步。

### Step 2: 运行 KB Bootstrap

读取并执行 `skills/kb-bootstrap/BOOTSTRAP.md` 中的完整流程：

1. 运行环境检查（`python3 skills/kb-bootstrap/scripts/check_env.py`）
2. 向用户报告检查结果
3. 逐个询问用户 KB 配置信息
4. 生成 KB 文件到 `kb/` 目录
5. 在 MEMORY.md 末尾追加 KB 信息

### Step 3: 确认完成

告诉用户 KB 已设置完毕，并汇报创建了哪些文件。

## 重要提醒

- **不要修改** SOUL.md、IDENTITY.md、USER.md、AGENTS.md
- 所有 KB 文件放在 `kb/` 子目录下
- 对 MEMORY.md 仅追加，不覆盖
