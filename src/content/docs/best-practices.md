---
title: "Claude Code 的最佳实践"
order: 8
section: "core-concepts"
sectionLabel: "核心概念"
sectionOrder: 2
summary: "充分利用 Claude Code 的提示和模式，从配置环境到跨并行会话进行扩展。"
sourceUrl: "https://code.claude.com/docs/en/best-practices.md"
sourceTitle: "Best Practices for Claude Code"
tags: []
---
# Claude Code 的最佳实践

> 充分利用 Claude Code 的提示和模式，从配置环境到跨并行会话进行扩展。

Claude Code 是一个代理编码环境。与回答问题和等待的聊天机器人不同，Claude Code 可以在您观看、重定向或完全离开时读取您的文件、运行命令、进行更改并自主解决问题。

这会改变你的工作方式。您无需自己编写代码并要求 Claude 进行审查，而是描述您想要的内容，然后 Claude 找出如何构建它。 Claude 探索、计划和实施。

但这种自主权仍然有一个学习曲线。 Claude 在您需要了解的某些限制下工作。

本指南涵盖了已在 Anthropic 内部团队以及跨各种代码库、语言和环境使用 Claude Code 的工程师证明有效的模式。有关代理循环的内部工作原理，请参阅[Claude Code 的工作原理](./how-claude-code-works)。

***

大多数最佳实践都基于一个约束：Claude 的上下文窗口很快就会填满，并且性能会随着填满而降低。

Claude 的上下文窗口保存您的整个对话，包括每条消息、Claude 读取的每个文件以及每个命令输出。然而，这很快就会被填满。单个调试会话或代码库探索可能会生成并消耗数万个令牌。

这很重要，因为法学硕士的表现会随着上下文的填充而降低。当上下文窗口变满时，Claude 可能会开始“忘记”之前的指令或犯更多错误。上下文窗口是最重要的管理资源。使用[自定义状态行](./statusline) 持续跟踪上下文使用情况，并参阅[减少令牌使用](./costs#reduce-token-usage) 了解减少令牌使用的策略。

***

## 给Claude一个验证其工作的方法

**提示**

包括测试、屏幕截图或预期输出，以便 Claude 可以自行检查。这是你能做的最有影响力的事情。

当 Claude 可以验证自己的工作（例如运行测试、比较屏幕截图和验证输出）时，其性能会显着提高。

如果没有明确的成功标准，它可能会产生一些看起来正确但实际上行不通的东西。你成为唯一的反馈循环，每个错误都需要你的注意。|战略|之前 |之后|
| -------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **提供验证标准** | *“实现验证电子邮件地址的功能”* | *“编写一个 validateEmail 函数。示例测试用例：[user@example.com](mailto:user@example.com) 为 true，invalid 为 false，[user@.com](mailto:user@.com) 为 false。实施后运行测试”* |
| **直观地验证 UI 更改** | *“让仪表板看起来更好”* | *“\[粘贴屏幕截图]实现此设计。对结果进行屏幕截图并将其与原始结果进行比较。列出差异并修复它们”* |
| **解决根本原因，而不是症状** | *“构建失败”* | *“构建失败并出现此错误：\[粘贴错误]。修复它并验证构建是否成功。解决根本原因，不要抑制错误”* |

可以使用 [Chrome 扩展中的 Claude](./chrome) 来验证 UI 更改。它会在浏览器中打开新选项卡、测试 UI 并进行迭代，直到代码正常运行。

您的验证还可以是测试套件、linter 或检查输出的 Bash 命令。投资让您的验证坚如磐石。

***

## 先探索，然后计划，最后编码

**提示**

将研究和规划与实施分开，以避免解决错误的问题。

让 Claude 直接跳转到编码可能会产生解决错误问题的代码。使用 [Plan Mode](./common-workflows#use-plan-mode-for-safe-code-analysis) 将探索与执行分开。

推荐的工作流程分为四个阶段：

### 探索

输入 Plan Mode。 Claude 无需进行更改即可读取文件并回答问题。

```txt claude (Plan Mode)
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```

  
### 计划

要求 Claude 创建详细的实施计划。

```txt claude (Plan Mode)
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```

按 `Ctrl+G` 在文本编辑器中打开计划，以便在 Claude 继续之前进行直接编辑。

  
### 实施

切换回正常模式并让 Claude 编码，根据其计划进行验证。

```txt claude (Normal Mode)
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```

  
### 提交

要求 Claude 提交描述性消息并创建 PR。

```txt claude (Normal Mode)
commit with a descriptive message and open a PR
```

**提示**

Plan Mode 很有用，但也增加了开销。

对于范围明确且修复量较小的任务（例如修复拼写错误、添加日志行或重命名变量），请直接要求 Claude 执行。

当您不确定方法、更改修改多个文件或不熟悉所修改的代码时，规划最有用。如果您可以用一句话描述差异，请跳过该计划。

***

## 在提示中提供具体上下文

**提示**您的指示越精确，您需要的纠正就越少。

Claude 可以推断意图，但它无法读懂您的想法。参考特定文件、提及约束并指出示例模式。|战略|之前 |之后|
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | —————————————————————————————————————————————————————————————————————————————————————————
| **确定任务范围。**指定哪个文件、什么场景以及测试首选项。                  | *“为 foo.py 添加测试”* | *“为 foo.py 编写一个测试，涵盖用户注销的边缘情况。避免模拟。”* |
| **指向来源。** 将 Claude 定向到可以回答问题的来源。                    | *“为什么 ExecutionFactory 有这么奇怪的 api？”* | *“查看 ExecutionFactory 的 git 历史记录并总结其 api 是如何形成的”* |
| **参考现有模式。** 将 Claude 指向代码库中的模式。                      | *“添加日历小部件”* | *“看看现有的小部件是如何在主页上实现的，以了解这些模式。HotDogWidget.php 是一个很好的例子。遵循该模式来实现一个新的日历小部件，它允许用户选择月份并向前/向后分页以选择年份。从头开始构建，除了代码库中已使用的库之外，无需其他库。”* |
| **描述症状。**提供症状、可能的位置以及“固定”的样子。 | *“修复登录错误”* | *“用户报告会话超时后登录失败。检查 src/auth/ 中的身份验证流程，尤其是令牌刷新。编写一个重现该问题的失败测试，​​然后修复它”* |当您正在探索并且有能力纠正路线时，模糊的提示可能会很有用。像 `"what would you improve in this file?"` 这样的提示可以显示您不会想到询问的事情。

### 提供丰富的内容

**提示**

使用 `@` 引用文件、粘贴屏幕截图/图像或直接管道数据。

您可以通过多种方式向 Claude 提供丰富的数据：

* **使用 `@`** 引用文件，而不是描述代码所在的位置。 Claude 在响应之前读取文件。
* **直接粘贴图像**。将图像复制/粘贴或拖放到提示中。
* **提供文档和 API 参考的 URL**。使用 `/permissions` 将常用域列入白名单。
* **通过管道输入数据** 通过运行 `cat error.log | claude` 直接发送文件内容。
* **让 Claude 获取它需要的东西**。告诉 Claude 使用 Bash 命令、MCP 工具或通过读取文件来提取上下文本身。

***

## 配置您的环境

几个设置步骤可以使 Claude Code 在所有会话中显着更加有效。有关扩展功能以及何时使用每一项功能的完整概述，请参阅[扩展 Claude Code](./features-overview)。

### 写一个有效的CLAUDE.md

**提示**

运行 `/init` 以根据您当前的项目结构生成起始 CLAUDE.md 文件，然后随着时间的推移进行完善。

CLAUDE.md 是 Claude 在每次对话开始时读取的特殊文件。包括 Bash 命令、代码风格和工作流程规则。这为 Claude 提供了它无法单独从代码推断的持久上下文。

`/init` 命令分析您的代码库以检测构建系统、测试框架和代码模式，为您的改进奠定坚实的基础。

CLAUDE.md 文件没有必需的格式，但请保持简短且易于阅读。例如：

```markdown CLAUDE.md
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md 在每个会话中都会加载，因此仅包含广泛适用的内容。对于仅有时相关的领域知识或工作流程，请改用[技能](./skills)。 Claude 按需加载它们，不会使每个对话都变得臃肿。

保持简洁。对于每一行，询问：*“删除此行会导致 Claude 出错吗？”* 如果不会，请将其删除。臃肿的 CLAUDE.md 文件会导致 Claude 忽略您的实际指令！| ✅ 包括 | ❌排除|
| ---------------------------------------------------------------- | -------------------------------------------------- |
| Bash 命令 Claude 无法猜测 |任何 Claude 都可以通过阅读代码弄清楚 |
|与默认值不同的代码样式规则 |标准语言约定 Claude 已经知道 |
|测试说明和首选测试运行者 |详细的 API 文档（改为链接到文档）|
|存储库礼仪（分支命名、PR 约定）|经常变化的信息 |
|针对您的项目的架构决策 |长解释或教程 |
|开发人员环境怪癖（必需的环境变量）|代码库的逐文件描述 |
|常见问题或不明显的行为 |不言而喻的实践，如“编写干净的代码”|

如果 Claude 尽管有规则反对，但仍继续执行您不希望执行的操作，则文件可能太长并且规则丢失。如果 Claude 询问您的问题在 CLAUDE.md 中得到了回答，则措辞可能不明确。像对待代码一样对待 CLAUDE.md：在出现问题时对其进行审查，定期对其进行修剪，并通过观察 Claude 的行为是否确实发生变化来测试更改。

您可以通过添加强调（例如“重要”或“您必须”）来调整说明，以提高依从性。将 CLAUDE.md 签入 git，以便您的团队可以做出贡献。随着时间的推移，该文件的价值会不断增加。

CLAUDE.md 文件可以使用 `@path/to/import` 语法导入其他文件：

```markdown CLAUDE.md
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

您可以将 CLAUDE.md 文件放置在多个位置：

* **主文件夹 (`~/.claude/CLAUDE.md`)**：适用于所有 Claude 会话
* **项目根目录 (`./CLAUDE.md`)**：签入 git 以与您的团队共享
* **父目录**：对于自动拉入 `root/CLAUDE.md` 和 `root/foo/CLAUDE.md` 的 monorepos 很有用
* **子目录**：Claude 在处理这些目录中的文件时按需提取子 CLAUDE.md 文件

### 配置权限

**提示**

使用 `/permissions` 将安全命令列入白名单，或使用 `/sandbox` 进行操作系统级隔离。这可以减少干扰，同时让您保持掌控。

默认情况下，Claude Code 请求可能修改系统的操作权限：文件写入、Bash 命令、MCP 工具等。这很安全但乏味。第十次批准后，您不再真正进行审阅，您只是点击通过。有两种方法可以减少这些干扰：

* **权限白名单**：允许您知道安全的特定工具（例如 `npm run lint` 或 `git commit`）
* **沙盒**：启用操作系统级隔离，限制文件系统和网络访问，允许 Claude 在定义的边界内更自由地工作

或者，使用 `--dangerously-skip-permissions` 绕过包含工作流程的权限提示，例如修复 lint 错误或生成样板文件。请参阅[权限模式](./permissions#permission-modes) 了解跳过和不跳过的内容。

**警告**让 Claude 运行任意命令可能会导致数据丢失、系统损坏或通过提示注入进行数据泄露。仅在无法访问互联网的沙箱中使用 `--dangerously-skip-permissions`。

了解有关[配置权限](./permissions) 和[启用沙箱](./sandboxing) 的更多信息。

### 使用 CLI 工具

**提示**

告诉 Claude Code 在与外部服务交互时使用 `gh`、`aws`、`gcloud` 和 `sentry-cli` 等 CLI 工具。

CLI 工具是与外部服务交互的最上下文有效的方式。如果您使用 GitHub，请安装 `gh` CLI。 Claude 知道如何使用它来创建问题、打开拉取请求和阅读评论。如果没有 `gh`，Claude 仍可以使用 GitHub API，但未经身份验证的请求通常会达到速率限制。

Claude 在学习它还不知道的 CLI 工具方面也很有效。尝试类似 `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.` 的提示

### 连接 MCP 服务器

**提示**

运行 `claude mcp add` 以连接外部工具，例如 Notion、Figma 或您的数据库。

借助 [MCP 服务器](./mcp)，您可以要求 Claude 实现问题跟踪器的功能、查询数据库、分析监控数据、集成 Figma 的设计以及自动化工作流程。

### 设置钩子

**提示**

对每次都必须发生且零异常的操作使用钩子。

[Hooks](./hooks-guide) 在 Claude 工作流程中的特定点自动运行脚本。与建议性的 CLAUDE.md 指令不同，挂钩是确定性的并保证操作发生。

Claude 可以为您编写钩子。尝试像“编写一个在每次文件编辑后运行 eslint 的钩子”* 或“编写一个阻止写入迁移文件夹的钩子”这样的提示。 直接编辑 `.claude/settings.json` 以手动配置钩子，然后运行 ​​`/hooks` 来浏览配置的内容。

### 创造技能

**提示**

在 `.claude/skills/` 中创建 `SKILL.md` 文件，以提供 Claude 领域知识和可重用工作流程。

[技能](./skills) 通过特定于您的项目、团队或领域的信息扩展 Claude 的知识。 Claude 会在相关时自动应用它们，或者您可以使用 `/skill-name` 直接调用它们。

通过将 `SKILL.md` 的目录添加到 `.claude/skills/` 来创建技能：

```markdown .claude/skills/api-conventions/SKILL.md
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

技能还可以定义您直接调用的可重复工作流程：

```markdown .claude/skills/fix-issue/SKILL.md
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

运行 `/fix-issue 1234` 来调用它。将 `disable-model-invocation: true` 用于具有您想要手动触发的副作用的工作流程。

### 创建自定义子代理

**提示**

在 `.claude/agents/` 中定义 Claude 可以委派独立任务的专业助理。

[子代理](./sub-agents) 使用自己的一组允许的工具在自己的上下文中运行。它们对于读取许多文件或需要专门关注而又不会扰乱您的主要对话的任务非常有用。

```markdown .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

告诉 Claude 显式使用子代理：*“使用子代理检查此代码是否存在安全问题。”*

### 安装插件

**提示**

运行 `/plugin` 浏览市场。插件无需配置即可添加技能、工具和集成。[插件](./plugins) 将社区和 Anthropic 中的技能、挂钩、子代理和 MCP 服务器捆绑到单个可安装单元中。如果您使用类型化语言，请安装[代码智能插件](./discover-plugins#code-intelligence)，以在编辑后为 Claude 提供精确的符号导航和自动错误检测。

有关在技能、子代理、挂钩和 MCP 之间进行选择的指南，请参阅[扩展 Claude Code](./features-overview#match-features-to-your-goal)。

***

## 有效沟通

您与 Claude Code 的沟通方式会显着影响结果的质量。

### 问代码库问题

**提示**

问 Claude 您会问高级工程师的问题。

加入新的代码库时，请使用 Claude Code 进行学习和探索。您可以向 Claude 提出与其他工程师相同的问题：

* 日志记录是如何工作的？
* 如何创建新的 API 端点？
* `async move { ... }` 在 `foo.rs` 的第 134 行做什么？
* `CustomerOnboardingFlowImpl` 处理哪些边缘情况？
* 为什么此代码在第 333 行调用 `foo()` 而不是 `bar()`？

以这种方式使用 Claude Code 是一种有效的入职工作流程，可以缩短启动时间并减少其他工程师的负担。无需特殊提示：直接提问。

### 让 Claude 采访您

**提示**

对于更大的功能，请先让 Claude 采访您。从最简单的提示开始，然后要求 Claude 使用 `AskUserQuestion` 工具采访您。

Claude 询问您可能尚未考虑的事项，包括技术实现、UI/UX、边缘情况和权衡。

```text
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

规范完成后，启动一个新会话来执行它。新的会议有干净的背景，完全专注于实施，并且您有一份书面规范可供参考。

***

## 管理你的会话

对话是持续且可逆的。利用这一点来发挥你的优势！

### 尽早且经常纠正路线

**提示**

一旦发现 Claude 偏离轨道，请立即纠正。

最好的结果来自紧密的反馈循环。尽管 Claude 有时会在第一次尝试时完美解决问题，但快速纠正通常会更快地产生更好的解决方案。

* **`Esc`**：使用 `Esc` 键停止 Claude 的中间动作。上下文被保留，因此您可以重定向。
* **`Esc + Esc` 或 `/rewind`**：按 `Esc` 两次或运行 `/rewind` 打开快退菜单并恢复之前的对话和代码状态，或从所选消息进行摘要。
* **`"Undo that"`**：让 Claude 恢复其更改。
* **`/clear`**：重置不相关任务之间的上下文。具有不相关上下文的长时间会话会降低性能。

如果您在一次会话中就同一问题纠正 Claude 两次以上，则上下文会因失败的方法而变得混乱。运行 `/clear` 并通过包含您学到的内容的更具体的提示重新开始。带有更好提示的干净会话几乎总是胜过带有累积修正的长时间会话。

### 积极管理环境

**提示**

在不相关的任务之间运行 `/clear` 以重置上下文。当您接近上下文限制时，Claude Code 会自动压缩对话历史记录，从而在释放空间的同时保留重要的代码和决策。

在长时间会话期间，Claude 的上下文窗口可能会充满不相关的对话、文件内容和命令。这会降低性能，有时还会分散 Claude 的注意力。

* 在任务之间频繁使用 `/clear` 来完全重置上下文窗口
* 当自动压缩触发时，Claude 会总结最重要的内容，包括代码模式、文件状态和关键决策
* 如需更多控制，请运行 `/compact <instructions>`，如 `/compact Focus on the API changes`
* 要仅压缩部分对话，请使用 `Esc + Esc` 或 `/rewind`，选择消息检查点，然后选择 **从此处总结**。这会压缩从该点开始的消息，同时保持先前的上下文完整。
* 使用 `"When compacting, always preserve the full list of modified files and any test commands"` 等指令自定义 CLAUDE.md 中的压缩行为，以确保关键上下文能够在汇总中幸存下来
* 对于不需要停留在上下文中的快速问题，请使用 [`/btw`](./interactive-mode#side-questions-with-btw)。答案显示在可忽略的叠加层中，并且永远不会进入对话历史记录，因此您可以在不增加上下文的情况下检查详细信息。

### 使用子代理进行调查

**提示**

委托 `"use subagents to investigate X"` 进行研究。他们在单独的上下文中进行探索，使您的主要对话保持清晰以便于实施。

由于上下文是您的基本约束，因此子代理是可用的最强大的工具之一。当 Claude 研究代码库时，它会读取大量文件，所有这些文件都会消耗您的上下文。子代理在单独的上下文窗口中运行并报告摘要：

```text
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

子代理探索代码库、读取相关文件并报告结果，所有这些都不会扰乱您的主要对话。

您还可以在 Claude 实现某些功能后使用子代理进行验证：

```text
use a subagent to review this code for edge cases
```

### 使用检查点倒带

**提示**

Claude 所做的每个操作都会创建一个检查点。您可以将对话、代码或两者恢复到任何先前的检查点。

Claude 在更改之前自动检查点。双击 `Escape` 或运行 `/rewind` 打开快退菜单。您可以仅恢复对话、仅恢复代码、恢复两者或从选定的消息中进行摘要。有关详细信息，请参阅[检查点](./checkpointing)。

您可以告诉 Claude 尝试一些有风险的事情，而不是仔细计划每一步。如果不起作用，请倒带并尝试其他方法。检查点在会话中持续存在，因此您可以关闭终端并稍后再倒带。

**警告**

检查点仅跟踪*由 Claude* 所做的更改，而不跟踪外部进程。这不是 git 的替代品。

### 恢复对话

**提示**

运行 `claude --continue` 从上次中断的地方继续，或运行 `--resume` 从最近的会话中进行选择。

Claude Code 在本地保存对话。当任务跨越多个会话时，您不必重新解释上下文：

```bash
claude --continue    # Resume the most recent conversation
claude --resume      # Select from recent conversations
```

使用 `/rename` 为会话提供描述性名称，例如 `"oauth-migration"` 或 `"debugging-memory-leak"`，以便您以后可以找到它们。将会话视为分支：不同的工作流可以具有单独的持久上下文。

***

## 自动化和规模化一旦您能够有效地使用一台 Claude，就可以通过并行会话、非交互模式和扇出模式来增加您的输出。

到目前为止，一切都假设一个人、一个 Claude 和一次对话。但 Claude Code 可以水平扩展。本节中的技术展示了如何完成更多工作。

### 运行非交互模式

**提示**

在 CI、预提交挂钩或脚本中使用 `claude -p "prompt"`。添加 `--output-format stream-json` 以进行流式 JSON 输出。

使用 `claude -p "your prompt"`，您可以非交互方式运行 Claude，无需会话。非交互模式是您将 Claude 集成到 CI 管道、预提交挂钩或任何自动化工作流程中的方式。输出格式允许您以编程方式解析结果：纯文本、JSON 或流式 JSON。

```bash
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### 运行多个 Claude 会话

**提示**

并行运行多个 Claude 会话以加快开发速度、运行独立实验或启动复杂的工作流程。

运行并行会话的主要方式有以下三种：

* [Claude Code 桌面应用程序](./desktop#work-in-parallel-with-sessions)：直观地管理多个本地会话。每个会话都有自己独立的工作树。
* [网络上的 Claude Code](./claude-code-on-the-web)：在隔离虚拟机中的 Anthropic 安全云基础架构上运行。
* [代理团队](./agent-teams)：通过共享任务、消息传递和团队领导自动协调多个会话。

除了并行工作之外，多个会话还可以实现以质量为中心的工作流程。新的上下文可以改善代码审查，因为 Claude 不会偏向于它刚刚编写的代码。

例如，使用编写者/审阅者模式：

|会议A（作家）|会议 B（审稿人）|
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Implement a rate limiter for our API endpoints` |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

您可以对测试执行类似的操作：让一个 Claude 编写测试，然后另一个编写代码以通过测试。

### 跨文件扇出

**提示**

循环调用每个任务的 `claude -p`。使用 `--allowedTools` 确定批量操作的权限范围。

对于大型迁移或分析，您可以在多个并行 Claude 调用之间分配工作：

### 生成任务列表

让 Claude 列出所有需要迁移的文件（例如 `list all 2,000 Python files that need migrating`）

  
### 编写一个脚本来循环列表

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

  
### 在几个文件上进行测试，然后大规模运行根据前 2-3 个文件的问题来优化提示，然后运行完整的文件集。 `--allowedTools` 标志限制 Claude 可以执行的操作，这在无人值守运行时很重要。

您还可以将 Claude 集成到现有数据/处理管道中：

```bash
claude -p "<your prompt>" --output-format json | your_command
```

在开发过程中使用 `--verbose` 进行调试，并在生产中将其关闭。

***

## 避免常见的故障模式

这些都是常见的错误。尽早认识它们可以节省时间：

* **厨房水槽会议。** 您从一个任务开始，然后询问 Claude 一些不相关的问题，然后返回第一个任务。上下文充满了不相关的信息。
  > **修复**：不相关任务之间的 `/clear`。
* **一遍又一遍地纠正。** Claude 做错了什么，你纠正它，它仍然是错误的，你再次纠正。上下文被失败的方法污染了。
  > **修复**：两次失败的更正后，`/clear` 并结合您所学到的内容编写更好的初始提示。
* **过度指定的 CLAUDE.md。** 如果您的 CLAUDE.md 太长，Claude 会忽略其中的一半，因为重要的规则会在噪音中丢失。
  > **修复**：无情地修剪。如果 Claude 在没有指令的情况下已经正确执行某些操作，请将其删除或将其转换为挂钩。
* **信任然后验证的差距。** Claude 产生了一个看似合理的实现，但不处理边缘情况。
  > **修复**：始终提供验证（测试、脚本、屏幕截图）。如果无法验证，请勿发货。
* **无限的探索。** 您要求 Claude “调查”某些事物而不限定其范围。 Claude 读取数百个文件，填充上下文。
  > **修复**：缩小调查范围或使用子代理，以便探索不会消耗您的主要上下文。

***

## 培养你的直觉

本指南中的模式并不是一成不变的。它们是总体上行之有效的起点，但可能并不适合所有情况。

有时你“应该”让背景积累起来，因为你深陷一个复杂的问题而历史很有价值。有时您应该跳过计划并让 Claude 弄清楚，因为任务是探索性的。有时，模糊的提示是完全正确的，因为您想在限制问题之前了解 Claude 如何解释问题。

注意什么有效。当 Claude 产生出色的输出时，请注意您所做的事情：提示结构、您提供的上下文、您所处的模式。当 Claude 遇到困难时，问为什么。周围环境是否太嘈杂？提示太模糊？任务太大，无法完成一次？

随着时间的推移，您将发展出任何指南都无法捕捉到的直觉。你会知道什么时候要具体，什么时候要开放，什么时候要计划，什么时候要探索，什么时候要理清背景，什么时候要让它积累。

## 相关资源

* [Claude Code 的工作原理](./how-claude-code-works)：代理循环、工具和上下文管理
* [扩展 Claude Code](./features-overview)：技能、挂钩、MCP、子代理和插件
* [常见工作流程](./common-workflows)：调试、测试、PR 等的分步方法
* [CLAUDE.md](./memory): 存储项目约定和持久上下文
