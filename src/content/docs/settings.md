---
title: "Claude Code 设置"
order: 48
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "使用全局和项目级设置以及环境变量配置 Claude Code。"
sourceUrl: "https://code.claude.com/docs/en/settings.md"
sourceTitle: "Claude Code settings"
tags: []
---
# Claude Code 设置

> 通过全局和项目级设置及环境变量来配置 Claude Code。

Claude Code 提供了丰富的设置来定制其行为。在交互式 REPL 中运行 `/config` 命令即可打开分页式设置界面，查看状态信息和修改配置选项。

## 配置范围

Claude Code 使用**范围系统**来决定配置的作用范围和共享对象。理解范围有助于你决定如何配置 Claude Code——无论是个人使用、团队协作还是企业部署。

### 可用范围

| 范围 | 位置 | 影响谁 | 与团队共享？ |
| :--- | :--- | :--- | :--- |
| **托管** | 服务器托管设置、plist/注册表或系统级 `managed-settings.json` | 机器上的所有用户 | 是（由 IT 部署）|
| **用户** | `~/.claude/` 目录 | 你自己，跨所有项目 | 否 |
| **项目** | 仓库中的 `.claude/` | 该仓库的所有协作者 | 是（提交到 git）|
| **本地** | `.claude/settings.local.json` | 仅你自己在该仓库中 | 否（git 忽略）|

### 何时使用每个范围

**托管范围**适合：

* 必须在整个组织范围内执行的安全策略
* 不可推翻的合规性要求
* IT/DevOps 部署的标准化配置

**用户范围**适合：

* 你希望在所有项目中通用的个人偏好（主题、编辑器设置等）
* 你在所有项目中使用的工具和插件
* API 密钥和认证信息（安全存储）

**项目范围**适合：

* 团队共享设置（权限、hook、MCP 服务器）
* 整个团队都应该有的插件
* 统一协作者的工具配置

**本地范围**适合：

* 针对特定项目的个人覆盖
* 在分享给团队之前测试配置
* 不适用于其他机器的本机特定设置

### 范围之间的交互

当同一个设置在多个范围中都有配置时，更具体的范围优先：

1. **托管**（最高）— 不可被任何其他级别覆盖
2. **命令行参数** — 临时 session 覆盖
3. **本地** — 覆盖项目和用户设置
4. **项目** — 覆盖用户设置
5. **用户**（最低）— 没有其他级别指定时生效

例如，如果某个权限在用户设置中是 Allow 但在项目设置中是 Deny，项目设置优先，该权限会被阻止。

### 各范围的适用对象

范围适用于 Claude Code 的多种功能：

| 功能 | 用户位置 | 项目位置 | 本地位置 |
| :--- | :--- | :--- | :--- |
| **设置** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **子 agent** | `~/.claude/agents/` | `.claude/agents/` | 无 |
| **MCP 服务器** | `~/.claude.json` | `.mcp.json` | `~/.claude.json`（按项目）|
| **插件** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` 或 `.claude/CLAUDE.md` | 无 |

---

## 设置文件

`settings.json` 文件是配置 Claude Code 的官方机制，通过分层设置实现：

* **用户设置**定义在 `~/.claude/settings.json` 中，适用于所有项目。
* **项目设置**保存在项目目录中：
  * `.claude/settings.json` 用于签入版本控制、与团队共享的设置
  * `.claude/settings.local.json` 用于不签入的设置，适合个人偏好和实验。Claude Code 会在创建时自动配置 git 忽略 `.claude/settings.local.json`。
* **托管设置**：对于需要集中管控的组织，Claude Code 支持多种托管设置的分发机制。所有机制使用相同的 JSON 格式，且不可被用户或项目设置覆盖：

  * **服务器托管设置**：通过 Claude.ai 管理控制台从 Anthropic 服务器下发。参见[服务器托管设置](./server-managed-settings)。
  * **MDM/操作系统级策略**：通过 macOS 和 Windows 原生设备管理下发：
    * macOS：`com.anthropic.claudecode` 托管偏好域（通过 Jamf、Kandji 或其他 MDM 工具的配置文件部署）
    * Windows：`HKLM\SOFTWARE\Policies\ClaudeCode` 注册表项，其中 `Settings` 值（REG\_SZ 或 REG\_EXPAND\_SZ）包含 JSON（通过组策略或 Intune 部署）
    * Windows（用户级）：`HKCU\SOFTWARE\Policies\ClaudeCode`（最低策略优先级，仅在没有管理级来源时使用）
  * **基于文件**：`managed-settings.json` 和 `managed-mcp.json` 部署到系统目录：

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux 和 WSL：`/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`


**警告**

从 v2.1.75 开始，不再支持旧版 Windows 路径 `C:\ProgramData\ClaudeCode\managed-settings.json`。管理员需要将文件迁移到 `C:\Program Files\ClaudeCode\managed-settings.json`。

  详情参见[托管设置](./permissions#managed-only-settings)和[托管 MCP 配置](./mcp#managed-mcp-configuration)。


**注意**

托管部署还可以用 `strictKnownMarketplaces` 来限制**插件市场的添加**。详情参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions)。

* **其他配置**存储在 `~/.claude.json` 中。该文件包含你的偏好（主题、通知设置、编辑器模式）、OAuth session、用户和本地范围的 [MCP 服务器](./mcp)配置、按项目的状态（允许的工具、信任设置）以及各种缓存。项目范围的 MCP 服务器单独存储在 `.mcp.json` 中。

**注意** Claude Code 会自动创建配置文件的带时间戳备份，保留最近五份以防数据丢失。

```JSON Example settings.json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

示例中的 `$schema` 行指向 Claude Code 设置的[官方 JSON Schema](https://json.schemastore.org/claude-code-settings.json)。把它加到 `settings.json` 中可以在 VS Code、Cursor 等支持 JSON Schema 验证的编辑器中获得自动补全和内联校验。

### 可用设置

`settings.json` 支持以下选项：

| 键 | 说明 | 示例 |
| :--- | :--- | :--- |
| `apiKeyHelper` | 自定义脚本，在 `/bin/sh` 中执行，生成认证值。该值会作为 `X-Api-Key` 和 `Authorization: Bearer` 标头发送 | `/bin/generate_temp_api_key.sh` |
| `autoMemoryDirectory` | [自动记忆](./memory#storage-location)存储的自定义目录。支持 `~/` 路径展开。不接受项目设置 (`.claude/settings.json`) 中的值，防止共享仓库将记忆写入重定向到敏感位置。可在策略、本地和用户设置中使用 | `"~/my-memory-dir"` |
| `cleanupPeriodDays` | 超过此天数不活跃的 session 会在启动时删除（默认 30 天）。设为 `0` 会在启动时删除所有现有记录并完全禁用 session 持久化。不会写入新的 `.jsonl` 文件，`/resume` 不会显示任何对话，hook 会收到空的 `transcript_path`。 | `20` |
| `companyAnnouncements` | 启动时向用户显示的公告。如果有多条公告，会随机轮播。 | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env` | 应用于每个 session 的环境变量 | `{"FOO": "bar"}` |
| `attribution` | 自定义 git commit 和 PR 的署名。参见[署名设置](#attribution-settings) | `{"commit": "🤖 Generated with Claude Code", "pr": ""}` |
| `includeCoAuthoredBy` | **已弃用**：请用 `attribution` 代替。是否在 git commit 和 PR 中包含 `co-authored-by Claude` 署名（默认 `true`） | `false` |
| `includeGitInstructions` | 在 Claude 的系统提示中包含内置的 commit 和 PR 工作流说明（默认 `true`）。设为 `false` 可移除这些指令，比如使用自己的 git 工作流技能时。设置时 `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 环境变量优先于此设置 | `false` |
| `permissions` | 权限结构，详见下面的表格。 | |
| `hooks` | 配置在生命周期事件中运行的自定义命令。参见 [hook 文档](./hooks) | 参见 [Hooks](./hooks) |
| `disableAllHooks` | 禁用所有 [hook](./hooks) 和任何自定义[状态行](./statusline) | `true` |
| `allowManagedHooksOnly` | （仅限托管设置）阻止加载用户、项目和插件 hook。只允许托管 hook 和 SDK hook。参见 [Hook 配置](#hook-configuration) | `true` |
| `allowedHttpHookUrls` | HTTP hook 可以请求的 URL 模式白名单。支持 `*` 通配符。设置后，URL 不匹配的 hook 会被阻止。未定义 = 无限制，空数组 = 阻止所有 HTTP hook。数组跨设置来源合并。参见 [Hook 配置](#hook-configuration) | `["https://hooks.example.com/*"]` |
| `httpHookAllowedEnvVars` | HTTP hook 可以插入到标头中的环境变量白名单。设置后，每个 hook 的有效 `allowedEnvVars` 是其自身列表与此列表的交集。未定义 = 无限制。数组跨设置来源合并。参见 [Hook 配置](#hook-configuration) | `["MY_TOKEN", "HOOK_SECRET"]` |
| `allowManagedPermissionRulesOnly` | （仅限托管设置）阻止用户和项目设置定义 `allow`、`ask` 或 `deny` 权限规则。仅托管设置中的规则生效。参见[仅限托管设置](./permissions#managed-only-settings) | `true` |
| `allowManagedMcpServersOnly` | （仅限托管设置）只考虑托管设置中的 `allowedMcpServers`。`deniedMcpServers` 仍从所有来源合并。用户仍可添加 MCP 服务器，但只有管理员定义的白名单生效。参见[托管 MCP 配置](./mcp#managed-mcp-configuration) | `true` |
| `model` | 覆盖 Claude Code 使用的默认模型 | `"claude-sonnet-4-6"` |
| `availableModels` | 限制用户可通过 `/model`、`--model`、配置工具或 `ANTHROPIC_MODEL` 选择的模型。不影响默认选项。参见[限制模型选择](./model-config#restrict-model-selection) | `["sonnet", "haiku"]` |
| `modelOverrides` | 将 Anthropic 模型 ID 映射到特定提供商的模型 ID，如 Bedrock 推理配置文件 ARN。每个模型选择器条目在调用提供商 API 时使用其映射值。参见[覆盖每个版本的模型 ID](./model-config#override-model-ids-per-version) | `{"claude-opus-4-6": "arn:aws:bedrock:..."}` |
| `effortLevel` | 跨 session 保持[努力级别](./model-config#adjust-effort-level)。接受 `"low"`、`"medium"` 或 `"high"`。运行 `/effort low`、`/effort medium` 或 `/effort high` 时自动写入。Opus 4.6 和 Sonnet 4.6 支持 | `"medium"` |
| `otelHeadersHelper` | 用于生成动态 OpenTelemetry 标头的脚本。启动时定期运行（参见[动态标头](./monitoring-usage#dynamic-headers)）| `/bin/generate_otel_headers.sh` |
| `statusLine` | 配置自定义状态行以显示上下文信息。参见[状态行文档](./statusline) | `{"type": "command", "command": "~/.claude/statusline.sh"}` |
| `fileSuggestion` | 为 `@` 文件自动补全配置自定义脚本。参见[文件建议设置](#file-suggestion-settings) | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}` |
| `respectGitignore` | 控制 `@` 文件选择器是否遵循 `.gitignore` 模式。为 `true`（默认）时，匹配 `.gitignore` 模式的文件会从建议中排除 | `false` |
| `outputStyle` | 配置输出风格以调整系统提示。参见[输出风格文档](./output-styles) | `"Explanatory"` |
| `agent` | 将主线程作为指定子 agent 运行。应用该子 agent 的系统提示、工具限制和模型。参见[显式调用子 agent](./sub-agents#invoke-subagents-explicitly) | `"code-reviewer"` |
| `forceLoginMethod` | 用 `claudeai` 限制登录 Claude.ai 账号，用 `console` 限制登录 Claude 控制台（API 计费）账号 | `claudeai` |
| `forceLoginOrgUUID` | 指定组织的 UUID，在登录时自动选择该组织，跳过组织选择步骤。需要同时设置 `forceLoginMethod` | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` |
| `enableAllProjectMcpServers` | 自动批准项目 `.mcp.json` 文件中定义的所有 MCP 服务器 | `true` |
| `enabledMcpjsonServers` | `.mcp.json` 文件中要批准的特定 MCP 服务器列表 | `["memory", "github"]` |
| `disabledMcpjsonServers` | `.mcp.json` 文件中要拒绝的特定 MCP 服务器列表 | `["filesystem"]` |
| `allowedMcpServers` | 在 managed-settings.json 中设置时，允许用户配置的 MCP 服务器白名单。未定义 = 无限制，空数组 = 全部锁定。适用于所有范围。Deny 优先。参见[托管 MCP 配置](./mcp#managed-mcp-configuration) | `[{ "serverName": "github" }]` |
| `deniedMcpServers` | 在 managed-settings.json 中设置时，明确阻止的 MCP 服务器黑名单。适用于所有范围，包括托管服务器。黑名单优先于白名单。参见[托管 MCP 配置](./mcp#managed-mcp-configuration) | `[{ "serverName": "filesystem" }]` |
| `strictKnownMarketplaces` | 在 managed-settings.json 中设置时，允许用户添加的插件市场白名单。未定义 = 无限制，空数组 = 全部锁定。仅适用于市场添加。参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions) | `[{ "source": "github", "repo": "acme-corp/plugins" }]` |
| `blockedMarketplaces` | （仅限托管设置）市场来源黑名单。在下载前就会检查，所以被阻止的来源永远不会碰到文件系统。参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions) | `[{ "source": "github", "repo": "untrusted/plugins" }]` |
| `pluginTrustMessage` | （仅限托管设置）自定义消息，附加到安装前显示的插件信任警告中。用于添加组织特定的上下文，例如确认来自内部市场的插件已经过审查。 | `"All plugins from our marketplace are approved by IT"` |
| `awsAuthRefresh` | 修改 `.aws` 目录的自定义脚本（参见[高级凭据配置](./amazon-bedrock#advanced-credential-configuration)）| `aws sso login --profile myprofile` |
| `awsCredentialExport` | 输出 AWS 凭据 JSON 的自定义脚本（参见[高级凭据配置](./amazon-bedrock#advanced-credential-configuration)）| `/bin/generate_aws_grant.sh` |
| `alwaysThinkingEnabled` | 默认为所有 session 启用[扩展思考](./common-workflows#use-extended-thinking-thinking-mode)。通常通过 `/config` 命令配置，而不是直接编辑 | `true` |
| `plansDirectory` | 自定义计划文件的存储位置。路径相对于项目根目录。默认 `~/.claude/plans` | `"./plans"` |
| `spinnerVerbs` | 自定义 spinner 中显示的动作词和转动持续时间消息。`mode` 设为 `"replace"` 只用你的词，`"append"` 则追加到默认值 | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}` |
| `language` | 配置 Claude 的首选响应语言（如 `"japanese"`、`"spanish"`、`"french"`）。Claude 默认会用该语言响应。也设置[语音听写](./voice-dictation#change-the-dictation-language)语言 | `"japanese"` |
| `voiceEnabled` | 启用一键通[语音听写](./voice-dictation)。运行 `/voice` 时自动写入。需要 Claude.ai 账号 | `true` |
| `autoUpdatesChannel` | 更新频道。`"stable"` 获取约一周前的稳定版本并跳过有重大回归的版本，`"latest"`（默认）获取最新版本 | `"stable"` |
| `spinnerTipsEnabled` | Claude 工作时在 spinner 中显示提示。设为 `false` 可禁用提示（默认 `true`） | `false` |
| `spinnerTipsOverride` | 用自定义字符串覆盖 spinner 提示。`tips`：提示字符串数组。`excludeDefault`：为 `true` 时只显示自定义提示；为 `false` 或不存在时，自定义提示与内置提示合并 | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }` |
| `prefersReducedMotion` | 减少或禁用 UI 动画（旋转、闪烁等效果）以提高无障碍性 | `true` |
| `fastModePerSessionOptIn` | 为 `true` 时，快速模式不会跨 session 持续。每个 session 启动时快速模式关闭，需要用户用 `/fast` 手动启用。用户的快速模式偏好仍会保存。参见[需要每个 session 选择加入](./fast-mode#require-per-session-opt-in) | `true` |
| `teammateMode` | [Agent 团队](./agent-teams)队友的显示方式：`auto`（在 tmux 或 iTerm2 中选择分割窗格，否则 in-process）、`in-process` 或 `tmux`。参见[设置 Agent 团队](./agent-teams#set-up-agent-teams) | `"in-process"` |
| `feedbackSurveyRate` | [session 质量调查](./data-usage#session-quality-surveys)在符合条件时出现的概率（0-1）。设为 `0` 可完全抑制。使用 Bedrock、Vertex 或 Foundry 时默认采样率不适用，这时很有用 | `0.05` |

### 全局配置设置

以下显示偏好存储在 `~/.claude.json` 而不是 `settings.json` 中。把它们加到 `settings.json` 里会触发 Schema 验证错误。

| 键 | 说明 | 示例 |
| :--- | :--- | :--- |
| `showTurnDuration` | 响应后显示回合耗时，如"耗时 1m 6s"。默认 `true`。直接编辑 `~/.claude.json` 修改 | `false` |
| `terminalProgressBarEnabled` | 在支持的终端（如 Windows Terminal 和 iTerm2）中显示终端进度条。默认 `true`。在 `/config` 中显示为 **终端进度条** | `false` |

### Worktree 设置

配置 `--worktree` 如何创建和管理 git worktree。用这些设置可以减少大型 monorepo 的磁盘占用和启动时间。

| 键 | 说明 | 示例 |
| :--- | :--- | :--- |
| `worktree.symlinkDirectories` | 从主仓库符号链接到每个 worktree 的目录，避免复制大型目录。默认无符号链接目录 | `["node_modules", ".cache"]` |
| `worktree.sparsePaths` | 通过 git 稀疏检出（cone 模式）在每个 worktree 中检出的目录。只有列出的路径会写入磁盘，在大型 monorepo 中更快 | `["packages/my-app", "shared/utils"]` |

### 权限设置

| 键 | 说明 | 示例 |
| :--- | :--- | :--- |
| `allow` | Allow 权限规则数组。模式匹配详情参见[权限规则语法](#permission-rule-syntax) | `[ "Bash(git diff *)" ]` |
| `ask` | Ask 权限规则数组，使用工具时需要确认。参见[权限规则语法](#permission-rule-syntax) | `[ "Bash(git push *)" ]` |
| `deny` | Deny 权限规则数组。用这个来排除 Claude Code 对敏感文件的访问。参见[权限规则语法](#permission-rule-syntax)和 [Bash 权限限制](./permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories` | Claude 有权访问的附加[工作目录](./permissions#working-directories) | `[ "../docs/" ]` |
| `defaultMode` | 打开 Claude Code 时的默认[权限模式](./permissions#permission-modes) | `"acceptEdits"` |
| `disableBypassPermissionsMode` | 设为 `"disable"` 可禁用 `bypassPermissions` 模式。这会同时禁用 `--dangerously-skip-permissions` 命令行标志。参见[托管设置](./permissions#managed-only-settings) | `"disable"` |

### 权限规则语法

权限规则的格式为 `Tool` 或 `Tool(specifier)`。规则按顺序评估：先 Deny，再 Ask，最后 Allow。第一个匹配的规则生效。

简单示例：

| 规则 | 效果 |
| :--- | :--- |
| `Bash` | 匹配所有 Bash 命令 |
| `Bash(npm run *)` | 匹配以 `npm run` 开头的命令 |
| `Read(./.env)` | 匹配读取 `.env` 文件 |
| `WebFetch(domain:example.com)` | 匹配对 example.com 的请求 |

完整的规则语法参考（包括通配符行为、Read/Edit/WebFetch/MCP/Agent 各工具的特定模式，以及 Bash 模式的安全限制）请参见[权限规则语法](./permissions#permission-rule-syntax)。

### 沙箱设置

配置高级沙箱行为。沙箱将 Bash 命令与文件系统和网络隔离。详情参见[沙箱](./sandboxing)。

| 键 | 说明 | 示例 |
| :--- | :--- | :--- |
| `enabled` | 启用 Bash 沙箱（macOS、Linux 和 WSL2）。默认 false | `true` |
| `autoAllowBashIfSandboxed` | 在沙箱中自动批准 Bash 命令。默认 true | `true` |
| `excludedCommands` | 应在沙箱外运行的命令 | `["git", "docker"]` |
| `allowUnsandboxedCommands` | 允许命令通过 `dangerouslyDisableSandbox` 参数在沙箱外运行。为 `false` 时完全禁用该逃生口，所有命令都必须在沙箱中运行（或在 `excludedCommands` 中）。适合需要严格沙箱的企业策略。默认 true | `false` |
| `filesystem.allowWrite` | 沙箱命令可以写入的额外路径。数组在所有设置范围内合并（而非替换）。也与 `Edit(...)` Allow 权限规则中的路径合并。参见[路径前缀](#sandbox-path-prefixes)。 | `["//tmp/build", "~/.kube"]` |
| `filesystem.denyWrite` | 沙箱命令不可写入的路径。数组在所有设置范围内合并。也与 `Edit(...)` Deny 权限规则中的路径合并。 | `["//etc", "//usr/local/bin"]` |
| `filesystem.denyRead` | 沙箱命令不可读取的路径。数组在所有设置范围内合并。也与 `Read(...)` Deny 权限规则中的路径合并。 | `["~/.aws/credentials"]` |
| `filesystem.allowRead` | 在 `denyRead` 区域内重新允许读取的路径。优先于 `denyRead`。数组在所有设置范围内合并。用来创建仅限工作区的读取访问模式。 | `["."]` |
| `filesystem.allowManagedReadPathsOnly` | （仅限托管设置）只考虑托管设置中的 `allowRead` 路径。来自用户、项目和本地设置的 `allowRead` 条目被忽略。默认 false | `true` |
| `network.allowUnixSockets` | 沙箱中可访问的 Unix socket 路径（用于 SSH agent 等） | `["~/.ssh/agent-socket"]` |
| `network.allowAllUnixSockets` | 允许沙箱中的所有 Unix socket 连接。默认 false | `true` |
| `network.allowLocalBinding` | 允许绑定到 localhost 端口（仅 macOS）。默认 false | `true` |
| `network.allowedDomains` | 允许出站网络流量的域名数组。支持通配符（如 `*.example.com`）。 | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | （仅限托管设置）只有托管设置中的 `allowedDomains` 和 `WebFetch(domain:...)` Allow 规则生效。来自用户、项目和本地设置的域名被忽略。不允许的域名自动阻止，不提示用户。Deny 域名仍从所有来源合并。默认 false | `true` |
| `network.httpProxyPort` | 自带 HTTP 代理端口。未指定时 Claude 会运行自己的代理。 | `8080` |
| `network.socksProxyPort` | 自带 SOCKS5 代理端口。未指定时 Claude 会运行自己的代理。 | `8081` |
| `enableWeakerNestedSandbox` | 为非特权 Docker 环境启用较弱的沙箱（仅 Linux 和 WSL2）。**会降低安全性。** 默认 false | `true` |
| `enableWeakerNetworkIsolation` | （仅 macOS）允许沙箱访问系统 TLS 信任服务 (`com.apple.trustd.agent`)。`gh`、`gcloud`、`terraform` 等基于 Go 的工具在配合 `httpProxyPort` 使用 MITM 代理和自定义 CA 时需要验证 TLS 证书。**会降低安全性，因为打开了潜在的数据泄露通道**。默认 false | `true` |

#### 沙箱路径前缀

`filesystem.allowWrite`、`filesystem.denyWrite`、`filesystem.denyRead` 和 `filesystem.allowRead` 中的路径支持以下前缀：

| 前缀 | 含义 | 示例 |
| :--- | :--- | :--- |
| `//` | 文件系统根目录的绝对路径 | `//tmp/build` 变为 `/tmp/build` |
| `~/` | 相对于 home 目录 | `~/.kube` 变为 `$HOME/.kube` |
| `/` | 相对于设置文件所在目录 | `/build` 变为 `$SETTINGS_DIR/build` |
| `./` 或无前缀 | 相对路径（由沙箱运行时解析） | `./output` |

**配置示例：**

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**文件系统和网络限制**可以通过两种方式配置（两者会合并）：

* **`sandbox.filesystem` 设置**（如上所示）：控制操作系统级沙箱边界的路径。这些限制适用于所有子进程命令（如 `kubectl`、`terraform`、`npm`），而不仅仅是 Claude 的文件工具。
* **权限规则**：用 `Edit` Allow/Deny 规则控制 Claude 文件工具的访问，用 `Read` Deny 规则阻止读取，用 `WebFetch` Allow/Deny 规则控制网络域名。这些规则中的路径也会合并到沙箱配置中。

### 署名设置

Claude Code 会为 git commit 和 PR 添加署名。两者分别配置：

* commit 默认使用 [git trailers](https://git-scm.com/docs/git-interpret-trailers)（如 `Co-Authored-By`），可自定义或禁用
* PR 描述是纯文本

| 键 | 说明 |
| :--- | :--- |
| `commit` | git commit 的署名，包括所有 trailer。空字符串可隐藏 commit 署名 |
| `pr` | PR 描述的署名。空字符串可隐藏 PR 署名 |

**默认 commit 署名：**

```text
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**默认 PR 署名：**

```text
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**示例：**

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

**注意**

`attribution` 设置优先于已弃用的 `includeCoAuthoredBy` 设置。要隐藏所有署名，把 `commit` 和 `pr` 都设为空字符串。

### 文件建议设置

为 `@` 文件路径自动补全配置自定义命令。内置文件建议使用快速文件系统遍历，但大型 monorepo 可能受益于项目特定的索引（如预构建的文件索引或自定义工具）。

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

该命令使用与 [hook](./hooks) 相同的环境变量运行，包括 `CLAUDE_PROJECT_DIR`。它通过 stdin 接收带 `query` 字段的 JSON：

```json
{"query": "src/comp"}
```

输出换行分隔的文件路径到 stdout（当前限制 15 个）：

```text
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**示例：**

```bash
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook 配置

这些设置控制哪些 hook 允许运行以及 HTTP hook 可以访问什么。`allowManagedHooksOnly` 只能在[托管设置](#settings-files)中配置。URL 和环境变量白名单可以在任何设置级别设置，跨来源合并。

**当 `allowManagedHooksOnly` 为 `true` 时：**

* 托管 hook 和 SDK hook 正常加载
* 用户 hook、项目 hook、插件 hook 被屏蔽

**限制 HTTP hook URL：**

限制 HTTP hook 可以请求的 URL。支持 `*` 通配符。定义后，URL 不匹配的 HTTP hook 会被静默阻止。

```json
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**限制 HTTP hook 环境变量：**

限制 HTTP hook 可以插入到标头值中的环境变量名称。每个 hook 的有效 `allowedEnvVars` 是其自身列表与此设置的交集。

```json
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### 设置优先级

设置按以下优先级应用（从高到低）：

1. **托管设置**（[服务器托管](./server-managed-settings)、[MDM/操作系统级策略](#configuration-scopes)或[托管设置](./settings#settings-files)）
   * IT 通过服务器、MDM 配置文件、注册表策略或托管设置文件部署的策略
   * 不可被任何其他级别覆盖，包括命令行参数
   * 在托管层内，优先级为：服务器托管 > MDM/操作系统级策略 > `managed-settings.json` > HKCU 注册表（仅限 Windows）。只使用一个托管来源，不会合并。

2. **命令行参数**
   * 针对特定 session 的临时覆盖

3. **本地项目设置** (`.claude/settings.local.json`)
   * 个人的项目特定设置

4. **共享项目设置** (`.claude/settings.json`)
   * 签入版本控制、团队共享的项目设置

5. **用户设置** (`~/.claude/settings.json`)
   * 个人全局设置

这种层级确保组织策略始终得到执行，同时团队和个人仍可定制自己的体验。

比如你的用户设置允许 `Bash(npm run *)`，但项目的共享设置拒绝了它，那么项目设置优先，该命令会被阻止。

**注意**

**数组设置跨范围合并。** 当同一个数组设置（如 `sandbox.filesystem.allowWrite` 或 `permissions.allow`）出现在多个范围中时，数组会被**拼接并去重**，而非替换。低优先级范围可以添加条目而不会覆盖高优先级范围设置的条目，反之亦然。例如托管设置将 `allowWrite` 设为 `["//opt/company-tools"]`，用户添加 `["~/.kube"]`，两个路径都会包含在最终配置中。

### 验证当前设置

在 Claude Code 中运行 `/status` 可以查看哪些设置来源处于活动状态及其来源。输出显示每个配置层（托管、用户、项目）及其来源，如 `Enterprise managed settings (remote)`、`Enterprise managed settings (plist)`、`Enterprise managed settings (HKLM)` 或 `Enterprise managed settings (file)`。如果设置文件包含错误，`/status` 会报告问题方便你修复。

### 配置系统要点

* **记忆文件 (`CLAUDE.md`)**：包含 Claude 在启动时加载的指令和上下文
* **设置文件 (JSON)**：配置权限、环境变量和工具行为
* **技能**：可用 `/skill-name` 调用或由 Claude 自动加载的自定义提示
* **MCP 服务器**：通过附加工具和集成扩展 Claude Code
* **优先级**：高级别配置（托管）优先于低级别配置（用户/项目）
* **继承**：设置会合并，更具体的设置会添加到或覆盖更广泛的设置

### 系统提示

Claude Code 的内部系统提示未公开发布。要添加自定义指令，请使用 `CLAUDE.md` 文件或 `--append-system-prompt` 标志。

### 排除敏感文件

要阻止 Claude Code 访问包含 API 密钥、密钥和环境文件等敏感信息的文件，在 `.claude/settings.json` 中使用 `permissions.deny` 设置：

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

这取代了已弃用的 `ignorePatterns` 配置。匹配这些模式的文件会从文件发现和搜索结果中排除，对这些文件的读取操作会被拒绝。

## 子 agent 配置

Claude Code 支持可在用户和项目级别配置的自定义 AI 子 agent。这些子 agent 存储为带 YAML frontmatter 的 Markdown 文件：

* **用户子 agent**：`~/.claude/agents/` — 在你的所有项目中可用
* **项目子 agent**：`.claude/agents/` — 特定于项目，可与团队共享

子 agent 文件定义具有自定义提示和工具权限的专用 AI 助手。在[子 agent 文档](./sub-agents)中了解更多关于创建和使用子 agent 的信息。

## 插件配置

Claude Code 支持插件系统，让你通过技能、agent、hook 和 MCP 服务器扩展功能。插件通过市场分发，可在用户和仓库级别配置。

### 插件设置

`settings.json` 中与插件相关的设置：

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

控制启用哪些插件。格式：`"plugin-name@marketplace-name": true/false`

**范围**：

* **用户设置** (`~/.claude/settings.json`)：个人插件偏好
* **项目设置** (`.claude/settings.json`)：与团队共享的项目特定插件
* **本地设置** (`.claude/settings.local.json`)：本机覆盖（不提交）

**示例**：

```json
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

定义仓库应可使用的额外市场。通常在仓库级别设置，确保团队成员能访问所需的插件来源。

**当仓库包含 `extraKnownMarketplaces` 时**：

1. 团队成员信任该文件夹时，系统会提示安装市场
2. 然后提示从该市场安装插件
3. 用户可以跳过不需要的市场或插件（选择会存在用户设置中）
4. 安装尊重信任边界，需要明确同意

**示例**：

```json
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**市场来源类型**：

* `github`：GitHub 仓库（用 `repo`）
* `git`：任意 git URL（用 `url`）
* `directory`：本地文件系统路径（用 `path`，仅用于开发）
* `hostPattern`：匹配市场主机的正则表达式模式（用 `hostPattern`）

#### `strictKnownMarketplaces`

**仅限托管设置**：控制用户可以添加哪些插件市场。只能在[托管设置](./settings#settings-files)中配置，给管理员提供对市场来源的严格控制。

**托管设置文件位置**：

* **macOS**：`/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux 和 WSL**：`/etc/claude-code/managed-settings.json`
* **Windows**：`C:\Program Files\ClaudeCode\managed-settings.json`

**主要特点**：

* 仅在托管设置 (`managed-settings.json`) 中可用
* 不可被用户或项目设置覆盖（最高优先级）
* 在网络/文件系统操作前执行（被阻止的来源永远不会执行）
* 对来源规范使用精确匹配（包括 git 来源的 `ref`、`path`），`hostPattern` 除外（使用正则匹配）

**白名单行为**：

* `undefined`（默认）：无限制 — 用户可以添加任何市场
* 空数组 `[]`：完全锁定 — 用户无法添加任何新市场
* 来源列表：用户只能添加完全匹配的市场

**所有支持的来源类型**：

白名单支持七种市场来源类型。大多数来源使用精确匹配，而 `hostPattern` 使用正则匹配市场主机。

1. **GitHub 仓库**：

```json
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

字段：`repo`（必填）、`ref`（可选：分支/标签/SHA）、`path`（可选：子目录）

2. **Git 仓库**：

```json
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

字段：`url`（必填）、`ref`（可选：分支/标签/SHA）、`path`（可选：子目录）

3. **基于 URL 的市场**：

```json
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

字段：`url`（必填）、`headers`（可选：用于认证访问的 HTTP 标头）

**注意**

基于 URL 的市场仅下载 `marketplace.json` 文件，不会从服务器下载插件文件。基于 URL 的市场中的插件必须使用外部来源（GitHub、npm 或 git URL）而非相对路径。对于使用相对路径的插件，请改用基于 Git 的市场。详情参见[故障排除](./plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)。

4. **NPM 包**：

```json
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

字段：`package`（必填，支持 scoped 包）

5. **文件路径**：

```json
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

字段：`path`（必填：marketplace.json 文件的绝对路径）

6. **目录路径**：

```json
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

字段：`path`（必填：包含 `.claude-plugin/marketplace.json` 的目录绝对路径）

7. **主机模式匹配**：

```json
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

字段：`hostPattern`（必填：匹配市场主机的正则模式）

当你想允许来自特定主机的所有市场而不逐一列举每个仓库时，使用主机模式匹配。这对于有内部 GitHub Enterprise 或 GitLab 服务器、开发者会自建市场的组织特别有用。

按来源类型提取主机：

* `github`：始终匹配 `github.com`
* `git`：从 URL 提取主机名（支持 HTTPS 和 SSH 格式）
* `url`：从 URL 提取主机名
* `npm`、`file`、`directory`：不支持主机模式匹配

**配置示例**：

示例 — 仅允许特定市场：

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

示例 — 禁用所有市场添加：

```json
{
  "strictKnownMarketplaces": []
}
```

示例 — 允许来自内部 git 服务器的所有市场：

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**精确匹配要求**：

市场来源必须**完全**匹配才能被允许。对于基于 git 的来源（`github` 和 `git`），这包括所有可选字段：

* `repo` 或 `url` 必须完全匹配
* `ref` 字段必须完全匹配（或者两者都未定义）
* `path` 字段必须完全匹配（或者两者都未定义）

**不匹配**的来源示例：

```json
// These are DIFFERENT sources:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// These are also DIFFERENT:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**与 `extraKnownMarketplaces` 的对比**：

| 方面 | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| --- | --- | --- |
| **用途** | 组织策略执行 | 团队便利 |
| **设置文件** | 仅限 `managed-settings.json` | 任何设置文件 |
| **行为** | 阻止不在白名单中的添加 | 自动安装缺失的市场 |
| **执行时机** | 网络/文件系统操作之前 | 用户信任后弹出提示 |
| **可被覆盖** | 否（最高优先级） | 是（通过更高优先级的设置） |
| **来源格式** | 直接来源对象 | 带嵌套来源的命名市场 |
| **适用场景** | 合规、安全限制 | 新人入职、工具标准化 |

**格式差异**：

`strictKnownMarketplaces` 使用直接来源对象：

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` 需要指定市场名称：

```json
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**同时使用两者**：

`strictKnownMarketplaces` 是策略门：它控制用户可以添加什么，但不会注册任何市场。要同时限制和预注册市场，在 `managed-settings.json` 中两个都设置：

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

如果只设置了 `strictKnownMarketplaces`，用户仍然可以通过 `/plugin marketplace add` 手动添加允许的市场，但不会自动使用。

**重要说明**：

* 在任何网络请求或文件系统操作之前检查限制
* 被阻止时，用户会看到明确的错误消息，说明来源被托管策略阻止
* 限制仅适用于添加新市场；已安装的市场仍可访问
* 托管设置具有最高优先级，不可被覆盖

面向用户的文档参见[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions)。

### 管理插件

用 `/plugin` 命令可以交互式地管理插件：

* 从市场浏览可用插件
* 安装/卸载插件
* 启用/禁用插件
* 查看插件详情（提供的命令、agent、hook）
* 添加/删除市场

在[插件文档](./plugins)中了解更多关于插件系统的信息。

## 环境变量

环境变量让你无需编辑设置文件即可控制 Claude Code 的行为。也可以在 [`settings.json`](#available-settings) 的 `env` 键下配置任何变量，以将其应用到每个 session 或推广到团队。

完整列表参见[环境变量参考](./env-vars)。

## Claude 可用的工具

Claude Code 可以访问一组用于读取、编辑、搜索、运行命令和编排子 agent 的工具。工具名称就是你在权限规则和 hook 匹配器中使用的字符串。

完整列表和 Bash 工具行为详情参见[工具参考](./tools-reference)。

## 另请参阅

* [权限](./permissions)：权限系统、规则语法、工具特定模式和托管策略
* [认证](./authentication)：设置 Claude Code 的用户访问
* [故障排除](./troubleshooting)：常见配置问题的解决方案
