---
title: "扩展 Claude 技能"
order: 24
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "创建、管理和共享技能以扩展 Claude 在 Claude Code 中的功能。包括自定义命令和捆绑技能。"
sourceUrl: "https://code.claude.com/docs/en/skills.md"
sourceTitle: "Extend Claude with skills"
tags: []
---
# 用技能扩展 Claude

> 创建、管理和共享技能以扩展 Claude 在 Claude Code 中的功能。包括自定义命令和捆绑技能。

技能扩展了 Claude 的能力。创建包含说明的 `SKILL.md` 文件，Claude 将其添加到其工具包中。 Claude 在相关时使用技能，或者您可以直接使用 `/skill-name` 调用一项技能。

**注意**

对于 `/help` 和 `/compact` 等内置命令，请参阅[内置命令参考](./commands)。

**自定义命令已合并到技能中。** `.claude/commands/deploy.md` 处的文件和 `.claude/skills/deploy/SKILL.md` 处的技能都会创建 `/deploy` 并以相同的方式工作。您现有的 `.claude/commands/` 文件将继续工作。技能添加了可选功能：支持文件的目录、[控制您或 Claude 是否调用它们](#control-who-invokes-a-skill) 的 frontmatter，以及 Claude 在相关时自动加载它们的能力。

Claude Code 技能遵循 [代理技能](https://agentskills.io) 开放标准，适用于多种 AI 工具。 Claude Code 通过[调用控制](#control-who-invokes-a-skill)、[子代理执行](#run-skills-in-a-subagent) 和[动态上下文注入](#inject-dynamic-context) 等附加功能扩展了标准。

## 捆绑技能

Claude Code 附带捆绑技能，并且在每个会话中都可用。与直接执行固定逻辑的[内置命令](./commands)不同，捆绑技能是基于提示的：它们为 Claude 提供了详细的剧本，并让它使用其工具来编排工作。这意味着捆绑技能可以生成并行代理、读取文件并适应您的代码库。

您可以像调用任何其他技能一样调用捆绑技能：键入 `/`，后跟技能名称。下表中，`<arg>` 表示必填参数，`[arg]` 表示可选参数。|技能|目的|
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/batch <instruction>` |并行协调代码库中的大规模更改。研究代码库，将工作分解为 5 到 30 个独立单元，并提出计划。一旦获得批准，就会在隔离的 [git 工作树](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中为每个单元生成一个后台代理。每个代理实现其单元、运行测试并打开拉取请求。需要 git 存储库。示例：`/batch migrate src/ from Solid to React` |
| `/claude-api` |加载适用于您的项目语言（Python、TypeScript、Java、Go、Ruby、C#、PHP 或 cURL）的 Claude API 参考材料以及适用于 Python 和 TypeScript 的 Agent SDK 参考。涵盖工具使用、流式传输、批处理、结构化输出和常见陷阱。当您的代码导入 `anthropic`、`@anthropic-ai/sdk` 或 `claude_agent_sdk` 时也会自动激活 |
| `/debug [description]` |通过阅读会话调试日志对当前 Claude Code 会话进行故障排除。 （可选）描述问题以集中分析 |
| `/loop [interval] ` |当会话保持打开状态时，按一定时间间隔重复运行提示。对于轮询部署、维护 PR 或定期重新运行其他技能很有用。示例：`/loop 5m check if the deploy finished`。请参阅[按计划运行提示](./scheduled-tasks) || `/simplify [focus]` |检查最近更改的文件是否存在代码重用、质量和效率问题，然后修复它们。并行产生三个审核代理，汇总他们的发现并应用修复。传递文本以关注特定问题：`/simplify focus on memory efficiency` |## 开始使用

### 创建你的第一个技能

此示例创建了一项技能，教 Claude 使用可视化图表和类比来解释代码。由于它使用默认的 frontmatter，因此当您询问某些内容如何工作时，Claude 可以自动加载它，或者您可以直接使用 `/explain-code` 调用它。

### 创建技能目录

在您的个人技能文件夹中为该技能创建一个目录。个人技能适用于您的所有项目。

```bash
mkdir -p ~/.claude/skills/explain-code
```

  
### 编写 SKILL.md

每个技能都需要一个 `SKILL.md` 文件，该文件包含两部分：YAML frontmatter（在 `---` 标记之间），告诉 Claude 何时使用该技能，以及调用技能时跟随的带有指令 Claude 的 Markdown 内容。 `name` 字段变为 `/slash-command`，`description` 帮助 Claude 决定何时自动加载它。

创建 `~/.claude/skills/explain-code/SKILL.md`：

```yaml
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

  
### 测试技能

您可以通过两种方式进行测试：

**让 Claude 通过询问与描述相匹配的内容来自动调用它**：

```text
How does this code work?
```

**或者直接使用技能名称调用**：

```text
/explain-code src/auth/login.ts
```

无论哪种方式，Claude 都应该在其解释中包含类比和 ASCII 图。

### 技能所在

技能的存储位置决定了谁可以使用它：

|地点 |路径|适用于 |
| :--------- | :-------------------------------------------------- | ：-------------------------- |
|企业 |请参阅[托管设置](./settings#settings-files) |您组织中的所有用户 |
|个人| `~/.claude/skills/<skill-name>/SKILL.md` |您的所有项目 |
|项目| `.claude/skills/<skill-name>/SKILL.md` |仅限此项目|
|插件 | `/skills/<skill-name>/SKILL.md` |插件在哪里启用 |

当不同级别的技能共享相同的名称时，优先级较高的位置会获胜：企业 > 个人 > 项目。插件技能使用 `plugin-name:skill-name` 命名空间，因此它们不会与其他级别冲突。如果您的文件位于 `.claude/commands/` 中，这些文件的工作方式相同，但如果技能和命令共享相同的名称，则技能优先。

#### 从嵌套目录自动发现

当您处理子目录中的文件时，Claude Code 会自动从嵌套的 `.claude/skills/` 目录中发现技能。例如，如果您正在编辑 `packages/frontend/` 中的文件，则 Claude Code 也会查找 `packages/frontend/.claude/skills/` 中的技能。这支持 monorepo 设置，其中包有自己的技能。

每个技能都是一个以 `SKILL.md` 为入口点的目录：

```text
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

`SKILL.md` 包含主要指令并且是必需的。其他文件是可选的，可让您构建更强大的技能：供 Claude 填写的模板、显示预期格式的示例输出、Claude 可以执行的脚本或详细的参考文档。从 `SKILL.md` 引用这些文件，以便 Claude 知道它们包含什么以及何时加载它们。有关更多详细信息，请参阅[添加支持文件](#add-supporting-files)。

**注意**

`.claude/commands/` 中的文件仍然有效并支持相同的 [frontmatter](#frontmatter-reference)。建议使用技能，因为它们支持附加功能（例如支持文件）。#### 来自其他目录的技能

通过 `--add-dir` 添加的目录中 `.claude/skills/` 中定义的技能会自动加载，并通过实时更改检测来获取，因此您可以在会话期间编辑它们，而无需重新启动。

**注意**

默认情况下，不会加载 `--add-dir` 目录中的 CLAUDE.md 文件。要加载它们，请设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`。请参阅[从其他目录加载](./memory#load-from-additional-directories)。

## 配置技能

技能通过 `SKILL.md` 顶部的 YAML frontmatter 和后面的 markdown 内容进行配置。

### 技能内容类型

技能文件可以包含任何指令，但考虑如何调用它们有助于指导要包含的内容：

**参考内容**添加了适用于您当前工作的知识 Claude。惯例、模式、风格指南、领域知识。此内容内联运行，因此 Claude 可以将其与对话上下文一起使用。

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**任务内容** 为 Claude 提供特定操作的分步说明，例如部署、提交或代码生成。您通常希望使用 `/skill-name` 直接调用这些操作，而不是让 Claude 决定何时运行它们。添加 `disable-model-invocation: true` 以防止 Claude 自动触发。

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

您的 `SKILL.md` 可以包含任何内容，但仔细考虑您希望如何调用该技能（由您、由 Claude 或两者）以及您希望它在何处运行（内联或在子代理中）有助于指导包含哪些内容。对于复杂的技能，您还可以[添加支持文件](#add-supporting-files)以保持主要技能的重点。

### Frontmatter 参考

除了 Markdown 内容之外，您还可以使用 `SKILL.md` 文件顶部 `---` 标记之间的 YAML frontmatter 字段来配置技能行为：

```yaml
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...
```

所有字段都是可选的。仅推荐 `description`，以便 Claude 知道何时使用该技能。|领域|必填|描述 |
| ：-------------------------- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` |没有 |技能的显示名称。如果省略，则使用目录名称。仅限小写字母、数字和连字符（最多 64 个字符）。                    |
| `description` |推荐|该技能的作用是什么以及何时使用它。 Claude 使用它来决定何时应用该技能。如果省略，则使用 Markdown 内容的第一段。 |
| `argument-hint` |没有 |自动完成期间显示的提示以指示预期的参数。例如：`[issue-number]` 或 `[filename] [format]`。                                    |
| `disable-model-invocation` |没有 |设置为 `true` 可防止 Claude 自动加载该技能。用于您想要使用 `/name` 手动触发的工作流程。默认值：`false`。 |
| `user-invocable` |没有 |设置为 `false` 可从 `/` 菜单中隐藏。用于背景知识的用户不应直接调用。默认值：`true`。                              |
| `allowed-tools` |没有 |当此技能处于活动状态时，Claude 无需征得许可即可使用工具。                                                                             |
| `model` |没有 |该技能激活时使用的模型。                                                                                                               |
| `context` |没有 |设置为 `fork` 以在分叉子代理上下文中运行。                                                                                                    |
| `agent` |没有 |设置 `context: fork` 时要使用的子代理类型。                                                                                               |
| `hooks` |没有 |挂钩的范围是该技能的生命周期。配置格式请参见[技能和代理中的挂钩](./hooks#hooks-in-skills-and-agents)。              |

#### 可用的字符串替换

技能支持技能内容中动态值的字符串替换：|变量|描述 |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS` |调用该技能时所有参数都通过。如果内容中不存在 `$ARGUMENTS`，则参数将附加为 `ARGUMENTS: <value>`。                                                                                                                                             |
| `$ARGUMENTS[N]` |通过基于 0 的索引访问特定参数，例如第一个参数为 `$ARGUMENTS[0]`。                                                                                                                                                                                             |
| `$N` | `$ARGUMENTS[N]` 的简写，例如第一个参数为 `$0`，第二个参数为 `$1`。                                                                                                                                                                                               |
| `${CLAUDE_SESSION_ID}` |当前会话 ID。对于记录、创建特定于会话的文件或将技能输出与会话相关联非常有用。                                                                                                                                                                  |
| `${CLAUDE_SKILL_DIR}` |包含技能的 `SKILL.md` 文件的目录。对于插件技能，这是插件内技能的子目录，而不是插件根目录。在 bash 注入命令中使用它来引用与技能捆绑的脚本或文件，无论当前工作目录如何。 |

**使用替换的示例：**

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### 添加支持文件

技能的目录中可以包含多个文件。这使得 `SKILL.md` 能够专注于要点，同时让 Claude 仅在需要时访问详细的参考资料。大型参考文档、API 规范或示例集合不需要在每次技能运行时加载到上下文中。

```text
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

参考 `SKILL.md` 中的支持文件，以便 Claude 知道每个文件包含什么以及何时加载它：

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

**提示**

将 `SKILL.md` 保持在 500 行以下。将详细的参考材料移至单独的文件中。

### 控制谁调用技能

默认情况下，您和 Claude 都可以调用任何技能。您可以键入 `/skill-name` 直接调用它，Claude 可以在与您的对话相关时自动加载它。两个 frontmatter 字段可以让您限制这一点：* **`disable-model-invocation: true`**：只有您可以调用该技能。将此用于具有副作用的工作流程或您想要控制时序的工作流程，例如 `/commit`、`/deploy` 或 `/send-slack-message`。您不希望 Claude 因为您的代码看起来已准备就绪而决定部署。

* **`user-invocable: false`**：只有Claude可以调用该技能。将此用于无法作为命令操作的背景知识。 `legacy-system-context` 技能解释了旧系统的工作原理。 Claude 在相关时应该知道这一点，但 `/legacy-system-context` 对于用户来说并不是一个有意义的操作。

此示例创建只有您可以触发的部署技能。 `disable-model-invocation: true` 字段阻止 Claude 自动运行：

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

以下是这两个字段如何影响调用和上下文加载：

|前沿 |您可以调用 | Claude 可以调用|当加载到上下文中时 |
| :-------------------------------- | :------------- | :---------------- | ：------------------------------------------------------------------------ |
| （默认）|是的 |是的 |描述始终在上下文中，调用时会加载全部技能 |
| `disable-model-invocation: true` |是的 |没有 |描述不在上下文中，调用时会加载全部技能 |
| `user-invocable: false` |没有 |是的 |描述始终在上下文中，调用时会加载全部技能 |

**注意**

在常规会话中，技能描述会加载到上下文中，以便 Claude 知道可用的内容，但完整的技能内容仅在调用时加载。 [具有预加载技能的子代理](./sub-agents#preload-skills-into-subagents) 的工作方式有所不同：在启动时注入完整的技能内容。

### 限制工具访问

使用 `allowed-tools` 字段可限制 Claude 在技能处于活动状态时可以使用哪些工具。此技能创建一个只读模式，Claude 可以浏览文件但不能修改它们：

```yaml
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### 将参数传递给技能

您和 Claude 都可以在调用技能时传递参数。可通过 `$ARGUMENTS` 占位符获取参数。

此技能按编号修复了 GitHub 问题。 `$ARGUMENTS` 占位符将替换为技能名称后面的内容：

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

当您运行 `/fix-issue 123` 时，Claude 会收到“按照我们的编码标准修复 GitHub 问题 123...”

如果您使用参数调用技能，但该技能不包含 `$ARGUMENTS`，则 Claude Code 会将 `ARGUMENTS: <your input>` 附加到技能内容的末尾，以便 Claude 仍然可以看到您键入的内容。

要按位置访问各个参数，请使用 `$ARGUMENTS[N]` 或更短的 `$N`：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

运行 `/migrate-component SearchBar React Vue` 会将 `$ARGUMENTS[0]` 替换为 `SearchBar`，将 `$ARGUMENTS[1]` 替换为 `React`，将 `$ARGUMENTS[2]` 替换为 `Vue`。使用 `$N` 简写的相同技巧：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## 高级模式

### 注入动态上下文

`!`command\`\` 语法在技能内容发送到 Claude 之前运行 shell 命令。命令输出替换占位符，因此 Claude 接收实际数据，而不是命令本身。此技能通过使用 GitHub CLI 获取实时 PR 数据来总结拉取请求。 `!`gh pr diff\`\` 和其他命令首先运行，它们的输出被插入到提示符中：

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

当该技能运行时：

1. 每个 `!` 命令\`\` 立即执行（在 Claude 看到任何内容之前）
2. 输出替换技能内容中的占位符
3. Claude 收到带有实际 PR 数据的完全渲染提示

这是预处理，而不是 Claude 执行的操作。 Claude只看到最终结果。

**提示**

要在技能中启用[扩展思维](./common-workflows#use-extended-thinking-thinking-mode)，请在技能内容中的任意位置包含“超思维”一词。

### 在子代理中运行技能

当您希望一项技能单独运行时，请将 `context: fork` 添加到您的 frontmatter 中。技能内容成为驱动子代理的提示。它无法访问您的对话历史记录。

**警告**

`context: fork` 仅对有明确说明的技能才有意义。如果您的技能包含诸如“使用这些 API 约定”之类的指南，但没有任务，则子代理会收到指南，但没有可操作的提示，并且返回时没有有意义的输出。

技能和[子代理](./sub-agents)在两个方向上协同工作：

|方法|系统提示|任务|还加载 |
| :---------------------------- | :---------------------------------------- | :-------------------------- | :---------------------------- |
| `context: fork` 的技能 |从代理类型（`Explore`、`Plan`等）|技能.md 内容 | CLAUDE.md |
|具有 `skills` 字段的子代理 | Subagent 的 markdown 正文 | Claude的委托消息|预装技能+CLAUDE.md |

使用 `context: fork`，您可以在技能中编写任务并选择代理类型来执行它。对于相反的情况（定义使用技能作为参考材料的自定义子代理），请参阅[子代理](./sub-agents#preload-skills-into-subagents)。

#### 示例：使用 Explore 代理研究技能

该技能在分叉的 Explore 代理中运行研究。技能内容成为任务，代理提供针对代码库探索优化的只读工具：

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

当该技能运行时：

1. 创建一个新的隔离上下文
2. 子代理接收技能内容作为其提示（“彻底研究\$ARGUMENTS...”）
3、`agent`字段决定执行环境（模型、工具、权限）
4. 结果被总结并返回到您的主要对话

`agent` 字段指定要使用的子代理配置。选项包括内置代理（`Explore`、`Plan`、`general-purpose`）或 `.claude/agents/` 中的任何自定义子代理。如果省略，则使用 `general-purpose`。

### 限制Claude的技能访问默认情况下，Claude 可以调用任何未设置 `disable-model-invocation: true` 的技能。当技能处于活动状态时，定义 `allowed-tools` 的技能将授予 Claude 对这些工具的访问权限，而无需每次使用批准。您的[权限设置](./permissions) 仍控制所有其他工具的基准审批行为。 `/compact` 和 `/init` 等内置命令无法通过技能工具使用。

控制 Claude 可以调用哪些技能的三种方法：

**通过拒绝 `/permissions` 中的技能工具来禁用所有技能**：

```text
# Add to deny rules:
Skill
```

**使用[权限规则](./permissions)允许或拒绝特定技能**：

```text
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

权限语法：`Skill(name)` 表示完全匹配，`Skill(name *)` 表示与任何参数的前缀匹配。

**通过将 `disable-model-invocation: true` 添加到其 frontmatter 中来隐藏个人技能**。这完全从 Claude 的上下文中删除了该技能。

**注意**

`user-invocable` 字段仅控制菜单可见性，而不控制技能工具访问。使用 `disable-model-invocation: true` 阻止编程调用。

## 分享技能

根据您的受众，技能可以分布在不同的范围：

* **项目技巧**：将`.claude/skills/`提交到版本控制
* **插件**：在您的[插件](./plugins)中创建一个 `skills/` 目录
* **托管**：通过[托管设置](./settings#settings-files) 在组织范围内部署

### 生成视觉输出

技能可以捆绑和运行任何语言的脚本，为 Claude 提供超出单个提示所能实现的功能。一种强大的模式是生成可视化输出：在浏览器中打开交互式 HTML 文件以探索数据、调试或创建报告。

此示例创建一个代码库资源管理器：一个交互式树视图，您可以在其中展开和折叠目录、一目了然地查看文件大小并通过颜色识别文件类型。

创建技能目录：

```bash
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

创建 `~/.claude/skills/codebase-visualizer/SKILL.md`。描述告诉 Claude 何时激活此技能，指令告诉 Claude 运行捆绑的脚本：

```
`yaml
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py 。
```text
This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
```
`

创建 `~/.claude/skills/codebase-visualizer/scripts/visualize.py`。该脚本扫描目录树并生成一个独立的 HTML 文件：

* **摘要侧边栏**显示文件计数、目录计数、总大小和文件类型数量
* **条形图** 按文件类型细分代码库（按大小排名前 8 位）
* **可折叠树**，您可以在其中展开和折叠目录，并带有颜色编码的文件类型指示器

该脚本需要 Python，但仅使用内置库，因此无需安装任何包：

```python expandable
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'{ext}'
        f''
        f'{(size/total_size)*100:.1f}%'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>

  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>

  
    
      <h1>📊 Summary</h1>
      Files{stats["files"]:,}
      Directories{stats["dirs"]:,}
      Total size{fmt(data["size"])}
      File types{len(stats["extensions"])}
      <h2>By file type</h2>
      {lang_bars}
    
    
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    
  
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `📁 ${{node.name}}${{fmt(node.size)}}`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `${{node.name}}${{fmt(node.size)}}`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

要进行测试，请在任何项目中打开 Claude Code 并询问“可视化此代码库”。 Claude 运行脚本，生成 `codebase-map.html`，并在浏览器中打开它。

此模式适用于任何可视化输出：依赖关系图、测试覆盖率报告、API 文档或数据库模式可视化。捆绑脚本负责繁重的工作，而 Claude 则负责编排。

## 故障排除

### 技能未触发

如果 Claude 没有按预期使用您的技能：1. 检查描述是否包含用户自然会说的关键词
2. 验证技能是否出现在`What skills are available?`中
3. 尝试重新表述您的请求，使其更符合描述
4. 如果该技能是用户可调用的，则直接使用 `/skill-name` 调用它

### 技能触发过于频繁

如果 Claude 在您不需要时使用您的技能：

1. 使描述更加具体
2. 如果只想手动调用，请添加`disable-model-invocation: true`

### Claude 没有看到我所有的技能

技能描述已加载到上下文中，以便 Claude 知道可用的内容。如果你有很多技能，它们可能会超出角色预算。预算以上下文窗口的 2% 动态缩放，并回退 16,000 个字符。运行 `/context` 以检查有关排除技能的警告。

要覆盖该限制，请设置 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量。

## 相关资源

* **[子代理](./sub-agents)**：将任务委托给专门代理
* **[Plugins](./plugins)**：与其他扩展一起打包和分发技能
* **[Hooks](./hooks)**：围绕工具事件自动化工作流程
* **[内存](./memory)**：管理持久上下文的 CLAUDE.md 文件
* **[内置命令](./commands)**：内置 `/` 命令参考
* **[权限](./permissions)**：控制工具和技能访问
