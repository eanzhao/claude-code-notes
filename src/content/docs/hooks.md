---
title: "挂钩参考"
order: 63
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "Claude Code 挂钩事件、配置架构、JSON 输入/输出格式、退出代码、异步挂钩、HTTP 挂钩、提示挂钩和 MCP 工具挂钩的参考。"
sourceUrl: "https://code.claude.com/docs/en/hooks.md"
sourceTitle: "Hooks reference"
tags: []
---
# 钩子参考

> Claude Code 挂钩事件、配置模式、JSON 输入/输出格式、退出代码、异步挂钩、HTTP 挂钩、提示挂钩和 MCP 工具挂钩的参考。

**提示**

有关示例的快速入门指南，请参阅[使用挂钩自动化工作流程](./hooks-guide)。

挂钩是用户定义的 shell 命令、HTTP 端点或 LLM 提示，它们在 Claude Code 生命周期的特定点自动执行。使用此参考来查找事件架构、配置选项、JSON 输入/输出格式以及异步挂钩、HTTP 挂钩和 MCP 工具挂钩等高级功能。如果您是第一次设置挂钩，请从[指南](./hooks-guide)开始。

## 钩子生命周期

在 Claude Code 会话期间，挂钩在特定点触发。当事件触发且匹配器匹配时，Claude Code 会将有关该事件的 JSON 上下文传递给您的挂钩处理程序。对于命令挂钩，输入到达标准输入。对于 HTTP 挂钩，它作为 POST 请求正文到达。然后，您的处理程序可以检查输入、采取操作，并可选择返回决策。有些事件每个会话触发一次，而其他事件则在代理循环内重复触发：

  ![钩子生命周期图，显示从 SessionStart 通过代理循环（PreToolUse、PermissionRequest、PostToolUse、SubagentStart/Stop、TaskCompleted）到 PostCompact 和 SessionEnd 的钩子序列，Eliitation 和 EliitationResult 嵌套在 MCP 工具执行中，WorktreeCreate、WorktreeRemove、Notification、ConfigChange 和InstructionsLoaded 作为独立异步事件](https://mintcdn.com/claude-code/lBsitdsGyD9caWJQ/images/hooks-lifecycle.svg?fit=max&auto=format&n=lBsitdsGyD9caWJQ&q=85&s=be3486ef2cf2563eb213b6cbbce93982)
  

下表总结了每个事件触发的时间。 [Hook events](#hook-events) 部分记录了每个事件的完整输入架构和决策控制选项。|活动 |当它发生时 |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SessionStart` |当会话开始或恢复时 |
| `UserPromptSubmit` |当您提交提示时，在 Claude 处理它之前 |
| `PreToolUse` |在执行工具调用之前。可以屏蔽吗|
| `PermissionRequest` |当出现权限对话框时 |
| `PostToolUse` |工具调用成功后 |
| `PostToolUseFailure` |工具调用失败后 |
| `Notification` |当 Claude Code 发送通知时 |
| `SubagentStart` |当子代理产生时 |
| `SubagentStop` |当子代理完成时 |
| `Stop` |当 Claude 完成响应时 |
| `TeammateIdle` |当[特工队](./agent-teams)队友即将闲置时 |
| `TaskCompleted` |当任务被标记为已完成时 |
| `InstructionsLoaded` |当 CLAUDE.md 或 `.claude/rules/*.md` 文件加载到上下文中时。在会话开始时以及在会话期间延迟加载文件时触发 |
| `ConfigChange` |当配置文件在会话期间发生更改时 |
| `WorktreeCreate` |当通过 `--worktree` 或 `isolation: "worktree"` 创建工作树时。替换默认的 git 行为 |
| `WorktreeRemove` |当工作树被删除时，无论是在会话退出时还是在子代理完成时 |
| `PreCompact` |上下文压缩之前 || `PostCompact` |上下文压缩完成后 |
| `Elicitation` |当 MCP 服务器在工具调用期间请求用户输入时 |
| `ElicitationResult` |用户响应 MCP 启发后，响应被发送回服务器之前 |
| `SessionEnd` |当会话终止时 |### 钩子如何解析

要了解这些部分如何组合在一起，请考虑使用这个阻止破坏性 shell 命令的 `PreToolUse` 挂钩。该钩子在每次 Bash 工具调用之前运行 `block-rm.sh`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

该脚本从 stdin 读取 JSON 输入，提取命令，如果包含 `rm -rf`，则返回 `"deny"` 的 `permissionDecision`：

```bash
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

现在假设 Claude Code 决定运行 `Bash "rm -rf /tmp/build"`。发生的情况如下：

![钩子解析流程：触发 PreToolUse 事件，匹配器检查 Bash 匹配，运行钩子处理程序，结果返回 Claude Code](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df)

### 事件触发

`PreToolUse` 事件触发。 Claude Code 将标准输入上的工具输入作为 JSON 发送到挂钩：

```json
{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
```

  
### 匹配器检查

匹配器 `"Bash"` 与工具名称匹配，因此 `block-rm.sh` 运行。如果省略匹配器或使用 `"*"`，则挂钩将在事件每次发生时运行。仅当定义了匹配器但不匹配时，挂钩才会跳过。

  
### 钩子处理程序运行

该脚本从输入中提取 `"rm -rf /tmp/build"` 并找到 `rm -rf`，因此它将决定打印到标准输出：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

如果命令是安全的（如 `npm test`），脚本将改为命中 `exit 0`，这告诉 Claude Code 允许工具调用，无需采取进一步操作。

  
### Claude Code 对结果起作用

Claude Code 读取 JSON 决策，阻止工具调用，并向 Claude 显示原因。

下面的 [Configuration](#configuration) 部分记录了完整的架构，每个 [hook event](#hook-events) 部分记录了您的命令接收的输入以及它可以返回的输出。

## 配置

挂钩在 JSON 设置文件中定义。该配置具有三层嵌套：

1. 选择要响应的[挂钩事件](#hook-events)，例如`PreToolUse`或`Stop`
2. 添加[匹配器组](#matcher-patterns)以在触发时进行过滤，例如“仅适用于Bash工具”
3. 定义一个或多个[hook handlers](#hook-handler-fields)，匹配时运行

请参阅上面的[挂钩如何解析](#how-a-hook-resolves)，了解带有注释示例的完整演练。

**注意**

此页面使用每个级别的特定术语：**钩子事件**代表生命周期点，**匹配器组**代表过滤器，**钩子处理程序**代表运行的 shell 命令、HTTP 端点、提示或代理。 “钩子”本身指的是一般特征。

### 挂钩位置

定义钩子的位置决定了它的范围：|地点 |范围 |可分享|
| :-------------------------------------------------------- | :---------------------------- | :--------------------------------- |
| `~/.claude/settings.json` |您的所有项目 |不，在您的机器本地 |
| `.claude/settings.json` |单个项目 |是的，可以提交给 repo |
| `.claude/settings.local.json` |单个项目|不，gitignored |
|托管策略设置 |组织范围 |是的，由管理员控制 |
| [插件](./plugins) `hooks/hooks.json` |当插件启用时 |是的，与插件捆绑在一起 |
| [技能](./skills) 或 [代理](./sub-agents) frontmatter |当组件处于活动状态时 |是的，在组件文件中定义 |

有关设置文件分辨率的详细信息，请参阅[设置](./settings)。企业管理员可以使用 `allowManagedHooksOnly` 来阻止用户、项目和插件挂钩。请参见[挂钩配置](./settings#hook-configuration)。

### 匹配器模式

`matcher` 字段是一个正则表达式字符串，用于在钩子触发时进行过滤。使用 `"*"`、`""` 或完全省略 `matcher` 以匹配所有匹配项。每个事件类型在不同的字段上匹配：|活动 |匹配器过滤什么 |匹配器值示例 |
| :------------------------------------------------------------------------------------------------------------------------ | :------------------------ | :------------------------------------------------------------------------------------------------ |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` |工具名称| `Bash`、`Edit\|Write`、`mcp__.*` |
| `SessionStart` |会议如何开始 | `startup`、`resume`、`clear`、`compact` |
| `SessionEnd` |会议为何结束 | `clear`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other` |
| `Notification` |通知类型 | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog` |
| `SubagentStart` |代理类型 | `Bash`、`Explore`、`Plan` 或自定义代理名称 |
| `PreCompact`、`PostCompact` |是什么触发了压缩| `manual`、`auto` |
| `SubagentStop` |代理类型 |与 `SubagentStart` 相同的值 |
| `ConfigChange` |配置源码| `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills` |
| `UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`InstructionsLoaded` |没有匹配器支持 |总是在每次发生时触发 |

匹配器是正则表达式，因此 `Edit|Write` 匹配任一工具，而 `Notebook.*` 匹配以 Notebook 开头的任何工具。匹配器针对 Claude Code 发送到标准输入上的挂钩的 [JSON 输入](#hook-input-and-output) 中的字段运行。对于工具事件，该字段为 `tool_name`。每个 [hook event](#hook-events) 部分都会列出该事件的完整匹配器值集和输入架构。

此示例仅在 Claude 写入或编辑文件时运行 linting 脚本：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```
`UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove` 和 `InstructionsLoaded` 不支持匹配器，并且每次出现时都会触发。如果您向这些事件添加 `matcher` 字段，它将被静默忽略。

#### 匹配 MCP 工具

[MCP](./mcp) 服务器工具在工具事件中显示为常规工具（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`），因此您可以像匹配任何其他工具名称一样来匹配它们。

MCP 工具遵循命名模式 `mcp__<server>__<tool>`，例如：

* `mcp__memory__create_entities`：内存服务器的创建实体工具
* `mcp__filesystem__read_file`：文件系统服务器的读文件工具
* `mcp__github__search_repositories`：GitHub服务器的搜索工具

使用正则表达式模式来定位特定的 MCP 工具或工具组：

* `mcp__memory__.*` 与 `memory` 服务器中的所有工具相匹配
* `mcp__.*__write.*` 匹配任何包含来自任何服务器的“写入”的工具

此示例记录所有内存服务器操作并验证来自任何 MCP 服务器的写入操作：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### 钩子处理程序字段

内部 `hooks` 数组中的每个对象都是一个钩子处理程序：shell 命令、HTTP 端点、LLM 提示符或匹配器匹配时运行的代理。有四种类型：

* **[命令挂钩](#command-hook-fields)** (`type: "command"`)：运行 shell 命令。您的脚本在标准输入上接收事件的 [JSON 输入](#hook-input-and-output)，并通过退出代码和标准输出传回结果。
* **[HTTP 挂钩](#http-hook-fields)** (`type: "http"`)：将事件的 JSON 输入作为 HTTP POST 请求发送到 URL。端点使用与命令挂钩相同的 [JSON 输出格式](#json-output) 通过响应正文传回结果。
* **[提示挂钩](#prompt-and-agent-hook-fields)** (`type: "prompt"`)：向 Claude 模型发送提示以进行单轮评估。该模型返回是/否决定作为 JSON。请参阅[基于提示的挂钩](#prompt-based-hooks)。
* **[代理挂钩](#prompt-and-agent-hook-fields)** (`type: "agent"`)：生成一个子代理，该子代理可以使用 Read、Grep 和 Glob 等工具在返回决策之前验证条件。请参阅[基于代理的挂钩](#agent-based-hooks)。

#### 常用字段

这些字段适用于所有钩子类型：

|领域 |必填|描述 |
| :-------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` |是的 | `"command"`、`"http"`、`"prompt"` 或 `"agent"` |
| `timeout` |没有|取消前几秒。默认值：命令 600、提示 30、代理 60 |
| `statusMessage` |没有|挂钩运行时显示的自定义微调器消息 |
| `once` |没有|如果是 `true`，则每个会话仅运行一次，然后被删除。只有技能，没有代理。请参阅[技能和代理中的挂钩](#hooks-in-skills-and-agents) |#### 命令挂钩字段

除了 [常见字段](#common-fields) 之外，命令挂钩还接受以下字段：

|领域 |必填|描述 |
| :-------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `command` |是的 |执行的 Shell 命令 |
| `async` |没有|如果是`true`，则在后台运行，不会阻塞。请参阅[在后台运行挂钩](#run-hooks-in-the-background) |

#### HTTP 挂钩字段

除了 [常见字段](#common-fields) 之外，HTTP 挂钩还接受以下字段：

|领域 |必填|描述 |
| ：-------------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` |是的 |将 POST 请求发送到的 URL |
| `headers` |没有|作为键值对的附加 HTTP 标头。值支持使用 `$VAR_NAME` 或 `${VAR_NAME}` 语法进行环境变量插值。仅解析 `allowedEnvVars` 中列出的变量 |
| `allowedEnvVars` |没有|可以插入到标头值中的环境变量名称列表。对未列出变量的引用将替换为空字符串。任何环境变量插值工作所需的 |

Claude Code 将挂钩的 [JSON 输入](#hook-input-and-output) 作为 POST 请求正文与 `Content-Type: application/json` 一起发送。响应正文使用与命令挂钩相同的[JSON 输出格式](#json-output)。

错误处理与命令挂钩不同：非 2xx 响应、连接失败和超时都会产生允许继续执行的非阻塞错误。要阻止工具调用或拒绝权限，请返回 2xx 响应，其中 JSON 主体包含 `decision: "block"` 或 `hookSpecificOutput` 包含 `permissionDecision: "deny"`。

此示例将 `PreToolUse` 事件发送到本地验证服务，使用 `MY_TOKEN` 环境变量中的令牌进行身份验证：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### 提示和代理挂钩字段

除了 [通用字段](#common-fields) 之外，提示和代理挂钩还接受以下字段：

|领域 |必填|描述 |
| :----- | :----- | :---------------------------------------------------------------------------------------------- |
| `prompt` |是的 |提示文本发送给模型。使用 `$ARGUMENTS` 作为挂钩输入 JSON 的占位符 |
| `model` |没有|用于评估的模型。默认为快速模型 |所有匹配的挂钩并行运行，并且相同的处理程序会自动进行重复数据删除。命令钩子通过命令字符串去重，HTTP钩子通过URL去重。处理程序在 Claude Code 环境的当前目录中运行。 `$CLAUDE_CODE_REMOTE` 环境变量在远程 Web 环境中设置为 `"true"`，而不是在本地 CLI 中设置。

### 按路径引用脚本

使用环境变量来引用相对于项目或插件根目录的钩子脚本，无论钩子运行时的工作目录如何：

* `$CLAUDE_PROJECT_DIR`：项目根目录。用引号括起来以处理带有空格的路径。
* `${CLAUDE_PLUGIN_ROOT}`：插件的安装目录，用于与[插件](./plugins)捆绑的脚本。每个插件更新的变化。
* `${CLAUDE_PLUGIN_DATA}`：插件的[持久数据目录](./plugins-reference#persistent-data-directory)，用于在插件更新后仍然存在的依赖项和状态。

### 项目脚本

此示例使用 `$CLAUDE_PROJECT_DIR` 在任何 `Write` 或 `Edit` 工具调用后从项目的 `.claude/hooks/` 目录运行样式检查器：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

  
### 插件脚本

使用可选的顶级 `description` 字段在 `hooks/hooks.json` 中定义插件挂钩。启用插件后，它的挂钩会与您的用户和项目挂钩合并。

此示例运行与插件捆绑在一起的格式化脚本：

```json
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

有关创建插件挂钩的详细信息，请参阅[插件组件参考](./plugins-reference#hooks)。

### 技能和特工的挂钩

除了设置文件和插件之外，还可以使用 frontmatter 在 [skills](./skills) 和 [subagents](./sub-agents) 中直接定义钩子。这些挂钩的范围仅限于组件的生命周期，并且仅在该组件处于活动状态时运行。

支持所有挂钩事件。对于子代理，`Stop` 挂钩会自动转换为 `SubagentStop`，因为这是子代理完成时触发的事件。

钩子使用与基于设置的钩子相同的配置格式，但范围仅限于组件的生命周期，并在完成时清除。

此技能定义了一个 `PreToolUse` 挂钩，该挂钩在每个 `Bash` 命令之前运行安全验证脚本：

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

代理在其 YAML frontmatter 中使用相同的格式。

### `/hooks` 菜单

在 Claude Code 中键入 `/hooks`，为您配置的挂钩打开只读浏览器。该菜单显示每个挂钩事件以及配置的挂钩数量，让您深入了解匹配器，并显示每个挂钩处理程序的完整详细信息。使用它来验证配置，检查挂钩来自哪个设置文件，或检查挂钩的命令、提示符或 URL。

该菜单显示所有四种挂钩类型：`command`、`prompt`、`agent` 和 `http`。每个钩子都标有 `[type]` 前缀和指示其定义位置的源：

* `User`：来自 `~/.claude/settings.json`
* `Project`：来自 `.claude/settings.json`
* `Local`：来自 `.claude/settings.local.json`
* `Plugin`：来自插件的 `hooks/hooks.json`
* `Session`：在内存中注册当前会话
* `Built-in`：由Claude Code内部注册选择一个钩子会打开一个详细视图，显示其事件、匹配器、类型、源文件以及完整的命令、提示或 URL。该菜单是只读的：要添加、修改或删除挂钩，请直接编辑设置 JSON 或要求 Claude 进行更改。

### 禁用或删除钩子

要删除挂钩，请从设置 JSON 文件中删除其条目。

要暂时禁用所有挂钩而不删除它们，请在设置文件中设置 `"disableAllHooks": true`。无法在将单个挂钩保留在配置中的同时禁用它。

`disableAllHooks` 设置遵循托管设置层次结构。如果管理员通过托管策略设置配置了挂钩，则在用户、项目或本地设置中设置的 `disableAllHooks` 无法禁用这些托管挂钩。只有在托管设置级别设置的 `disableAllHooks` 才能禁用托管挂钩。

对设置文件中的挂钩的直接编辑通常由文件观察器自动拾取。

## 钩子输入和输出

命令挂钩通过 stdin 接收 JSON 数据，并通过退出代码、stdout 和 stderr 传达结果。 HTTP 挂钩接收与 POST 请求正文相同的 JSON，并通过 HTTP 响应正文传达结果。本节涵盖所有事件通用的字段和行为。 [挂钩事件](#hook-events) 下的每个事件部分都包含其特定的输入架构和决策控制选项。

### 常用输入字段

除了每个 [挂钩事件](#hook-events) 部分中记录的事件特定字段之外，所有挂钩事件都会接收这些字段作为 JSON。对于命令挂钩，此 JSON 通过 stdin 到达。对于 HTTP 挂钩，它作为 POST 请求正文到达。

|领域|描述 |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id` |当前会话标识符 |
| `transcript_path` |对话路径 JSON |
| `cwd` |调用钩子时的当前工作目录 |
| `permission_mode` |当前[权限模式](./permissions#permission-modes)：`"default"`、`"plan"`、`"acceptEdits"`、`"dontAsk"` 或 `"bypassPermissions"` |
| `hook_event_name` |触发的事件的名称 |

当与 `--agent` 一起运行或在子代理内运行时，包含两个附加字段：|领域 |描述 |
| ：---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id` |子代理的唯一标识符。仅当钩子在子代理调用内触发时才存在。使用它来区分子代理挂钩调用和主线程调用。                                                                     |
| `agent_type` |代理名称（例如，`"Explore"` 或 `"security-reviewer"`）。当会话使用 `--agent` 或钩子在子代理内部触发时出现。对于子代理，子代理的类型优先于会话的 `--agent` 值。 |

例如，Bash 命令的 `PreToolUse` 挂钩在标准输入上接收以下内容：

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

`tool_name` 和 `tool_input` 字段是特定于事件的。每个 [挂钩事件](#hook-events) 部分都记录了该事件的附加字段。

### 退出代码输出

挂钩命令的退出代码告诉 Claude Code 该操作是否应该继续、被阻止或被忽略。

**退出0**表示成功。 Claude Code 解析标准输出以获取 [JSON 输出字段](#json-output)。 JSON 输出仅在出口 0 上处理。对于大多数事件，stdout 仅以详细模式显示 (`Ctrl+O`)。 `UserPromptSubmit` 和 `SessionStart` 是例外，其中 stdout 被添加为 Claude 可以查看并执行操作的上下文。

**退出2**表示阻塞错误。 Claude Code 忽略标准输出和其中的任何 JSON。相反，stderr 文本会作为错误消息反馈到 Claude。效果取决于事件：`PreToolUse` 阻止工具调用、`UserPromptSubmit` 拒绝提示等。有关完整列表，请参阅[退出代码 2 行为](#exit-code-2-behavior-per-event)。

**任何其他退出代码**都是非阻塞错误。 stderr 以详细模式 (`Ctrl+O`) 显示并继续执行。

例如，阻止危险 Bash 命令的钩子命令脚本：

```bash
#!/bin/bash
# Reads JSON input from stdin, checks the command
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # Success: tool call proceeds
```

#### 每个事件的退出代码 2 行为

退出代码 2 是钩子发出“停止，不要这样做”信号的方式。效果取决于事件，因为有些事件代表可以阻止的操作（例如尚未发生的工具调用），而其他事件则代表已经发生或无法阻止的事情。|挂钩事件|可以拦截吗？ | 2 号出口会发生什么 |
| :-------------------- | :--------- | :---------------------------------------------------------------------------------------- |
| `PreToolUse` |是的 |阻止工具调用 |
| `PermissionRequest` |是的 |拒绝许可 |
| `UserPromptSubmit` |是的 |阻止提示处理并删除提示 |
| `Stop` |是的 |防止 Claude 停止，继续对话 |
| `SubagentStop` |是的 |防止子代理停止 |
| `TeammateIdle` |是的 |防止队友闲置（队友继续工作）|
| `TaskCompleted` |是的 |防止任务被标记为已完成 |
| `ConfigChange` |是的 |阻止配置更改生效（`policy_settings` 除外）|
| `PostToolUse` |没有 |将 stderr 显示为 Claude（工具已运行） |
| `PostToolUseFailure` |没有 |向 Claude 显示 stderr（工具已失败） |
| `Notification` |没有 |仅向用户显示 stderr |
| `SubagentStart` |没有 |仅向用户显示 stderr |
| `SessionStart` |没有 |仅向用户显示 stderr |
| `SessionEnd` |没有 |仅向用户显示 stderr |
| `PreCompact` |没有 |仅向用户显示 stderr |
| `PostCompact` |没有 |仅向用户显示 stderr |
| `Elicitation` |是的 |否认引诱 |
| `ElicitationResult` |是的 |阻止响应（行动变为拒绝）|
| `WorktreeCreate` |是的 |任何非零退出代码都会导致工作树创建失败 |
| `WorktreeRemove` |没有 |仅在调试模式下记录失败 |
| `InstructionsLoaded` |没有 |退出代码被忽略 |

### HTTP 响应处理

HTTP 挂钩使用 HTTP 状态代码和响应主体，而不是退出代码和标准输出：

* **2xx 为空主体**：成功，相当于退出代码 0，没有输出
* **2xx 带有纯文本正文**：成功，文本被添加为上下文
* **2xx 具有 JSON 主体**：成功，使用与命令挂钩相同的 [JSON 输出](#json-output) 架构进行解析
* **非2xx状态**：非阻塞错误，继续执行
* **连接失败或超时**：非阻塞错误，继续执行与命令挂钩不同，HTTP 挂钩无法仅通过状态代码发出阻塞错误信号。要阻止工具调用或拒绝权限，请返回 2xx 响应，其中包含包含适当决策字段的 JSON 正文。

### JSON 输出

退出代码允许您允许或阻止，但 JSON 输出为您提供更细粒度的控制。不要使用代码 2 退出来阻止，而是退出 0 并将 JSON 对象打印到 stdout。 Claude Code 从 JSON 读取特定字段以控制行为，包括用于阻止、允许或升级给用户的 [决策控制](#decision-control)。

**注意**

您必须为每个钩子选择一种方法，而不是同时选择两种方法：要么单独使用退出代码进行信号发送，要么退出 0 并打印 JSON 进行结构化控制。 Claude Code 仅在退出 0 时处理 JSON。如果退出 2，则忽略任何 JSON。

您的挂钩的标准输出必须仅包含 JSON 对象。如果您的 shell 配置文件在启动时打印文本，则可能会干扰 JSON 解析。请参阅故障排除指南中的[JSON 验证失败](./hooks-guide#json-validation-failed)。

JSON 对象支持三种字段：

* **通用字段**（如 `continue`）适用于所有事件。这些列于下表中。
* **顶级 `decision` 和 `reason`** 被某些事件用来阻止或提供反馈。
* **`hookSpecificOutput`** 是需要更丰富控制的事件的嵌套对象。它需要将 `hookEventName` 字段设置为事件名称。

|领域 |默认 |描述 |
| ：-------------- | :------ | :------------------------------------------------------------------------------------------------------------------------ |
| `continue` | `true` |如果 `false`、Claude 在挂钩运行后完全停止处理。优先于任何特定于事件的决策字段 |
| `stopReason` |无 |当 `continue` 为 `false` 时向用户显示的消息。未显示给 Claude |
| `suppressOutput` | `false` |如果是 `true`，则隐藏详细模式输出中的 stdout |
| `systemMessage` |无 |向用户显示警告消息 |

要完全停止 Claude，无论事件类型如何：

```json
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### 决策控制

并非每个事件都支持通过 JSON 阻止或控制行为。每个执行的事件都使用一组不同的字段来表达该决定。在编写钩子之前，请使用此表作为快速参考：|活动 |决策模式|关键领域 |
| :---------------------------------------------------------------------------------------- | ：-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit、PostToolUse、PostToolUseFailure、停止、SubagentStop、ConfigChange |顶级`decision` | `decision: "block"`、`reason` |
|队友空闲，任务已完成 |退出代码或 `continue: false` |退出代码 2 会阻止带有 stderr 反馈的操作。 JSON `{"continue": false, "stopReason": "..."}` 也会完全阻止队友，与 `Stop` 钩子行为相匹配 |
|预工具使用 | `hookSpecificOutput` | `permissionDecision`（允许/拒绝/询问），`permissionDecisionReason` |
|许可请求 | `hookSpecificOutput` | `decision.behavior`（允许/拒绝）|
|工作树创建 |标准输出路径 | Hook 打印创建的工作树的绝对路径。非零退出创建失败 |
|启发| `hookSpecificOutput` | `action`（接受/拒绝/取消）、`content`（接受的表单字段值）|
|引出结果 | `hookSpecificOutput` | `action`（接受/拒绝/取消）、`content`（表单字段值覆盖）|
| WorktreeRemove、通知、SessionEnd、PreCompact、PostCompact、InstructionsLoaded |无 |没有决策控制。用于日志记录或清理等副作用 |

以下是每种模式的实际应用示例：

### 高层决策

由 `UserPromptSubmit`、`PostToolUse`、`PostToolUseFailure`、`Stop`、`SubagentStop` 和 `ConfigChange` 使用。唯一的值是 `"block"`。要允许该操作继续进行，请从 JSON 中省略 `decision`，或者完全退出 0，不添加任何 JSON：

```json
{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}
```

  
### 工具使用前使用 `hookSpecificOutput` 进行更丰富的控制：允许、拒绝或升级给用户。您还可以在运行之前修改工具输入或为 Claude 注入其他上下文。有关全套选项，请参阅 [PreToolUse 决策控制](#pretooluse-decision-control)。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed"
  }
}
```

  
### 权限请求

使用 `hookSpecificOutput` 代表用户允许或拒绝权限请求。允许时，您还可以修改工具的输入或应用权限规则，以便不会再次提示用户。请参阅 [PermissionRequest 决策控制](#permissionrequest-decision-control) 了解完整的选项集。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

有关 Bash 命令验证、提示过滤和自动批准脚本等扩展示例，请参阅指南中的[可以自动化的功能](./hooks-guide#what-you-can-automate) 和 [Bash 命令验证器参考实现](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。

## 挂钩事件

每个事件对应于 Claude Code 生命周期中可以运行挂钩的点。以下部分的顺序与生命周期相匹配：从会话设置到代理循环再到会话结束。每个部分描述事件何时触发、它​​支持哪些匹配器、它接收的 JSON 输入以及如何通过输出控制行为。

### 会话开始

当 Claude Code 启动新会话或恢复现有会话时运行。对于加载开发上下文（例如现有问题或最近对代码库的更改）或设置环境变量很有用。对于不需要脚本的静态上下文，请改用 [CLAUDE.md](./memory)。

SessionStart 在每个会话上运行，因此请保持这些挂钩快速。仅支持 `type: "command"` 挂钩。

匹配器值对应于会话的启动方式：

|匹配器|当它发生时 |
| :-------- | :------------------------------------ |
| `startup` |新会议|
| `resume` | `--resume`、`--continue` 或 `/resume` |
| `clear` | `/clear` |
| `compact` |自动或手动压实 |

#### 会话开始输入

除了[通用输入字段](#common-input-fields) 之外，SessionStart 挂钩还接收 `source`、`model` 和可选的 `agent_type`。 `source` 字段指示会话的启动方式：`"startup"` 表示新会话、`"resume"` 表示恢复的会话、`/clear` 之后的 `"clear"` 或压缩之后的 `"compact"`。 `model` 字段包含型号标识符。如果您使用 `claude --agent <name>` 启动 Claude Code，则 `agent_type` 字段包含代理名称。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart决策控制

挂钩脚本打印到 stdout 的任何文本都会添加为 Claude 的上下文。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您还可以返回以下特定于事件的字段：

|领域 |描述 |
| :------------------ | :------------------------------------------------------------------------ |
| `additionalContext` |添加到 Claude 上下文的字符串。多个钩子的值被连接起来 |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### 保存环境变量SessionStart 挂钩可以访问 `CLAUDE_ENV_FILE` 环境变量，该变量提供了一个文件路径，您可以在其中为后续 Bash 命令保留环境变量。

要设置各个环境变量，请将 `export` 语句写入 `CLAUDE_ENV_FILE`。使用append (`>>`)来保存其他钩子设置的变量：

```bash
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

要捕获设置命令中的所有环境更改，请比较之前和之后导出的变量：

```bash
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

写入此文件的任何变量将在 Claude Code 在会话期间执行的所有后续 Bash 命令中可用。

**注意**

`CLAUDE_ENV_FILE` 可用于 SessionStart 挂钩。其他钩子类型无法访问此变量。

### 说明已加载

当 `CLAUDE.md` 或 `.claude/rules/*.md` 文件加载到上下文中时触发。此事件在会话开始时针对急切加载的文件触发，并在稍后延迟加载文件时触发，例如当 Claude 访问包含嵌套 `CLAUDE.md` 的子目录时或当条件规则与 `paths:` frontmatter 匹配时触发。该钩子不支持阻塞或决策控制。出于可观察性的目的，它异步运行。

instructionsLoaded 不支持匹配器，并且会在每次加载发生时触发。

####说明加载输入

除了 [通用输入字段](#common-input-fields) 之外，InstructionsLoaded 挂钩还接收以下字段：

|领域 |描述 |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path` |已加载指令文件的绝对路径 |
| `memory_type` |文件范围：`"User"`、`"Project"`、`"Local"` 或 `"Managed"` |
| `load_reason` |加载文件的原因：`"session_start"`、`"nested_traversal"`、`"path_glob_match"`、`"include"` 或 `"compact"`。压缩事件后重新加载指令文件时会触发 `"compact"` 值 |
| `globs` |文件 `paths:` frontmatter 中的路径 glob 模式（如果有）。仅适用于 `path_glob_match` 负载 |
| `trigger_file_path` |对于延迟加载，访问触发此加载的文件的路径 |
| `parent_file_path` |包含此文件的父指令文件的路径，用于 `include` 加载 |```json 
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "permission_mode": "default",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

####指令加载决策控制

说明Loaded hooks 没有决策控制。它们不能阻止或修改指令加载。使用此事件进行审核日志记录、合规性跟踪或可观察性。

### 用户提示提交

当用户提交提示时运行，然后 Claude 处理它。这可以让你
根据提示/对话添加其他上下文、验证提示或
阻止某些类型的提示。

#### 用户提示提交输入

除了 [通用输入字段](#common-input-fields) 之外，UserPromptSubmit 挂钩还接收包含用户提交的文本的 `prompt` 字段。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit 决策控制

`UserPromptSubmit` 挂钩可以控制是否处理用户提示并添加上下文。所有 [JSON 输出字段](#json-output) 均可用。

有两种方法可以在退出代码 0 时向对话添加上下文：

* **纯文本标准输出**：写入标准输出的任何非 JSON 文本都会添加为上下文
* **JSON 与 `additionalContext`**：使用下面的 JSON 格式进行更多控制。 `additionalContext` 字段添加为上下文

普通标准输出在记录中显示为挂钩输出。 `additionalContext` 字段的添加更加离散。

要阻止提示，请返回 JSON 对象，并将 `decision` 设置为 `"block"`：

|领域 |描述 |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| `decision` | `"block"` 阻止处理提示并将其从上下文中删除。省略以允许提示继续 |
| `reason` |当 `decision` 为 `"block"` 时向用户显示。未添加到上下文中 |
| `additionalContext` |字符串已添加到 Claude 的上下文 |

```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

**注意**

简单用例不需要 JSON 格式。要添加上下文，您可以使用退出代码 0 将纯文本打印到 stdout。需要时使用 JSON
阻止提示或想要更结构化的控制。

### 工具使用前

在 Claude 创建工具参数之后、处理工具调用之前运行。匹配工具名称：`Bash`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`WebFetch`、`WebSearch` 和任何 [MCP工具名称](#match-mcp-tools)。

使用 [PreToolUse 决策控制](#pretooluse-decision-control) 允许、拒绝或请求使用该工具的权限。

#### PreToolUse 输入

除了[通用输入字段](#common-input-fields) 之外，PreToolUse 挂钩还接收 `tool_name`、`tool_input` 和 `tool_use_id`。 `tool_input` 字段取决于工具：

##### 重击

执行外壳命令。|领域 |类型 |示例|描述 |
| :------------------ | :------ | ：------------------ | :-------------------------------------------------------- |
| `command` |字符串| `"npm test"` |要执行的 shell 命令 |
| `description` |字符串| `"Run test suite"` |该命令的作用的可选描述 |
| `timeout` |数量 | `120000` |可选超时（以毫秒为单位）|
| `run_in_background` |布尔 | `false` |是否在后台运行命令 |

##### 写

创建或覆盖文件。

|领域|类型 |示例|描述 |
| :---------- | :-----| :-------------------- | :--------------------------------- |
| `file_path` |字符串| `"/path/to/file.txt"` |要写入的文件的绝对路径 |
| `content` |字符串| `"file content"` |要写入文件的内容 |

##### 编辑

替换现有文件中的字符串。

|领域 |类型 |示例|描述 |
| :------------ | :------ | :-------------------- | :--------------------------------- |
| `file_path` |字符串| `"/path/to/file.txt"` |要编辑的文件的绝对路径 |
| `old_string` |字符串| `"original text"` |查找和替换的文本 |
| `new_string` |字符串| `"replacement text"` |替换文字|
| `replace_all` |布尔 | `false` |是否替换所有出现的情况 |

##### 阅读

读取文件内容。

|领域|类型 |示例|描述 |
| :---------- | :-----| :-------------------- | ：------------------------------------------ |
| `file_path` |字符串| `"/path/to/file.txt"` |要读取的文件的绝对路径 |
| `offset` |数量 | `10` |从 | 开始读取的可选行号
| `limit` |数量 | `50` |可选的读取行数 |

##### 全局

查找与 glob 模式匹配的文件。

|领域 |类型 |示例|描述 |
| :-------- | :-----| ：-------------- | :--------------------------------------------------------------------- |
| `pattern` |字符串| `"**/*.ts"` |用于匹配文件的全局模式 |
| `path` |字符串| `"/path/to/dir"` |可选的搜索目录。默认为当前工作目录 |

##### 格列普

使用正则表达式搜索文件内容。|领域 |类型 |示例|描述 |
| :------------ | :------ | ：-------------- | :---------------------------------------------------------------------------------------- |
| `pattern` |字符串| `"TODO.*fix"` |要搜索的正则表达式模式 |
| `path` |字符串| `"/path/to/dir"` |要搜索的可选文件或目录 |
| `glob` |字符串| `"*.ts"` |用于过滤文件的可选 glob 模式 |
| `output_mode` |字符串| `"content"` | `"content"`、`"files_with_matches"` 或 `"count"`。默认为 `"files_with_matches"` |
| `-i` |布尔 | `true` |不区分大小写的搜索 |
| `multiline` |布尔 | `false` |启用多行匹配 |

##### 网页获取

获取并处理网页内容。

|领域 |类型 |示例|描述 |
| :----- | :-----| :---------------------------- | ：------------------------------------------------ |
| `url` |字符串| `"https://example.com/api"` |从中获取内容的 URL |
| `prompt` |字符串| `"Extract the API endpoints"` |提示对获取的内容运行 |

##### 网络搜索

搜索网络。

|领域|类型 |示例|描述 |
| :---------------- | :-----| ：-------------------------- | :------------------------------------------------ |
| `query` |字符串| `"react hooks best practices"` |搜索查询 |
| `allowed_domains` |数组| `["docs.example.com"]` |可选：仅包含来自这些域的结果 |
| `blocked_domains` |数组| `["spam.example.com"]` |可选：排除这些域中的结果 |

##### 代理

生成一个[子代理](./sub-agents)。

|领域 |类型 |示例|描述 |
| :-------------- | :-----| ：-------------------------- | ：-------------------------------------------------------- |
| `prompt` |字符串| `"Find all API endpoints"` |代理要执行的任务 |
| `description` |字符串| `"Find API endpoints"` |任务的简短描述 |
| `subagent_type` |字符串| `"Explore"` |使用的专业代理类型 |
| `model` |字符串| `"sonnet"` |可选的模型别名来覆盖默认值 |

#### PreToolUse 决策控制

`PreToolUse` 挂钩可以控制工具调用是否继续。与使用顶级 `decision` 字段的其他挂钩不同，PreToolUse 在 `hookSpecificOutput` 对象内返回其决策。这赋予它更丰富的控制：三种结果（允许、拒绝或询问）加上在执行之前修改工具输入的能力。|领域|描述 |
| ：-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision` | `"allow"` 跳过权限提示。 `"deny"` 阻止工具调用。 `"ask"` 提示用户确认。 [拒绝和询问规则](./permissions#manage-permissions) 当钩子返回 `"allow"` 时仍然适用 |
| `permissionDecisionReason` |对于 `"allow"` 和 `"ask"`，向用户显示，但不向 Claude 显示。对于 `"deny"`，显示为 Claude |
| `updatedInput` |在执行前修改工具的输入参数。与 `"allow"` 结合自动批准，或与 `"ask"` 结合向用户显示修改后的输入 |
| `additionalContext` |在工具执行之前添加到 Claude 上下文的字符串 |

当挂钩返回 `"ask"` 时，向用户显示的权限提示包括标识挂钩来源的标签：例如 `[User]`、`[Project]`、`[Plugin]` 或 `[Local]`。这有助于用户了解哪个配置源正在请求确认。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

**注意**

PreToolUse 之前使用过顶级 `decision` 和 `reason` 字段，但此事件已弃用这些字段。请改用 `hookSpecificOutput.permissionDecision` 和 `hookSpecificOutput.permissionDecisionReason`。已弃用的值 `"approve"` 和 `"block"` 分别映射到 `"allow"` 和 `"deny"`。其他事件（例如 PostToolUse 和 Stop）继续使用顶级 `decision` 和 `reason` 作为其当前格式。

### 权限请求

当向用户显示权限对话框时运行。
使用[PermissionRequest 决策控制](#permissionrequest-decision-control) 代表用户允许或拒绝。

匹配工具名称，值与 PreToolUse 相同。

#### 权限请求输入

PermissionRequest 挂钩像 PreToolUse 挂钩一样接收 `tool_name` 和 `tool_input` 字段，但不接收 `tool_use_id`。可选的 `permission_suggestions` 阵列包含用户通常会在权限对话框中看到的“始终允许”选项。区别在于钩子触发的时间：PermissionRequest 钩子在即将向用户显示权限对话框时运行，而 PreToolUse 钩子在工具执行之前运行，无论权限状态如何。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### PermissionRequest决策控制

`PermissionRequest` 挂钩可以允许或拒绝权限请求。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您的挂钩脚本还可以返回具有以下特定于事件的字段的 `decision` 对象：|领域|描述 |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior` | `"allow"` 授予权限，`"deny"` 拒绝 |
| `updatedInput` |仅适用于 `"allow"`：执行前修改工具的输入参数 |
| `updatedPermissions` |仅适用于 `"allow"`：要应用的[权限更新条目](#permission-update-entries) 数组，例如添加允许规则或更改会话权限模式 |
| `message` |仅适用于 `"deny"`：告诉 Claude 权限被拒绝的原因 |
| `interrupt` |仅适用于 `"deny"`：如果 `true`，则停止 Claude |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### 权限更新条目

`updatedPermissions` 输出字段和 [`permission_suggestions` 输入字段](#permissionrequest-input) 均使用相同的条目对象数组。每个条目都有一个确定其其他字段的 `type` 和一个控制更改写入位置的 `destination`。| `type` |领域 |效果|
| :------------------ | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules` | `rules`、`behavior`、`destination` |添加权限规则。 `rules` 是 `{toolName, ruleContent?}` 对象的数组。省略 `ruleContent` 以匹配整个工具。 `behavior` 是 `"allow"`、`"deny"` 或 `"ask"` |
| `replaceRules` | `rules`、`behavior`、`destination` |将 `destination` 处给定 `behavior` 的所有规则替换为提供的 `rules` |
| `removeRules` | `rules`、`behavior`、`destination` |删除给定 `behavior` 的匹配规则 |
| `setMode` | `mode`、`destination` |更改权限模式。有效模式为 `default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 和 `plan` |
| `addDirectories` | `directories`、`destination` |添加工作目录。 `directories` 是路径字符串数组 |
| `removeDirectories` | `directories`、`destination` |删除工作目录 |

每个条目上的 `destination` 字段确定更改是保留在内存中还是保留到设置文件中。

| `destination` |写入 |
| :---------------- | :---------------------------------------------------------- |
| `session` |仅在内存中，会话结束时丢弃 |
| `localSettings` | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json` |
| `userSettings` | `~/.claude/settings.json` |

挂钩可以回显它收到的 `permission_suggestions` 之一作为其自己的 `updatedPermissions` 输出，这相当于用户在对话框中选择“始终允许”选项。

### 后置工具使用

工具成功完成后立即运行。

匹配工具名称，值与 PreToolUse 相同。

#### PostTool使用输入

`PostToolUse` 在工具成功执行后触发。输入包括 `tool_input`（发送到工具的参数）和 `tool_response`（它返回的结果）。两者的确切架构取决于工具。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### PostToolUse决策控制

`PostToolUse` 挂钩可以在工具执行后向 Claude 提供反馈。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您的挂钩脚本还可以返回以下特定于事件的字段：|领域 |描述 |
| :-------------------- | :---------------------------------------------------------------------------------------- |
| `decision` | `"block"` 使用 `reason` 提示 Claude。省略以允许操作继续进行 |
| `reason` |当 `decision` 为 `"block"` 时对 Claude 显示的说明 |
| `additionalContext` | Claude 需要考虑的其他背景 |
| `updatedMCPToolOutput` |仅适用于 [MCP 工具](#match-mcp-tools)：将工具的输出替换为提供的值 |

```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### 工具使用失败后

当工具执行失败时运行。当工具调用抛出错误或返回失败结果时会触发此事件。使用它来记录故障、发送警报或向 Claude 提供纠正反馈。

匹配工具名称，值与 PreToolUse 相同。

#### PostToolUseFailure 输入

PostToolUseFailure 挂钩接收与 PostToolUse 相同的 `tool_name` 和 `tool_input` 字段，以及作为顶级字段的错误信息：

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

|领域 |描述 |
| :------------- | :------------------------------------------------------------------------------------------ |
| `error` |描述问题所在的字符串 |
| `is_interrupt` |可选布尔值，指示失败是否是由用户中断引起的 |

#### PostToolUseFailure决策控制

`PostToolUseFailure` 挂钩可以在工具发生故障后为 Claude 提供上下文。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您的挂钩脚本还可以返回以下特定于事件的字段：

|领域 |描述 |
| :------------------ | :------------------------------------------------------------------------ |
| `additionalContext` | Claude 与错误一起考虑的其他上下文 |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### 通知

当 Claude Code 发送通知时运行。与通知类型匹配：`permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`。省略匹配器来为所有通知类型运行挂钩。

根据通知类型，使用单独的匹配器运行不同的处理程序。当 Claude 需要权限批准时，此配置会触发特定于权限的警报脚本，并在 Claude 空闲时触发不同的通知：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

####通知输入

除了[通用输入字段](#common-input-fields) 之外，通知挂钩还会接收带有通知文本的 `message`、可选的 `title` 以及指示触发哪种类型的 `notification_type`。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

通知挂钩无法阻止或修改通知。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您还可以返回 `additionalContext` 以向对话添加上下文：|领域 |描述 |
| :------------------ | :-------------------------------- |
| `additionalContext` |字符串已添加到 Claude 的上下文 |

### 子代理启动

当通过代理工具生成 Claude Code 子代理时运行。支持匹配器按代理类型名称进行过滤（内置代理，如 `Bash`、`Explore`、`Plan` 或 `.claude/agents/` 中的自定义代理名称）。

#### 子代理启动输入

除了 [通用输入字段](#common-input-fields) 之外，SubagentStart 挂钩还接收带有子代理唯一标识符的 `agent_id` 和带有代理名称的 `agent_type`（内置代理，如 `"Bash"`、`"Explore"`、`"Plan"` 或自定义代理名称）。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart 挂钩无法阻止子代理创建，但它们可以将上下文注入子代理中。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您还可以返回：

|领域 |描述 |
| :------------------ | :------------------------------------ |
| `additionalContext` |添加到子代理上下文的字符串 |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### 子代理停止

当 Claude Code 子代理完成响应时运行。匹配代理类型，与 SubagentStart 的值相同。

#### 子代理停止输入

除了[通用输入字段](#common-input-fields) 之外，SubagentStop 挂钩还接收 `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path` 和 `last_assistant_message`。 `agent_type` 字段是用于匹配器过滤的值。 `transcript_path` 是主会话的转录本，而 `agent_transcript_path` 是存储在嵌套 `subagents/` 文件夹中的子代理自己的转录本。 `last_assistant_message` 字段包含子代理最终响应的文本内容，因此挂钩可以访问它而无需解析脚本文件。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop 挂钩使用与 [Stop 挂钩](#stop-decision-control) 相同的决策控制格式。

### 停止

当主 Claude Code 代理完成响应时运行。不运行，如果
由于用户中断而发生停止。

#### 停止输入

除了[通用输入字段](#common-input-fields) 之外，停止挂钩还接收 `stop_hook_active` 和 `last_assistant_message`。当 Claude Code 已因停止挂钩而继续运行时，`stop_hook_active` 字段为 `true`。检查此值或处理脚本以防止 Claude Code 无限期运行。 `last_assistant_message` 字段包含 Claude 最终响应的文本内容，因此挂钩可以访问它而无需解析转录文件。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### 停止决策控制

`Stop`和`SubagentStop`钩子可以控制Claude是否继续。除了可用于所有挂钩的 [JSON 输出字段](#json-output) 之外，您的挂钩脚本还可以返回以下特定于事件的字段：

|领域 |描述 |
| :--------- | :------------------------------------------------------------------------- |
| `decision` | `"block"` 阻止 Claude 停止。省略允许 Claude 停止 |
| `reason` |当 `decision` 为 `"block"` 时需要。告诉 Claude 为什么应该继续 |

```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### 队友空闲当[特工队](./agent-teams)队友完成回合后即将闲置时运行。使用此功能可以在队友停止工作之前强制实施质量关卡，例如要求通过 lint 检查或验证输出文件是否存在。

当 `TeammateIdle` 挂钩以代码 2 退出时，队友会收到 stderr 消息作为反馈并继续工作而不是闲置。要完全停止队友而不是重新运行它，请返回 JSON 和 `{"continue": false, "stopReason": "..."}`。 TeammateIdle 挂钩不支持匹配器，并且每次发生时都会触发。

#### 队友空闲输入

除了[通用输入字段](#common-input-fields) 之外，TeammateIdle 挂钩还接收 `teammate_name` 和 `team_name`。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

|领域 |描述 |
| :-------------- | :-------------------------------------------------------- |
| `teammate_name` |即将闲置的队友姓名 |
| `team_name` |团队名称|

#### 队友空闲决策控制

TeammateIdle 钩子支持两种控制队友行为的方法：

* **退出代码2**：队友收到stderr消息作为反馈并继续工作而不是闲置。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` 挂钩行为。向用户展示 `stopReason`。

此示例在允许队友闲置之前检查构建工件是否存在：

```bash
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### 任务完成

当任务被标记为已完成时运行。这会在两种情况下触发：当任何代理通过 TaskUpdate 工具明确将任务标记为已完成时，或者当[代理团队](./agent-teams)队友完成正在进行的任务时。使用它来强制执行完成标准，例如在任务关闭之前通过测试或 lint 检查。

当 `TaskCompleted` 挂钩以代码 2 退出时，任务不会标记为已完成，并且 stderr 消息会作为反馈反馈给模型。要完全停止队友而不是重新运行它，请返回 JSON 和 `{"continue": false, "stopReason": "..."}`。 TaskCompleted 挂钩不支持匹配器，并且每次出现时都会触发。

#### 任务完成输入

除了[通用输入字段](#common-input-fields) 之外，TaskCompleted 挂钩还接收 `task_id`、`task_subject` 以及可选的 `task_description`、`teammate_name` 和 `team_name`。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

|领域|描述 |
| ：------------------ | :------------------------------------------------------ |
| `task_id` |正在完成的任务的标识符 |
| `task_subject` |任务标题 |
| `task_description` |任务的详细描述。可能缺席|
| `teammate_name` |完成任务的队友姓名。可能缺席|
| `team_name` |团队名称。可能缺席|

####任务完成决策控制

TaskCompleted 钩子支持两种控制任务完成的方法：* **退出代码 2**：任务未标记为已完成，并且 stderr 消息作为反馈反馈给模型。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` 挂钩行为。 `stopReason` 显示给用户。

此示例运行测试并在失败时阻止任务完成：

```bash
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### 配置更改

当配置文件在会话期间发生更改时运行。使用它来审核设置更改、实施安全策略或阻止对配置文件进行未经授权的修改。

ConfigChange 会触发对设置文件、托管策略设置和技能文件的更改。输入中的 `source` 字段告诉您更改的配置类型，可选的 `file_path` 字段提供已更改文件的路径。

匹配器过滤配置源：

|匹配器|当它发生时 |
| ：------------------ | :---------------------------------------- |
| `user_settings` | `~/.claude/settings.json` 更改 |
| `project_settings` | `.claude/settings.json` 更改 |
| `local_settings` | `.claude/settings.local.json` 更改 |
| `policy_settings` |托管策略设置更改 |
| `skills` | `.claude/skills/` 中的技能文件发生变化 |

此示例记录安全审核的所有配置更改：

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### 配置更改输入

除了[通用输入字段](#common-input-fields) 之外，ConfigChange 挂钩还接收 `source` 和可选的 `file_path`。 `source` 字段指示更改的配置类型，`file_path` 提供已修改的特定文件的路径。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange决策控制

ConfigChange 挂钩可以阻止配置更改生效。使用退出代码 2 或 JSON `decision` 来阻止更改。阻止时，新设置不会应用于正在运行的会话。

|领域 |描述 |
| :--------- | :---------------------------------------------------------------------------------------------------- |
| `decision` | `"block"` 阻止应用配置更改。省略以允许更改 |
| `reason` |当 `decision` 为 `"block"` 时向用户显示的说明 |

```json
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` 更改无法被阻止。挂钩仍然会触发 `policy_settings` 源，因此您可以使用它们进行审核日志记录，但任何阻止决定都会被忽略。这可确保企业管理的设置始终生效。

### 工作树创建

当您运行 `claude --worktree` 或[子代理使用 `isolation: "worktree"`](./sub-agents#choose-the-subagent-scope) 时，Claude Code 使用 `git worktree` 创建独立的工作副本。如果您配置 WorktreeCreate 挂钩，它会替换默认的 git 行为，让您可以使用不同的版本控制系统，例如 SVN、Perforce 或 Mercurial。

该钩子必须在标准输出上打印创建的工作树目录的绝对路径。 Claude Code 使用此路径作为隔离会话的工作目录。

此示例创建 SVN 工作副本并打印路径以供 Claude Code 使用。将存储库 URL 替换为您自己的：

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```该钩子从标准输入上的 JSON 输入读取工作树 `name`，将新副本检出到新目录中，并打印目录路径。最后一行的 `echo` 是 Claude Code 读取的工作树路径。将任何其他输出重定向到 stderr，这样它就不会干扰路径。

#### Worktree创建输入

除了[通用输入字段](#common-input-fields) 之外，WorktreeCreate 挂钩还接收 `name` 字段。这是新工作树的段标识符，由用户指定或自动生成（例如，`bold-oak-a3f2`）。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Worktree创建输出

该钩子必须在标准输出上打印创建的工作树目录的绝对路径。如果挂钩失败或不产生任何输出，工作树创建将失败并出现错误。

WorktreeCreate 挂钩不使用标准的允许/阻止决策模型。相反，钩子的成败决定了结果。仅支持 `type: "command"` 挂钩。

### 工作树删除

[WorktreeCreate](#worktreecreate) 的清理对应项。当删除工作树时，或者当您退出 `--worktree` 会话并选择删除它时，或者当具有 `isolation: "worktree"` 的子代理完成时，会触发此挂钩。对于基于 git 的工作树，Claude 使用 `git worktree remove` 自动处理清理。如果您为非 git 版本控制系统配置了 WorktreeCreate 挂钩，请将其与 WorktreeRemove 挂钩配对以处理清理。如果没有，工作树目录将保留在磁盘上。

Claude Code 将 WorktreeCreate 在标准输出上打印的路径作为挂钩输入中的 `worktree_path` 传递。此示例读取该路径并删除该目录：

```json
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### Worktree删除输入

除了[通用输入字段](#common-input-fields) 之外，WorktreeRemove 挂钩还接收 `worktree_path` 字段，它是要删除的工作树的绝对路径。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove 挂钩没有决策控制。它们无法阻止工作树删除，但可以执行清理任务，例如删除版本控制状态或归档更改。仅在调试模式下记录挂钩失败。仅支持 `type: "command"` 挂钩。

### 预压缩

在 Claude Code 即将运行紧凑操作之前运行。

匹配器值指示压缩是手动还是自动触发：

|匹配器|当它发生时 |
| :----- | ：-------------------------------------------------------- |
| `manual` | `/compact` |
| `auto` |上下文窗口满时自动压缩 |

#### 预压缩输入

除了[通用输入字段](#common-input-fields) 之外，PreCompact 挂钩还接收 `trigger` 和 `custom_instructions`。对于 `manual`，`custom_instructions` 包含用户传递到 `/compact` 的内容。对于 `auto`，`custom_instructions` 为空。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### 后紧凑

在 Claude Code 完成紧凑操作后运行。使用此事件对新的压缩状态做出反应，例如记录生成的摘要或更新外部状态。

相同的匹配器值适用于 `PreCompact`：|匹配器|当它发生时 |
| :----- | :------------------------------------------------- |
| `manual` | `/compact` 之后 |
| `auto` |当上下文窗口已满时自动压缩后 |

#### 后压缩输入

除了[通用输入字段](#common-input-fields) 之外，PostCompact 挂钩还接收 `trigger` 和 `compact_summary`。 `compact_summary` 字段包含压缩操作生成的会话摘要。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact 钩子没有决策控制。它们不会影响压实结果，但可以执行后续任务。

### 会话结束

当 Claude Code 会话结束时运行。对于清理任务、记录会话很有用
统计数据，或保存会话状态。支持匹配器按退出原因进行过滤。

挂钩输入中的 `reason` 字段指示会话结束的原因：

|原因 |描述 |
| :---------------------------- | ：------------------------------------------ |
| `clear` |使用 `/clear` 命令清除会话 |
| `logout` |用户已退出 |
| `prompt_input_exit` |用户在提示输入可见时退出 |
| `bypass_permissions_disabled` |绕过权限模式被禁用 |
| `other` |其他退出原因 |

#### 会话结束输入

除了 [通用输入字段](#common-input-fields) 之外，SessionEnd 挂钩还会收到一个 `reason` 字段，指示会话结束的原因。有关所有值，请参阅上面的[原因表](#sessionend)。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd 挂钩没有决策控制。它们不能阻止会话终止，但可以执行清理任务。

SessionEnd 挂钩的默认超时为 1.5 秒。这适用于会话退出和 `/clear`。如果您的挂钩需要更多时间，请将 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 环境变量设置为更高的值（以毫秒为单位）。任何每个挂钩 `timeout` 设置也受此值限制。

```bash
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### 引出

当 MCP 服务器在任务中间请求用户输入时运行。默认情况下，Claude Code 显示一个交互式对话框供用户响应。挂钩可以拦截此请求并以编程方式响应，完全跳过对话框。

匹配器字段与 MCP 服务器名称相匹配。

#### 诱导输入

除了[通用输入字段](#common-input-fields) 之外，诱导挂钩还接收 `mcp_server_name`、`message` 以及可选的 `mode`、`url`、`elicitation_id` 和 `requested_schema` 字段。

对于形式模式启发（最常见的情况）：

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

对于 URL 模式引发（基于浏览器的身份验证）：

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### 启发输出

要以编程方式响应而不显示对话框，请返回带有 `hookSpecificOutput` 的 JSON 对象：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```
|领域 |价值观 |描述 |
| :-------- | :---------------------------- | :---------------------------------------------------------------------------- |
| `action` | `accept`、`decline`、`cancel` |是否接受、拒绝或取消请求 |
| `content` |对象|要提交的表单字段值。仅当 `action` 为 `accept` 时使用 |

退出代码 2 拒绝引发并向用户显示 stderr。

### 启发结果

在用户响应 MCP 引发后运行。挂钩可以在响应发送回 MCP 服务器之前观察、修改或阻止响应。

匹配器字段与 MCP 服务器名称相匹配。

#### 启发结果输入

除了[通用输入字段](#common-input-fields) 之外，EliitationResult 挂钩还接收 `mcp_server_name`、`action` 以及可选的 `mode`、`elicitation_id` 和 `content` 字段。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### 启发结果输出

要覆盖用户的响应，请返回带有 `hookSpecificOutput` 的 JSON 对象：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

|领域 |价值观 |描述 |
| :-------- | :---------------------------- | :--------------------------------------------------------------------- |
| `action` | `accept`、`decline`、`cancel` |覆盖用户的操作 |
| `content` |对象|覆盖表单字段值。仅当 `action` 为 `accept` 时才有意义 |

退出代码 2 阻止响应，将有效操作更改为 `decline`。

## 基于提示的钩子

除了命令和 HTTP 挂钩之外，Claude Code 还支持基于提示的挂钩 (`type: "prompt"`)（使用 LLM 评估是否允许或阻止操作）以及代理挂钩 (`type: "agent"`)（生成具有工具访问权限的代理验证程序）。并非所有事件都支持每种挂钩类型。

支持所有四种挂钩类型（`command`、`http`、`prompt` 和 `agent`）的事件：

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

仅支持 `type: "command"` 挂钩的事件：

* `ConfigChange`
* `Elicitation`
* `ElicitationResult`
* `InstructionsLoaded`
* `Notification`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### 基于提示的挂钩如何工作

基于提示的挂钩不执行 Bash 命令：

1. 将 hook 输入和提示发送到 Claude 模型，默认为 Haiku
2. LLM 以包含决定的结构化 JSON 进行响应
3. Claude Code 自动处理决策

### 提示钩子配置

将 `type` 设置为 `"prompt"` 并提供 `prompt` 字符串而不是 `command`。使用 `$ARGUMENTS` 占位符将挂钩的 JSON 输入数据注入到提示文本中。 Claude Code 将组合的提示和输入发送到快速 Claude 模型，该模型返回 JSON 决策。

此 `Stop` 挂钩要求 LLM 在允许 Claude 完成之前评估所有任务是否已完成：```json 
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

|领域 |必填|描述 |
| :-------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` |是的 |必须是 `"prompt"` |
| `prompt` |是的 |发送给 LLM 的提示文本。使用 `$ARGUMENTS` 作为挂钩输入 JSON 的占位符。如果 `$ARGUMENTS` 不存在，则输入 JSON 会附加到提示 |
| `model` |没有|用于评估的模型。默认为快速模型 |
| `timeout` |没有|超时（以秒为单位）。默认值：30 |

### 响应模式

LLM 必须回复 JSON，其中包含：

```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

|领域 |描述 |
| :----- | :-------------------------------------------------------- |
| `ok` | `true` 允许该操作，`false` 阻止该操作 |
| `reason` |当 `ok` 为 `false` 时需要。 Claude 的说明 |

### 示例：多标准停止挂钩

此 `Stop` 挂钩使用详细的提示来检查三个条件，然后才允许 Claude 停止。如果 `"ok"` 是 `false`，则 Claude 会继续使用提供的原因作为其下一条指令。 `SubagentStop` 挂钩使用相同的格式来评估 [subagent](./sub-agents) 是否应停止：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 基于代理的钩子

基于代理的挂钩 (`type: "agent"`) 类似于基于提示的挂钩，但具有多轮工具访问。代理挂钩生成一个子代理，该子代理可以读取文件、搜索代码并检查代码库以验证条件，而不是单个 LLM 调用。代理挂钩支持与基于提示的挂钩相同的事件。

### 代理挂钩如何工作

当代理钩子触发时：

1. Claude Code 使用您的提示和挂钩的 JSON 输入生成一个子代理
2. 子代理可以使用Read、Grep、Glob等工具进行调查
3. 最多 50 个回合后，子代理返回结构化的 `{ "ok": true/false }` 决策
4. Claude Code 以与提示挂钩相同的方式处理决策

当验证需要检查实际文件或测试输出而不仅仅是单独评估挂钩输入数据时，代理挂钩非常有用。

### 代理挂钩配置

将 `type` 设置为 `"agent"` 并提供 `prompt` 字符串。配置字段与[prompt hooks](#prompt-hook-configuration)相同，但默认超时时间更长：|领域 |必填|描述 |
| :-------- | :----- | :---------------------------------------------------------------------------------------------- |
| `type` |是的 |必须是 `"agent"` |
| `prompt` |是的 |提示描述要验证的内容。使用 `$ARGUMENTS` 作为挂钩输入 JSON 的占位符 |
| `model` |没有|使用的模型。默认为快速模型 |
| `timeout` |没有|超时（以秒为单位）。默认值：60 |

响应架构与提示挂钩相同：`{ "ok": true }` 允许或 `{ "ok": false, "reason": "..." }` 阻止。

此 `Stop` 挂钩会在允许 Claude 完成之前验证所有单元测试是否已通过：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## 在后台运行钩子

默认情况下，挂钩会阻止 Claude 的执行，直到完成为止。对于部署、测试套件或外部 API 调用等长时间运行的任务，请将 `"async": true` 设置为在后台运行挂钩，同时 Claude 继续工作。异步挂钩无法阻止或控制 Claude 的行为：`decision`、`permissionDecision` 和 `continue` 等响应字段没有任何效果，因为它们本来控制的操作已经完成。

### 配置异步钩子

将 `"async": true` 添加到命令挂钩的配置中，以在后台运行它，而不会阻止 Claude。此字段仅在 `type: "command"` 挂钩上可用。

此挂钩在每次 `Write` 工具调用后运行一个测试脚本。 Claude 立即继续工作，而 `run-tests.sh` 执行长达 120 秒。脚本完成后，其输出将在下一个对话回合中传递：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

`timeout` 字段设置后台进程的最长时间（以秒为单位）。如果未指定，异步挂钩将使用与同步挂钩相同的 10 分钟默认值。

### 异步钩子如何执行

当异步挂钩触发时，Claude Code 启动挂钩进程并立即继续，而不等待其完成。该挂钩通过 stdin 接收与同步挂钩相同的 JSON 输入。

后台进程退出后，如果挂钩生成带有 `systemMessage` 或 `additionalContext` 字段的 JSON 响应，则该内容将作为下一个对话回合的上​​下文传递到 Claude。

默认情况下会抑制异步挂钩完成通知。要查看它们，请使用 `Ctrl+O` 启用详细模式或使用 `--verbose` 启动 Claude Code。

### 示例：文件更改后运行测试

每当 Claude 写入文件时，此挂钩就会在后台启动测试套件，然后在测试完成时将结果报告给 Claude。将此脚本保存到项目中的 `.claude/hooks/run-tests-async.sh` 中，并使其可以使用 `chmod +x` 执行：

```bash
#!/bin/bash
# run-tests-async.sh

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results via systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

然后将此配置添加到项目根目录中的 `.claude/settings.json` 中。 `async: true` 标志让 Claude 在测试运行时继续工作：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### 限制

与同步钩子相比，异步钩子有几个限制：* 仅 `type: "command"` 挂钩支持 `async`。基于提示的挂钩无法异步运行。
* 异步钩子不能阻止工具调用或返回决策。当钩子完成时，触发操作已经开始。
* 挂钩输出在下一个对话回合传递。如果会话空闲，响应将等到下一次用户交互。
* 每次执行都会创建一个单独的后台进程。同一异步挂钩的多次触发不会进行重复数据删除。

## 安全考虑

### 免责声明

命令挂钩以系统用户的完全权限运行。

**警告**

命令挂钩使用您的完整用户权限执行 shell 命令。他们可以修改、删除或访问您的用户帐户可以访问的任何文件。在将所有挂钩命令添加到您的配置之前，请检查并测试它们。

### 安全最佳实践

编写钩子时请记住这些做法：

* **验证和清理输入**：永远不要盲目信任输入数据
* **始终引用 shell 变量**：使用 `"$VAR"` 而不是 `$VAR`
* **阻止路径遍历**：检查文件路径中是否有 `..`
* **使用绝对路径**：指定脚本的完整路径，使用`"$CLAUDE_PROJECT_DIR"`作为项目根目录
* **跳过敏感文件**：避免`.env`、`.git/`、密钥等。

## 调试钩子

运行 `claude --debug` 以查看挂钩执行详细信息，包括匹配的挂钩、其退出代码和输出。使用 `Ctrl+O` 切换详细模式以查看转录中的挂钩进度。

```text
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

有关对钩子未触发、无限停止钩环或配置错误等常见问题进行故障排除的信息，请参阅指南中的[限制和故障排除](./hooks-guide#limitations-and-troubleshooting)。
