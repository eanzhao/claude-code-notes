---
title: "插件参考"
order: 64
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "Claude Code 插件系统的完整技术参考，包括架构、CLI 命令和组件规范。"
sourceUrl: "https://code.claude.com/docs/en/plugins-reference.md"
sourceTitle: "Plugins reference"
tags: []
---
# 插件参考

> Claude Code 插件系统的完整技术参考，包括架构、CLI 命令和组件规范。

**提示**

想要安装插件？请参阅[发现并安装插件](./discover-plugins)。有关创建插件的信息，请参阅[插件](./plugins)。有关分发插件的信息，请参阅[插件市场](./plugin-marketplaces)。

本参考提供了 Claude Code 插件系统的完整技术规范，包括组件架构、CLI 命令和开发工具。

**插件**是一个独立的组件目录，它通过自定义功能扩展 Claude Code。插件组件包括技能、代理、挂钩、MCP 服务器和 LSP 服务器。

## 插件组件参考

### 技能

插件为 Claude Code 添加技能，创建您或 Claude 可以调用的 `/name` 快捷方式。

**位置**：插件根目录中的 `skills/` 或 `commands/` 目录

**文件格式**：技能为`SKILL.md`的目录；命令是简单的 Markdown 文件

**技能结构**：

```text
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

**集成行为**：

* 安装插件时会自动发现技能和命令
* Claude可以根据任务上下文自动调用它们
* 技能可以包括支持文件以及 SKILL.md

有关完整详细信息，请参阅[技能](./skills)。

### 代理

插件可以为特定任务提供专门的子代理，Claude 可以在适当的时候自动调用这些子代理。

**位置**：插件根目录中的 `agents/` 目录

**文件格式**：描述代理功能的 Markdown 文件

**代理结构**：

```markdown
---
name: agent-name
description: What this agent specializes in and when Claude should invoke it
---

Detailed system prompt for the agent describing its role, expertise, and behavior.
```

**整合点**：

* 代理出现在`/agents`界面
* Claude可以根据任务上下文自动调用代理
* 代理可以由用户手动调用
* 插件代理与内置 Claude 代理一起工作

有关完整详细信息，请参阅[子代理](./sub-agents)。

### 挂钩

插件可以提供自动响应 Claude Code 事件的事件处理程序。

**位置**：插件根目录中的`hooks/hooks.json`，或内联在plugin.json中

**格式**：带有事件匹配器和操作的 JSON 配置

**挂钩配置**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**可用活动**：

* `PreToolUse`：在 Claude 使用任何工具之前
* `PostToolUse`：Claude成功使用任何工具后
* `PostToolUseFailure`：Claude工具执行失败后
* `PermissionRequest`：当显示权限对话框时
* `UserPromptSubmit`：当用户提交提示时
* `Notification`：当 Claude Code 发送通知时
* `Stop`：当 Claude 尝试停止时
* `SubagentStart`：启动子代理时
* `SubagentStop`：当子代理尝试停止时
* `SessionStart`：在会议开始时
* `SessionEnd`：课程结束时
* `TeammateIdle`：当特工队队友即将闲置时
* `TaskCompleted`：当任务被标记为已完成时
* `PreCompact`：压缩对话历史之前
* `PostCompact`：压缩对话历史记录后

**挂钩类型**：

* `command`：执行shell命令或脚本
* `prompt`：使用 LLM 评估提示（使用 `$ARGUMENTS` 占位符作为上下文）
* `agent`：使用用于复杂验证任务的工具运行代理验证器### MCP 服务器

插件可以捆绑 Model Context Protocol (MCP) 服务器，以将 Claude Code 与外部工具和服务连接。

**位置**：插件根目录中的`.mcp.json`，或内联在plugin.json中

**格式**：标准 MCP 服务器配置

**MCP 服务器配置**：

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**集成行为**：

* 插件 MCP 服务器在插件启用时自动启动
* 服务器在 Claude 工具包中显示为标准 MCP 工具
* 服务器功能与 Claude 现有工具无缝集成
* 插件服务器可以独立于用户MCP服务器进行配置

### LSP 服务器

**提示**

想要使用 LSP 插件？从官方市场安装它们：在 `/plugin` Discover 选项卡中搜索“lsp”。本节介绍如何为官方市场未涵盖的语言创建 LSP 插件。

插件可以提供[语言服务器协议](https://microsoft.github.io/language-server-protocol/) (LSP) 服务器，以便在处理代码库时为 Claude 提供实时代码智能。

LSP 集成提供：

* **即时诊断**：Claude 在每次编辑后立即看到错误和警告
* **代码导航**：转到定义、查找引用和悬停信息
* **语言意识**：代码符号的类型信息和文档

**位置**：插件根目录中的 `.lsp.json`，或内嵌在 `plugin.json` 中

**格式**：JSON 配置将语言服务器名称映射到其配置

**`.lsp.json` 文件格式**：

```json
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

**内联于 `plugin.json`**：

```json
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**必填字段：**

|领域 |描述 |
| :-------------------- | ：-------------------------------------------------------- |
| `command` |要执行的 LSP 二进制文件（必须位于 PATH 中）|
| `extensionToLanguage` |将文件扩展名映射到语言标识符 |

**可选字段：**

|领域|描述 |
| :---------------------- | :-------------------------------------------------------- |
| `args` | LSP 服务器的命令行参数 |
| `transport` |通信传输：`stdio`（默认）或 `socket` |
| `env` |启动服务器时设置的环境变量 |
| `initializationOptions` |初始化期间传递给服务器的选项 |
| `settings` |通过 `workspace/didChangeConfiguration` 传递的设置 |
| `workspaceFolder` |服务器的工作区文件夹路径 |
| `startupTimeout` |等待服务器启动的最长时间（毫秒）|
| `shutdownTimeout` |等待正常关闭的最长时间（毫秒）|
| `restartOnCrash` |服务器崩溃时是否自动重启 |
| `maxRestarts` |放弃之前尝试重新启动的最大次数 |

**警告**

**您必须单独安装语言服务器二进制文件。** LSP 插件配置 Claude Code 连接到语言服务器的方式，但它们不包括服务器本身。如果您在 `/plugin` 错误选项卡中看到 `Executable not found in $PATH`，请安装您的语言所需的二进制文件。**可用的 LSP 插件：**

|插件 |语言服务器|安装命令 |
| ：-------------- | ：-------------------------- | :---------------------------------------------------------------------------------------- |
| `pyright-lsp` | Pyright (Python) | `pip install pyright` 或 `npm install -g pyright` |
| `typescript-lsp` | TypeScript 语言服务器 | `npm install -g typescript-language-server typescript` |
| `rust-lsp` |锈迹分析仪| [参见 rust-analyzer 安装](https://rust-analyzer.github.io/manual.html#installation) |

首先安装语言服务器，然后从市场安装插件。

***

## 插件安装范围

安装插件时，您选择一个 **范围** 来确定插件的可用位置以及其他人可以使用它：

|范围 |设置文件 |使用案例 |
| :-------- | :---------------------------------------------------------- | :-------------------------------------------------------------------- |
| `user` | `~/.claude/settings.json` |所有项目都可用的个人插件（默认）|
| `project` | `.claude/settings.json` |通过版本控制共享团队插件 |
| `local` | `.claude/settings.local.json` |项目特定的插件，gitignored |
| `managed` | [托管设置](./settings#settings-files) |托管插件（只读，仅更新）|

插件使用与其他 Claude Code 配置相同的范围系统。有关安装说明和范围标志，请参阅[安装插件](./discover-plugins#install-plugins)。有关范围的完整说明，请参阅[配置范围](./settings#configuration-scopes)。

***

## 插件清单架构

`.claude-plugin/plugin.json` 文件定义插件的元数据和配置。本节记录了所有支持的字段和选项。

清单是可选的。如果省略，Claude Code 会自动发现[默认位置](#file-locations-reference) 中的组件，并从目录名称中派生插件名称。当您需要提供元数据或自定义组件路径时，请使用清单。

### 完整架构

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### 必填字段

如果您包含清单，则 `name` 是唯一必填字段。

|领域 |类型 |描述 |示例|
| :-----| :-----| :---------------------------------------- | :-------------------- |
| `name` |字符串|唯一标识符（短横线大小写，无空格）| `"deployment-tools"` |

该名称用于命名空间组件。例如，在用户界面中，
名为 `plugin-dev` 的插件的代理 `agent-creator` 将显示为
`plugin-dev:agent-creator`。

### 元数据字段|领域 |类型 |描述 |示例|
| :------------ | :-----| :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `version` |字符串|语义版本。如果也在市场条目中设置，则 `plugin.json` 优先。您只需将其设置在一处即可。 | `"2.1.0"` |
| `description` |字符串|插件用途简述| `"Deployment automation tools"` |
| `author` |对象|作者信息 | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage` |字符串|文档网址 | `"https://docs.example.com"` |
| `repository` |字符串|源代码网址| `"https://github.com/user/plugin"` |
| `license` |字符串|许可证标识符| `"MIT"`、`"Apache-2.0"` |
| `keywords` |数组|发现标签| `["deployment", "ci-cd"]` |

### 组件路径字段|领域 |类型 |描述 |示例|
| :------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ |
| `commands` |字符串\|数组|附加命令文件/目录| `"./custom/cmd.md"` 或 `["./cmd1.md"]` |
| `agents` |字符串\|数组|附加代理文件 | `"./custom/agents/reviewer.md"` |
| `skills` |字符串\|数组|附加技能目录 | `"./custom/skills/"` |
| `hooks` |字符串\|数组\|对象|挂钩配置路径或内联配置 | `"./my-extra-hooks.json"` |
| `mcpServers` |字符串\|数组\|对象| MCP 配置路径或内联配置 | `"./my-extra-mcp-config.json"` |
| `outputStyles` |字符串\|数组|附加输出样式文件/目录 | `"./styles/"` |
| `lspServers` |字符串\|数组\|对象| [语言服务器协议](https://microsoft.github.io/language-server-protocol/) 代码智能配置（转到定义、查找引用等）| `"./.lsp.json"` |

### 路径行为规则

**重要**：自定义路径补充默认目录 - 它们不会替换它们。

* 如果 `commands/` 存在，除了自定义命令路径之外还会加载它
* 所有路径必须相对于插件根目录并以 `./` 开头
* 来自自定义路径的命令使用相同的命名和命名空间规则
* 可以将多个路径指定为数组以提高灵活性

**路径示例**：

```json
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### 环境变量

Claude Code 提供两个变量用于引用插件路径。两者在技能内容、代理内容、挂钩命令和 MCP 或 LSP 服务器配置中出现的任何位置都会被内联替换。两者还作为环境变量导出以挂钩进程和 MCP 或 LSP 服务器子进程。

**`${CLAUDE_PLUGIN_ROOT}`**：插件安装目录的绝对路径。使用它来引用与插件捆绑的脚本、二进制文件和配置文件。当插件更新时，此路径会发生变化，因此您在此处编写的文件不会在更新后保留下来。**`${CLAUDE_PLUGIN_DATA}`**：更新后仍然存在的插件状态的持久目录。将此用于已安装的依赖项，例如 `node_modules` 或 Python 虚拟环境、生成的代码、缓存以及应在插件版本之间保留的任何其他文件。第一次引用该变量时会自动创建该目录。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### 持久数据目录

`${CLAUDE_PLUGIN_DATA}` 目录解析为 `~/.claude/plugins/data/{id}/`，其中 `{id}` 是插件标识符，其中 `a-z`、`A-Z`、`0-9`、`_` 和 `-` 之外的字符被 `-` 替换。对于安装为 `formatter@my-marketplace` 的插件，目录为 `~/.claude/plugins/data/formatter-my-marketplace/`。

常见用途是安装语言依赖项一次，然后在会话和插件更新中重复使用它们。由于数据目录的寿命比任何单个插件版本的寿命都长，因此仅检查目录存在无法检测更新何时更改插件的依赖项清单。推荐的模式将捆绑清单与数据目录中的副本进行比较，并在它们不同时重新安装。

此 `SessionStart` 挂钩会在第一次运行时安装 `node_modules`，并在插件更新包含更改的 `package.json` 时再次安装：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

当存储的副本丢失或与捆绑的副本不同时，`diff` 退出非零，涵盖首次运行和依赖项更改更新。如果 `npm install` 失败，尾随 `rm` 将删除复制的清单，以便下一个会话重试。

然后，捆绑在 `${CLAUDE_PLUGIN_ROOT}` 中的脚本可以针对持久的 `node_modules` 运行：

```json
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

当您从最后安装的范围卸载插件时，数据目录会自动删除。 `/plugin`界面显示目录大小并在删除前进行提示。 CLI默认删除；通过 [`--keep-data`](#plugin-uninstall) 来保存它。

***

## 插件缓存和文件解析

插件通过以下两种方式之一指定：

* 在会话期间通过 `claude --plugin-dir`。
* 通过市场，为未来的会议安装。

出于安全和验证目的，Claude Code 将 *marketplace* 插件复制到用户的本地 **插件缓存** (`~/.claude/plugins/cache`)，而不是就地使用它们。在开发引用外部文件的插件时，理解这种行为非常重要。

### 路径遍历限制

安装的插件无法引用其目录之外的文件。遍历插件根目录之外的路径（例如 `../shared-utils`）在安装后将不起作用，因为这些外部文件不会复制到缓存中。

### 使用外部依赖项

如果您的插件需要访问其目录之外的文件，您可以在插件目录中创建指向外部文件的符号链接。在复制过程中遵循符号链接：

```bash
# Inside your plugin directory
ln -s /path/to/shared-utils ./shared-utils
```

符号链接的内容将被复制到插件缓存中。这提供了灵活性，同时保持了缓存系统的安全优势。

***

## 插件目录结构

### 标准插件布局

一个完整的插件遵循以下结构：

```text
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── settings.json            # Default settings for the plugin
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

**警告**`.claude-plugin/` 目录包含 `plugin.json` 文件。所有其他目录（commands/、agents/、skills/、hooks/）必须位于插件根目录，而不是在 `.claude-plugin/` 内。

### 文件位置参考

|组件|默认位置 |目的|
| :-------------- | :---------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **清单** | `.claude-plugin/plugin.json` |插件元数据和配置（可选）|
| **命令** | `commands/` |技能 Markdown 文件（旧版；使用 `skills/` 获取新技能）|
| **代理** | `agents/` |子代理 Markdown 文件 |
| **技能** | `skills/` | `<name>/SKILL.md`结构的技巧|
| **挂钩** | `hooks/hooks.json` |挂钩配置|
| **MCP 服务器** | `.mcp.json` | MCP 服务器定义 |
| **LSP 服务器** | `.lsp.json` |语言服务器配置|
| **设置** | `settings.json` |启用插件时应用默认配置。目前仅支持 [`agent`](./sub-agents) 设置 |

***

## CLI 命令参考

Claude Code 提供用于非交互式插件管理的 CLI 命令，对于脚本编写和自动化非常有用。

### 插件安装

从可用市场安装插件。

```bash
claude plugin install  [options]
```

**参数：**

* 针对特定市场的“`: Plugin name or `plugin-name@marketplace-name”

**选项：**

|选项 |描述 |默认 |
| :-------------------- | :------------------------------------------------ | :------ |
| `-s, --scope <scope>` |安装范围：`user`、`project` 或 `local` | `user` |
| `-h, --help` |显示命令的帮助|         |

范围决定了已安装的插件将添加到哪个设置文件。例如，--scope project 写入 .claude/settings.json 中的 `enabledPlugins`，使该插件可供克隆项目存储库的每个人使用。

**示例：**

```bash
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope (shared with team)
claude plugin install formatter@my-marketplace --scope project

# Install to local scope (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### 插件卸载

删除已安装的插件。

```bash
claude plugin uninstall  [options]
```

**参数：**

* ``: Plugin name or `插件名称@市场名称`

**选项：**|选项 |描述 |默认 |
| :-------------------- | :---------------------------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>` |从范围卸载：`user`、`project` 或 `local` | `user` |
| `--keep-data` |保留插件的[持久数据目录](#persistent-data-directory) |         |
| `-h, --help` |显示命令的帮助|         |

**别名：** `remove`、`rm`

默认情况下，从最后剩余范围卸载也会删除插件的 `${CLAUDE_PLUGIN_DATA}` 目录。使用 `--keep-data` 保留它，例如在测试新版本后重新安装时。

### 插件启用

启用已禁用的插件。

```bash
claude plugin enable  [options]
```

**参数：**

* ``: Plugin name or `插件名称@市场名称`

**选项：**

|选项 |描述 |默认 |
| :-------------------- | ：------------------------------------------ | :------ |
| `-s, --scope <scope>` |要启用的范围：`user`、`project` 或 `local` | `user` |
| `-h, --help` |显示命令的帮助|         |

### 插件禁用

禁用插件而不卸载它。

```bash
claude plugin disable  [options]
```

**参数：**

* ``: Plugin name or `插件名称@市场名称`

**选项：**

|选项 |描述 |默认 |
| :-------------------- | :---------------------------------------------------------- | :------ |
| `-s, --scope <scope>` |要禁用的范围：`user`、`project` 或 `local` | `user` |
| `-h, --help` |显示命令的帮助|         |

### 插件更新

将插件更新到最新版本。

```bash
claude plugin update  [options]
```

**参数：**

* ``: Plugin name or `插件名称@市场名称`

**选项：**

|选项 |描述 |默认 |
| :-------------------- | :-------------------------------------------------------- | :------ |
| `-s, --scope <scope>` |更新范围：`user`、`project`、`local` 或 `managed` | `user` |
| `-h, --help` |显示命令的帮助 |         |

***

## 调试和开发工具

### 调试命令

使用 `claude --debug`（或 TUI 中的 `/debug`）查看插件加载详细信息：

这表明：

* 正在加载哪些插件
* 插件清单中的任何错误
* 命令、代理和钩子注册
* MCP服务器初始化

### 常见问题|问题 |原因 |解决方案 |
| :---------------------------------- | :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|插件未加载 | `plugin.json` 无效 |运行 `claude plugin validate` 或 `/plugin validate` 以检查 `plugin.json`、技能/代理/命令 frontmatter 和 `hooks/hooks.json` 的语法和架构错误 |
|命令未出现|错误的目录结构 |确保 `commands/` 位于根目录，而不是 `.claude-plugin/` |
|钩子不发射 |脚本不可执行 |运行 `chmod +x script.sh` |
| MCP 服务器失败 |缺少 `${CLAUDE_PLUGIN_ROOT}` |对所有插件路径使用变量 |
|路径错误 |使用的绝对路径|所有路径必须是相对路径并以 `./` | 开头
| LSP `Executable not found in $PATH` |未安装语言服务器 |安装二进制文件（例如 `npm install -g typescript-language-server typescript`）|

### 错误消息示例

**清单验证错误**：

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`：检查是否缺少逗号、多余逗号或不带引号的字符串
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`：缺少必填字段
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON 语法错误

**插件加载错误**：

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`：命令路径存在，但不包含有效的命令文件
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`：marketplace.json 中的 `source` 路径指向不存在的目录
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`：删除重复的组件定义或删除市场条目中的 `strict: false`

### 钩子故障排除

**挂钩脚本不执行**：

1. 检查脚本是否可执行：`chmod +x ./scripts/your-script.sh`
2. 验证shebang行：第一行应该是`#!/bin/bash`或`#!/usr/bin/env bash`
3. 检查路径使用`${CLAUDE_PLUGIN_ROOT}`：`"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. 手动测试脚本：`./scripts/your-script.sh`

**挂钩未触发预期事件**：

1. 验证事件名称是否正确（区分大小写）：`PostToolUse`，而不是 `postToolUse`
2. 检查匹配器模式是否与您的工具匹配：`"matcher": "Write|Edit"` 用于文件操作
3. 确认挂钩类型有效：`command`、`prompt` 或 `agent`

### MCP 服务器故障排除

**服务器未启动**：

1. 检查命令是否存在且可执行
2. 验证所有路径都使用`${CLAUDE_PLUGIN_ROOT}`变量
3. 检查MCP服务器日志：`claude --debug`显示初始化错误
4. 在 Claude Code 之外手动测试服务器

**服务器工具未出现**：1. 确保服务器在 `.mcp.json` 或 `plugin.json` 中正确配置
2. 验证服务器正确实现MCP协议
3. 检查调试输出中的连接超时

### 目录结构错误

**症状**：插件加载但组件（命令、代理、挂钩）丢失。

**正确的结构**：组件必须位于插件根目录，而不是在 `.claude-plugin/` 内部。只有 `plugin.json` 属于 `.claude-plugin/`。

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Only manifest here
├── commands/            ← At root level
├── agents/              ← At root level
└── hooks/               ← At root level
```

如果您的组件位于 `.claude-plugin/` 内，请将它们移至插件根目录。

**调试清单**：

1. 运行 `claude --debug` 并查找“正在加载插件”消息
2. 检查调试输出中是否列出了每个组件目录
3. 验证文件权限是否允许读取插件文件

***

## 发行版和版本控制参考

### 版本管理

遵循插件版本的语义版本控制：

```json
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**版本格式**：`MAJOR.MINOR.PATCH`

* **主要**：重大更改（不兼容的 API 更改）
* **次要**：新功能（向后兼容的附加功能）
* **PATCH**：错误修复（向后兼容修复）

**最佳实践**：

* 从 `1.0.0` 开始您的第一个稳定版本
* 在分发更改之前更新 `plugin.json` 中的版本
* `CHANGELOG.md` 文件中的文档更改
* 使用 `2.0.0-beta.1` 等预发布版本进行测试

**警告**

Claude Code 使用版本来确定是否更新您的插件。如果您更改插件的代码但不升级 `plugin.json` 中的版本，则由于缓存，您的插件的现有用户将看不到您的更改。

如果您的插件位于 [marketplace](./plugin-marketplaces) 目录中，您可以通过 `marketplace.json` 管理版本，并省略 `plugin.json` 中的 `version` 字段。

***

## 另请参阅

* [插件](./plugins) - 教程和实际使用
* [插件市场](./plugin-marketplaces) - 创建和管理市场
* [技能](./skills) - 技能发展详情
* [子代理](./sub-agents) - 代理配置和功能
* [Hooks](./hooks) - 事件处理和自动化
* [MCP](./mcp) - 外部工具集成
* [设置](./settings) - 插件的配置选项
