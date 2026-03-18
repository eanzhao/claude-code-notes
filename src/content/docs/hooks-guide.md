---
title: "使用钩子自动化工作流程"
order: 27
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "当 Claude Code 编辑文件、完成任务或需要输入时自动运行 shell 命令。格式化代码、发送通知、验证命令并执行项目规则。"
sourceUrl: "https://code.claude.com/docs/en/hooks-guide.md"
sourceTitle: "Automate workflows with hooks"
tags: []
---
# 使用钩子自动化工作流程

> 当 Claude Code 编辑文件、完成任务或需要输入时自动运行 shell 命令。格式化代码、发送通知、验证命令并执行项目规则。

挂钩是用户定义的 shell 命令，在 Claude Code 生命周期的特定点执行。它们对 Claude Code 的行为提供确定性控制，确保某些操作始终发生，而不是依赖 LLM 选择运行它们。使用挂钩强制执行项目规则、自动执行重复任务并将 Claude Code 与现有工具集成。

对于需要判断而非确定性规则的决策，您还可以使用 [基于提示的挂钩](#prompt-based-hooks) 或 [基于代理的挂钩](#agent-based-hooks)，它们使用 Claude 模型来评估条件。

有关扩展 Claude Code 的其他方法，请参阅[技能](./skills)，为 Claude 提供额外的指令和可执行命令，请参阅[子代理](./sub-agents)，以在隔离上下文中运行任务，并参阅[插件](./plugins)，以打包扩展以在项目之间共享。

**提示**

本指南涵盖常见用例以及如何开始。有关完整事件架构、JSON 输入/输出格式以及异步挂钩和 MCP 工具挂钩等高级功能，请参阅[挂钩参考](./hooks)。

## 设置你的第一个钩子

要创建挂钩，请将 `hooks` 块添加到 [设置文件](#configure-hook-location)。本演练创建了一个桌面通知挂钩，因此只要 Claude 等待您的输入而不是观看终端，您就会收到警报。

### 将挂钩添加到您的设置中

打开 `~/.claude/settings.json` 并添加 `Notification` 挂钩。下面的示例使用 `osascript` 代替 macOS；有关 Linux 和 Windows 命令，请参阅[当 Claude 需要输入时收到通知](#get-notified-when-claude-needs-input)。

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

如果您的设置文件已有 `hooks` 密钥，请将 `Notification` 条目合并到其中，而不是替换整个对象。您还可以要求 Claude 通过在 CLI 中描述您想要的内容来为您编写挂钩。

  
### 验证配置

输入 `/hooks` 打开钩子浏览器。您将看到所有可用挂钩事件的列表，每个配置了挂钩的事件旁边都有一个计数。选择 `Notification` 以确认您的新挂钩出现在列表中。选择挂钩会显示其详细信息：事件、匹配器、类型、源文件和命令。

  
### 测试钩子

按 `Esc` 返回 CLI。要求 Claude 执行需要许可的操作，然后退出终端。您应该会收到桌面通知。

**提示**

`/hooks` 菜单是只读的。要添加、修改或删除挂钩，请直接编辑您的设置 JSON 或要求 Claude 进行更改。

## 你可以自动化什么

挂钩可让您在 Claude Code 生命周期的关键点运行代码：编辑后格式化文件、执行前阻止命令、在 Claude 需要输入时发送通知、在会话启动时注入上下文等等。有关挂钩事件的完整列表，请参阅[挂钩参考](./hooks#hook-lifecycle)。

每个示例都包含一个即用型配置块，您可以将其添加到[设置文件](#configure-hook-location)。最常见的模式：* [当 Claude 需要输入时收到通知](#get-notified-when-claude-needs-input)
* [编辑后自动格式化代码](#auto-format-code-after-edits)
* [阻止编辑受保护的文件](#block-edits-to-protected-files)
* [压缩后重新注入上下文](#re-inject-context-after-compaction)
* [审核配置变更](#audit-configuration-changes)
* [自动批准特定权限提示](#auto-approve-specific-permission-prompts)

### 当 Claude 需要输入时收到通知

每当 Claude 完成工作并需要您输入时，您都会收到桌面通知，这样您就可以切换到其他任务，而无需检查终端。

此挂钩使用 `Notification` 事件，该事件在 Claude 等待输入或权限时触发。下面的每个选项卡都使用平台的本机通知命令。将其添加到 `~/.claude/settings.json`：

### macOS

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

  
### Linux

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

  
### Windows (PowerShell)

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

### 编辑后自动格式化代码

自动对 Claude 编辑的每个文件运行 [Prettier](https://prettier.io/)，因此格式保持一致，无需手动干预。

此挂钩使用 `PostToolUse` 事件和 `Edit|Write` 匹配器，因此它仅在文件编辑工具之后运行。该命令提取编辑后的文件路径 [`jq`](https://jqlang.github.io/jq/) 并将其传递给 Prettier。将其添加到项目根目录中的 `.claude/settings.json` 中：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

**注意**

本页上的 Bash 示例使用 `jq` 进行 JSON 解析。使用 `brew install jq` (macOS)、`apt-get install jq` (Debian/Ubuntu) 安装它，或参阅 [`jq` 下载](https://jqlang.github.io/jq/download/)。

### 阻止对受保护文件的编辑

防止 Claude 修改敏感文件，例如 `.env`、`package-lock.json` 或 `.git/` 中的任何内容。 Claude 收到反馈解释编辑被阻止的原因，因此它可以调整其方法。

此示例使用挂钩调用的单独脚本文件。该脚本根据受保护模式列表检查目标文件路径，并以代码 2 退出以阻止编辑。

### 创建钩子脚本

将其保存到 `.claude/hooks/protect-files.sh`：

```bash
#!/bin/bash
# protect-files.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

  
### 使脚本可执行 (macOS/Linux)

挂钩脚本必须是可执行的，Claude Code 才能运行它们：

```bash
chmod +x .claude/hooks/protect-files.sh
```

  
### 注册钩子

将 `PreToolUse` 挂钩添加到 `.claude/settings.json`，该挂钩在任何 `Edit` 或 `Write` 工具调用之前运行脚本：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

### 压缩后重新注入上下文

当 Claude 的上下文窗口填满时，压缩会总结对话以释放空间。这可能会丢失重要的细节。使用 `SessionStart` 挂钩和 `compact` 匹配器在每次压缩后重新注入关键上下文。

命令写入 stdout 的任何文本都会添加到 Claude 的上下文中。此示例让 Claude 想起了项目惯例和最近的工作。将其添加到项目根目录中的 `.claude/settings.json` 中：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

您可以将 `echo` 替换为任何生成动态输出的命令，例如 `git log --oneline -5` 来显示最近的提交。要在每次会话启动时注入上下文，请考虑使用 [CLAUDE.md](./memory)。有关环境变量，请参阅参考中的 [`CLAUDE_ENV_FILE`](./hooks#persist-environment-variables)。

### 审核配置更改跟踪会话期间设置或技能文件何时发生更改。当外部进程或编辑器修改配置文件时，`ConfigChange` 事件会触发，因此您可以记录更改以确保合规性或阻止未经授权的修改。

此示例将每个更改附加到审核日志中。将其添加到 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

匹配器按配置类型进行筛选：`user_settings`、`project_settings`、`local_settings`、`policy_settings` 或 `skills`。要阻止更改生效，请使用代码 2 退出或返回 `{"decision": "block"}`。有关完整输入架构，请参阅 [ConfigChange 参考](./hooks#configchange)。

### 自动批准特定权限提示

跳过您始终允许的工具调用的批准对话框。此示例自动批准 `ExitPlanMode`，该工具 Claude 在完成呈现计划并要求继续时调用，因此每次计划准备就绪时都不会提示您。

与上面的退出代码示例不同，自动批准要求您的挂钩将 JSON 决策写入标准输出。当 Claude Code 即将显示权限对话框时，`PermissionRequest` 挂钩会触发，并返回 `"behavior": "allow"` 代表您应答。

匹配器仅将挂钩范围限定为 `ExitPlanMode`，因此其他提示不会受到影响。将其添加到 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

当挂钩批准后，Claude Code 退出计划模式并恢复进入计划模式之前处于活动状态的任何权限模式。文字记录显示“Allowed by PermissionRequest hook”，其中会出现对话框。挂钩路径始终保留当前对话：它无法像对话框那样清除上下文并启动新的实现会话。

要设置特定的权限模式，挂钩的输出可以包含带有 `setMode` 条目的 `updatedPermissions` 数组。 `mode` 值是任何权限模式，例如 `default`、`acceptEdits` 或 `bypassPermissions`，而 `destination: "session"` 仅将其应用于当前会话。

要将会话切换到 `acceptEdits`，您的挂钩会将此 JSON 写入标准输出：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

保持匹配器尽可能窄。在 `.*` 上匹配或将匹配器留空将自动批准每个权限提示，包括文件写入和 shell 命令。有关完整的决策字段集，请参阅 [PermissionRequest 参考](./hooks#permissionrequest-decision-control)。

## 钩子如何工作

挂钩事件在 Claude Code 中的特定生命周期点触发。当事件触发时，所有匹配的挂钩并行运行，并且相同的挂钩命令会自动进行重复数据删除。下表显示了每个事件及其触发时间：|活动 |当它发生时 |
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
| `SessionEnd` |当会话终止时 |每个钩子都有一个 `type` 来确定它的运行方式。大多数挂钩使用 `"type": "command"`，它运行 shell 命令。还提供其他三种类型：

* `"type": "http"`：将事件数据 POST 到 URL。请参阅 [HTTP 挂钩](#http-hooks)。
* `"type": "prompt"`：单轮法学硕士评估。请参阅[基于提示的挂钩](#prompt-based-hooks)。
* `"type": "agent"`：带工具访问的多圈验证。请参阅[基于代理的挂钩](#agent-based-hooks)。

### 读取输入并返回输出

挂钩通过 stdin、stdout、stderr 和退出代码与 Claude Code 进行通信。当事件触发时，Claude Code 会将特定于事件的数据作为 JSON 传递到脚本的标准输入。您的脚本读取该数据，执行其工作，并通过退出代码告诉 Claude Code 接下来要做什么。

#### 挂钩输入

每个事件都包含 `session_id` 和 `cwd` 等通用字段，但每种事件类型都会添加不同的数据。例如，当 Claude 运行 Bash 命令时，`PreToolUse` 挂钩在 stdin 上收到类似以下内容：

```json
{
  "session_id": "abc123",          // unique ID for this session
  "cwd": "/Users/sarah/myproject", // working directory when the event fired
  "hook_event_name": "PreToolUse", // which event triggered this hook
  "tool_name": "Bash",             // the tool Claude is about to use
  "tool_input": {                  // the arguments Claude passed to the tool
    "command": "npm test"          // for Bash, this is the shell command
  }
}
```

您的脚本可以解析 JSON 并对这些字段中的任何一个执行操作。 `UserPromptSubmit` 挂钩获取 `prompt` 文本，`SessionStart` 挂钩获取 `source`（启动、恢复、清除、压缩），依此类推。请参阅参考中的[通用输入字段](./hooks#common-input-fields) 了解共享字段，以及每个事件的特定事件架构部分。

#### 钩子输出

您的脚本通过写入 stdout 或 stderr 并使用特定代码退出来告诉 Claude Code 接下来要做什么。例如，想要阻止命令的 `PreToolUse` 挂钩：

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2                                               # exit 2 = block the action
fi

exit 0  # exit 0 = let it proceed
```

退出代码决定接下来会发生什么：

* **退出 0**：操作继续进行。对于 `UserPromptSubmit` 和 `SessionStart` 挂钩，写入 stdout 的任何内容都会添加到 Claude 的上下文中。
* **出口 2**：操作被阻止。向 stderr 写入原因，Claude 会收到它作为反馈，以便进行调整。
* **任何其他退出代码**：操作继续。 Stderr 已记录，但未显示给 Claude。使用 `Ctrl+O` 切换详细模式以在记录中查看这些消息。

#### 结构化 JSON 输出

退出代码为您提供两个选项：允许或阻止。要获得更多控制，请退出 0 并将 JSON 对象打印到 stdout。

**注意**

使用 exit 2 通过 stderr 消息进行阻止，或使用 exit 0 通过 JSON 进行结构化控制。不要混合它们：当您退出 2 时，Claude Code 会忽略 JSON。

例如，`PreToolUse` 挂钩可以拒绝工具调用并告诉 Claude 原因，或将其升级给用户以供批准：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code 读取 `permissionDecision` 并取消工具调用，然后将 `permissionDecisionReason` 作为反馈反馈给 Claude。这三个选项特定于 `PreToolUse`：

* `"allow"`：跳过交互权限提示。拒绝和询问规则，包括企业管理的拒绝列表，仍然适用
* `"deny"`：取消工具调用并将原因发送至Claude
* `"ask"`: 正常向用户显示权限提示返回 `"allow"` 会跳过交互式提示，但不会覆盖 [权限规则](./permissions#manage-permissions)。如果拒绝规则与工具调用匹配，则即使您的挂钩返回 `"allow"`，该调用也会被阻止。如果询问规则匹配，仍会提示用户。这意味着来自任何设置范围（包括[托管设置](./settings#settings-files)）的拒绝规则始终优先于挂钩批准。

其他事件使用不同的决策模式。例如，`PostToolUse` 和 `Stop` 挂钩使用顶级 `decision: "block"` 字段，而 `PermissionRequest` 使用 `hookSpecificOutput.decision.behavior`。请参阅参考资料中的[摘要表](./hooks#decision-control)，了解按事件的完整细分。

对于 `UserPromptSubmit` 挂钩，请使用 `additionalContext` 将文本注入 Claude 的上下文中。基于提示的挂钩 (`type: "prompt"`) 以不同方式处理输出：请参阅[基于提示的挂钩](#prompt-based-hooks)。

### 带匹配器的过滤钩子

如果没有匹配器，钩子就会在每次发生事件时触发。匹配器可以让你缩小范围。例如，如果您只想在文件编辑后（而不是在每次工具调用后）运行格式化程序，请将匹配器添加到 `PostToolUse` 挂钩：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

`"Edit|Write"` 匹配器是与工具名称匹配的正则表达式模式。该挂钩仅在 Claude 使用 `Edit` 或 `Write` 工具时触发，而在使用 `Bash`、`Read` 或任何其他工具时不会触发。

每个事件类型都与特定字段匹配。匹配器支持精确的字符串和正则表达式模式：|活动 |匹配器过滤什么 |匹配器值示例 |
| :---------------------------------------------------------------------------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------ |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` |工具名称| `Bash`、`Edit\|Write`、`mcp__.*` |
| `SessionStart` |会议如何开始 | `startup`、`resume`、`clear`、`compact` |
| `SessionEnd` |会议为何结束 | `clear`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other` |
| `Notification` |通知类型 | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog` |
| `SubagentStart` |代理类型 | `Bash`、`Explore`、`Plan` 或自定义代理名称 |
| `PreCompact`、`PostCompact` |是什么触发了压缩| `manual`、`auto` |
| `SubagentStop` |代理类型 |与 `SubagentStart` 相同的值 |
| `ConfigChange` |配置源码| `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills` |
| `UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove` |没有匹配器支持 |总是在每次发生时触发 |

更多显示不同事件类型匹配器的示例：

### 记录每个 Bash 命令

仅匹配 `Bash` 工具调用并将每个命令记录到文件中。命令完成后会触发 `PostToolUse` 事件，因此 `tool_input.command` 包含运行的内容。该挂钩在标准输入上接收作为 JSON 的事件数据，`jq -r '.tool_input.command'` 仅提取命令字符串，`>>` 将其附加到日志文件中：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

  
### 匹配 MCP 工具

MCP 工具使用与内置工具不同的命名约定：`mcp__<server>__<tool>`，其中 `<server>` 是 MCP 服务器名称，`<tool>` 是它提供的工具。例如，`mcp__github__search_repositories` 或 `mcp__filesystem__read_file`。使用正则表达式匹配器来定位特定服务器中的所有工具，或使用 `mcp__.*__write.*` 等模式跨服务器进行匹配。有关示例的完整列表，请参阅参考资料中的[匹配 MCP 工具](./hooks#match-mcp-tools)。下面的命令使用 `jq` 从挂钩的 JSON 输入中提取工具名称，并将其写入 stderr，在其中以详细模式显示 (`Ctrl+O`)：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
          }
        ]
      }
    ]
  }
}
```

  
### 会话结束时清理

`SessionEnd` 事件支持会话结束原因的匹配器。此挂钩仅在 `clear` 上触发（当您运行 `/clear` 时），而不是在正常退出时触发：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "clear",
        "hooks": [
          {
            "type": "command",
            "command": "rm -f /tmp/claude-scratch-*.txt"
          }
        ]
      }
    ]
  }
}
```

有关完整匹配器语法，请参阅 [Hooks 参考](./hooks#configuration)。

### 配置钩子位置

添加钩子的位置决定了它的范围：

|地点 |范围 |可分享|
| :-------------------------------------------------------- | :--------------------------------- | :--------------------------------- |
| `~/.claude/settings.json` |您的所有项目 |不，在您的机器本地 |
| `.claude/settings.json` |单个项目 |是的，可以提交给 repo |
| `.claude/settings.local.json` |单个项目 |不，gitignored |
|托管策略设置 |组织范围 |是的，由管理员控制 |
| [插件](./plugins) `hooks/hooks.json` |当插件启用时 |是的，与插件捆绑在一起 |
| [技能](./skills) 或 [代理](./sub-agents) frontmatter |当技能或代理处于活动状态时 |是的，在组件文件中定义 |

在 Claude Code 中运行 [`/hooks`](./hooks#the-hooks-menu) 以浏览按事件分组的所有已配置挂钩。要立即禁用所有挂钩，请在设置文件中设置 `"disableAllHooks": true`。

如果您在 Claude Code 运行时直接编辑设置文件，文件观察器通常会自动拾取挂钩更改。

## 基于提示的钩子

对于需要判断而不是确定性规则的决策，请使用 `type: "prompt"` 挂钩。 Claude Code 不运行 shell 命令，而是将提示和挂钩的输入数据发送到 Claude 模型（默认为 Haiku）来做出决定。如果您需要更多功能，可以使用 `model` 字段指定不同的型号。

该模型的唯一工作是返回是/否决定，如 JSON：

* `"ok": true`：行动继续进行
* `"ok": false`：操作被阻止。该模型的 `"reason"` 会反馈到 Claude，以便进行调整。

此示例使用 `Stop` 挂钩询问模型是否所有请求的任务均已完成。如果模型返回 `"ok": false`，则 Claude 继续工作并使用 `reason` 作为其下一条指令：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

有关完整配置选项，请参阅参考中的[基于提示的挂钩](./hooks#prompt-based-hooks)。

## 基于代理的钩子

当验证需要检查文件或运行命令时，请使用 `type: "agent"` 挂钩。与进行单个 LLM 调用的提示挂钩不同，代理挂钩生成一个子代理，该子代理可以读取文件、搜索代码并使用其他工具在返回决策之前验证条件。

代理挂钩使用与提示挂钩相同的 `"ok"` / `"reason"` 响应格式，但具有更长的默认超时（60 秒）和最多 50 次工具使用轮次。此示例在允许 Claude 停止之前验证测试是否通过：

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

当仅钩子输入数据足以做出决定时，请使用提示钩子。当您需要根据代码库的实际状态验证某些内容时，请使用代理挂钩。

有关完整配置选项，请参阅参考中的[基于代理的挂钩](./hooks#agent-based-hooks)。

## HTTP 钩子

使用 `type: "http"` 挂钩将事件数据 POST 到 HTTP 端点，而不是运行 shell 命令。端点接收与命令挂钩在标准输入上接收的相同的 JSON，并使用相同的 JSON 格式通过 HTTP 响应正文返回结果。

当您希望 Web 服务器、云功能或外部服务处理挂钩逻辑时，HTTP 挂钩非常有用：例如，记录整个团队的工具使用事件的共享审核服务。

此示例将使用的每个工具发布到本地日志服务：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
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

端点应使用与命令挂钩相同的[输出格式](./hooks#json-output)返回 JSON 响应正文。要阻止工具调用，请返回带有相应 `hookSpecificOutput` 字段的 2xx 响应。仅 HTTP 状态代码无法阻止操作。

标头值支持使用 `$VAR_NAME` 或 `${VAR_NAME}` 语法进行环境变量插值。仅解析 `allowedEnvVars` 数组中列出的变量；所有其他 `$VAR` 引用均保留为空。

有关完整的配置选项和响应处理，请参阅参考中的 [HTTP 挂钩](./hooks#http-hook-fields)。

## 限制和故障排除

### 限制

* 命令挂钩仅通过 stdout、stderr 和退出代码进行通信。它们无法直接触发命令或工具调用。 HTTP 挂钩通过响应正文进行通信。
* 挂钩超时默认为 10 分钟，可通过 `timeout` 字段对每个挂钩进行配置（以秒为单位）。
* `PostToolUse` 挂钩无法撤消操作，因为该工具已执行。
* `PermissionRequest` 挂钩在[非交互模式](./headless) (`-p`) 下不会触发。使用 `PreToolUse` 挂钩进行自动权限决策。
* `Stop` 钩子在 Claude 完成响应时触发，而不仅仅是在任务完成时触发。它们不会因用户中断而触发。

### 钩子未触发

该钩子已配置但从未执行。

* 运行 `/hooks` 并确认挂钩出现在正确的事件下
* 检查匹配器模式是否与工具名称完全匹配（匹配器区分大小写）
* 验证您正在触发正确的事件类型（例如，`PreToolUse` 在工具执行之前触发，`PostToolUse` 在工具执行之后触发）
* 如果在非交互模式 (`-p`) 下使用 `PermissionRequest` 挂钩，请切换到 `PreToolUse`

### 输出中的钩子错误

您会在记录中看到类似“PreToolUse hook error: ...”的消息。

* 您的脚本意外退出并显示非零代码。通过管道样品 JSON 手动测试：
  ```bash 
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* 如果看到“找不到命令”，请使用绝对路径或 `$CLAUDE_PROJECT_DIR` 来引用脚本
* 如果看到“jq: command not found”，请安装 `jq` 或使用 Python/Node.js 进行 JSON 解析
* 如果脚本根本没有运行，请将其设为可执行：`chmod +x ./my-hook.sh`

### `/hooks` 显示未配置挂钩

您编辑了设置文件，但挂钩未出现在菜单中。* 文件编辑通常会自动获取。如果几秒钟后它们还没有出现，则文件观察器可能错过了更改：重新启动会话以强制重新加载。
* 验证您的 JSON 是否有效（不允许使用尾随逗号和注释）
* 确认设置文件位于正确的位置：`.claude/settings.json` 用于项目挂钩，`~/.claude/settings.json` 用于全局挂钩

### 停止钩子永远运行

Claude 继续无限循环工作而不是停止。

您的 Stop 挂钩脚本需要检查它是否已经触发了延续。从 JSON 输入中解析 `stop_hook_active` 字段，如果是 `true`，则提前退出：

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### JSON 验证失败

即使您的挂钩脚本输出有效的 JSON，Claude Code 也会显示 JSON 解析错误。

当 Claude Code 运行挂钩时，它会生成一个外壳来获取您的配置文件（`~/.zshrc` 或 `~/.bashrc`）。如果您的配置文件包含无条件 `echo` 语句，则该输出将添加到您的钩子的 JSON 之前：

```text
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code 尝试将其解析为 JSON 但失败。要解决此问题，请将 echo 语句包装在 shell 配置文件中，以便它们仅在交互式 shell 中运行：

```bash
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

`$-` 变量包含 shell 标志，`i` 表示交互式。挂钩在非交互式 shell 中运行，因此会跳过回显。

### 调试技巧

使用 `Ctrl+O` 切换详细模式以查看转录中的钩子输出，或运行 `claude --debug` 以获取完整的执行详细信息，包括匹配的钩子及其退出代码。

## 了解更多

* [Hooks 参考](./hooks)：完整事件架构、JSON 输出格式、异步钩子和 MCP 工具钩子
* [安全考虑](./hooks#security-considerations)：在共享或生产环境中部署钩子之前进行审查
* [Bash 命令验证器示例](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)：完整参考实现
