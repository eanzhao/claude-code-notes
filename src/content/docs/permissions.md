---
title: "配置权限"
order: 49
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "使用细粒度的权限规则、模式和托管策略控制 Claude Code 可以访问和执行的操作。"
sourceUrl: "https://code.claude.com/docs/en/permissions.md"
sourceTitle: "Configure permissions"
tags: []
---
# 配置权限

> 通过细粒度的权限规则、模式和托管策略，精确控制 Claude Code 能做什么、不能做什么。

Claude Code 支持细粒度权限，让你精确指定 agent 可以执行哪些操作。权限设置可以签入版本控制，分发给团队里的每个人，也可以由各个开发者自行定制。

## 权限系统

Claude Code 使用分层权限系统来平衡能力和安全性：

| 工具类型 | 示例 | 需要审批 | "是，不再询问"的行为 |
| :--- | :--- | :--- | :--- |
| 只读 | 文件读取、Grep | 否 | 不适用 |
| Bash 命令 | Shell 执行 | 是 | 对每个项目目录和命令永久生效 |
| 文件修改 | 编辑/写入文件 | 是 | 仅在当前 session 内有效 |

## 管理权限

你可以用 `/permissions` 查看和管理 Claude Code 的工具权限。这个界面会列出所有权限规则及其来源的 settings.json 文件。

* **Allow** 规则：允许 Claude Code 使用指定工具，无需手动审批。
* **Ask** 规则：每当 Claude Code 尝试使用指定工具时，会弹出确认提示。
* **Deny** 规则：直接阻止 Claude Code 使用指定工具。

规则按顺序评估：**Deny -> Ask -> Allow**。第一个匹配的规则生效，所以 Deny 规则始终优先。

## 权限模式

Claude Code 支持多种权限模式来控制工具审批方式。在你的[设置文件](./settings#settings-files)中设置 `defaultMode`：

| 模式 | 说明 |
| :--- | :--- |
| `default` | 标准行为：首次使用每个工具时提示授权 |
| `acceptEdits` | 自动接受 session 内的文件编辑权限 |
| `plan` | Plan Mode：Claude 可以分析但不能修改文件或执行命令 |
| `dontAsk` | 除非通过 `/permissions` 或 `permissions.allow` 规则预先批准，否则自动拒绝工具 |
| `bypassPermissions` | 跳过权限提示，写入受保护目录除外（见下方警告）|

**警告** `bypassPermissions` 模式会跳过权限提示。写入 `.git`、`.claude`、`.vscode` 和 `.idea` 目录仍会弹出确认，防止意外破坏仓库状态和本地配置。对 `.claude/commands`、`.claude/agents` 和 `.claude/skills` 的写入不受限制也不会提示，因为 Claude 在创建技能、子 agent 和命令时本来就需要写入这些目录。仅在 Claude Code 无法造成破坏的隔离环境（如容器或虚拟机）中使用此模式。管理员可以在[托管设置](#managed-settings)中将 `disableBypassPermissionsMode` 设为 `"disable"` 来禁用此模式。

## 权限规则语法

权限规则的格式为 `Tool` 或 `Tool(specifier)`。

### 匹配工具的所有用法

不带括号的工具名称可匹配该工具的所有用法：

| 规则 | 效果 |
| :--- | :--- |
| `Bash` | 匹配所有 Bash 命令 |
| `WebFetch` | 匹配所有网络请求 |
| `Read` | 匹配所有文件读取 |

`Bash(*)` 等价于 `Bash`，匹配所有 Bash 命令。

### 用 specifier 做细粒度控制

在括号中添加 specifier 来匹配特定的工具用法：

| 规则 | 效果 |
| :--- | :--- |
| `Bash(npm run build)` | 匹配精确命令 `npm run build` |
| `Read(./.env)` | 匹配读取当前目录下的 `.env` 文件 |
| `WebFetch(domain:example.com)` | 匹配对 example.com 的请求 |

### 通配符模式

Bash 规则支持 `*` 通配符。通配符可以出现在命令中的任何位置。下面的配置允许 npm 和 git commit 命令，同时阻止 git push：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

`*` 之前的空格很重要：`Bash(ls *)` 匹配 `ls -la` 但不匹配 `lsof`，而 `Bash(ls*)` 两者都匹配。旧版 `:*` 后缀语法与 ` *` 等效，但已弃用。

## 工具特定的权限规则

### Bash

Bash 权限规则支持 `*` 通配符匹配。通配符可以出现在命令中的任何位置，包括开头、中间或结尾：

* `Bash(npm run build)` 精确匹配 `npm run build`
* `Bash(npm run test *)` 匹配以 `npm run test` 开头的命令
* `Bash(npm *)` 匹配以 `npm ` 开头的命令
* `Bash(* install)` 匹配以 ` install` 结尾的命令
* `Bash(git * main)` 匹配 `git checkout main`、`git merge main` 等

当 `*` 出现在末尾且前面有空格时（如 `Bash(ls *)`），会强制匹配单词边界，要求前缀后跟空格或字符串结束。例如 `Bash(ls *)` 匹配 `ls -la` 但不匹配 `lsof`。而不带空格的 `Bash(ls*)` 两者都匹配，因为没有单词边界约束。

**提示**

Claude Code 能识别 shell 操作符（如 `&&`），所以像 `Bash(safe-cmd *)` 这样的前缀匹配规则不会授权运行 `safe-cmd && other-cmd`。当你用"是，不再询问"批准复合命令时，Claude Code 会为每个需要批准的子命令分别保存规则，而不是保存整条复合命令。比如批准 `git status && npm test` 会保存 `npm test` 的规则，之后无论 `&&` 前面是什么都能识别 `npm test`。像 `cd` 进入子目录这样的子命令会为该路径生成自己的读取规则。单条复合命令最多保存 5 条规则。

**警告**

试图限制命令参数的 Bash 权限模式其实很脆弱。比如 `Bash(curl http://github.com/ *)` 想把 curl 限制在 GitHub URL，但以下变体都不会被匹配：

* URL 前有选项：`curl -X GET http://github.com/...`
* 不同协议：`curl https://github.com/...`
* 重定向：`curl -L http://bit.ly/xyz`（重定向到 GitHub）
* 变量：`URL=http://github.com && curl $URL`
* 多余空格：`curl  http://github.com`

如果需要更可靠的 URL 过滤，可以考虑：

* **限制 Bash 网络工具**：用 Deny 规则阻止 `curl`、`wget` 等命令，然后用 WebFetch 工具配合 `WebFetch(domain:github.com)` 权限来处理允许的域名
* **使用 PreToolUse hook**：实现一个 hook 来验证 Bash 命令中的 URL，阻止不允许的域名
* 通过 CLAUDE.md 指导 Claude Code 使用允许的 curl 模式

注意，单独使用 WebFetch 并不能阻止网络访问。如果允许了 Bash，Claude 仍然可以用 `curl`、`wget` 或其他工具访问任意 URL。

### Read 和 Edit

`Edit` 规则适用于所有内置的文件编辑工具。Claude 会尽力将 `Read` 规则应用于 Grep 和 Glob 等所有内置的文件读取工具。

**警告**

Read 和 Edit 的 Deny 规则只适用于 Claude 的内置文件工具，不适用于 Bash 子进程。`Read(./.env)` 的 Deny 规则会阻止 Read 工具，但不会阻止 Bash 中的 `cat .env`。如果需要操作系统级别的强制阻止所有进程访问某些路径，请[启用沙箱](./sandboxing)。

Read 和 Edit 规则都遵循 [gitignore](https://git-scm.com/docs/gitignore) 规范，有四种路径模式：

| 模式 | 含义 | 示例 | 匹配 |
| --- | --- | --- | --- |
| `//path` | 文件系统根目录的**绝对**路径 | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**` |
| `~/path` | **home** 目录路径 | `Read(~/Documents/*.pdf)` | `/Users/alice/Documents/*.pdf` |
| `/path` | **相对于项目根目录**的路径 | `Edit(/src/**/*.ts)` | `/src/**/*.ts` |
| `path` 或 `./path` | **相对于当前目录**的路径 | `Read(*.env)` | `<cwd>/*.env` |

**警告**

像 `/Users/alice/file` 这样的模式不是绝对路径，而是相对于项目根目录的。绝对路径请用 `//Users/alice/file`。

在 Windows 上，路径在匹配前会标准化为 POSIX 格式。`C:\Users\alice` 变为 `/c/Users/alice`，所以用 `//c/**/.env` 来匹配该驱动器上任意位置的 `.env` 文件。要匹配所有驱动器，用 `//**/.env`。

示例：
* `Edit(/docs/**)` — 编辑 `/docs/` 下的文件（不是 `/.claude/docs/`）
* `Read(~/.zshrc)` — 读取 home 目录的 `.zshrc`
* `Edit(//tmp/scratch.txt)` — 编辑绝对路径 `/tmp/scratch.txt`
* `Read(src/**)` — 从 `<当前目录>/src/` 读取

**注意**

在 gitignore 模式中，`*` 匹配单个目录中的文件，而 `**` 跨目录递归匹配。要允许所有文件访问，直接用不带括号的工具名：`Read`、`Edit` 或 `Write`。

### WebFetch

* `WebFetch(domain:example.com)` 匹配对 example.com 的请求

### MCP

* `mcp__puppeteer` 匹配 `puppeteer` 服务器提供的所有工具（在 Claude Code 中配置的名称）
* `mcp__puppeteer__*` 通配符语法也匹配 `puppeteer` 服务器中的所有工具
* `mcp__puppeteer__puppeteer_navigate` 匹配 `puppeteer` 服务器提供的 `puppeteer_navigate` 工具

### Agent（子 agent）

用 `Agent(AgentName)` 规则控制 Claude 可以使用哪些[子 agent](./sub-agents)：

* `Agent(Explore)` 匹配 Explore 子 agent
* `Agent(Plan)` 匹配 Plan 子 agent
* `Agent(my-custom-agent)` 匹配名为 `my-custom-agent` 的自定义子 agent

将这些规则添加到设置的 `deny` 数组中，或用 `--disallowedTools` CLI 标志来禁用特定 agent。禁用 Explore agent 的示例：

```json
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## 通过 hook 扩展权限

[Claude Code hook](./hooks-guide) 提供了一种注册自定义 shell 命令来在运行时做权限判断的机制。当 Claude Code 调用工具时，PreToolUse hook 会在权限提示之前运行。hook 的输出可以拒绝工具调用、强制提示或跳过提示让调用继续。

跳过提示并不会绕过权限规则。hook 返回 `"allow"` 后，仍会评估 Deny 和 Ask 规则，所以匹配的 Deny 规则仍然会阻止调用。这保持了[管理权限](#manage-permissions)中所述的 Deny 优先原则，包括托管设置中定义的 Deny 规则。

## 工作目录

默认情况下，Claude 有权访问其启动目录中的文件。你可以扩展访问范围：

* **启动时**：使用 `--add-dir <path>` CLI 参数
* **session 内**：使用 `/add-dir` 命令
* **持久配置**：在[设置文件](./settings#settings-files)中添加 `additionalDirectories`

附加目录中的文件遵循与原始工作目录相同的权限规则：无需提示即可读取，文件编辑权限遵循当前权限模式。

## 权限与沙箱的关系

权限和[沙箱](./sandboxing)是互补的安全层：

* **权限** 控制 Claude Code 可以使用哪些工具、访问哪些文件或域名，适用于所有工具（Bash、Read、Edit、WebFetch、MCP 等）。
* **沙箱** 提供操作系统级别的强制隔离，限制 Bash 工具的文件系统和网络访问，仅适用于 Bash 命令及其子进程。

两者结合实现纵深防御：
* 权限 Deny 规则阻止 Claude 尝试访问受限资源
* 沙箱限制防止 Bash 命令越界访问，即使 prompt injection 绕过了 Claude 的决策也不行
* 沙箱中的文件系统限制复用 Read 和 Edit 的 Deny 规则，不需要单独的沙箱配置
* 网络限制将 WebFetch 权限规则与沙箱的 `allowedDomains` 列表结合使用

## 托管设置

对于需要集中管控 Claude Code 配置的组织，管理员可以部署不可被用户或项目设置覆盖的托管设置。这些策略设置使用与普通设置文件相同的 JSON 格式，可通过 MDM/OS 级策略、托管设置文件或[服务器托管设置](./server-managed-settings)来下发。具体的分发机制和文件位置请参阅[设置文件](./settings#settings-files)。

### 仅限托管的设置

以下设置仅在托管设置中生效：

| 设置 | 说明 |
| :--- | :--- |
| `disableBypassPermissionsMode` | 设为 `"disable"` 可禁用 `bypassPermissions` 模式和 `--dangerously-skip-permissions` 标志 |
| `allowManagedPermissionRulesOnly` | 为 `true` 时，阻止用户和项目设置定义 `allow`、`ask` 或 `deny` 权限规则，仅托管设置中的规则生效 |
| `allowManagedHooksOnly` | 为 `true` 时，阻止加载用户、项目和插件 hook，只允许托管 hook 和 SDK hook |
| `allowManagedMcpServersOnly` | 为 `true` 时，只考虑托管设置中的 `allowedMcpServers`。`deniedMcpServers` 仍从所有来源合并。参见[托管 MCP 配置](./mcp#managed-mcp-configuration) |
| `blockedMarketplaces` | 市场来源的黑名单。在下载前就会检查，所以被阻止的来源永远不会碰到文件系统。参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions) |
| `sandbox.network.allowManagedDomainsOnly` | 为 `true` 时，只有托管设置中的 `allowedDomains` 和 `WebFetch(domain:...)` Allow 规则生效。不允许的域名自动阻止，不提示用户。Deny 域名仍从所有来源合并 |
| `sandbox.filesystem.allowManagedReadPathsOnly` | 为 `true` 时，只考虑托管设置中的 `allowRead` 路径。用户、项目和本地设置的 `allowRead` 条目被忽略 |
| `strictKnownMarketplaces` | 控制用户可以添加哪些插件市场。参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions) |
| `allow_remote_sessions` | 为 `true` 时，允许用户启动 [Remote Control](./remote-control) 和 [Web session](./claude-code-on-the-web)。默认为 `true`。设为 `false` 可阻止远程 session 访问 |

## 设置优先级

权限规则与所有其他 Claude Code 设置遵循相同的[设置优先级](./settings#settings-precedence)：

1. **托管设置**：不可被任何其他级别覆盖，包括命令行参数
2. **命令行参数**：临时 session 覆盖
3. **本地项目设置** (`.claude/settings.local.json`)
4. **共享项目设置** (`.claude/settings.json`)
5. **用户设置** (`~/.claude/settings.json`)

如果某个工具在任何级别被 Deny，其他级别都无法 Allow 它。比如 `--allowedTools` 无法覆盖托管设置的 Deny，而 `--disallowedTools` 可以在托管设置之外添加额外限制。

如果某个权限在用户设置中是 Allow 但在项目设置中是 Deny，项目设置优先，该权限会被阻止。

## 配置示例

这个[仓库](https://github.com/anthropics/claude-code/tree/main/examples/settings)包含常见部署场景的入门设置配置。可以作为起点，根据你的需求调整。

## 另请参阅

* [设置](./settings)：完整的配置参考，包括权限设置表
* [沙箱](./sandboxing)：Bash 命令的操作系统级文件系统和网络隔离
* [认证](./authentication)：设置 Claude Code 的用户访问
* [安全](./security)：安全保障和最佳实践
* [Hooks](./hooks-guide)：自动化工作流和扩展权限评估
