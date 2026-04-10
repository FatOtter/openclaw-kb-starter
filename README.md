# OpenClaw KB Starter

给任何运行中的 OpenClaw Bot 添加知识库（KB）系统。通过飞书发送 zip 文件即可触发安装，不会影响 Bot 的现有人设和配置。

## Quickstart

### 飞书发送（推荐）

1. 下载 `openclaw-kb-starter.zip`（从 [Releases](https://github.com/FatOtter/openclaw-kb-starter/releases) 或自行打包）
2. 在飞书中打开与 Bot 的对话
3. 发送 zip 文件，附带一句话："帮我安装这个知识库工具"
4. Bot 会自动：
   - 下载并解压 zip
   - 读取 `INSTALL.md` 安装指南
   - 运行环境检查
   - 逐步询问你 KB 配置（名称、Wiki 来源、语言等）
   - 在 `kb/` 目录下创建知识库文件

### 手动安装（SSH）

```bash
# 克隆到服务器
git clone https://github.com/FatOtter/openclaw-kb-starter.git /tmp/kb-starter

# 只复制技能目录到 workspace
cp -r /tmp/kb-starter/skills/kb-bootstrap/ ~/.openclaw/workspace/skills/kb-bootstrap/

# 然后在飞书中告诉 Bot："帮我设置知识库" 或 "run kb-bootstrap"
```

## 工作原理

```
用户发送 zip → Bot 下载解压 → 读取 INSTALL.md → 运行环境检查 → 询问用户配置 → 创建 kb/ 目录
```

Bot 会执行以下步骤：

1. **环境检查** — 验证 LLM 配置、飞书插件、workspace 读写权限
2. **用户访谈** — 逐个询问：KB 名称/用途、Wiki 根节点 URL、语言、索引规则
3. **创建 KB** — 在 `kb/` 子目录下生成 `KB_CONFIG.md`、`KB_MEMORY.md`、`KB_INDEX.md`
4. **Wiki 对接** — 如果提供了飞书 Wiki URL，验证插件可用性并记录
5. **注册** — 在现有 `MEMORY.md` 末尾追加 KB 引用（不覆盖）

## Zip 内容

```
openclaw-kb-starter/
├── INSTALL.md                 ← Bot 读取的安装指南（核心）
├── README.md                  ← 本文件（给人看的）
├── skills/
│   └── kb-bootstrap/
│       ├── SKILL.md           ← 技能描述（告诉 Bot 何时触发）
│       ├── BOOTSTRAP.md       ← 详细执行步骤
│       └── scripts/
│           └── check_env.py   ← 运行时依赖检查脚本
├── templates/                 ← 参考模板
│   ├── AGENTS.md
│   ├── SOUL.example.md
│   ├── USER.example.md
│   └── IDENTITY.example.md
└── memory/
    └── daily/                 ← 空目录占位
```

## 安全保证

- **不修改** Bot 的 SOUL.md、IDENTITY.md、USER.md、AGENTS.md
- 所有 KB 文件在 `kb/` 子目录下，与现有文件隔离
- 对 MEMORY.md 仅做追加操作

## 支持的 Wiki 来源

| 来源 | 状态 |
|------|------|
| 飞书 Wiki | 支持（需要 Lark 插件） |
| 本地 Markdown 文件夹 | 支持 |
| Notion | 记录 URL，需手动集成 |
| 手动输入 | 始终可用 |

## 前置要求

- 运行中的 OpenClaw Bot
- 至少一个 LLM API Key
- Python 3.8+（环境检查脚本）
- 飞书 Lark 插件（如果通过飞书使用）
