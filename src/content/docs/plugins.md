---
title: "创建插件"
order: 22
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "创建自定义插件以通过技能、代理、挂钩和 MCP 服务器扩展 Claude Code。"
sourceUrl: "https://code.claude.com/docs/en/plugins.md"
sourceTitle: "Create plugins"
tags: []
---
# 创建插件

> 创建自定义插件以通过技能、代理、挂钩和 MCP 服务器扩展 Claude Code。

插件允许您使用可在项目和团队之间共享的自定义功能来扩展 Claude Code。本指南涵盖使用技能、代理、挂钩和 MCP 服务器创建您自己的插件。

想要安装现有插件？请参阅[发现并安装插件](./discover-plugins)。有关完整的技术规格，请参阅[插件参考](./plugins-reference)。

## 何时使用插件 vs 独立配置

Claude Code 支持两种添加自定义技能、代理和挂钩的方式：

|方法|技能名称|最适合 |
| :---------------------------------------------------------- | :-------------------- | :---------------------------------------------------------------------------------------------- |
| **独立**（`.claude/` 目录）| `/hello` |个人工作流程、特定于项目的定制、快速实验 |
| **插件**（带有 `.claude-plugin/plugin.json` 的目录）| `/plugin-name:hello` |与队友共享、分发到社区、版本化发布、跨项目可重用 |

**在以下情况下使用独立配置：

* 您正在为单个项目定制 Claude Code
* 配置是个人的，不需要共享
* 在打包之前你正在试验技能或钩子
* 您需要简短的技能名称，例如 `/hello` 或 `/deploy`

**在以下情况下使用插件**：

* 您想与您的团队或社区共享功能
* 您在多个项目中需要相同的技能/代理
* 您需要版本控制和轻松更新您的扩展
* 您正在通过市场进行分发
* 您可以使用诸如 `/my-plugin:hello` 这样的命名空间技能（命名空间可以防止插件之间发生冲突）

**提示**

从 `.claude/` 中的独立配置开始进行快速迭代，然后在准备好共享时[转换为插件](#convert-existing-configurations-to-plugins)。

## 快速入门

本快速入门将引导您创建具有自定义技能的插件。您将创建一个清单（定义插件的配置文件），添加技能，并使用 `--plugin-dir` 标志在本地测试它。

### 先决条件

* Claude Code [已安装并经过验证](./quickstart#step-1-install-claude-code)
* Claude Code版本1.0.33或更高版本（运行`claude --version`检查）

**注意**

如果您没有看到 `/plugin` 命令，请将 Claude Code 更新到最新版本。请参阅[故障排除](./troubleshooting) 了解升级说明。

### 创建你的第一个插件

### 创建插件目录

每个插件都位于自己的目录中，其中包含清单和您的技能、代理或挂钩。立即创建一个：

```bash
mkdir my-first-plugin
```

  
### 创建插件清单

`.claude-plugin/plugin.json` 处的清单文件定义了您的插件的身份：其名称、描述和版本。 Claude Code 使用此元数据在插件管理器中显示您的插件。

在插件文件夹中创建 `.claude-plugin` 目录：

```bash
mkdir my-first-plugin/.claude-plugin
```

然后使用以下内容创建 `my-first-plugin/.claude-plugin/plugin.json`：

```json my-first-plugin/.claude-plugin/plugin.json
{
"name": "my-first-plugin",
"description": "A greeting plugin to learn the basics",
"version": "1.0.0",
"author": {
"name": "Your Name"
}
}
```
|领域 |目的|
| :------------ | :-------------------------------------------------------------------------------------------------------- |
| `name` |唯一标识符和技能命名空间。技能以此为前缀（例如，`/my-first-plugin:hello`）。 |
| `description` |浏览或安装插件时显示在插件管理器中。                                       |
| `version` |使用[语义版本控制](./plugins-reference#version-management) 跟踪版本。                  |
| `author` |选修的。有助于归因。                                                                     |

有关 `homepage`、`repository` 和 `license` 等其他字段，请参阅[完整清单架构](./plugins-reference#plugin-manifest-schema)。

  
### 添加技能

技能位于 `skills/` 目录中。每个技能都是一个包含 `SKILL.md` 文件的文件夹。文件夹名称成为技能名称，以插件的命名空间为前缀（名为 `my-first-plugin` 的插件中的 `hello/` 创建 `/my-first-plugin:hello`）。

在你的插件文件夹中创建一个技能目录：

```bash
mkdir -p my-first-plugin/skills/hello
```

然后使用以下内容创建 `my-first-plugin/skills/hello/SKILL.md`：

```markdown my-first-plugin/skills/hello/SKILL.md
---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.
```

  
### 测试你的插件

使用 `--plugin-dir` 标志运行 Claude Code 来加载您的插件：

```bash
claude --plugin-dir ./my-first-plugin
```

Claude Code 启动后，尝试您的新技能：

```shell
/my-first-plugin:hello
```

您将看到 Claude 回复问候语。运行 `/help` 以查看插件命名空间下列出的您的技能。

**注意**

**为什么要命名空间？** 插件技能始终是命名空间的（如 `/greet:hello`），以防止多个插件具有同名技能时发生冲突。

要更改命名空间前缀，请更新 `plugin.json` 中的 `name` 字段。

  
### 添加技能参数

通过接受用户输入使您的技能充满活力。 `$ARGUMENTS` 占位符捕获用户在技能名称后提供的任何文本。

更新您的 `SKILL.md` 文件：

```markdown my-first-plugin/skills/hello/SKILL.md
---
description: Greet the user with a personalized message
---

# Hello Skill

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
```

运行 `/reload-plugins` 以获取更改，然后尝试使用您的名字执行该技能：

```shell
/my-first-plugin:hello Alex
```

Claude 会叫出您的名字来迎接您。有关将参数传递给技能的更多信息，请参阅[技能](./skills#pass-arguments-to-skills)。

您已经成功创建并测试了具有以下关键组件的插件：

* **插件清单** (`.claude-plugin/plugin.json`)：描述插件的元数据
* **技能目录** (`skills/`)：包含您的自定义技能
* **技能参数** (`$ARGUMENTS`)：捕获动态行为的用户输入

**提示**

`--plugin-dir` 标志对于开发和测试很有用。当您准备好与其他人共享您的插件时，请参阅[创建和分发插件市场](./plugin-marketplaces)。

## 插件结构概述

您已经创建了一个具有技能的插件，但插件可以包含更多内容：自定义代理、挂钩、MCP 服务器和 LSP 服务器。

**警告**

**常见错误**：请勿将 `commands/`、`agents/`、`skills/` 或 `hooks/` 放入 `.claude-plugin/` 目录中。只有 `plugin.json` 位于 `.claude-plugin/` 内部。所有其他目录必须位于插件根级别。|目录 |地点 |目的|
| :---------------- | :---------- | :---------------------------------------------------------------------------------------- |
| `.claude-plugin/` |插件根目录 |包含 `plugin.json` 清单（如果组件使用默认位置，则可选）|
| `commands/` |插件根目录 | Markdown 文件形式的技能 |
| `agents/` |插件根目录 |自定义代理定义 |
| `skills/` |插件根目录 | `SKILL.md` 文件的代理技能 |
| `hooks/` |插件根目录 | `hooks.json` 中的事件处理程序 |
| `.mcp.json` |插件根目录 | MCP 服务器配置 |
| `.lsp.json` |插件根目录 |用于代码智能的 LSP 服务器配置 |
| `settings.json` |插件根目录 |启用插件时应用默认[设置](./settings) |

**注意**

**后续步骤**：准备好添加更多功能了吗？跳转到[开发更复杂的插件](#develop-more-complex-plugins)添加代理、钩子、MCP服务器和LSP服务器。有关所有插件组件的完整技术规格，请参阅[插件参考](./plugins-reference)。

## 开发更复杂的插件

一旦您熟悉了基本插件，您就可以创建更复杂的扩展。

### 将技能添加到您的插件中

插件可以包含[代理技能](./skills)以扩展Claude的功能。技能是模型调用的：Claude 根据任务上下文自动使用它们。

在插件根目录中添加 `skills/` 目录，其中包含包含 `SKILL.md` 文件的 Skill 文件夹：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

每个 `SKILL.md` 都需要包含 `name` 和 `description` 字段的 frontmatter，后面是说明：

```yaml
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

安装插件后，运行 `/reload-plugins` 加载技能。有关完整的技能创作指南，包括渐进式披露和工具限制，请参阅[代理技能](./skills)。

### 将 LSP 服务器添加到您的插件中

**提示**

对于 TypeScript、Python 和 Rust 等常见语言，请从官方市场安装预构建的 LSP 插件。仅当您需要支持尚未涵盖的语言时，才创建自定义 LSP 插件。

LSP（语言服务器协议）插件为 Claude 提供实时代码智能。如果您需要支持没有官方 LSP 插件的语言，您可以通过向插件添加 `.lsp.json` 文件来创建自己的插件：

```json .lsp.json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

安装插件的用户必须在其计算机上安装语言服务器二进制文件。

有关完整的 LSP 配置选项，请参阅 [LSP 服务器](./plugins-reference#lsp-servers)。

### 使用您的插件提供默认设置

插件可以在插件根目录中包含 `settings.json` 文件，以便在启用插件时应用默认配置。目前仅支持 `agent` 密钥。设置 `agent` 会激活插件的 [自定义代理](./sub-agents) 之一作为主线程，应用其系统提示、工具限制和模型。这允许插件更改 Claude Code 在启用时的默认行为方式。

```json settings.json
{
  "agent": "security-reviewer"
}
```

此示例激活在插件的 `agents/` 目录中定义的 `security-reviewer` 代理。 `settings.json` 中的设置优先于 `plugin.json` 中声明的 `settings`。未知的键将被默默地忽略。

### 组织复杂的插件

对于具有许多组件的插件，请按功能组织目录结构。有关完整的目录布局和组织模式，请参阅[插件目录结构](./plugins-reference#plugin-directory-structure)。

### 在本地测试您的插件

在开发过程中使用 `--plugin-dir` 标志来测试插件。这会直接加载您的插件，无需安装。

```bash
claude --plugin-dir ./my-plugin
```

当 `--plugin-dir` 插件与已安装的市场插件同名时，本地副本优先用于该会话。这使您可以测试对已安装插件的更改，而无需先卸载它。由托管设置强制启用的市场插件是唯一的例外，并且无法覆盖。

当您对插件进行更改时，运行 `/reload-plugins` 即可获取更新，而无需重新启动。这将重新加载命令、技能、代理、挂钩、插件 MCP 服务器和插件 LSP 服务器。测试您的插件组件：

* 使用 `/plugin-name:skill-name` 试试你的技能
* 检查代理是否出现在 `/agents` 中
* 验证钩子是否按预期工作

**提示**

您可以通过多次指定标志来一次加载多个插件：

```bash
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

### 调试插件问题

如果您的插件未按预期工作：

1. **检查结构**：确保您的目录位于插件根目录，而不是 `.claude-plugin/` 内
2. **单独测试组件**：分别检查每个命令、代理和钩子
3. **使用验证和调试工具**：有关 CLI 命令和故障排除技巧，请参阅[调试和开发工具](./plugins-reference#debugging-and-development-tools)

### 分享你的插件

当您的插件准备好共享时：

1. **添加文档**：包含带有安装和使用说明的 `README.md`
2. **版本化您的插件**：在 `plugin.json` 中使用 [语义版本控制](./plugins-reference#version-management)
3. **创建或使用市场**：通过[插件市场](./plugin-marketplaces)分发进行安装
4. **与其他人一起测试**：让团队成员在更广泛的分发之前测试插件

一旦您的插件进入市场，其他人就可以按照[发现并安装插件](./discover-plugins)中的说明安装它。

### 将您的插件提交到官方市场

要将插件提交到官方 Anthropic 市场，请使用应用内提交表单之一：

* **Claude.ai**：[claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **控制台**：[platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

**注意**

完整的技术规范、调试技巧和分发策略，请参见[插件参考](./plugins-reference)。

## 将现有配置转换为插件

如果您的 `.claude/` 目录中已有技能或挂钩，您可以将它们转换为插件，以便于共享和分发。

### 迁移步骤### 创建插件结构

创建一个新的插件目录：

```bash
mkdir -p my-plugin/.claude-plugin
```

在 `my-plugin/.claude-plugin/plugin.json` 创建清单文件：

```json my-plugin/.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

  
### 复制现有文件

将现有配置复制到插件目录：

```bash
# Copy commands
cp -r .claude/commands my-plugin/

# Copy agents (if any)
cp -r .claude/agents my-plugin/

# Copy skills (if any)
cp -r .claude/skills my-plugin/
```

  
### 迁移钩子

如果您的设置中有钩子，请创建一个钩子目录：

```bash
mkdir my-plugin/hooks
```

使用您的挂钩配置创建 `my-plugin/hooks/hooks.json`。从 `.claude/settings.json` 或 `settings.local.json` 复制 `hooks` 对象，因为格式相同。该命令在标准输入上接收作为 JSON 的挂钩输入，因此使用 `jq` 提取文件路径：

```json my-plugin/hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
      }
    ]
  }
}
```

  
### 测试您迁移的插件

加载您的插件以验证一切正常：

```bash
claude --plugin-dir ./my-plugin
```

测试每个组件：运行命令，检查 `/agents` 中出现的代理，并验证钩子是否正确触发。

### 迁移时会发生什么变化

|独立 (`.claude/`) |插件 |
| :---------------------------- | :-------------------------------- |
|仅在一个项目中可用 |可以通过市场共享 |
| `.claude/commands/` 中的文件 | `plugin-name/commands/` 中的文件 |
| `settings.json` 中的挂钩 | `hooks/hooks.json` 中的挂钩 |
|必须手动复制才能分享|使用 `/plugin install` 安装 |

**注意**

迁移后，您可以从 `.claude/` 中删除原始文件以避免重复。加载时插件版本将优先。

## 后续步骤

现在您已经了解了 Claude Code 的插件系统，以下是针对不同目标的建议路径：

### 对于插件用户

* [发现并安装插件](./discover-plugins)：浏览市场并安装插件
* [配置团队市场](./discover-plugins#configure-team-marketplaces)：为您的团队设置存储库级插件

### 对于插件开发者

* [创建并分发市场](./plugin-marketplaces)：打包并共享您的插件
* [插件参考](./plugins-reference)：完整的技术规范
* 深入研究特定的插件组件：
  * [技能](./skills)：技能发展详情
  * [子代理](./sub-agents)：代理配置和功能
  * [Hooks](./hooks)：事件处理和自动化
  * [MCP](./mcp): 外部工具集成
