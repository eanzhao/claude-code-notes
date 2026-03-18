---
title: "创建自定义子代理"
order: 20
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "在 Claude Code 中创建和使用专门的 AI 子代理，以实现特定于任务的工作流程并改进上下文管理。"
sourceUrl: "https://code.claude.com/docs/en/sub-agents.md"
sourceTitle: "Create custom subagents"
tags: []
---
# 创建自定义 subagent

> 在 Claude Code 中创建专用的 AI subagent，针对特定任务优化工作流和上下文管理。

Subagent 是处理特定类型任务的专用 AI 助手。每个 subagent 都在独立的上下文窗口中运行，拥有自定义系统提示、受限的工具权限和独立的权限设置。当 Claude 遇到与 subagent 描述匹配的任务时，会自动委派给它，subagent 独立完成工作后返回结果。

**注意**

如果你需要多个 agent 并行工作并互相通信，请参阅[代理团队](./agent-teams)。Subagent 在单个会话内工作；代理团队跨不同会话协调。

Subagent 能帮你：

* **保留上下文**——把探索和实现过程隔离在主对话之外
* **强制约束**——限制 subagent 可用的工具
* **跨项目复用**——通过用户级 subagent 在所有项目中共享配置
* **专业化**——用针对特定领域的系统提示实现专业行为
* **控制成本**——把任务路由到更快更便宜的模型（如 Haiku）

Claude 根据每个 subagent 的描述来决定何时委派任务。创建 subagent 时，写清楚描述，让 Claude 知道什么时候该用它。

Claude Code 内置了几个 subagent，包括 **Explore**、**Plan** 和 **General Purpose**。你也可以创建自定义 subagent 来处理特定任务。本页介绍[内置 subagent](#built-in-subagents)、[如何创建你的第一个 subagent](#quickstart-create-your-first-subagent)、[完整配置选项](#configure-subagents)、[使用模式](#work-with-subagents)和[示例](#example-subagents)。

## 内置 subagent

Claude Code 内置了一些 subagent，Claude 会在合适的时候自动使用。每个 subagent 继承父对话的权限，并有额外的工具限制。

### Explore

快速的只读 agent，专为搜索和分析代码库优化。

* **模型**：Haiku（快速、低延迟）
* **工具**：只读工具（不能写入或编辑文件）
* **用途**：文件查找、代码搜索、代码库探索

当 Claude 需要搜索或理解代码库但不需要做修改时，会委派给 Explore。这样探索过程的输出不会占用你主对话的上下文。

调用 Explore 时，Claude 会指定深入程度：**快速**用于精准查找，**中等**用于平衡探索，**非常彻底**用于全面分析。


### Plan

在[计划模式](./common-workflows#use-plan-mode-for-safe-code-analysis)下，用于在提出方案之前收集背景信息的研究 agent。

* **模型**：继承自主对话
* **工具**：只读工具（不能写入或编辑文件）
* **用途**：为规划阶段做代码库调研

当你处于计划模式且 Claude 需要了解代码库时，会把调研任务委派给 Plan subagent。这样可以避免无限嵌套（subagent 不能再生成其他 subagent），同时仍能收集必要的上下文。


### General Purpose

能处理复杂多步骤任务的 agent，既能探索也能动手修改。

* **模型**：继承自主对话
* **工具**：所有工具
* **用途**：复杂调研、多步骤操作、代码修改

当任务需要同时探索和修改代码、需要复杂推理来解读结果、或涉及多个相关步骤时，Claude 会委派给 General Purpose。


### 其他

Claude Code 还包含一些用于特定任务的辅助 agent。它们通常自动调用，你不需要直接使用。

| Agent | 模型 | Claude 何时使用 |
| :---------------- | :----- | :-------------------------------------------------------------------- |
| Bash | 继承 | 在独立上下文中运行终端命令 |
| Statusline Setup | Sonnet | 当你运行 `/statusline` 配置状态栏时 |
| Claude Code Guide | Haiku | 当你询问 Claude Code 功能相关问题时 |

除了这些内置 subagent，你还可以用自定义提示、工具限制、权限模式、hook 和 skill 创建自己的 subagent。下面的内容介绍如何上手和自定义 subagent。

## 快速入门：创建你的第一个 subagent

Subagent 定义在带有 YAML frontmatter 的 Markdown 文件中。你可以[手动创建](#write-subagent-files)，也可以用 `/agents` 命令。

下面的步骤会带你用 `/agents` 命令创建一个用户级 subagent。这个 subagent 负责审查代码并提出改进建议。

### 打开 subagent 界面

在 Claude Code 中运行：

```text
/agents
```

  
### 选择位置

选择”**创建新代理**”，然后选择”**个人**”。这会把 subagent 保存到 `~/.claude/agents/`，在你所有项目中都可用。


### 用 Claude 生成

选择 **使用 Claude 生成**。出现提示时，描述你的 subagent：

```text
A code improvement agent that scans files and suggests improvements
for readability, performance, and best practices. It should explain
each issue, show the current code, and provide an improved version.
```

Claude 会为你生成标识符、描述和系统提示。


### 选择工具

对于只读审查者，取消勾选除**只读工具**以外的所有选项。如果选择所有工具，subagent 会继承主对话中可用的全部工具。


### 选择模型

选择 subagent 使用的模型。这个示例选 **Sonnet**，在代码分析能力和速度之间取得平衡。


### 选择颜色

为 subagent 选择背景颜色，方便你在 UI 中识别当前运行的是哪个 subagent。


### 配置记忆

选择 **启用** 可为 subagent 提供位于 `~/.claude/agent-memory/` 的[持久记忆目录](#enable-persistent-memory)。Subagent 会在此积累跨对话的经验，比如代码库模式和常见问题。如果不需要持续学习，选择**无**。


### 保存并试用

查看配置摘要。按 `s` 或 `Enter` 保存，或按 `e` 保存并在编辑器中打开文件。Subagent 立即可用，试试看：

```text
Use the code-improver agent to suggest improvements in this project
```

Claude 会委派给你的新 subagent，它会扫描代码库并返回改进建议。

现在你有了一个可以在所有项目中使用的 subagent，用来分析代码库并提出改进建议。你也可以手动创建 Markdown 文件、通过 CLI 标志定义、或通过插件分发 subagent。下面介绍所有配置选项。

## 配置 subagent

### 使用 /agents 命令

`/agents` 命令提供管理 subagent 的交互界面。运行 `/agents` 可以：

* 查看所有可用的 subagent（内置、用户、项目和插件）
* 通过引导设置或 Claude 生成来创建新 subagent
* 编辑现有 subagent 的配置和工具权限
* 删除自定义 subagent
* 有重名时查看哪些 subagent 处于活动状态

这是创建和管理 subagent 的推荐方式。如果需要手动创建或做自动化，也可以直接添加 subagent 文件。

要在不启动交互式会话的情况下列出所有已配置的 subagent，运行 `claude agents`。它会按来源分组显示 agent，并标注哪些被更高优先级的定义覆盖了。

### 选择 subagent 作用域

Subagent 是带有 YAML frontmatter 的 Markdown 文件，根据作用域存放在不同位置。当多个 subagent 同名时，优先级高的位置胜出。

| 位置 | 作用域 | 优先级 | 创建方式 |
| :---------------------------- | :---------------------- | :---------- | :------------------------------------ |
| `--agents` CLI 标志 | 当前会话 | 1（最高） | 启动 Claude Code 时传入 JSON |
| `.claude/agents/` | 当前项目 | 2 | 交互式或手动 |
| `~/.claude/agents/` | 你的所有项目 | 3 | 交互式或手动 |
| 插件的 `agents/` 目录 | 插件启用的范围 | 4（最低） | 已安装的[插件](./plugins) |

**项目 subagent**（`.claude/agents/`）适合与代码库绑定的 subagent。提交到版本控制中，团队成员可以一起使用和改进。

**用户 subagent**（`~/.claude/agents/`）是你在所有项目中都可用的个人 subagent。

**CLI 定义的 subagent** 在启动 Claude Code 时通过 JSON 传入，只存在于当前会话，不保存到磁盘，适合快速测试或自动化脚本。可以在一个 `--agents` 调用中定义多个 subagent：

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

`--agents` 标志接受的 JSON 字段与文件 subagent 的 [frontmatter](#supported-frontmatter-fields) 相同：`description`、`prompt`、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills` 和 `memory`。用 `prompt` 作为系统提示，等同于文件 subagent 中的 markdown 正文。

**插件 subagent** 来自你已安装的[插件](./plugins)，与自定义 subagent 一起显示在 `/agents` 中。创建插件 subagent 的详情请参阅[插件组件参考](./plugins-reference#agents)。

**注意** 出于安全原因，插件 subagent 不支持 `hooks`、`mcpServers` 或 `permissionMode` frontmatter 字段。从插件加载 agent 时这些字段会被忽略。如需这些功能，请把 agent 文件复制到 `.claude/agents/` 或 `~/.claude/agents/` 中。你也可以在 `settings.json` 或 `settings.local.json` 的 [`permissions.allow`](./settings#permission-settings) 中添加规则，但这些规则作用于整个会话，不仅限于插件 subagent。

### 编写 subagent 文件

Subagent 文件使用 YAML frontmatter 配置，后面跟着 Markdown 格式的系统提示：

**注意**

Subagent 在会话开始时加载。如果你手动添加了文件，需要重启会话或使用 `/agents` 立即加载。

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter 定义 subagent 的元数据和配置，正文内容成为指导 subagent 行为的系统提示。Subagent 只接收这个系统提示（加上工作目录等基本环境信息），不会收到完整的 Claude Code 系统提示。

#### 支持的 frontmatter 字段

以下字段可在 YAML frontmatter 中使用。只有 `name` 和 `description` 是必填的。

| 字段 | 必填 | 说明 |
| :---------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` | 是 | 唯一标识符，使用小写字母和连字符 |
| `description` | 是 | 描述 Claude 应在什么情况下委派给此 subagent |
| `tools` | 否 | subagent 可用的[工具](#available-tools)。省略则继承所有工具 |
| `disallowedTools` | 否 | 禁用的工具，从继承或指定的列表中排除 |
| `model` | 否 | 使用的[模型](#choose-a-model)：`sonnet`、`opus`、`haiku`、完整模型 ID（如 `claude-opus-4-6`）或 `inherit`。默认 `inherit` |
| `permissionMode` | 否 | [权限模式](#permission-modes)：`default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 或 `plan` |
| `maxTurns` | 否 | subagent 停止前的最大 agent 轮数 |
| `skills` | 否 | 启动时加载到 subagent 上下文的 [skill](./skills)。注入的是完整 skill 内容，而非仅供调用。Subagent 不会从父对话继承 skill |
| `mcpServers` | 否 | 此 subagent 可用的 [MCP 服务器](./mcp)。每个条目可以是引用已配置服务器的名称（如 `"slack"`），或以服务器名称为键、完整 [MCP 服务器配置](./mcp#configure-mcp-servers)为值的内联定义 |
| `hooks` | 否 | 作用域限于此 subagent 的[生命周期 hook](#define-hooks-for-subagents) |
| `memory` | 否 | [持久记忆作用域](#enable-persistent-memory)：`user`、`project` 或 `local`，实现跨会话学习 |
| `background` | 否 | 设为 `true` 则始终作为[后台任务](#run-subagents-in-foreground-or-background)运行。默认 `false` |
| `isolation` | 否 | 设为 `worktree` 则在临时 [git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中运行 subagent，给它一份独立的仓库副本。如果 subagent 没有做任何修改，worktree 会自动清理 |

### 选择模型

`model` 字段控制 subagent 使用哪个 [AI 模型](./model-config)：

* **模型别名**：使用 `sonnet`、`opus` 或 `haiku`
* **完整模型 ID**：使用完整 ID，如 `claude-opus-4-6` 或 `claude-sonnet-4-6`，与 `--model` 标志接受的值相同
* **继承**：使用与主对话相同的模型
* **省略**：不指定时默认为 `inherit`

### 控制 subagent 能力

你可以通过工具权限、权限模式和条件规则来控制 subagent 能做什么。

#### 可用工具

Subagent 可以使用 Claude Code 的任何[内置工具](./tools-reference)。默认继承主对话中的所有工具，包括 MCP 工具。

用 `tools` 字段（白名单）或 `disallowedTools` 字段（黑名单）来限制工具：

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---
```

#### 限制可生成的 subagent 类型

当 agent 作为 `claude --agent` 的主线程运行时，可以用 Agent 工具生成 subagent。要限制它能生成哪些类型，在 `tools` 字段中使用 `Agent(agent_type)` 语法。

**注意**

在 2.1.63 版本中，Task 工具更名为 Agent。设置和 agent 定义中已有的 `Task(...)` 引用仍可作为别名使用。

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

这是白名单：只能生成 `worker` 和 `researcher` subagent。如果尝试生成其他类型，请求会失败，agent 在提示中只能看到允许的类型。要禁止特定 agent 而允许其他所有 agent，改用 [`permissions.deny`](#disable-specific-subagents)。

要允许不受限制地生成任何 subagent，使用不带括号的 `Agent`：

```yaml
tools: Agent, Read, Bash
```

如果从 `tools` 列表中完全省略 `Agent`，则 agent 无法生成任何 subagent。此限制仅适用于通过 `claude --agent` 作为主线程运行的 agent。Subagent 不能生成其他 subagent，所以 `Agent(agent_type)` 对 subagent 定义没有影响。

#### 为 subagent 限定 MCP 服务器作用域

用 `mcpServers` 字段给 subagent 授权访问主对话中不可用的 [MCP](./mcp) 服务器。内联定义的服务器在 subagent 启动时连接，完成时断开。字符串引用则共享父会话的连接。

列表中的每个条目可以是内联服务器定义，或引用会话中已配置的 MCP 服务器名称：

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

内联定义使用与 `.mcp.json` 服务器条目（`stdio`、`http`、`sse`、`ws`）相同的 schema，以服务器名称作为键。

如果你想让 MCP 服务器完全不出现在主对话中（避免工具描述消耗主对话上下文），就在这里内联定义而不是在 `.mcp.json` 中。Subagent 拿到工具，主对话则不会。

#### 权限模式

`permissionMode` 字段控制 subagent 如何处理权限提示。Subagent 从主对话继承权限上下文，但可以覆盖模式。

| 模式 | 行为 |
| :------------------ | :---------------------------------------------------------------- |
| `default` | 标准权限检查，会弹出提示 |
| `acceptEdits` | 自动接受文件编辑 |
| `dontAsk` | 自动拒绝权限提示（明确允许的工具仍然有效） |
| `bypassPermissions` | 跳过权限提示 |
| `plan` | 计划模式（只读探索） |

**警告**

谨慎使用 `bypassPermissions`。它会跳过权限提示，允许 subagent 在未经批准的情况下执行操作。写入 `.git`、`.claude`、`.vscode` 和 `.idea` 目录时仍会提示确认，但 `.claude/commands`、`.claude/agents` 和 `.claude/skills` 除外。详情参阅[权限模式](./permissions#permission-modes)。

如果父级使用了 `bypassPermissions`，则此值优先且不可覆盖。

#### 预加载 skill 到 subagent 中

用 `skills` 字段在启动时将 skill 内容注入到 subagent 的上下文中。这样 subagent 直接就有了领域知识，不需要在执行过程中去发现和加载 skill。

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

每个 skill 的完整内容都会注入到 subagent 上下文中，不只是可供调用。Subagent 不会从父对话继承 skill，你必须显式列出。

**注意**

这是[在 subagent 中运行 skill](./skills#run-skills-in-a-subagent) 的反向操作。通过 subagent 中的 `skills`，subagent 控制系统提示并加载 skill 内容。通过 skill 中的 `context: fork`，skill 内容被注入到你指定的 agent 中。两者使用相同的底层机制。

#### 启用持久记忆

`memory` 字段为 subagent 提供一个跨对话持久化的目录。Subagent 可以在此积累知识，比如代码库模式、调试经验和架构决策。

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

根据记忆的适用范围选择：

| 作用域 | 路径 | 适用场景 |
| :-------- | :-------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | subagent 需要记住跨所有项目的经验 |
| `project` | `.claude/agent-memory/<name-of-agent>/` | 知识是项目专属的，可以通过版本控制共享 |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | 知识是项目专属的，但不应提交到版本控制 |

启用记忆后：

* Subagent 的系统提示会包含读写记忆目录的指令
* 系统提示还会包含记忆目录中 `MEMORY.md` 的前 200 行，以及超过 200 行时整理 `MEMORY.md` 的指令
* 自动启用 Read、Write 和 Edit 工具，以便 subagent 管理记忆文件

##### 持久记忆技巧

* `user` 是推荐的默认作用域。当 subagent 的知识仅与特定代码库相关时，用 `project` 或 `local`。
* 让 subagent 在开始工作前查阅记忆：”看看这个 PR，检查你的记忆里有没有之前见过的模式。”
* 让 subagent 在完成任务后更新记忆：”既然做完了，把学到的东西保存到记忆里。”随着时间推移，这会积累起让 subagent 越来越高效的知识库。
* 把记忆指令直接写在 subagent 的 markdown 文件中，让它主动维护自己的知识库：

  ```markdown 
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### 带钩子的条件规则

为了对工具使用进行更动态的控制，请在执行操作之前使用 `PreToolUse` 挂钩来验证操作。当您需要允许工具的某些操作而阻止其他操作时，这非常有用。

此示例创建一个仅允许只读数据库查询的子代理。 `PreToolUse` 挂钩在执行每个 Bash 命令之前运行 `command` 中指定的脚本：

```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [将挂钩输入作为 JSON](./hooks#pretooluse-input) 通过 stdin 传递到挂钩命令。验证脚本读取此 JSON，提取 Bash 命令，并[以代码 2 退出](./hooks#exit-code-2-behavior-per-event) 以阻止写入操作：

```bash
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

请参阅 [挂钩输入](./hooks#pretooluse-input) 了解完整的输入架构，并参阅[退出代码](./hooks#exit-code-output) 了解退出代码如何影响行为。

#### 禁用特定子代理

您可以通过将特定子代理添加到[设置](./settings#permission-settings) 中的 `deny` 阵列来阻止 Claude 使用特定子代理。使用格式 `Agent(subagent-name)`，其中 `subagent-name` 与子代理的名称字段匹配。

```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

这适用于内置子代理和自定义子代理。您还可以使用 `--disallowedTools` CLI 标志：

```bash
claude --disallowedTools "Agent(Explore)"
```

有关权限规则的更多详细信息，请参阅[权限文档](./permissions#tool-specific-permission-rules)。

### 定义子代理的钩子

子代理可以定义在子代理生命周期内运行的 [hooks](./hooks)。配置钩子有两种方法：

1. **在子代理的 frontmatter 中**：定义仅在子代理处于活动状态时运行的钩子
2. **在 `settings.json`** 中：定义当子代理启动或停止时在主会话中运行的挂钩

#### 子代理 frontmatter 中的钩子

直接在子代理的 markdown 文件中定义钩子。这些挂钩仅在特定子代理处于活动状态时运行，并在完成后被清除。

支持所有[挂钩事件](./hooks#hook-events)。子代理最常见的事件是：|活动 |匹配器输入|当它发生时 |
| :------------ | :------------ | :------------------------------------------------------------------ |
| `PreToolUse` |工具名称|子代理使用工具之前 |
| `PostToolUse` |工具名称|子代理使用工具后 |
| `Stop` | （无）|当子代理完成时（在运行时转换为 `SubagentStop`）|

此示例使用 `PreToolUse` 挂钩验证 Bash 命令，并在使用 `PostToolUse` 编辑文件后运行 linter：

```yaml
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

frontmatter 中的 `Stop` 挂钩会自动转换为 `SubagentStop` 事件。

#### 子代理事件的项目级挂钩

在 `settings.json` 中配置响应主会话中的子代理生命周期事件的挂钩。

|活动 |匹配器输入|当它发生时 |
| :-------------- | :-------------- | :-------------------------------- |
| `SubagentStart` |代理类型名称 |当子代理开始执行时 |
| `SubagentStop` |代理类型名称 |当子代理完成 |

这两个事件都支持匹配器按名称定位特定代理类型。此示例仅在 `db-agent` 子代理启动时运行设置脚本，并在任何子代理停止时运行清理脚本：

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

请参阅 [Hooks](./hooks) 了解完整的钩子配置格式。

## 与子代理合作

### 了解自动委派

Claude 根据请求中的任务描述、子代理配置中的 `description` 字段以及当前上下文自动委派任务。为了鼓励主动委派，请在子代理的描述字段中包含“主动使用”等短语。

### 显式调用子代理

当自动委派不够时，您可以自己请求子代理。三种模式从一次性建议升级为会话范围内的默认模式：

* **自然语言**：在提示中命名子代理； Claude决定是否委托
* **@-mention**：保证子代理针对一项任务运行
* **会话范围**：整个会话通过 `--agent` 标志或 `agent` 设置使用该子代理的系统提示、工具限制和模型

对于自然语言来说，没有特殊的语法。命名子代理和 Claude 通常代表：

```text
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-提及子代理。** 输入 `@` 并从预先输入中选择子代理，就像@-提及文件一样。这可确保特定的子代理运行，而不是将选择留给 Claude：

```text
@"code-reviewer (agent)" look at the auth changes
```

您的完整消息仍发送至 Claude，它根据您的要求编写子代理的任务提示。 @-mention 控制 Claude 调用哪个子代理，而不是它收到的提示。

由已启用的[插件](./plugins) 提供的子代理在预输入中显示为 `:<agent-name>`。您还可以在不使用选择器的情况下手动键入提及：对于本地子代理，请输入 `@agent-<name>`；对于插件子代理，请输入 `@agent-:<agent-name>`。**作为子代理运行整个会话。** 通过 [`--agent <name>`](./cli-reference) 启动一个会话，其中主线程本身采用该子代理的系统提示符、工具限制和模型：

```bash
claude --agent code-reviewer
```

子代理的系统提示符完全替换了默认的 Claude Code 系统提示符，与 [`--system-prompt`](./cli-reference) 的方式相同。 `CLAUDE.md` 文件和项目内存仍通过正常消息流加载。代理名称在启动标头中显示为 `@<name>`，以便您可以确认其处于活动状态。

这适用于内置和自定义子代理，并且当您恢复会话时该选择仍然存在。

对于插件提供的子代理，请传递范围名称：`claude --agent :<agent-name>`。

要使其成为项目中每个会话的默认值，请在 `.claude/settings.json` 中设置 `agent`：

```json
{
  "agent": "code-reviewer"
}
```

如果两者都存在，则 CLI 标志将覆盖该设置。

### 在前台或后台运行子代理

子代理可以在前台（阻塞）或后台（并发）运行：

* **前台子代理** 阻止主对话直到完成。权限提示和澄清问题（如 [`AskUserQuestion`](./tools-reference)）将传递给您。
* **后台子代理**在您继续工作时同时运行。在启动之前，Claude Code 会提示子代理所需的任何工具权限，确保其预先获得必要的批准。运行后，子代理将继承这些权限并自动拒绝任何未经预先批准的内容。如果后台子代理需要询问澄清问题，则该工具调用将失败，但子代理会继续。

如果后台子代理因缺少权限而失败，您可以启动一个具有相同任务的新前台子代理，以便通过交互式提示重试。

Claude 根据任务决定是否在前台或后台运行子代理。您还可以：

* 要求 Claude“在后台运行”
* 按 **Ctrl+B** 将正在运行的任务置于后台

要禁用所有后台任务功能，请将 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量设置为 `1`。请参阅[环境变量](./env-vars)。

### 常见模式

#### 隔离大批量操作

子代理最有效的用途之一是隔离产生大量输出的操作。运行测试、获取文档或处理日志文件可能会消耗大量上下文。通过将这些委托给子代理，详细输出将保留在子代理的上下文中，而只有相关摘要返回到您的主要对话。

```text
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### 进行并行研究

对于独立调查，生成多个子代理以同时工作：

```text
Research the authentication, database, and API modules in parallel using separate subagents
```

每个子代理独立探索其区域，然后 Claude 综合结果。当研究路径不相互依赖时，这种方法效果最好。

**警告**

当子代理完成后，他们的结果将返回到您的主要对话中。运行许多子代理（每个子代理都会返回详细结果）可能会消耗大量上下文。

对于需要持续并行性或超出上下文窗口的任务，[代理团队](./agent-teams) 为每个工作人员提供自己的独立上下文。

####连锁分代理对于多步骤工作流程，请要求 Claude 按顺序使用子代理。每个子代理完成其任务并将结果返回给 Claude，然后 Claude 将相关上下文传递给下一个子代​​理。

```text
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### 在子代理和主对话之间选择

在以下情况下使用**主要对话**：

* 任务需要频繁的来回或迭代细化
* 多个阶段共享重要的背景（规划→实施→测试）
* 你正在做出快速、有针对性的改变
* 延迟很重要。子代理重新开始，可能需要时间收集背景信息

在以下情况下使用**子代理**：

* 该任务会产生您在主要上下文中不需要的详细输出
* 您想要强制实施特定的工具限制或权限
* 作品是独立的，可以返回摘要

当您希望在主对话上下文而不是独立的子代理上下文中运行可重用的提示或工作流时，请考虑[技能](./skills)。

如果要快速询问对话中已有的内容，请使用 [`/btw`](./interactive-mode#side-questions-with-btw) 而不是子代理。它可以看到您的完整上下文，但没有工具访问权限，并且答案将被丢弃而不是添加到历史记录中。

**注意**

子代理不能生成其他子代理。如果您的工作流程需要嵌套委派，请使用主对话中的[技能](./skills) 或[链子代理](#chain-subagents)。

### 管理子代理上下文

#### 恢复子代理

每个子代理调用都会创建一个具有新上下文的新实例。要继续现有子代理的工作而不是重新开始，请要求 Claude 恢复它。

恢复的子代理保留其完整的对话历史记录，包括所有以前的工具调用、结果和推理。子代理会准确地从停止的地方开始，而不是重新开始。

当子代理完成时，Claude 会收到其代理 ID。 Claude 使用 `SendMessage` 工具，将代理 ID 作为 `to` 字段来恢复。要恢复子代理，请要求 Claude 继续之前的工作：

```text
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

如果停止的子代理收到 `SendMessage`，它会在后台自动恢复，而不需要新的 `Agent` 调用。

如果您想明确引用它，您还可以向 Claude 询问代理 ID，或者在 `~/.claude/projects/{project}/{sessionId}/subagents/` 的转录文件中查找 ID。每个转录本都存储为 `agent-{agentId}.jsonl`。

子代理记录独立于主要对话而持续存在：

* **主要对话压缩**：当主要对话压缩时，子代理记录不受影响。它们存储在单独的文件中。
* **会话持久性**：子代理记录在其会话中持续存在。重新启动 Claude Code 后，您可以通过恢复同一会话来[恢复子代理](#resume-subagents)。
* **自动清理**：根据 `cleanupPeriodDays` 设置清理转录本（默认值：30 天）。

#### 自动压缩

子代理使用与主会话相同的逻辑支持自动压缩。默认情况下，自动压缩在大约 95% 容量时触发。要更早触发压缩，请将 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 设置为较低的百分比（例如 `50`）。有关详细信息，请参阅[环境变量](./env-vars)。压缩事件记录在子代理转录文件中：

```json
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

`preTokens` 值显示压缩发生之前使用了多少令牌。

## 子代理示例

这些示例展示了构建子代理的有效模式。使用它们作为起点，或使用 Claude 生成自定义版本。

**提示**

**最佳实践：**

* **设计重点子代理：** 每个子代理应擅长完成一项特定任务
* **编写详细描述：** Claude 使用描述来决定何时委托
* **限制工具访问：** 仅授予安全和焦点所需的权限
* **检查版本控制：** 与您的团队共享项目子代理

### 代码审查者

只读子代理，可在不修改代码的情况下查看代码。此示例展示了如何设计一个具有有限工具访问权限（无编辑或写入）的重点子代理，以及详细说明要查找的内容以及如何格式化输出的详细提示。

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### 调试器

可以分析和解决问题的子代理。与代码审阅者不同，此审阅者包括编辑，因为修复错误需要修改代码。该提示提供了从诊断到验证的清晰工作流程。

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### 数据科学家

用于数据分析工作的特定领域子代理。此示例演示如何为典型编码任务之外的专门工作流程创建子代理。它明确设置 `model: sonnet` 以进行更强大的分析。

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### 数据库查询验证器

允许 Bash 访问但验证命令以仅允许只读 SQL 查询的子代理。此示例演示当您需要比 `tools` 字段提供的更精细的控制时，如何使用 `PreToolUse` 挂钩进行条件验证。

```markdown
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [将挂钩输入作为 JSON](./hooks#pretooluse-input) 通过 stdin 传递到挂钩命令。验证脚本读取此 JSON，提取正在执行的命令，并根据 SQL 写入操作列表对其进行检查。如果检测到写入操作，脚本[以代码 2 退出](./hooks#exit-code-2-behavior-per-event) 以阻止执行，并通过 stderr 将错误消息返回到 Claude。

在项目中的任意位置创建验证脚本。该路径必须与挂钩配置中的 `command` 字段匹配：

```bash
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

使脚本可执行：

```bash
chmod +x ./scripts/validate-readonly-query.sh
```

该挂钩通过标准输入使用 `tool_input.command` 中的 Bash 命令接收 JSON。退出代码 2 阻止操作并将错误消息反馈给 Claude。有关退出代码的详细信息，请参阅 [Hooks](./hooks#exit-code-output)；有关完整的输入架构，请参阅 [Hook 输入](./hooks#pretooluse-input)。

## 后续步骤

现在您已经了解了子代理，请探索以下相关功能：

* [通过插件分发子代理](./plugins) 在团队或项目之间共享子代理
* [以编程方式运行 Claude Code](./headless) 与 Agent SDK 一起用于 CI/CD 和自动化
* [使用 MCP 服务器](./mcp) 使子代理能够访问外部工具和数据
