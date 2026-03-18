---
title: "延长 Claude Code"
order: 5
section: "core-concepts"
sectionLabel: "核心概念"
sectionOrder: 2
summary: "了解何时使用 CLAUDE.md、技能、子代理、挂钩、MCP 和插件。"
sourceUrl: "https://code.claude.com/docs/en/features-overview.md"
sourceTitle: "Extend Claude Code"
tags: []
---
# 扩展 Claude Code

> 了解何时使用 CLAUDE.md、skill、subagent、hook、MCP 和插件。

Claude Code 把推理代码的模型和[内置工具](./how-claude-code-works#tools)（文件操作、搜索、执行和 Web 访问）结合在一起。内置工具能搞定大多数编码任务。本指南介绍扩展层：你可以添加的功能，用来自定义 Claude 的知识、连接外部服务、自动化工作流程。

**注意**

代理循环的工作原理请看 [Claude Code 的工作原理](./how-claude-code-works)。

**刚接触 Claude Code？** 从 [CLAUDE.md](./memory) 开始，写上项目约定。其他扩展按需添加就好。

## 概述

各扩展插入代理循环的不同位置：

* **[CLAUDE.md](./memory)** 添加持久上下文，每次 session Claude 都能看到
* **[Skill](./skills)** 添加可复用的知识和可调用的工作流程
* **[MCP](./mcp)** 把 Claude 连接到外部服务和工具
* **[Subagent](./sub-agents)** 在隔离上下文中运行自己的循环，返回摘要
* **[代理团队](./agent-teams)** 通过共享任务和点对点消息来协调多个独立 session
* **[Hook](./hooks)** 作为确定性脚本在循环外运行
* **[插件](./plugins)** 和 **[市场](./plugin-marketplaces)** 打包并分发这些功能

[Skill](./skills) 是最灵活的扩展。Skill 是包含知识、工作流程或指令的 Markdown 文件。你可以用 `/deploy` 这样的命令调用 skill，Claude 也可以在相关时自动加载。Skill 可以在当前对话中运行，也可以通过 subagent 在隔离上下文中运行。

## 功能与目标的匹配

功能范围从始终加载的上下文，到按需调用的能力，再到针对特定事件运行的后台自动化。下表展示了各功能及其适用场景。

| 功能 | 做什么 | 什么时候用 | 示例 |
| ---------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **CLAUDE.md** | 每次对话都加载的持久上下文 | 项目约定、"永远要做 X"的规则 | "用 pnpm 而不是 npm。提交前跑测试。" |
| **Skill** | Claude 可以使用的指令、知识和工作流程 | 可复用的内容、参考文档、可重复的任务 | `/deploy` 运行你的部署清单；API 文档端点模式的 skill |
| **Subagent** | 返回汇总结果的隔离执行上下文 | 上下文隔离、并行任务、专项工作 | 读大量文件但只返回关键发现的调研任务 |
| **[代理团队](./agent-teams)** | 协调多个独立的 Claude Code session | 并行调研、新功能开发、用竞争假设来调试 | 派出审查员同时检查安全性、性能和测试 |
| **MCP** | 连接外部服务 | 外部数据或操作 | 查询数据库、发消息到 Slack、控制浏览器 |
| **Hook** | 针对事件运行的确定性脚本 | 可预测的自动化，不需要 LLM | 每次文件编辑后跑 ESLint |

**[Plugin](./plugins)** 是包装层。Plugin 把 skill、hook、subagent 和 MCP 服务器捆绑成一个可安装单元。Plugin 中的 skill 有命名空间（如 `/my-plugin:review`），所以多个 plugin 可以共存。当你想在多个仓库中复用同一套配置，或通过**[市场](./plugin-marketplaces)**分发给别人时，就用 plugin。

### 相似功能的区分

有些功能看起来很像。下面说说怎么区分。

### Skill vs Subagent

Skill 和 subagent 解决不同的问题：

* **Skill** 是可复用的内容，你可以加载到任何上下文中
* **Subagent** 是独立的执行者，和你的主对话分开运行

| 方面 | Skill | Subagent |
| ---------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| **是什么** | 可复用的指令、知识或工作流程 | 有自己上下文的独立执行者 |
| **主要优势** | 跨环境共享内容 | 上下文隔离。工作独立进行，只返回摘要 |
| **最适合** | 参考资料、可调用的工作流程 | 需要读大量文件的任务、并行工作、专项执行者 |

**Skill 可以是参考型或操作型。** 参考型 skill 提供 Claude 在整个 session 中使用的知识（如 API 风格指南）。操作型 skill 告诉 Claude 执行特定操作（如 `/deploy` 运行部署流程）。

**需要上下文隔离或上下文窗口快满时，用 subagent。** Subagent 可能会读几十个文件或做大范围搜索，但你的主对话只收到摘要。由于 subagent 的工作不消耗你的主上下文，当你不需要看中间过程时也很有用。自定义 subagent 可以有自己的指令并预加载 skill。

**它们可以组合。** Subagent 可以预加载特定 skill（`skills:` 字段）。Skill 可以用 `context: fork` 在隔离上下文中运行。详见 [Skill](./skills)。


### CLAUDE.md vs Skill

两者都存储指令，但加载方式和用途不同。

| 方面 | CLAUDE.md | Skill |
| ---------------------------------- | ---------------------------- | --------------------------------------- |
| **加载时机** | 每次 session，自动 | 按需 |
| **可以包含文件** | 是，`@path` 导入 | 是，`@path` 导入 |
| **可以触发工作流程** | 不行 | 可以，用 `/<name>` |
| **最适合** | "永远要做 X"的规则 | 参考资料、可调用的工作流程 |

**放进 CLAUDE.md**：Claude 应该始终知道的东西——编码约定、构建命令、项目结构、"绝不要做 X"的规则。

**做成 skill**：Claude 偶尔需要的参考资料（API 文档、风格指南），或用 `/<name>` 触发的工作流程（部署、审查、发布）。

**经验法则：** CLAUDE.md 保持 200 行以内。如果越来越长，把参考内容移到 skill 里，或者拆分到 [`.claude/rules/`](./memory#organize-rules-with-clauderules) 文件中。


### CLAUDE.md vs 规则 vs Skill

三者都存储指令，但加载方式不同：

| 方面 | CLAUDE.md | `.claude/rules/` | Skill |
| ------------ | ----------------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| **加载时机** | 每次 session | 每次 session 或打开匹配文件时 | 按需、调用或相关时 |
| **作用范围** | 整个项目 | 可以限定到特定文件路径 | 特定任务 |
| **最适合** | 核心约定和构建命令 | 特定语言或目录的指南 | 参考资料、可重复的工作流程 |

**用 CLAUDE.md** 放每次 session 都需要的指令：构建命令、测试约定、项目架构。

**用规则** 让 CLAUDE.md 保持精简。带 [`paths` frontmatter](./memory#path-specific-rules) 的规则只在 Claude 使用匹配文件时才加载，节省上下文空间。

**用 skill** 放 Claude 只是偶尔需要的东西，比如 API 文档或用 `/<name>` 触发的部署清单。


### Subagent vs 代理团队

两者都能并行工作，但架构不同：

* **Subagent** 在你的 session 中运行，把结果报告回你的主上下文
* **代理团队**是相互通信的独立 Claude Code session

| 方面 | Subagent | 代理团队 |
| ----------------- | ------------------------------------------------ | --------------------------------------------------- |
| **上下文** | 自己的上下文窗口；结果返回给调用者 | 自己的上下文窗口；完全独立 |
| **通信** | 只向主代理报告结果 | 队友之间直接互相发消息 |
| **协调** | 主代理管理所有工作 | 共享任务列表，自行协调 |
| **最适合** | 只关注结果的专项任务 | 需要讨论和协作的复杂工作 |
| **Token 开销** | 较低：结果摘要返回主上下文 | 较高：每个队友都是独立的 Claude 实例 |

**需要快速、专注的执行者时用 subagent**：调研问题、验证结论、审查文件。Subagent 完成工作返回摘要，你的主对话保持干净。

**队友之间需要分享发现、互相质疑、独立协调时用代理团队。** 代理团队最适合研究竞争假设、并行代码审查和新功能开发——每个成员负责一个独立部分。

**什么时候升级：** 如果你在跑并行 subagent 但碰到了上下文限制，或者 subagent 之间需要互相通信，代理团队就是自然的下一步。

**注意**

代理团队还在实验阶段，默认禁用。详见[代理团队](./agent-teams)。


### MCP vs Skill

MCP 把 Claude 连接到外部服务。Skill 扩展 Claude 的知识，包括如何有效使用这些服务。

| 方面 | MCP | Skill |
| -------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| **是什么** | 连接外部服务的协议 | 知识、工作流程和参考资料 |
| **提供** | 工具和数据访问 | 知识、工作流程、参考资料 |
| **示例** | Slack 集成、数据库查询、浏览器控制 | 代码审查清单、部署工作流程、API 风格指南 |

这两个解决不同的问题，而且配合得很好：

**MCP** 让 Claude 能跟外部系统交互。没有 MCP，Claude 就没法查询你的数据库或发消息到 Slack。

**Skill** 给 Claude 提供如何有效使用这些工具的知识，以及可以用 `/<name>` 触发的工作流程。比如一个 skill 可以包含你团队的数据库 schema 和查询模式，或者一个带有你团队消息格式规范的 `/post-to-slack` 工作流程。

示例：MCP 服务器把 Claude 连接到你的数据库。一个 skill 教会 Claude 你的数据模型、常用查询模式以及不同任务该查哪些表。

### 功能的层级关系

功能可以在多个层级定义：用户级、项目级、通过 plugin、或通过托管策略。你也可以在子目录中嵌套 CLAUDE.md 文件，或把 skill 放在 monorepo 的特定包里。当同一功能在多个层级存在时，层级关系如下：

* **CLAUDE.md 文件**是叠加的：所有层级的内容同时贡献给 Claude 的上下文。启动时加载工作目录及以上目录中的文件；子目录的文件在你使用它们时加载。指令冲突时，Claude 会自行判断，通常优先遵循更具体的指令。详见[如何加载 CLAUDE.md 文件](./memory#how-claudemd-files-load)。
* **Skill 和 subagent** 按名称覆盖：同名时，根据优先级只有一个生效（托管 > 用户 > 项目 for skill；托管 > CLI 标志 > 项目 > 用户 > plugin for subagent）。Plugin 中的 skill 有[命名空间](./plugins#add-skills-to-your-plugin)以避免冲突。详见 [Skill 发现](./skills#where-skills-live)和 [subagent 作用域](./sub-agents#choose-the-subagent-scope)。
* **MCP 服务器**按名称覆盖：本地 > 项目 > 用户。详见 [MCP 作用域](./mcp#scope-hierarchy-and-precedence)。
* **Hook** 是合并的：所有注册的 hook 都会在匹配事件时触发，不管来源。详见 [Hook](./hooks)。

### 组合使用

每个扩展解决不同的问题：CLAUDE.md 处理始终在线的上下文，skill 处理按需知识和工作流程，MCP 处理外部连接，subagent 处理隔离，hook 处理自动化。实际使用中会根据工作流程把它们组合起来。比如，你可以用 CLAUDE.md 写项目约定、用 skill 做部署工作流程、用 MCP 连数据库、用 hook 在每次编辑后跑 linting。各司其职。

| 模式 | 怎么配合 | 示例 |
| ---------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Skill + MCP** | MCP 提供连接；skill 教 Claude 怎么用好 | MCP 连接到你的数据库，一个 skill 记录你的 schema 和查询模式 |
| **Skill + Subagent** | 一个 skill 启动并行工作的 subagent | `/audit` skill 启动在隔离环境中工作的安全、性能和风格 subagent |
| **CLAUDE.md + Skill** | CLAUDE.md 放始终在线的规则；skill 放按需加载的参考资料 | CLAUDE.md 写"遵循我们的 API 约定"，一个 skill 包含完整的 API 风格指南 |
| **Hook + MCP** | Hook 通过 MCP 触发外部操作 | Claude 修改关键文件时，编辑后 hook 发 Slack 通知 |

## 了解上下文成本

你添加的每个功能都会消耗 Claude 的一些上下文。太多的话不仅会填满上下文窗口，还会增加噪音，降低 Claude 的效率——skill 可能触发不正确，Claude 可能忘了你的约定。了解这些取舍能帮你建立高效的配置。

### 各功能的上下文成本

每个功能有不同的加载策略和上下文成本：

| 功能 | 何时加载 | 加载什么 | 上下文成本 |
| ---------------- | ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| **CLAUDE.md** | Session 开始 | 完整内容 | 每个请求都有 |
| **Skill** | Session 开始 + 使用时 | 开始时只加载描述，使用时加载完整内容 | 低（每个请求只有描述）\* |
| **MCP 服务器** | Session 开始 | 所有工具定义和 schema | 每个请求都有 |
| **Subagent** | 启动时 | 带有特定 skill 的全新上下文 | 与主 session 隔离 |
| **Hook** | 触发时 | 无（在外部运行） | 零，除非 hook 返回额外上下文 |

\*默认情况下，skill 描述在 session 开始时加载，让 Claude 能判断何时使用它们。在 skill 的 frontmatter 中设置 `disable-model-invocation: true` 可以完全隐藏它，直到你手动调用。对于你自己触发的 skill，这把上下文成本降到了零。

### 功能如何加载

每个功能在 session 中的不同时间点加载。下面解释各自的加载时机和上下文中的内容。

![上下文加载：CLAUDE.md 和 MCP 在 session 启动时加载并保留在每个请求中。Skill 开始时加载描述，调用时加载完整内容。Subagent 获得隔离上下文。Hook 在外部运行。](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/context-loading.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=729b5b634ba831d1d64772c6c9485b30)

### CLAUDE.md

**时机：** Session 开始

**加载什么：** 所有 CLAUDE.md 文件的完整内容（托管、用户和项目级别）。

**继承：** Claude 从工作目录开始向上遍历到根目录读取 CLAUDE.md 文件，访问子目录中的文件时会发现嵌套的 CLAUDE.md。详见[如何加载 CLAUDE.md 文件](./memory#how-claudemd-files-load)。

**提示**

CLAUDE.md 保持 500 行以内。参考资料移到 skill 里，按需加载。


### Skill

Skill 是 Claude 工具包中的额外能力。可以是参考资料（如 API 风格指南），也可以是用 `/<name>` 触发的工作流程（如 `/deploy`）。Claude Code 自带[捆绑 skill](./skills#bundled-skills)，比如 `/simplify`、`/batch` 和 `/debug`，开箱即用。你也可以创建自己的。Claude 会在合适的时候使用 skill，你也可以直接调用。

**时机：** 取决于 skill 的配置。默认情况下，描述在 session 开始时加载，完整内容在使用时加载。仅限手动调用的 skill（`disable-model-invocation: true`）在你调用前不会加载任何东西。

**加载什么：** 对于 Claude 可调用的 skill，Claude 在每个请求中能看到名称和描述。当你用 `/<name>` 或 Claude 自动调用 skill 时，完整内容加载到对话中。

**Claude 如何选择 skill：** Claude 把你的任务跟 skill 描述做匹配，判断哪些相关。如果描述模糊或重叠，Claude 可能加载错误的 skill 或错过有用的。要指定使用某个 skill，直接用 `/<name>` 调用。设了 `disable-model-invocation: true` 的 skill 在你调用前对 Claude 不可见。

**上下文成本：** 使用前很低。仅限手动调用的 skill 在被调用前成本为零。

**在 subagent 中：** Skill 在 subagent 中的行为不同。传给 subagent 的 skill 不是按需加载，而是在启动时完全预加载到上下文中。Subagent 不继承主 session 的 skill；你必须显式指定。

**提示**

有副作用的 skill 用 `disable-model-invocation: true`。这能节省上下文，并确保只有你手动触发。


### MCP 服务器

**时机：** Session 开始。

**加载什么：** 已连接服务器的所有工具定义和 JSON schema。

**上下文成本：** [工具搜索](./mcp#scale-with-mcp-tool-search)（默认启用）会把 MCP 工具的加载限制在上下文的 10%，其余推迟到需要时。

**可靠性提示：** MCP 连接可能在 session 中悄悄断开。如果服务器断连，它的工具会无声消失。Claude 可能尝试使用已经不存在的工具。如果 Claude 突然用不了之前能用的 MCP 工具，用 `/mcp` 检查连接状态。

**提示**

运行 `/mcp` 查看每个服务器的 token 开销。不常用的服务器可以断开。


### Subagent

**时机：** 按需，当你或 Claude 为某个任务启动一个时。

**加载什么：** 全新的隔离上下文，包含：

* 系统提示（与父级共享以提高缓存效率）
* 代理 `skills:` 字段中列出的 skill 的完整内容
* CLAUDE.md 和 git 状态（从父级继承）
* 主代理在 prompt 中传递的上下文

**上下文成本：** 与主 session 隔离。Subagent 不继承你的对话历史或已调用的 skill。

**提示**

不需要完整对话上下文的工作交给 subagent。它们的隔离能防止主 session 变臃肿。


### Hook

**时机：** 触发时。Hook 在特定的生命周期事件上触发，比如工具执行、session 边界、prompt 提交、权限请求和压缩。完整列表见 [Hook](./hooks)。

**加载什么：** 默认什么都不加载。Hook 作为外部脚本运行。

**上下文成本：** 零，除非 hook 返回的输出被添加到对话中。

**提示**

Hook 非常适合不需要影响 Claude 上下文的副作用（linting、日志记录）。

## 了解更多

每个功能都有自己的详细指南，包含设置说明、示例和配置选项。

### [CLAUDE.md](/en/memory)

存储项目上下文、约定和指令


### [Skill](/en/skills)

给 Claude 领域知识和可复用的工作流程


### [Subagent](/en/sub-agents)

把工作分派到隔离上下文中


### [代理团队](/en/agent-teams)

协调并行工作的多个 session


### [MCP](/en/mcp)

把 Claude 连接到外部服务


### [Hook](/en/hooks-guide)

用 hook 自动化工作流程


### [Plugin](/en/plugins)

打包和共享功能集


### [市场](/en/plugin-marketplaces)

托管和分发 plugin 集合
