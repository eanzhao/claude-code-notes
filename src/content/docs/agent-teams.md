---
title: "编排 Claude Code 会话团队"
order: 21
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "通过共享任务、代理间消息传递和集中管理，协调多个 Claude Code 实例作为一个团队协同工作。"
sourceUrl: "https://code.claude.com/docs/en/agent-teams.md"
sourceTitle: "Orchestrate teams of Claude Code sessions"
tags: []
---
# 编排 Claude Code 会话团队

> 通过共享任务、代理间消息传递和集中管理，协调多个 Claude Code 实例作为一个团队协同工作。

**警告**

代理团队处于实验阶段，默认情况下处于禁用状态。通过将 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 添加到您的 [settings.json](./settings) 或环境来启用它们。代理团队在会话恢复、任务协调和关闭行为方面存在[已知限制](#limitations)。

代理团队可让您协调多个 Claude Code 实例的协同工作。一名会议担任团队领导，协调工作、分配任务、综合结果。团队成员独立工作，每个人都在自己的上下文窗口中，并直接相互沟通。

与在单个会话中运行并且只能向主代理报告的[子代理](./sub-agents)不同，您还可以直接与各个队友互动，而无需通过领导。

**注意**

代理团队需要 Claude Code v2.1.32 或更高版本。使用 `claude --version` 检查您的版本。

此页面涵盖：

* [何时使用代理团队](#when-to-use-agent-teams)，包括最佳用例以及它们与子代理的比较
* [组建队伍](#start-your-first-agent-team)
* [控制队友](#control-your-agent-team)，包括显示模式、任务分配、委托
* [并行工作的最佳实践](#best-practices)

## 何时使用代理团队

代理团队对于并行探索能增加实际价值的任务最为有效。有关完整场景，请参阅[用例示例](#use-case-examples)。最强大的用例是：

* **研究和审查**：多个队友可以同时调查问题的不同方面，然后分享和质疑彼此的发现
* **新模块或功能**：队友可以各自拥有一个单独的棋子，而无需互相踩踏
* **使用相互竞争的假设进行调试**：队友并行测试不同的理论并更快地得出答案
* **跨层协调**：跨越前端、后端和测试的更改，每个更改由不同的队友拥有

代理团队增加了协调开销，并且比单个会话使用更多的令牌。当队友可以独立操作时，他们的工作效果最佳。对于顺序任务、同一文件编辑或处理多个依赖项，单个会话或[子代理](./sub-agents) 更有效。

### 与子代理比较

代理团队和[子代理](./sub-agents) 都允许您并行工作，但它们的操作方式不同。根据您的员工是否需要相互沟通进行选择：

![比较子代理和代理团队架构的图表。子代理由主代理生成，执行工作并报告结果。代理团队通过共享任务列表进行协调，队友之间直接沟通。](https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-light.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=2f8db9b4f3705dd3ab931fbe2d96e42a)![比较子代理和代理团队架构的图表。子代理由主代理生成，执行工作并报告结果。代理团队通过共享任务列表进行协调，队友之间直接沟通。](https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-dark.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=d573a037540f2ada6a9ae7d8285b46fd)
|                   |子代理 |代理团队|
| :---------------- | :------------------------------------------------------------ | :-------------------------------------------------- |
| **背景** |自己的上下文窗口；结果返回给调用者|自己的上下文窗口；完全独立|
| **通讯** |仅将结果报告给主要代理 |队友直接互相留言 |
| **协调** |主代理管理所有工作 |具有自我协调功能的共享任务列表 |
| **最适合** |只注重结果的重点任务 |需要讨论和协作的复杂工作 |
| **代币成本** |下：结果总结回到主要背景|更高：每个队友都是一个单独的 Claude 实例 |

当您需要快速、专注的工作人员进行汇报时，请使用子代理。当队友需要分享发现、互相挑战和自行协调时，请使用代理团队。

## 启用代理团队

默认情况下禁用代理团队。通过在 shell 环境中或通过 [settings.json](./settings) 将 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 环境变量设置为 `1` 来启用它们：

```json settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 组建你的第一个代理团队

启用代理团队后，告诉 Claude 创建代理团队并用自然语言描述您想要的任务和团队结构。 Claude 创建团队、生成队友并根据您的提示协调工作。

这个例子效果很好，因为三个角色是独立的，可以探索问题而无需互相等待：

```text
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

从那里，Claude 创建一个具有[共享任务列表](./interactive-mode#task-list) 的团队，为每个视角生成队友，让他们探索问题，综合发现结果，并在完成后尝试[清理团队](#clean-up-the-team)。

领导者的终端列出了所有队友以及他们正在做什么。使用 Shift+Down 循环选择队友并直接向他们发送消息。在最后一个队友之后，按 Shift+Down 重新回到领先位置。

如果您希望每个队友都在自己的分割窗格中，请参阅[选择显示模式](#choose-a-display-mode)。

## 控制你的代理团队

用自然语言告诉领导您想要什么。它根据您的指示处理团队协调、任务分配和委派。

### 选择显示模式

代理团队支持两种显示模式：

* **进程内**：所有队友都在您的主终端内运行。使用 Shift+Down 循环选择队友并直接输入消息给他们。适用于任何终端，无需额外设置。
* **分割窗格**：每个队友都有自己的窗格。您可以立即查看每个人的输出，然后单击窗格直接进行交互。需要 tmux 或 iTerm2。

**注意**`tmux` 在某些操作系统上存在已知限制，并且传统上在 macOS 上运行效果最佳。建议在 iTerm2 中使用 `tmux -CC` 进入 `tmux`。

默认值为 `"auto"`，如果您已经在 tmux 会话中运行，则它使用分割窗格，否则在进程内运行。 `"tmux"` 设置启用分割窗格模式，并根据您的终端自动检测是使用 tmux 还是 iTerm2。要覆盖，请在 [settings.json](./settings) 中设置 `teammateMode`：

```json
{
  "teammateMode": "in-process"
}
```

要强制单个会话使用进程内模式，请将其作为标志传递：

```bash
claude --teammate-mode in-process
```

分割窗格模式需要 [tmux](https://github.com/tmux/tmux/wiki) 或带有 [`it2` CLI](https://github.com/mkusaka/it2) 的 iTerm2。手动安装：

* **tmux**：通过系统的包管理器安装。请参阅 [tmux wiki](https://github.com/tmux/tmux/wiki/Installing) 了解特定于平台的说明。
* **iTerm2**：安装 [`it2` CLI](https://github.com/mkusaka/it2)，然后在 **iTerm2 → 设置 → 常规 → Magic → 启用 Python API** 中启用 Python API。

### 指定队友和模型

Claude 根据您的任务决定生成的队友数量，或者您可以准确指定您想要的数量：

```text
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### 需要队友批准计划

对于复杂或有风险的任务，您可以要求团队成员在实施之前进行计划。队友在只读计划模式下工作，直到领导批准他们的方法：

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

当团队成员完成计划时，它会向主管发送计划批准请求。领导审查该计划并批准或拒绝并提供反馈。如果被拒绝，团队成员将保持计划模式，根据反馈进行修改，然后重新提交。一旦获得批准，队友就会退出计划模式并开始实施。

领导自主做出批准决定。为了影响领导的判断，请在提示中给出标准，例如“仅批准包含测试覆盖范围的计划”或“拒绝修改数据库架构的计划”。

### 直接与队友交谈

每个队友都是一个完整、独立的 Claude Code 会话。您可以直接向任何队友发送消息，以提供更多说明、提出后续问题或重新引导他们的方法。

* **进程内模式**：使用 Shift+Down 循环选择队友，然后键入向他们发送消息。按 Enter 键查看队友的会话，然后按 Esc 键中断他们当前的回合。按 Ctrl+T 切换任务列表。
* **分割窗格模式**：单击队友的窗格即可直接与其会话进行交互。每个队友都可以看到自己终端的完整视图。

### 分配和领取任务

共享任务列表协调整个团队的工作。领导者创建任务，队友完成任务。任务具有三种状态：待处理、进行中和已完成。任务还可以依赖于其他任务：具有未解决的依赖关系的挂起任务在这些依赖关系完成之前无法声明。

领导可以明确分配任务，或者队友可以自我声明：

* **领导分配**：告诉领导将哪个任务分配给哪个队友
* **自我领取**：完成一个任务后，队友自行接下一个未分配、未阻塞的任务当多个队友尝试同时领取同一任务时，任务领取使用文件锁定来防止出现竞争情况。

### 关闭队友

要优雅地结束队友的会话：

```text
Ask the researcher teammate to shut down
```

潜在客户发送关闭请求。队友可以批准、优雅地退出，或者拒绝并给出解释。

### 清理团队

完成后，请领导清理：

```text
Clean up the team
```

这会删除共享的团队资源。当主导运行清理时，它会检查活跃的队友，如果有仍在运行的队友，则会失败，因此首先将其关闭。

**警告**

始终使用铅进行清理。队友不应该运行清理，因为他们的团队上下文可能无法正确解析，可能会使资源处于不一致的状态。

### 用钩子强化质量门

当队友完成工作或任务完成时，使用 [hooks](./hooks) 强制执行规则：

* [`TeammateIdle`](./hooks#teammateidle)：当队友即将空闲时运行。使用代码 2 退出以发送反馈并让队友继续工作。
* [`TaskCompleted`](./hooks#taskcompleted)：在任务标记为完成时运行。使用代码 2 退出以阻止完成并发送反馈。

## 代理团队如何工作

本节介绍代理团队背后的架构和机制。如果您想开始使用它们，请参阅上面的[控制您的代理团队](#control-your-agent-team)。

### Claude 如何启动代理团队

代理团队有两种启动方式：

* **您请求团队**：为 Claude 提供一项受益于并行工作的任务，并明确请求代理团队。 Claude 根据您的指示创建一个。
* **Claude 建议组建团队**：如果 Claude 确定您的任务将从并行工作中受益，它可能会建议创建一个团队。您在继续之前确认。

在这两种情况下，您都可以掌控一切。未经您的批准，Claude 不会创建团队。

### 架构

代理团队由以下人员组成：

|组件|角色 |
| :------------ | :---------------------------------------------------------------------------------------- |
| **团队领导** | Claude Code 主要会话，用于创建团队、生成队友并协调工作 |
| **队友** |单独的 Claude Code 实例，每个实例都处理分配的任务 |
| **任务清单** |队友领取并完成的工作项目共享列表 |
| **邮箱** |用于代理之间通信的消息系统|

有关显示配置选项，请参阅[选择显示模式](#choose-a-display-mode)。队友消息会自动到达领导。

系统自动管理任务依赖性。当队友完成其他任务所依赖的任务时，阻塞的任务会解锁，无需人工干预。

团队和任务存储在本地：

* **团队配置**：`~/.claude/teams/{team-name}/config.json`
* **任务列表**：`~/.claude/tasks/{team-name}/`

团队配置包含一个 `members` 数组，其中包含每个队友的姓名、代理 ID 和代理类型。队友可以阅读此文件来发现其他团队成员。

### 权限队友从领导的权限设置开始。如果领先者使用 `--dangerously-skip-permissions` 运行，则所有队友也会这样做。生成后，您可以更改单个队友模式，但无法在生成时设置每个队友模式。

### 背景和沟通

每个队友都有自己的上下文窗口。生成后，队友会加载与常规会话相同的项目上下文：CLAUDE.md、MCP 服务器和技能。它还会收到来自主角的生成提示。线索的对话历史记录不会保留。

**队友如何分享信息：**

* **自动消息传递**：当队友发送消息时，消息会自动传递给收件人。潜在客户不需要轮询更新。
* **空闲通知**：当队友完成并停止时，他们会自动通知领导。
* **共享任务列表**：所有代理都可以查看任务状态并声明可用的工作。

**队友消息：**

* **消息**：向一位特定的队友发送消息
* **广播**：同时发送给所有队友。请谨慎使用，因为成本随团队规模而变化。

### 代币使用

代理团队使用的代币比单个会话要多得多。每个队友都有自己的上下文窗口，令牌的使用量随着活跃队友的数量而变化。对于研究、审查和新功能工作，额外的代币通常是值得的。对于日常任务，单次会话更具成本效益。请参阅[代理团队令牌成本](./costs#agent-team-token-costs) 了解使用指南。

## 用例示例

这些示例展示了代理团队如何处理并行探索增加价值的任务。

### 运行并行代码审查

单个审阅者往往一次倾向于一种类型的问题。将审查标准分成独立的领域意味着安全性、性能和测试覆盖率都会同时得到彻底的关注。该提示为每个队友分配了一个不同的镜头，这样他们就不会重叠：

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

每个审阅者都使用相同的 PR，但应用不同的过滤器。领导者在完成后综合了所有三个人的发现。

### 用相互竞争的假设进行调查

当根本原因不清楚时，单一代理人往往会找到一个合理的解释并停止寻找。提示通过让队友明确地对抗来解决这个问题：每个人的工作不仅是研究自己的理论，而且挑战其他人的理论。

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

辩论结构是这里的关键机制。序贯研究会受到锚定的影响：一旦探索了一种理论，后续的研究就会偏向于它。

由于多名独立调查人员积极试图相互反驳，幸存下来的理论更有可能是真正的根本原因。

## 最佳实践

### 给队友足够的背景信息

队友会自动加载项目上下文，包括 CLAUDE.md、MCP 服务器和技能，但他们不会继承领导的对话历史记录。有关详细信息，请参阅[上下文和通信](#context-and-communication)。在生成提示中包含特定于任务的详细信息：

```text
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### 选择合适的团队规模

队友数量没有硬性限制，但有实际限制：* **令牌成本线性扩展**：每个队友都有自己的上下文窗口并独立消耗令牌。有关详细信息，请参阅[代理团队代币成本](./costs#agent-team-token-costs)。
* **协调开销增加**：更多的队友意味着更多的沟通、任务协调和潜在的冲突
* **收益递减**：超过某一点，额外的队友不会按比例加快工作速度

对于大多数工作流程，从 3-5 名队友开始。这平衡了并行工作与可管理的协调。本指南中的示例使用 3-5 名队友，因为该范围适用于不同的任务类型。

每个队友有 5-6 个[任务](./agent-teams#architecture)，可以让每个人保持高效，而无需过多的上下文切换。如果您有 15 项独立任务，那么 3 名队友是一个很好的起点。

只有当工作真正受益于让队友同时工作时，才能扩大规模。三个专注的队友往往比五个分散的队友表现更好。

### 适当调整任务大小

* **太小**：协调开销超过收益
* **太大**：队友在没有签到的情况下工作时间太长，增加了浪费精力的风险
* **恰到好处**：独立的单元可以产生清晰的可交付成果，例如功能、测试文件或评论

**提示**

领导者将工作分解为任务并自动将其分配给队友。如果它没有创建足够的任务，请要求它将工作分成更小的部分。每个队友分配 5-6 个任务可以保持每个人的工作效率，并在有人陷入困境时让领导重新分配工作。

### 等待队友完成

有时，领导者会开始自己执行任务，而不是等待队友。如果您注意到这一点：

```text
Wait for your teammates to complete their tasks before proceeding
```

### 从研究和回顾开始

如果您是代理团队的新手，请从具有明确边界且不需要编写代码的任务开始：审查 PR、研究库或调查错误。这些任务显示了并行探索的价值，而没有并行实施带来的协调挑战。

### 避免文件冲突

两个队友编辑同一文件会导致覆盖。打破工作，让每个团队成员拥有一组不同的文件。

### 监控和引导

检查团队成员的进度，重新调整不起作用的方法，并综合发现的结果。让团队在无人值守的情况下运行太长时间会增加浪费精力的风险。

## 故障排除

### 队友没有出现

如果您要求 Claude 创建团队后没有出现队友：

* 在进程内模式下，队友可能已经在运行但不可见。按 Shift+向下键可循环选择活跃的队友。
* 检查您交给 Claude 的任务是否足够复杂，足以保证组建一个团队。 Claude根据任务决定是否生成队友。
* 如果您明确请求分割窗格，请确保 tmux 已安装并在您的 PATH 中可用：
  ```bash 
  which tmux
  ```
* 对于 iTerm2，验证已安装 `it2` CLI 并在 iTerm2 首选项中启用 Python API。

### 权限提示太多队友的许可请求会向上浮到领先位置，这可能会产生摩擦。在生成队友之前，在[权限设置](./permissions)中预先批准常用操作，以减少干扰。

### 队友因错误而停止

队友可能会在遇到错误后停止而不是恢复。在进程内模式下使用 Shift+Down 或在拆分模式下单击窗格来检查其输出，然后：

* 直接给他们额外的指示
* 产生一个替代队友来继续工作

### Lead 在工作完成之前关闭

在所有任务实际完成之前，领导者可能会决定团队已完成。如果发生这种情况，请告诉它继续前进。如果领导开始做工作而不是委派任务，您还可以告诉领导等待队友完成后再继续。

### 孤立的 tmux 会话

如果 tmux 会话在团队结束后仍然存在，则可能尚未完全清理。列出会话并杀死团队创建的会话：

```bash
tmux ls
tmux kill-session -t <session-name>
```

## 限制

代理团队是实验性的。当前需要注意的限制：

* **无法恢复与进程内队友的会话**：`/resume` 和 `/rewind` 不会恢复进程内队友。恢复会话后，领导可能会尝试向不再存在的队友发送消息。如果发生这种情况，请告诉领导派出新的队友。
* **任务状态可能滞后**：队友有时无法将任务标记为已完成，这会阻止相关任务。如果任务出现卡顿，请检查工作是否实际完成并手动更新任务状态或告诉领导推动队友。
* **关闭可能会很慢**：队友在关闭之前完成当前的请求或工具调用，这可能需要一些时间。
* **每个会话一个团队**：领导一次只能管理一个团队。在开始新团队之前清理当前团队。
* **无嵌套团队**：队友无法生成自己的团队或队友。只有领导才能管理团队。
* **领导是固定的**：创建团队的会话是其生命周期的领导。您无法提升队友领导或转移领导权。
* **在生成时设置的权限**：所有队友都以领导者的权限模式开始。您可以在生成后更改单个队友模式，但无法在生成时设置每个队友模式。
* **分割窗格需要 tmux 或 iTerm2**：默认的进程内模式适用于任何终端。 VS Code 的集成终端、Windows 终端或 Ghostty 不支持分割窗格模式。

**提示**

**`CLAUDE.md` 正常工作**：队友从其工作目录读取 `CLAUDE.md` 文件。使用它为所有团队成员提供特定于项目的指导。

## 后续步骤

探索并行工作和授权的相关方法：

* **轻量级委托**：[子代理](./sub-agents) 生成辅助代理，用于在会话中进行研究或验证，更适合不需要代理间协调的任务
* **手动并行会话**：[Git worktrees](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 让您可以自己运行多个 Claude Code 会话，无需自动团队协调
* **比较方法**：请参阅[子代理与代理团队](./features-overview#compare-similar-features) 比较以进行并排细分
