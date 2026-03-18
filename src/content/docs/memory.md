---
title: "Claude 如何记住您的项目"
order: 6
section: "core-concepts"
sectionLabel: "核心概念"
sectionOrder: 2
summary: "通过 CLAUDE.md 文件给予 Claude 持久指令，并让 Claude 通过自动记忆自动积累学习内容。"
sourceUrl: "https://code.claude.com/docs/en/memory.md"
sourceTitle: "How Claude remembers your project"
tags: []
---
# Claude 如何记住你的项目

> 通过 CLAUDE.md 文件给 Claude 持久指令，让 Claude 通过自动记忆积累学习内容。

每个 Claude Code session 都从一个全新的上下文窗口开始。两种机制在 session 之间传递知识：

* **CLAUDE.md 文件**：你写的指令，给 Claude 提供持久上下文
* **自动记忆**：Claude 根据你的纠正和偏好自己写的笔记

本页介绍如何：

* [编写和整理 CLAUDE.md 文件](#claudemd-files)
* [用 `.claude/rules/` 为特定文件类型设置规则](#organize-rules-with-clauderules)
* [配置自动记忆](#auto-memory)让 Claude 自动做笔记
* [排查问题](#troubleshoot-memory-issues)，当指令没被遵循时

## CLAUDE.md 与自动记忆

Claude Code 有两个互补的记忆系统。两者都在每次对话开始时加载。Claude 把它们当作上下文而非强制配置。你的指令越具体简洁，Claude 就越能稳定地遵循。

|                      | CLAUDE.md 文件 | 自动记忆 |
| :-------------------- | :------------------------------------------------ | :---------------------------------------------------------------------------- |
| **谁写的** | 你 | Claude |
| **包含什么** | 指令和规则 | 学到的经验和模式 |
| **作用范围** | 项目、用户或组织 | 每个 worktree |
| **加载时机** | 每次 session | 每次 session（前 200 行） |
| **用途** | 编码规范、工作流程、项目架构 | Claude 发现的构建命令、调试心得、偏好 |

想引导 Claude 的行为，用 CLAUDE.md 文件。让 Claude 从你的纠正中学习而无需手动操作，用自动记忆。

Subagent 也可以维护自己的自动记忆。详见 [subagent 配置](./sub-agents#enable-persistent-memory)。

## CLAUDE.md 文件

CLAUDE.md 文件是 Markdown 文件，给项目、个人工作流程或整个组织提供 Claude 的持久指令。你以纯文本形式编写，Claude 在每次 session 开始时读取。

### 选择 CLAUDE.md 文件的位置

CLAUDE.md 文件可以放在多个位置，每个位置有不同的作用范围。更具体的位置优先于更宽泛的。

| 范围 | 位置 | 用途 | 示例 | 共享给 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| **托管策略** | macOS：`/Library/Application Support/ClaudeCode/CLAUDE.md`、Linux 和 WSL：`/etc/claude-code/CLAUDE.md`、Windows：`C:\Program Files\ClaudeCode\CLAUDE.md` | IT/DevOps 管理的组织级指令 | 公司编码规范、安全策略、合规要求 | 组织中的所有用户 |
| **项目指令** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目指令 | 项目架构、编码规范、通用工作流程 | 团队成员（通过版本控制） |
| **用户指令** | `~/.claude/CLAUDE.md` | 所有项目的个人偏好 | 代码风格偏好、个人工具快捷方式 | 只有你（所有项目） |

工作目录上方目录层次中的 CLAUDE.md 文件在启动时完整加载。子目录中的 CLAUDE.md 文件会在 Claude 读取那些目录中的文件时按需加载。完整的解析顺序见[如何加载 CLAUDE.md 文件](#how-claudemd-files-load)。

大型项目可以用[项目规则](#organize-rules-with-clauderules)把指令拆分成按主题组织的文件。规则允许你把指令限定到特定文件类型或子目录。

### 设置项目 CLAUDE.md

项目 CLAUDE.md 可以放在 `./CLAUDE.md` 或 `./.claude/CLAUDE.md`。创建这个文件，写上适用于项目所有参与者的指令：构建和测试命令、编码规范、架构决策、命名约定、通用工作流程。这些指令通过版本控制和团队共享，所以重点放在项目级规范上，别写个人偏好。

**提示**

运行 `/init` 可以自动生成起始 CLAUDE.md。Claude 会分析你的代码库，用发现的构建命令、测试指令和项目约定创建文件。如果 CLAUDE.md 已存在，`/init` 会建议改进而不是覆盖。然后你可以补充 Claude 自己发现不了的指令。设置 `CLAUDE_CODE_NEW_INIT=true` 启用交互式多阶段流程。`/init` 会问你要设置哪些内容：CLAUDE.md 文件、skill 和 hook。然后用 subagent 探索代码库，通过追问填补空白，在写文件前先给你审查建议。

### 写出有效的指令

CLAUDE.md 文件在每次 session 开始时加载到上下文窗口中，会消耗 token。因为它是上下文而非强制配置，你的写法会影响 Claude 遵循的程度。具体、简洁、结构清晰的指令效果最好。

**长度**：每个 CLAUDE.md 文件目标 200 行以内。越长消耗的上下文越多，遵循度也会下降。如果指令太多，用 [imports](#import-additional-files) 或 [`.claude/rules/`](#organize-rules-with-clauderules) 拆分。

**结构**：用 Markdown 标题和列表把相关指令分组。Claude 扫描结构的方式跟人一样：有组织的段落比密密麻麻的大段文字容易理解。

**具体性**：写出能验证的具体指令。比如：

* "用 2 个空格缩进"而不是"好好格式化代码"
* "提交前运行 `npm test`"而不是"测试你的修改"
* "API handler 放在 `src/api/handlers/`"而不是"把文件组织好"

**一致性**：如果两条规则互相矛盾，Claude 可能随机选一条。定期检查你的 CLAUDE.md 文件、子目录中的嵌套 CLAUDE.md 和 [`.claude/rules/`](#organize-rules-with-clauderules)，删掉过时或冲突的指令。在 monorepo 中，用 [`claudeMdExcludes`](#exclude-specific-claudemd-files) 跳过其他团队跟你无关的 CLAUDE.md 文件。

### 导入其他文件

CLAUDE.md 文件可以用 `@path/to/import` 语法导入其他文件。导入的文件在启动时展开，和引用它们的 CLAUDE.md 一起加载到上下文中。

相对路径和绝对路径都可以。相对路径基于包含导入的文件所在目录解析，而非工作目录。导入的文件可以递归导入其他文件，最深五层。

要引入 README、package.json 和工作流程指南，在 CLAUDE.md 中任意位置用 `@` 语法引用：

```text
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

个人偏好不想签入版本控制的话，从主目录导入文件。导入写在共享的 CLAUDE.md 中，但指向的文件留在你的机器上：

```text
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

**警告**

Claude Code 第一次在项目中遇到外部导入时，会弹出审批对话框列出文件。如果你拒绝，导入会被禁用，且不会再弹出。

更结构化的指令组织方式，见 [`.claude/rules/`](#organize-rules-with-clauderules)。

### CLAUDE.md 文件如何加载

Claude Code 从当前工作目录开始向上遍历目录树，检查沿途每个目录中的 CLAUDE.md 文件。也就是说，如果你在 `foo/bar/` 中运行 Claude Code，它会加载 `foo/bar/CLAUDE.md` 和 `foo/CLAUDE.md`。

Claude 也会发现当前工作目录下子目录中的 CLAUDE.md 文件。它们不在启动时加载，而是在 Claude 读取这些子目录中的文件时才加载。

如果你在大型 monorepo 中工作，上级目录的 CLAUDE.md 文件可能包含跟你无关的指令，用 [`claudeMdExcludes`](#exclude-specific-claudemd-files) 跳过它们。

#### 从其他目录加载

`--add-dir` 标志让 Claude 能访问主工作目录外的其他目录。默认不加载这些目录中的 CLAUDE.md 文件。

要加载其他目录中的 CLAUDE.md 文件（包括 `CLAUDE.md`、`.claude/CLAUDE.md` 和 `.claude/rules/*.md`），设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` 环境变量：

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### 用 `.claude/rules/` 组织规则

大型项目可以用 `.claude/rules/` 目录把指令组织成多个文件。这样指令保持模块化，团队维护起来也方便。规则还能[限定到特定文件路径](#path-specific-rules)，只在 Claude 处理匹配文件时加载，减少噪音节省上下文。

**注意**

规则在每次 session 或打开匹配文件时加载到上下文中。不需要始终在上下文中的特定任务指令，改用 [skill](./skills)——只在你调用或 Claude 判断相关时才加载。

#### 设置规则

把 Markdown 文件放在项目的 `.claude/rules/` 目录中。每个文件覆盖一个主题，用描述性的文件名，比如 `testing.md` 或 `api-design.md`。所有 `.md` 文件会递归发现，所以你可以用子目录组织，比如 `frontend/` 或 `backend/`：

```text
your-project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       └── security.md     # Security requirements
```

没有 [`paths` frontmatter](#path-specific-rules) 的规则在启动时加载，优先级和 `.claude/CLAUDE.md` 相同。

#### 路径特定规则

规则可以用 YAML frontmatter 的 `paths` 字段限定到特定文件。这些条件规则只在 Claude 处理匹配文件时才生效。

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

不带 `paths` 字段的规则无条件加载，适用于所有文件。带路径的规则在 Claude 读取匹配文件时触发，而非每次工具使用时。

`paths` 字段中用 glob 模式按扩展名、目录或任意组合匹配文件：

| 模式 | 匹配 |
| ---------------------- | ---------------------------------------------------- |
| `**/*.ts` | 任何目录中的所有 TypeScript 文件 |
| `src/**/*` | `src/` 目录下的所有文件 |
| `*.md` | 项目根目录中的 Markdown 文件 |
| `src/components/*.tsx` | 特定目录中的 React 组件 |

可以指定多个模式，也能用大括号展开在一个模式中匹配多种扩展名：

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### 用符号链接跨项目共享规则

`.claude/rules/` 目录支持符号链接，你可以维护一套共享规则并链接到多个项目中。符号链接正常解析和加载，循环链接能正确检测和处理。下面的例子链接了一个共享目录和一个单独文件：

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### 用户级规则

`~/.claude/rules/` 中的个人规则适用于你机器上的所有项目。放不是项目特定的偏好：

```text
~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows
```

用户级规则在项目规则之前加载，项目规则有更高的优先级。

### 大型团队的 CLAUDE.md 管理

跨团队部署 Claude Code 的组织，可以集中管理指令并控制加载哪些 CLAUDE.md 文件。

#### 组织级部署 CLAUDE.md

组织可以部署集中管理的 CLAUDE.md，适用于机器上的所有用户。这个文件无法被个人设置排除。

### 在托管策略位置创建文件

* macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
* Linux 和 WSL：`/etc/claude-code/CLAUDE.md`
* Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`


### 用配置管理系统部署

用 MDM、组策略、Ansible 或类似工具在开发者机器间分发文件。其他组织级配置选项见[托管设置](./permissions#managed-settings)。

托管 CLAUDE.md 和[托管设置](./settings#settings-files)用途不同。技术强制用设置，行为引导用 CLAUDE.md：

| 关注点 | 配置位置 |
| :------------------------------------------ | :-------------------------------------------------------- |
| 禁止特定工具、命令或文件路径 | 托管设置：`permissions.deny` |
| 强制沙箱隔离 | 托管设置：`sandbox.enabled` |
| 环境变量和 API 路由 | 托管设置：`env` |
| 认证方式和组织锁定 | 托管设置：`forceLoginMethod`、`forceLoginOrgUUID` |
| 代码风格和质量指南 | 托管 CLAUDE.md |
| 数据处理和合规提醒 | 托管 CLAUDE.md |
| Claude 的行为指令 | 托管 CLAUDE.md |

无论 Claude 想做什么，设置规则都由客户端强制执行。CLAUDE.md 指令影响 Claude 的行为，但不是硬性强制层。

#### 排除特定 CLAUDE.md 文件

大型 monorepo 中，上级目录的 CLAUDE.md 文件可能包含跟你无关的指令。`claudeMdExcludes` 设置让你按路径或 glob 模式跳过特定文件。

下面这个例子排除了上级文件夹的顶级 CLAUDE.md 和规则目录。把它放在 `.claude/settings.local.json` 中，这样排除项只在你的机器上生效：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

用 glob 语法匹配绝对文件路径。`claudeMdExcludes` 可以在任何[设置层](./settings#settings-files)配置：用户、项目、本地或托管策略。数组跨层合并。

托管策略的 CLAUDE.md 文件无法被排除。这保证了组织级指令始终生效。

## 自动记忆

自动记忆让 Claude 无需你写任何东西就能积累跨 session 的知识。Claude 工作时会为自己做笔记：构建命令、调试心得、架构备注、代码风格偏好和工作流程习惯。Claude 不是每次 session 都保存东西，它会判断哪些信息对未来的对话有用才记下来。

**注意**

自动记忆需要 Claude Code v2.1.59 或更高版本。用 `claude --version` 检查。

### 开启或关闭自动记忆

自动记忆默认开启。要切换它，在 session 中运行 `/memory` 用开关控制，或在项目设置中设置 `autoMemoryEnabled`：

```json
{
  "autoMemoryEnabled": false
}
```

也可以通过环境变量禁用：`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。

### 存储位置

每个项目有自己的记忆目录：`~/.claude/projects//memory/`。`` 路径来自 git 仓库，所以同一仓库中的所有 worktree 和子目录共享一个自动记忆目录。不在 git 仓库中的话，使用项目根目录。

要把自动记忆存到别的位置，在用户或本地设置中设置 `autoMemoryDirectory`：

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

策略、本地和用户设置都接受这个配置。项目设置（`.claude/settings.json`）不接受，以防共享项目把自动记忆重定向到敏感位置。

目录包含 `MEMORY.md` 入口文件和可选的主题文件：

```text
~/.claude/projects//memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` 是记忆目录的索引。Claude 在整个 session 中读写这个目录中的文件，用 `MEMORY.md` 跟踪内容存放位置。

自动记忆是本机的。同一 git 仓库中的所有 worktree 和子目录共享一个自动记忆目录。文件不会在机器或云环境之间共享。

### 工作原理

`MEMORY.md` 的前 200 行在每次对话开始时加载。200 行以后的内容不会在 session 开始时加载。Claude 通过把详细笔记移到单独的主题文件来保持 `MEMORY.md` 精简。

这个 200 行限制只针对 `MEMORY.md`。CLAUDE.md 文件不管多长都完整加载，不过越短遵循度越好。

`debugging.md` 或 `patterns.md` 这样的主题文件启动时不加载。Claude 需要信息时用标准文件工具按需读取。

Claude 在 session 期间读写记忆文件。当你在 Claude Code 界面中看到"正在写入记忆"或"已调用记忆"时，说明 Claude 正在更新或读取 `~/.claude/projects//memory/`。

### 审查和编辑记忆

自动记忆文件就是普通的 Markdown 文件，你可以随时编辑或删除。运行 [`/memory`](#view-and-edit-with-memory) 在 session 中浏览和打开记忆文件。

## 用 `/memory` 查看和编辑

`/memory` 命令列出当前 session 中加载的所有 CLAUDE.md 和规则文件，让你开关自动记忆，还提供打开自动记忆文件夹的链接。选择任何文件可以在编辑器中打开。

当你让 Claude 记住某些东西，比如"永远用 pnpm 而不是 npm"或"记住 API 测试需要本地 Redis 实例"，Claude 会保存到自动记忆中。要往 CLAUDE.md 添加指令，直接跟 Claude 说"把这个加到 CLAUDE.md"，或通过 `/memory` 自己编辑。

## 排查记忆问题

这些是 CLAUDE.md 和自动记忆最常见的问题及排查步骤。

### Claude 没遵循我的 CLAUDE.md

CLAUDE.md 的内容作为用户消息传递，不是系统提示的一部分。Claude 会读取并尝试遵循，但不能保证严格执行，尤其是模糊或冲突的指令。

排查步骤：

* 运行 `/memory` 验证你的 CLAUDE.md 文件是否被加载。如果没列出来，Claude 看不到它。
* 检查相关 CLAUDE.md 是否在会被加载的位置（见[选择 CLAUDE.md 文件的位置](#choose-where-to-put-claudemd-files)）。
* 把指令写得更具体。"用 2 个空格缩进"比"好好格式化代码"有效得多。
* 检查 CLAUDE.md 文件之间是否有冲突指令。如果两个文件对同一行为给出不同指导，Claude 可能随机选一个。

要在系统提示级别注入指令，用 [`--append-system-prompt`](./cli-reference#system-prompt-flags)。这个参数每次调用都要传，所以比起交互使用更适合脚本和自动化。

**提示**

用 [`InstructionsLoaded` hook](./hooks#instructionsloaded) 可以精确记录加载了哪些指令文件、何时加载、为什么加载。这对排查子目录中路径特定规则或延迟加载的文件很有用。

### 不知道自动记忆保存了什么

运行 `/memory` 选择自动记忆文件夹，浏览 Claude 保存的内容。全部是普通 Markdown，你可以读、改或删。

### 我的 CLAUDE.md 太大了

超过 200 行的文件消耗更多上下文，遵循度也可能下降。把详细内容移到 `@path` 导入引用的单独文件中（见[导入其他文件](#import-additional-files)），或拆分到 `.claude/rules/` 文件中。

### `/compact` 之后指令好像丢了

CLAUDE.md 完全不受压缩影响。`/compact` 之后，Claude 会从磁盘重新读取 CLAUDE.md 并注入到 session 中。如果指令在压缩后消失了，说明它只是在对话中口头说的，没写进 CLAUDE.md。把它加到 CLAUDE.md 里才能跨 session 持久保留。

关于长度、结构和具体性的指导，见[写出有效的指令](#write-effective-instructions)。

## 相关资源

* [Skill](./skills)：打包按需加载的可复用工作流程
* [设置](./settings)：用设置文件配置 Claude Code 行为
* [管理 session](https://code.claude.com/docs/en/sessions)：管理上下文、恢复对话和运行并行 session
* [Subagent 记忆](./sub-agents#enable-persistent-memory)：让 subagent 维护自己的自动记忆
