---
title: "常见工作流程"
order: 7
section: "core-concepts"
sectionLabel: "核心概念"
sectionOrder: 2
summary: "使用 Claude Code 探索代码库、修复错误、重构、测试和其他日常任务的分步指南。"
sourceUrl: "https://code.claude.com/docs/en/common-workflows.md"
sourceTitle: "Common workflows"
tags: []
---
# 常用工作流程

> 使用 Claude Code 探索代码库、修复错误、重构、测试和其他日常任务的分步指南。

本页面涵盖了日常开发的实用工作流程：探索不熟悉的代码、调试、重构、编写测试、创建 PR 和管理会话。每个部分都包含示例提示，您可以根据自己的项目进行调整。有关更高级别的模式和提示，请参阅[最佳实践](./best-practices)。

## 了解新的代码库

### 快速了解代码库

假设您刚刚加入一个新项目，需要快速了解其结构。

### 导航到项目根目录

```bash
cd /path/to/project 
```

  
### 启动 Claude Code

```bash
claude 
```

  
### 请求高级概述

```text
give me an overview of this codebase
```

  
### 深入研究特定组件

```text
explain the main architecture patterns used here
```

```text
what are the key data models?
```

```text
how is authentication handled?
```

**提示**

温馨提示：

* 从广泛的问题开始，然后缩小到特定领域
* 询问项目中使用的编码约定和模式
* 索取项目特定术语表

### 查找相关代码

假设您需要查找与特定特性或功能相关的代码。

### 请Claude查找相关文件

```text
find the files that handle user authentication
```

  
### 获取有关组件如何交互的上下文

```text
how do these authentication files work together?
```

  
### 理解执行流程

```text
trace the login process from front-end to database
```

**提示**

温馨提示：

* 具体说明您要寻找的内容
* 使用项目中的领域语言
* 为您的语言安装一个[代码智能插件](./discover-plugins#code-intelligence)，为Claude提供精确的“转到定义”和“查找引用”导航

***

## 高效修复bug

假设您遇到错误消息并需要查找并修复其来源。

### 与 Claude 共享错误

```text
I'm seeing an error when I run npm test
```

  
### 寻求修复建议

```text
suggest a few ways to fix the @ts-ignore in user.ts
```

  
### 应用修复

```text
update user.ts to add the null check you suggested
```

**提示**

温馨提示：

* 告诉 Claude 重现问题的命令并获取堆栈跟踪
* 提及重现错误的任何步骤
* 让 Claude 知道错误是间歇性的还是持续的

***

## 重构代码

假设您需要更新旧代码以使用现代模式和实践。

### 识别遗留代码以进行重构

```text
find deprecated API usage in our codebase
```

  
### 获取重构建议

```text
suggest how to refactor utils.js to use modern JavaScript features
```

  
### 安全地应用更改

```text
refactor utils.js to use ES2024 features while maintaining the same behavior
```

  
### 验证重构

```text
run tests for the refactored code
```

**提示**

温馨提示：

* 请 Claude 解释现代方法的好处
* 请求更改在需要时保持向后兼容性
* 以小的、可测试的增量进行重构

***

## 使用专门的子代理

假设您想使用专门的 AI 子代理来更有效地处理特定任务。

### 查看可用的子代理

```text
/agents
```

这会显示所有可用的子代理并允许您创建新的子代理。

  
### 自动使用子代理

Claude Code 自动将适当的任务委派给专门的子代理：

```text
review my recent code changes for security issues
```

```text
run all tests and fix any failures
```

  
### 显式请求特定的子代理

```text
use the code-reviewer subagent to check the auth module
```

```text
have the debugger subagent investigate why users can't log in
```

  
### 为您的工作流程创建自定义子代理

```text
/agents
```

然后选择“Create New subagent”并按照提示进行定义：* 描述子代理用途的唯一标识符（例如，`code-reviewer`、`api-designer`）。
* Claude何时应使用该剂
* 它可以访问哪些工具
* 描述座席角色和行为的系统提示

**提示**

温馨提示：

* 在 `.claude/agents/` 中创建项目特定的子代理以供团队共享
* 使用描述性 `description` 字段启用自动委派
* 限制工具访问每个子代理实际需要的内容
* 查看[子代理文档](./sub-agents)以获取详细示例

***

## 使用 Plan Mode 进行安全代码分析

Plan Mode 指示 Claude 通过使用只读操作分析代码库来创建计划，非常适合探索代码库、规划复杂的更改或安全地审查代码。在 Plan Mode 中，Claude 使用 [`AskUserQuestion`](./tools-reference) 在提出计划之前收集要求并阐明您的目标。

### 何时使用 Plan Mode

* **多步骤实施**：当您的功能需要对多个文件进行编辑时
* **代码探索**：当您想在更改任何内容之前彻底研究代码库时
* **交互式开发**：当你想用Claude迭代方向时

### 如何使用Plan Mode

**在会话期间打开 Plan Mode**

您可以在会话期间使用 **Shift+Tab** 切换到 Plan Mode 以循环切换权限模式。

如果您处于正常模式，**Shift+Tab** 首先切换到自动接受模式，由终端底部的 `⏵⏵ accept edits on` 指示。随后的 **Shift+Tab** 将切换到 Plan Mode，由 `⏸ plan mode on` 指示。

**在 Plan Mode 中启动新会话**

要在 Plan Mode 中启动新会话，请使用 `--permission-mode plan` 标志：

```bash
claude --permission-mode plan
```

**在 Plan Mode 中运行“无头”查询**

您还可以直接使用 `-p` 在 Plan Mode 中运行查询（即在 [“无头模式”](./headless) 中）：

```bash
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### 示例：规划复杂的重构

```bash
claude --permission-mode plan
```

```text
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude 分析当前的实施情况并制定全面的计划。完善后续行动：

```text
What about backward compatibility?
```

```text
How should we handle database migration?
```

**提示**

按 `Ctrl+G` 在默认文本编辑器中打开计划，您可以在 Claude 继续之前直接对其进行编辑。

当您接受计划时，Claude 会自动根据计划内容命名会话。该名称显示在提示栏和会话选择器中。如果您已使用 `--name` 或 `/rename` 设置名称，接受计划不会覆盖它。

### 将 Plan Mode 配置为默认值

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

有关更多配置选项，请参阅[设置文档](./settings#available-settings)。

***

## 处理测试

假设您需要为未覆盖的代码添加测试。

### 识别未经测试的代码

```text
find functions in NotificationsService.swift that are not covered by tests
```

  
### 生成测试脚手架

```text
add tests for the notification service
```

  
### 添加有意义的测试用例

```text
add test cases for edge conditions in the notification service
```

  
### 运行并验证测试

```text
run the new tests and fix any failures
```

Claude 可以生成遵循项目现有模式和约定的测试。当要求进行测试时，请具体说明您想要验证的行为。 Claude 检查现有的测试文件以匹配已在使用的样式、框架和断言模式。如需全面覆盖，请询问 Claude 以确定您可能错过的边缘情况。 Claude 可以分析您的代码路径，并建议对错误条件、边界值和容易忽视的意外输入进行测试。

***

## 创建拉取请求

您可以通过直接询问 Claude（“为我的更改创建 pr”）来创建拉取请求，或指导 Claude 逐步完成：

### 总结一下你的改变

```text
summarize the changes I've made to the authentication module
```

  
### 生成拉取请求

```text
create a pr
```

  
### 审查和完善

```text
enhance the PR description with more context about the security improvements
```

当您使用 `gh pr create` 创建 PR 时，会话会自动链接到该 PR。您可以稍后使用 `claude --from-pr <number>` 恢复它。

**提示**

在提交之前查看 Claude 生成的 PR，并要求 Claude 突出显示潜在风险或注意事项。

## 处理文档

假设您需要添加或更新代码的文档。

### 识别未记录的代码

```text
find functions without proper JSDoc comments in the auth module
```

  
### 生成文档

```text
add JSDoc comments to the undocumented functions in auth.js
```

  
### 回顾并加强

```text
improve the generated documentation with more context and examples
```

  
### 验证文档

```text
check if the documentation follows our project standards
```

**提示**

温馨提示：

* 指定您想要的文档样式（JSDoc、文档字符串等）
* 询问文档中的示例
* 请求公共 API、接口和复杂逻辑的文档

***

## 处理图像

假设您需要处理代码库中的图像，并且需要 Claude 帮助分析图像内容。

### 在对话中添加图像

您可以使用以下任一方法：

1. 将图像拖放到 Claude Code 窗口中
2. 复制图像并使用 ctrl+v 将其粘贴到 CLI 中（请勿使用 cmd+v）
3. 提供 Claude 的图像路径。例如，“分析此图像：/path/to/your/image.png”

  
### 请 Claude 分析图像

```text
What does this image show?
```

```text
Describe the UI elements in this screenshot
```

```text
Are there any problematic elements in this diagram?
```

  
### 使用图像作为上下文

```text
Here's a screenshot of the error. What's causing it?
```

```text
This is our current database schema. How should we modify it for the new feature?
```

  
### 从视觉内容中获取代码建议

```text
Generate CSS to match this design mockup
```

```text
What HTML structure would recreate this component?
```

**提示**

温馨提示：

* 当文字描述不清楚或繁琐时使用图像
* 包括错误屏幕截图、UI 设计或图表以获得更好的上下文
* 您可以在对话中处理多个图像
* 图像分析适用于图表、屏幕截图、模型等
* 当 Claude 引用图像（例如 `[Image #1]`）、`Cmd+Click` (Mac) 或 `Ctrl+Click` (Windows/Linux) 时，用于在默认查看器中打开图像的链接

***

## 参考文件和目录

使用 @ 快速包含文件或目录，无需等待 Claude 读取它们。

### 引用单个文件

```text
Explain the logic in @src/utils/auth.js
```

这包括对话中文件的完整内容。

  
### 引用目录

```text
What's the structure of @src/components?
```

这提供了包含文件信息的目录列表。

  
###参考MCP资源

```text
Show me the data from @github:repos/owner/repo/issues
```

这使用 @server:resource 格式从连接的 MCP 服务器获取数据。有关详细信息，请参阅 [MCP 资源](./mcp#use-mcp-resources)。

**提示**

温馨提示：

* 文件路径可以是相对路径或绝对路径
* @文件引用 将文件目录和父目录中的 `CLAUDE.md` 添加到上下文
* 目录引用显示文件列表，而不是内容
* 您可以在一条消息中引用多个文件（例如，“@file1.js 和 @file2.js”）

***## 使用扩展思维（思维模式）

【扩展思维】(https://platform.claude.com/docs/en/build-with-claude/extended-thinking)默认启用，为Claude提供空间，让其在响应之前逐步推理复杂的问题。此推理在详细模式下可见，您可以使用 `Ctrl+O` 来打开该模式。

此外，Opus 4.6 和 Sonnet 4.6 支持自适应推理：该模型不是固定的思维令牌预算，而是根据您的[努力程度](./model-config#adjust-effort-level) 设置动态分配思维。扩展思维和自适应推理相结合，让您可以控制 Claude 在做出回应之前推理的深度。

扩展思维对于复杂的架构决策、具有挑战性的错误、多步骤实施规划以及评估不同方法之间的权衡特别有价值。

**注意**

“思考”、“认真思考”和“多思考”等短语被解释为常规提示指令，不会分配思考标记。

### 配置思维模式

默认情况下，思考处于启用状态，但您可以调整或禁用它。

|范围 |如何配置 |详情 |
| ------------------------ | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **努力程度** |运行 `/effort`，在 `/model` 中进行调整，或设置 [`CLAUDE_CODE_EFFORT_LEVEL`](./env-vars) |控制 Opus 4.6 和 Sonnet 4.6 的思维深度。请参阅[调整努力程度](./model-config#adjust-effort-level) |
| **`ultrathink` 关键字** |在提示中的任何位置包含“ultrathink”|将 Opus 4.6 和 Sonnet 4.6 上的回合的努力设置为高。对于需要深入推理而不永久改变您的努力设置的一次性任务很有用 |
| **切换快捷方式** |按 `Option+T` (macOS) 或 `Alt+T` (Windows/Linux) |打开/关闭当前会话的思考（所有模型）。可能需要[终端配置](./terminal-config) 才能启用选项快捷键 |
| **全局默认** |使用`/config`切换思维模式 |设置所有项目（所有模型）的默认值。
在 `~/.claude/settings.json` 中另存为 `alwaysThinkingEnabled` |
| **限制代币预算** |设置 [`MAX_THINKING_TOKENS`](./env-vars) 环境变量 |将思考预算限制在特定数量的代币内。在 Opus 4.6 和 Sonnet 4.6 上，仅 `0` 适用，除非禁用自适应推理。示例：`export MAX_THINKING_TOKENS=10000` |要查看 Claude 的思维过程，请按 `Ctrl+O` 切换详细模式，并查看显示为灰色斜体文本的内部推理。

### 扩展思维如何发挥作用

扩展思维控制 Claude 在做出响应之前执行的内部推理程度。更多的思考提供了更多的空间来探索解决方案、分析边缘案例和自我纠正错误。

**在 Opus 4.6 和 Sonnet 4.6** 中，思维使用自适应推理：模型根据您选择的[努力程度](./model-config#adjust-effort-level) 动态分配思维标记。这是调整速度和推理深度之间的权衡的推荐方法。

**对于旧模型**，思考使用从输出分配中提取的固定代币预算。预算因型号而异；请参阅 [`MAX_THINKING_TOKENS`](./env-vars) 了解每个型号的天花板。您可以使用该环境变量限制预算，或者通过 `/config` 或 `Option+T`/`Alt+T` 切换完全禁用思考。

在 Opus 4.6 和 Sonnet 4.6 上，[自适应推理](./model-config#adjust-effort-level) 控制思维深度，因此 `MAX_THINKING_TOKENS` 仅在设置为 `0` 以禁用思维时适用，或者当 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` 将这些模型恢复为固定预算时适用。请参阅[环境变量](./env-vars)。

**警告**

即使 Claude 4 模型显示汇总思维，您仍需要为使用的所有思维标记付费

***

## 恢复之前的对话

启动 Claude Code 时，您可以恢复之前的会话：

* `claude --continue` 继续当前目录中的最近一次对话
* `claude --resume` 打开对话选择器或按姓名继续
* `claude --from-pr 123` 恢复链接到特定拉取请求的会话

从活动会话内部，使用 `/resume` 切换到不同的对话。

会话按项目目录存储。 `/resume` 选择器显示来自同一 git 存储库的会话，包括工作树。

### 为你的会话命名

为会话提供描述性名称以便稍后找到它们。这是处理多个任务或功能时的最佳实践。

### 命名会话

在启动时使用 `-n` 命名会话：

```bash
claude -n auth-refactor
```

或者在会话期间使用 `/rename`，这也会在提示栏上显示名称：

```text
/rename auth-refactor
```

您还可以从选择器中重命名任何会话：运行 `/resume`，导航到会话，然后按 `R`。

  
### 稍后按姓名恢复

从命令行：

```bash
claude --resume auth-refactor
```

或者从活动会话内部：

```text
/resume auth-refactor
```

### 使用会话选择器

`/resume` 命令（或不带参数的 `claude --resume`）打开具有以下功能的交互式会话选择器：

**选择器中的键盘快捷键：**|快捷方式 |行动|
| :-------- | :------------------------------------------------ |
| `↑` / `↓` |在会话之间导航 |
| `→` / `←` |展开或折叠分组会话 |
| `Enter` |选择并恢复突出显示的会话 |
| `P` |预览会议内容 |
| `R` |重命名突出显示的会话 |
| `/` |搜索以过滤会话 |
| `A` |在当前目录和所有项目之间切换 |
| `B` |从当前 git 分支过滤会话 |
| `Esc` |退出选择器或搜索模式 |

**会议组织：**

选择器显示带有有用元数据的会话：

* 会话名称或初始提示
* 自上次活动以来经过的时间
* 消息数
* Git 分支（如果适用）

分叉会话（使用 `/branch`、`/rewind` 或 `--fork-session` 创建）在其根会话下分组在一起，以便更轻松地查找相关对话。

**提示**

温馨提示：

* **尽早命名会议**：开始处理不同任务时使用 `/rename`：找到“支付集成”比稍后“解释此功能”要容易得多
* 使用 `--continue` 快速访问当前目录中的最近对话
* 当您知道需要哪个会话时，请使用 `--resume session-name`
* 需要浏览选择时使用`--resume`（无名称）
* 对于脚本，使用 `claude --continue --print "prompt"` 以非交互模式恢复
* 在选择器中按 `P` 可在恢复之前预览会话
* 恢复的对话以与原始对话相同的型号和配置开始

工作原理：

1. **对话存储**：所有对话及其完整消息历史记录都会自动保存在本地
2. **消息反序列化**：恢复时，恢复整个消息历史记录以维护上下文
3. **工具状态**：保留上次对话的工具使用情况和结果
4. **上下文恢复**：对话恢复，之前的所有上下文都保持不变

***

## 使用 Git 工作树运行并行 Claude Code 会话

当同时处理多个任务时，您需要每个 Claude 会话都有自己的代码库副本，以便更改不会发生冲突。 Git 工作树通过创建单独的工作目录来解决这个问题，每个工作目录都有自己的文件和分支，同时共享相同的存储库历史记录和远程连接。这意味着您可以让 Claude 在一个工作树中处理某个功能，同时修复另一个工作树中的错误，而任一会话不会干扰另一个工作树。

使用 `--worktree` (`-w`) 标志创建独立的工作树并在其中启动 Claude。您传递的值将成为工作树目录名称和分支名称：

```bash
# Start Claude in a worktree named "feature-auth"
# Creates .claude/worktrees/feature-auth/ with a new branch
claude --worktree feature-auth

# Start another session in a separate worktree
claude --worktree bugfix-123
```

如果省略名称，Claude 会自动生成一个随机名称：

```bash
# Auto-generates a name like "bright-running-fox"
claude --worktree
```

工作树在 `<repo>/.claude/worktrees/<name>` 处创建，并从默认远程分支分支。工作树分支名为 `worktree-<name>`。您还可以要求 Claude 在会话期间“在工作树中工作”或“启动工作树”，它将自动创建一个。

### 子代理工作树

子代理还可以使用工作树隔离来并行工作而不会发生冲突。要求 Claude“为您的代理使用工作树”或通过将 `isolation: worktree` 添加到代理的 frontmatter 来在 [自定义子代理](./sub-agents#supported-frontmatter-fields) 中配置它。每个子代理都有自己的工作树，当子代理完成且没有任何更改时，该工作树会自动清理。

### 工作树清理

当您退出工作树会话时，Claude 根据您是否进行了更改来处理清理：

* **无变化**：工作树及其分支将自动删除
* **存在更改或提交**：Claude 提示您保留或删除工作树。保留会保留目录和分支，以便您稍后可以返回。删除会删除工作树目录及其分支，丢弃所有未提交的更改和提交

要清理 Claude 会话之外的工作树，请使用[手动工作树管理](#manage-worktrees-manually)。

**提示**

将 `.claude/worktrees/` 添加到 `.gitignore`，以防止工作树内容在主存储库中显示为未跟踪文件。

### 手动管理工作树

要更好地控制工作树位置和分支配置，请直接使用 Git 创建工作树。当您需要签出特定的现有分支或将工作树放置在存储库之外时，这非常有用。

```bash
# Create a worktree with a new branch
git worktree add ../project-feature-a -b feature-a

# Create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123

# Start Claude in the worktree
cd ../project-feature-a && claude

# Clean up when done
git worktree list
git worktree remove ../project-feature-a
```

请参阅[官方 Git 工作树文档](https://git-scm.com/docs/git-worktree) 了解更多信息。

**提示**

请记住根据项目的设置在每个新工作树中初始化您的开发环境。根据您的堆栈，这可能包括运行依赖项安装（`npm install`、`yarn`）、设置虚拟环境或遵循项目的标准设置过程。

### 非 git 版本控制

默认情况下，工作树隔离与 git 一起使用。对于 SVN、Perforce 或 Mercurial 等其他版本控制系统，请配置 [WorktreeCreate 和 WorktreeRemove 挂钩](./hooks#worktreecreate) 以提供自定义工作树创建和清理逻辑。配置后，当您使用 `--worktree` 时，这些挂钩将替换默认的 git 行为。

要自动协调具有共享任务和消息传递的并行会话，请参阅[代理团队](./agent-teams)。

***

## 当 Claude 需要您关注时收到通知

当您启动长时间运行的任务并切换到另一个窗口时，您可以设置桌面通知，以便您知道 Claude 何时完成或需要您的输入。这使用 `Notification` [挂钩事件](./hooks-guide#get-notified-when-claude-needs-input)，每当 Claude 等待许可、空闲并准备好新提示或完成身份验证时，该事件就会触发。

### 将挂钩添加到您的设置中

    打开 `~/.claude/settings.json` 并添加一个 `Notification` 挂钩来调用您平台的本机通知命令：

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

### Windows

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

    如果您的设置文件已有 `hooks` 密钥，请将 `Notification` 条目合并到其中而不是覆盖。您还可以要求 Claude 通过在 CLI 中描述您想要的内容来为您编写挂钩。

  
### 可选地缩小匹配器范围默认情况下，该钩子会在所有通知类型上触发。要仅针对特定事件触发，请将 `matcher` 字段设置为以下值之一：

|匹配器|何时触发 |
| :-------------------- | :---------------------------------------------------------- |
| `permission_prompt` | Claude 需要您批准工具使用 |
| `idle_prompt` | Claude 已完成并等待您的下一个提示 |
| `auth_success` |认证完成 |
| `elicitation_dialog` | Claude 正在问您一个问题 |

  
### 验证钩子

输入 `/hooks` 并选择 `Notification` 以确认出现挂钩。选择它会显示将运行的命令。要进行端到端测试，请要求 Claude 运行需要权限的命令并离开终端，或者要求 Claude 直接触发通知。

有关完整的事件架构和通知类型，请参阅[通知参考](./hooks#notification)。

***

## 使用 Claude 作为 unix 风格的实用程序

### 将 Claude 添加到您的验证过程中

假设您想使用 Claude Code 作为 linter 或代码审查器。

**将 Claude 添加到您的构建脚本中：**

```json
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

**提示**

温馨提示：

* 使用 Claude 在 CI/CD 管道中进行自动代码审查
* 自定义提示以检查与您的项目相关的特定问题
* 考虑为不同类型的验证创建多个脚本

### 管道输入，管道输出

假设您要将数据通过管道传输到 Claude，并以结构化格式取回数据。

**通过 Claude 传输数据：**

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

**提示**

温馨提示：

* 使用管道将Claude集成到现有的shell脚本中
* 与其他 Unix 工具结合使用，实现强大的工作流程
* 考虑使用 --output-format 进行结构化输出

### 控制输出格式

假设您需要 Claude 以特定格式输出，特别是在将 Claude Code 集成到脚本或其他工具中时。

### 使用文本格式（默认）

```bash
cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
```

这仅输出 Claude 的纯文本响应（默认行为）。

  
### 使用 JSON 格式

```bash
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
```

这会输出 JSON 消息数组，其中包含元数据，包括成本和持续时间。

  
### 使用流媒体 JSON 格式

```bash
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

当 Claude 处理请求时，这会实时输出一系列 JSON 对象。每条消息都是有效的 JSON 对象，但如果串联，整个输出就不是有效的 JSON。

**提示**

温馨提示：

* 使用 `--output-format text` 进行简单集成，您只需要 Claude 的响应
* 当您需要完整的对话日志时，请使用 `--output-format json`
* 使用`--output-format stream-json`实时输出每轮对话

***

## 向 Claude 询问其功能

Claude 具有对其文档的内置访问权限，并且可以回答有关其自身功能和限制的问题。

### 示例问题

```text
can Claude Code create pull requests?
```

```text
how does Claude Code handle permissions?
```

```text
what skills are available?
```

```text
how do I use MCP with Claude Code?
```

```text
how do I configure Claude Code for Amazon Bedrock?
```

```text
what are the limitations of Claude Code?
```

**注意**

Claude 为这些问题提供基于文档的答案。有关可执行示例和实践演示，请参阅上面的特定工作流程部分。

**提示**

温馨提示：* 无论您使用哪个版本，Claude 始终可以访问最新的 Claude Code 文档
* 提出具体问题以获得详细答案
* Claude 可以解释复杂的功能，例如 MCP 集成、企业配置和高级工作流程

***

## 后续步骤

### [最佳实践](/en/best-practices)

充分利用 Claude Code 的模式

  
### [Claude Code 的工作原理](/en/how-claude-code-works)

了解代理循环和上下文管理

  
### [扩展 Claude Code](/en/features-overview)

添加技能、挂钩、MCP、子代理和插件

  
### [参考实现](https://github.com/anthropics/claude-code/tree/main/.devcontainer)

克隆开发容器参考实现
