---
title: "Claude Code 的工作原理"
order: 4
section: "core-concepts"
sectionLabel: "核心概念"
sectionOrder: 2
summary: "了解代理循环、内置工具以及 Claude Code 如何与您的项目交互。"
sourceUrl: "https://code.claude.com/docs/en/how-claude-code-works.md"
sourceTitle: "How Claude Code works"
tags: []
---
# Claude Code 的工作原理

> 了解代理循环、内置工具，以及 Claude Code 如何与你的项目交互。

Claude Code 是一个运行在终端里的代理助手。它不只是写代码——它能帮你做任何命令行能做的事：写文档、跑构建、搜文件、查资料等等。

本指南介绍核心架构、内置功能和[高效使用的技巧](#work-effectively-with-claude-code)。分步操作指南请看[常见工作流程](./common-workflows)。skill、MCP、hook 等扩展功能请看[扩展 Claude Code](./features-overview)。

## 代理循环

当你给 Claude 分配任务时，它会经历三个阶段：**收集上下文**、**采取行动**和**验证结果**。这些阶段是交织在一起的。Claude 始终在使用工具——不管是搜索文件来理解代码、编辑文件来做更改，还是运行测试来检查结果。

![代理循环：您的提示导致 Claude 收集上下文、采取行动、验证结果并重复直到任务完成。您可以随时中断。](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38)

循环会根据你的需求自适应。问个代码库的问题可能只需要收集上下文；修 bug 则会反复经历所有三个阶段；重构可能需要大量验证。Claude 根据上一步学到的东西来决定下一步做什么，把数十个操作串联起来，一路调整方向。

你也是这个循环的一部分。你随时可以打断 Claude，把它引向不同的方向、提供额外的上下文，或者让它换个方法试试。Claude 自主工作，但始终响应你的输入。

代理循环由两个组件驱动：用于推理的[模型](#models)和用于执行的[工具](#tools)。Claude Code 充当 Claude 的**代理工具层**：它提供工具、上下文管理和执行环境，把语言模型变成一个有能力的编码代理。

### 模型

Claude Code 使用 Claude 模型来理解你的代码并推理任务。Claude 能读懂任何语言的代码，理解组件之间的关联，找出需要改什么才能达成你的目标。对于复杂任务，它会把工作拆分成步骤，执行这些步骤，并根据发现随时调整。

[多种模型](./model-config)提供不同的取舍。Sonnet 能很好地处理大多数编码任务。Opus 在复杂架构决策上有更强的推理能力。会话中可以用 `/model` 切换，或者启动时用 `claude --model <name>` 指定。

当本文说"Claude 选择"或"Claude 决定"时，指的是模型在进行推理。

### 工具

工具让 Claude Code 具有代理能力。没有工具时，Claude 只能用文本回复。有了工具，Claude 就能：读代码、编辑文件、运行命令、搜索网络、与外部服务交互。每次使用工具都会返回信息反馈到循环中，帮助 Claude 做出下一个决定。

内置工具大致分为五类，每类代表不同的能力。

| 类别 | Claude 能做什么 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **文件操作** | 读文件、编辑代码、创建新文件、重命名和重组 |
| **搜索** | 按模式查找文件、用正则搜索内容、探索代码库 |
| **执行** | 运行 shell 命令、启动服务器、跑测试、用 git |
| **网络** | 搜索网络、获取文档、查找错误信息 |
| **代码智能** | 编辑后查看类型错误和警告、跳转到定义、查找引用（需要[代码智能插件](./discover-plugins#code-intelligence)）|

以上是主要能力。Claude 还有用于创建 subagent、提问和其他编排任务的工具。完整列表见 [Claude 可用的工具](./tools-reference)。

Claude 根据你的提示以及沿途发现的信息来选择使用哪个工具。当你说"修复失败的测试"时，Claude 可能会：

1. 运行测试套件看哪些失败了
2. 读取错误输出
3. 搜索相关源文件
4. 阅读这些文件理解代码
5. 编辑文件修复问题
6. 再次运行测试验证修复

每次工具使用都给 Claude 提供新信息来指导下一步。这就是代理循环的运作方式。

**扩展基本功能：** 内置工具是基础。你可以用 [skill](./skills) 扩展 Claude 的知识，用 [MCP](./mcp) 连接外部服务，用 [hook](./hooks) 自动化工作流程，用 [subagent](./sub-agents) 分派任务。这些扩展在核心代理循环之上形成了一层。具体选择见[扩展 Claude Code](./features-overview)。

## Claude 能访问什么

本节重点介绍终端环境。Claude Code 也可以在 [VS Code](./vs-code)、[JetBrains IDE](./jetbrains) 等环境中运行。

当你在某个目录下运行 `claude` 时，Claude Code 可以访问：

* **你的项目。** 当前目录和子目录中的文件，以及经你许可的其他位置的文件。
* **你的终端。** 你能运行的任何命令：构建工具、git、包管理器、系统工具、脚本。你在命令行能做的，Claude 也能做。
* **你的 git 状态。** 当前分支、未提交的更改和最近的提交历史。
* **你的 [CLAUDE.md](./memory)。** 一个 Markdown 文件，你可以在里面写项目相关的指令、约定和上下文，Claude 每次会话都会读取。
* **[自动记忆](./memory#auto-memory)。** Claude 在工作过程中自动保存学到的东西，比如项目模式和你的偏好。MEMORY.md 的前 200 行会在每次会话开始时加载。
* **你配置的扩展。** [MCP 服务器](./mcp)用于外部服务，[skill](./skills) 用于工作流程，[subagent](./sub-agents) 用于分派任务，[Claude in Chrome](./chrome) 用于浏览器交互。

因为 Claude 能看到你的整个项目，所以它可以跨文件工作。当你让 Claude"修复认证 bug"时，它会搜索相关文件、读取多个文件理解上下文、协调编辑它们、运行测试验证修复，并按你的要求提交更改。这跟只看当前文件的内联代码助手完全不同。

## 环境和接口

无论你在哪里使用 Claude Code，上面说的代理循环、工具和功能都是一样的。变化的只是代码在哪里执行，以及你怎么跟它交互。

### 执行环境

Claude Code 在三种环境中运行，各有不同的取舍。

| 环境 | 代码在哪里运行 | 适用场景 |
| ------------------ | --------------------------------------- | ---------------------------------------------------------------------- |
| **本地** | 你的机器 | 默认。完全访问你的文件、工具和环境 |
| **云端** | Anthropic 管理的虚拟机 | 分派任务，处理本地没有的仓库 |
| **Remote Control** | 你的机器，由浏览器控制 | 用 Web UI，同时保持一切在本地 |

### 接口

你可以通过终端、[桌面应用](./desktop)、[IDE 扩展](https://code.claude.com/docs/en/ide-integrations)、[claude.ai/code](https://claude.ai/code)、[Remote Control](./remote-control)、[Slack](./slack) 和 [CI/CD 管道](./github-actions)使用 Claude Code。接口决定了你如何查看和操作 Claude，但底层的代理循环是一样的。完整列表见[到处使用 Claude Code](./overview#use-claude-code-everywhere)。

## 使用 session

Claude Code 会把你的对话保存在本地。每条消息、工具使用和结果都会被存储，支持[倒带](#undo-changes-with-checkpoints)、[恢复和分叉](#resume-or-fork-sessions) session。在 Claude 修改代码之前，它还会对受影响的文件做快照，方便你需要时恢复。

**session 是独立的。** 每个新 session 都以一个全新的上下文窗口开始，没有之前 session 的对话历史。Claude 可以通过[自动记忆](./memory#auto-memory)跨 session 持续学习，你也可以在 [CLAUDE.md](./memory) 中写入持久指令。

### 跨分支工作

每个 Claude Code 对话都是一个与当前目录关联的 session。恢复时，你只能看到该目录中的 session。

Claude 看到的是当前分支的文件。切换分支后，Claude 会看到新分支的文件，但对话历史不变。即使切换了分支，Claude 也记得你们之前讨论的内容。

由于 session 和目录关联，你可以用 [git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 运行并行 Claude session，worktree 会为各个分支创建独立目录。

### 恢复或分叉 session

用 `claude --continue` 或 `claude --resume` 恢复 session 时，你会使用同一个 session ID 从上次中断的地方继续。新消息会追加到已有对话中。完整的对话历史会恢复，但 session 级别的权限不会恢复，需要重新批准。

![Session 连续性：resume 继续同一 session，fork 用新 ID 创建分支。](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30)

如果你想分支出去尝试不同方法，又不影响原始 session，用 `--fork-session` 标志：

```bash
claude --continue --fork-session
```

这会创建一个新的 session ID，同时保留之前的对话历史。原来的 session 不受影响。和恢复一样，fork 出的 session 不会继承 session 级别的权限。

**同一 session 在多个终端中打开**：如果你在多个终端中恢复同一个 session，两个终端都会写入同一个 session 文件。两边的消息会交织在一起，像两个人在同一个笔记本上写字。数据不会损坏，但对话会变得混乱。每个终端在 session 期间只能看到自己的消息，但之后恢复时会看到所有交错的内容。要从同一起点并行工作，请用 `--fork-session` 给每个终端各自一个干净的 session。

### 上下文窗口

Claude 的上下文窗口保存你的对话历史、文件内容、命令输出、[CLAUDE.md](./memory)、加载的 skill 和系统指令。工作过程中上下文会逐渐填满。Claude 会自动压缩，但对话早期的指令可能会丢失。把持久规则写在 CLAUDE.md 里，用 `/context` 查看哪些内容在占用空间。

#### 上下文满了怎么办

接近限制时，Claude Code 会自动管理上下文。它先清除旧的工具输出，需要时再压缩对话。你的请求和关键代码片段会被保留；对话初期的详细说明可能会丢失。把持久规则写在 CLAUDE.md 里，别依赖对话历史。

要控制压缩时保留什么，可以在 CLAUDE.md 中添加"紧凑指令"部分，或者运行 `/compact`（如 `/compact focus on the API changes`）。运行 `/context` 查看空间使用情况。MCP 服务器会在每个请求中添加工具定义，有些服务器可能在你开始工作前就消耗了大量上下文。运行 `/mcp` 检查每个服务器的开销。

#### 用 skill 和 subagent 管理上下文

除了压缩，你还可以用其他方式控制加载到上下文中的内容。

[Skill](./skills) 按需加载。Claude 在 session 开始时看到 skill 的描述，但只在使用时才加载完整内容。手动调用的 skill 可以设置 `disable-model-invocation: true`，这样描述也不会出现在上下文中，直到你需要为止。

[Subagent](./sub-agents) 拥有自己的全新上下文，完全独立于你的主对话。它们的工作不会让你的上下文变臃肿。完成后，它们只返回一份摘要。正是这种隔离让 subagent 在长时间 session 中特别有用。

参阅[上下文成本](./features-overview#understand-context-costs)了解各功能的开销，以及[减少 token 使用](./costs#reduce-token-usage)了解管理上下文的技巧。

## 通过 checkpoint 和权限保障安全

Claude 有两种安全机制：checkpoint 让你撤销文件更改，权限控制 Claude 无需询问就能做什么。

### 用 checkpoint 撤销更改

**每次文件编辑都是可逆的。** 在 Claude 编辑任何文件之前，它会对当前内容做快照。如果出了问题，按两次 `Esc` 回到之前的状态，或者让 Claude 撤销。

Checkpoint 存储在你的 session 本地，和 git 无关。它们只覆盖文件更改。影响远程系统的操作（数据库、API、部署）无法用 checkpoint 恢复——这也是 Claude 在运行有外部副作用的命令前会先问你的原因。

### 控制 Claude 能做什么

按 `Shift+Tab` 循环切换权限模式：

* **默认**：Claude 在文件编辑和 shell 命令前询问
* **自动接受编辑**：Claude 不问就编辑文件，但仍然需要确认命令
* **Plan 模式**：Claude 只用只读工具，创建计划让你在执行前审批

你也可以在 `.claude/settings.json` 中允许特定命令，这样 Claude 就不用每次都问了。这对 `npm test` 或 `git status` 之类的安全命令很有用。权限设置的范围可以从组织策略到个人偏好。详见[权限](./permissions)。

***

## 高效使用 Claude Code

这些技巧能帮你从 Claude Code 获得更好的结果。

### 问 Claude Code 怎么用

Claude Code 可以教你怎么用它。直接问"怎么设置 hook？"或者"CLAUDE.md 怎么写最好？"之类的问题，Claude 会给你解释。

内置命令也能帮你入门：

* `/init` 帮你为项目生成 CLAUDE.md
* `/agents` 帮你配置自定义 subagent
* `/doctor` 诊断安装的常见问题

### 这是一次对话

Claude Code 是对话式的。你不需要写完美的 prompt。先说你想要什么，然后逐步改进：

```text
Fix the login bug
```

\[Claude 调查，尝试一些修复]

```text
That's not quite right. The issue is in the session handling.
```

\[Claude 调整方向]

第一次不对也不用从头来。你可以迭代。

#### 随时打断和引导

你随时可以打断 Claude。如果方向不对，直接输入修正内容按回车就行。Claude 会停下当前操作，根据你的输入调整方向。不用等它做完，也不用从头来。

### 一开始就说清楚

初始 prompt 越精确，后续需要的修正就越少。指明具体文件、提到约束条件、指出代码中的示例模式。

```text
The checkout flow is broken for users with expired cards.
Check src/payments/ for the issue, especially token refresh.
Write a failing test first, then fix it.
```

模糊的 prompt 也能用，但你得花更多时间引导。像上面这样具体的 prompt 通常一次就能成功。

### 给 Claude 验证手段

当 Claude 能检查自己的工作时，表现会好很多。提供测试用例、粘贴预期 UI 的截图，或者定义期望的输出。

```text
Implement validateEmail. Test cases: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Run the tests after.
```

对于视觉相关的工作，粘贴设计截图让 Claude 拿自己的实现去对比。

### 先探索再动手

对于复杂问题，把研究和编码分开。先用 Plan 模式（按两次 `Shift+Tab`）来分析代码库：

```text
Read src/auth/ and understand how we handle sessions.
Then create a plan for adding OAuth support.
```

审查计划，通过对话完善，然后让 Claude 去实现。这种两阶段方法比直接写代码效果好得多。

### 委派，别指挥

把 Claude 当作一个能力很强的同事。提供上下文和方向，然后信任它来搞定细节：

```text
The checkout flow is broken for users with expired cards.
The relevant code is in src/payments/. Can you investigate and fix it?
```

你不需要告诉它读哪些文件、跑什么命令。Claude 自己会搞定。

## 接下来

### [扩展功能](/en/features-overview)

添加 skill、MCP 连接和自定义命令


### [常用工作流程](/en/common-workflows)

典型任务的分步指南
