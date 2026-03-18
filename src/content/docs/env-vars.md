---
title: "环境变量"
order: 59
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "控制 Claude Code 行为的环境变量的完整参考。"
sourceUrl: "https://code.claude.com/docs/en/env-vars.md"
sourceTitle: "Environment variables"
tags: []
---
# 环境变量

> 控制 Claude Code 行为的环境变量完整参考。

Claude Code 支持以下环境变量来控制其行为。可以在启动 `claude` 前在 shell 中设置，也可以在 [`settings.json`](./settings#available-settings) 的 `env` 字段中配置，让它们应用到每个会话或在团队中统一推行。

| 变量 | 用途 |
| :------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY` | 作为 `X-Api-Key` 标头发送的 API 密钥。设置后会替代 Claude Pro、Max、Team 或 Enterprise 订阅。非交互模式 (`-p`) 下若存在则始终使用。交互模式下会提示你确认一次，之后会覆盖订阅。要恢复订阅，运行 `unset ANTHROPIC_API_KEY` |
| `ANTHROPIC_AUTH_TOKEN` | `Authorization` 标头的自定义值（设置的值会自动加上 `Bearer ` 前缀） |
| `ANTHROPIC_BASE_URL` | 覆盖 API 端点，用于通过代理或网关路由请求。设为非第一方主机时默认禁用 [MCP 工具搜索](./mcp#scale-with-mcp-tool-search)。如果代理会转发 `tool_reference` 块，可设置 `ENABLE_TOOL_SEARCH=true` |
| `ANTHROPIC_CUSTOM_HEADERS` | 添加到请求的自定义标头（`Name: Value` 格式，多个标头用换行符分隔） |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 详见[模型配置](./model-config#environment-variables) |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 详见[模型配置](./model-config#environment-variables) |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 详见[模型配置](./model-config#environment-variables) |
| `ANTHROPIC_FOUNDRY_API_KEY` | Microsoft Foundry 认证用的 API 密钥（详见 [Microsoft Foundry](./microsoft-foundry)） |
| `ANTHROPIC_FOUNDRY_BASE_URL` | Foundry 资源的完整基础 URL（如 `https://my-resource.services.ai.azure.com/anthropic`）。是 `ANTHROPIC_FOUNDRY_RESOURCE` 的替代方案（详见 [Microsoft Foundry](./microsoft-foundry)） |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry 资源名称（如 `my-resource`）。未设置 `ANTHROPIC_FOUNDRY_BASE_URL` 时必填（详见 [Microsoft Foundry](./microsoft-foundry)） |
| `ANTHROPIC_MODEL` | 要使用的模型名称（详见[模型配置](./model-config#environment-variables)） |
| `ANTHROPIC_SMALL_FAST_MODEL` | \[已弃用] [后台任务用的 Haiku 级模型](./costs)名称 |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | 使用 Bedrock 时覆盖 Haiku 级模型的 AWS 区域 |
| `AWS_BEARER_TOKEN_BEDROCK` | 用于认证的 Bedrock API 密钥（详见 [Bedrock API 密钥](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)） |
| `BASH_DEFAULT_TIMEOUT_MS` | 长时间运行的 bash 命令的默认超时时间 |
| `BASH_MAX_OUTPUT_LENGTH` | bash 输出被截断前的最大字符数 |
| `BASH_MAX_TIMEOUT_MS` | 模型可以为长时间运行的 bash 命令设置的最大超时时间 |
| `CLAUDECODE` | 在 Claude Code 生成的 shell 环境中设为 `1`（Bash 工具、tmux 会话）。不会在 [hook](./hooks) 或[状态栏](./statusline)命令中设置。用于检测脚本是否在 Claude Code 生成的 shell 内运行 |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 设置触发自动压缩的上下文容量百分比 (1-100)。默认约 95% 时触发。用更低的值（如 `50`）可提前压缩。高于默认阈值的值无效。适用于主对话和子代理。此百分比与[状态栏](./statusline)中的 `context_window.used_percentage` 字段一致 |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | 每条 Bash 命令后返回原始工作目录 |
| `CLAUDE_CODE_ACCOUNT_UUID` | 已认证用户的账户 UUID。供 SDK 调用方同步提供账户信息，避免早期遥测事件缺少账户元数据。还需设置 `CLAUDE_CODE_USER_EMAIL` 和 `CLAUDE_CODE_ORGANIZATION_UUID` |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 设为 `1` 可从 `--add-dir` 指定的目录加载 CLAUDE.md 文件。默认情况下附加目录不加载内存文件 |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | 设置用于自动压缩计算的上下文容量。默认为模型的上下文窗口：标准模型 200K，[扩展上下文](./model-config#extended-context)模型 1M。在 1M 模型上用较低值（如 `500000`）可将窗口视为 500K 进行压缩。上限为模型实际上下文窗口。`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 以此值的百分比应用。设置此变量会使压缩阈值与状态栏的 `used_percentage` 脱钩，后者始终基于模型完整上下文窗口 |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | 凭据刷新间隔（毫秒），用于 [`apiKeyHelper`](./settings#available-settings) |
| `CLAUDE_CODE_CLIENT_CERT` | mTLS 认证用的客户端证书文件路径 |
| `CLAUDE_CODE_CLIENT_KEY` | mTLS 认证用的客户端私钥文件路径 |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE` | 加密的 CLAUDE\_CODE\_CLIENT\_KEY 的密码（可选） |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | 设为 `1` 禁用 [1M 上下文窗口](./model-config#extended-context)支持。设置后 1M 模型变体在模型选择器中不可用。适用于有合规要求的企业环境 |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | 设为 `1` 禁用 Opus 4.6 和 Sonnet 4.6 的[自适应推理](./model-config#adjust-effort-level)。禁用后这些模型会回退到由 `MAX_THINKING_TOKENS` 控制的固定思维预算 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 设为 `1` 禁用[自动内存](./memory#auto-memory)。设为 `0` 可在逐步发布期间强制开启自动内存。禁用时 Claude 不会创建或加载自动内存文件 |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | 设为 `1` 从 Claude 的 system prompt 中移除内置的提交和 PR 工作流指令。当你使用自己的 git 工作流技能时很有用。设置时优先于 [`includeGitInstructions`](./settings#available-settings) |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 设为 `1` 禁用所有后台任务功能，包括 Bash 和子代理工具的 `run_in_background` 参数、自动后台以及 Ctrl+B 快捷键 |
| `CLAUDE_CODE_DISABLE_CRON` | 设为 `1` 禁用[计划任务](./scheduled-tasks)。`/loop` 技能和 cron 工具不可用，已安排的任务也会停止触发 |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | 设为 `1` 从 API 请求中剥离 Anthropic 专有的 `anthropic-beta` 请求标头和 beta 工具 schema 字段（如 `defer_loading` 和 `eager_input_streaming`）。当代理网关报错如"anthropic-beta 标头有意外值"或"不允许额外输入"时使用。标准字段（`name`、`description`、`input_schema`、`cache_control`）会保留 |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | 设为 `1` 禁用[快速模式](./fast-mode) |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | 设为 `1` 禁用"Claude 怎么样？"会话质量调查。设置 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时也会禁用。详见[会话质量调查](./data-usage#session-quality-surveys) |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 等同于同时设置 `DISABLE_AUTOUPDATER`、`DISABLE_FEEDBACK_COMMAND`、`DISABLE_ERROR_REPORTING` 和 `DISABLE_TELEMETRY` |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | 设为 `1` 禁用基于对话上下文的自动终端标题更新 |
| `CLAUDE_CODE_EFFORT_LEVEL` | 设置支持的模型的工作量级别。可选值：`low`、`medium`、`high`、`max`（仅限 Opus 4.6）或 `auto`（使用模型默认）。优先于 `/effort` 和 `effortLevel` 设置。详见[调整工作量级别](./model-config#adjust-effort-level) |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | 设为 `false` 禁用提示建议（`/config` 中的"提示建议"开关）。这是 Claude 回复后出现在提示输入框中的灰色预测文本。详见[提示建议](./interactive-mode#prompt-suggestions) |
| `CLAUDE_CODE_ENABLE_TASKS` | 设为 `true` 在非交互模式（`-p` flag）下启用任务跟踪系统。交互模式下任务默认开启。详见[任务列表](./interactive-mode#task-list) |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | 设为 `1` 启用 OpenTelemetry 数据收集，用于指标和日志。配置 OTel 导出器前需要先设置此项。详见[监控](./monitoring-usage) |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | 查询循环空闲后自动退出前等待的时间（毫秒）。适用于使用 SDK 模式的自动化工作流和脚本 |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 设为 `1` 启用[代理团队](./agent-teams)。代理团队为实验性功能，默认禁用 |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | 覆盖文件读取的默认 token 限制。需要完整读取较大文件时使用 |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` | 跳过 IDE 扩展的自动安装 |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 设置大多数请求的最大输出 token 数。默认值和上限因模型而异，详见[最大输出 token](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison)。增大此值会减少[自动压缩](./costs#reduce-token-usage)触发前的可用上下文窗口 |
| `CLAUDE_CODE_NEW_INIT` | 设为 `true` 让 `/init` 运行交互式设置流程。流程会先探索代码库再生成，询问要生成哪些文件，包括 CLAUDE.md、技能和 hook。不设此变量时 `/init` 会自动生成 CLAUDE.md 而无提示 |
| `CLAUDE_CODE_ORGANIZATION_UUID` | 已认证用户的组织 UUID。供 SDK 调用方同步提供账户信息。还需设置 `CLAUDE_CODE_ACCOUNT_UUID` 和 `CLAUDE_CODE_USER_EMAIL` |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | 动态 OpenTelemetry 标头的刷新间隔（毫秒，默认 1740000 / 29 分钟）。详见[动态标头](./monitoring-usage#dynamic-headers) |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED` | 对需要计划审批的[代理团队](./agent-teams)队友自动设为 `true`。只读，由 Claude Code 在生成队友时设置。详见[要求队友的计划审批](./agent-teams#require-plan-approval-for-teammates) |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | 安装或更新插件时 git 操作的超时时间（默认 120000）。大仓库或慢网络时可增大。详见 [Git 操作超时](./plugin-marketplaces#git-operations-time-out) |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | 只读插件种子目录的路径。用于将预填充的插件目录打包到容器镜像中。Claude Code 启动时从此目录注册市场，使用预缓存的插件无需重新克隆。详见[为容器预填充插件](./plugin-marketplaces#pre-populate-plugins-for-containers) |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS` | 设为 `true` 让代理代替调用方执行 DNS 解析。适用于需要由代理处理主机名解析的环境 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | [SessionEnd](./hooks#sessionend) hook 完成的最长时间（毫秒，默认 `1500`）。适用于会话退出和 `/clear`。每个 hook 的 `timeout` 值也受此限制 |
| `CLAUDE_CODE_SHELL` | 覆盖自动 shell 检测。当你的登录 shell 和常用工作 shell 不同时有用（如 `bash` vs `zsh`） |
| `CLAUDE_CODE_SHELL_PREFIX` | 用于包装所有 bash 命令的命令前缀（如用于日志或审计）。例如 `/path/to/logger.sh` 会执行 `/path/to/logger.sh <command>` |
| `CLAUDE_CODE_SIMPLE` | 设为 `1` 以最小 system prompt 运行，仅使用 Bash、文件读取和文件编辑工具。禁用 MCP 工具、附件、hook 和 CLAUDE.md 文件 |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | 跳过 Bedrock 的 AWS 认证（如使用 LLM 网关时） |
| `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` | 设为 `1` 允许在组织状态检查因网络错误失败时使用[快速模式](./fast-mode)。当公司代理阻止状态端点时有用。API 仍然独立执行组织级别的禁用 |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | 跳过 Microsoft Foundry 的 Azure 认证（如使用 LLM 网关时） |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | 跳过 Vertex 的 Google 认证（如使用 LLM 网关时） |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 详见[模型配置](./model-config) |
| `CLAUDE_CODE_TASK_LIST_ID` | 跨会话共享任务列表。在多个 Claude Code 实例中设置相同 ID 即可在共享任务列表上协作。详见[任务列表](./interactive-mode#task-list) |
| `CLAUDE_CODE_TEAM_NAME` | 该队友所属代理团队的名称。在[代理团队](./agent-teams)成员上自动设置 |
| `CLAUDE_CODE_TMPDIR` | 覆盖内部临时文件的目录。Claude Code 会在此路径后追加 `/claude/`。默认值：Unix/macOS 上 `/tmp`，Windows 上 `os.tmpdir()` |
| `CLAUDE_CODE_USER_EMAIL` | 已认证用户的邮箱。供 SDK 调用方同步提供账户信息。还需设置 `CLAUDE_CODE_ACCOUNT_UUID` 和 `CLAUDE_CODE_ORGANIZATION_UUID` |
| `CLAUDE_CODE_USE_BEDROCK` | 使用 [Amazon Bedrock](./amazon-bedrock) |
| `CLAUDE_CODE_USE_FOUNDRY` | 使用 [Microsoft Foundry](./microsoft-foundry) |
| `CLAUDE_CODE_USE_VERTEX` | 使用 [Google Vertex AI](./google-vertex-ai) |
| `CLAUDE_CONFIG_DIR` | 自定义 Claude Code 存储配置和数据文件的位置 |
| `CLAUDE_ENV_FILE` | Claude Code 在每条 Bash 命令前会 source 的 shell 脚本路径。用于跨命令保持 virtualenv 或 conda 激活状态。也可由 [SessionStart hook](./hooks#persist-environment-variables) 动态填充 |
| `DISABLE_AUTOUPDATER` | 设为 `1` 禁用自动更新 |
| `DISABLE_COST_WARNINGS` | 设为 `1` 禁用成本警告信息 |
| `DISABLE_ERROR_REPORTING` | 设为 `1` 退出 Sentry 错误上报 |
| `DISABLE_FEEDBACK_COMMAND` | 设为 `1` 禁用 `/feedback` 命令。旧名称 `DISABLE_BUG_COMMAND` 也有效 |
| `DISABLE_INSTALLATION_CHECKS` | 设为 `1` 禁用安装检查警告。仅在手动管理安装位置时使用，否则可能掩盖标准安装的问题 |
| `DISABLE_PROMPT_CACHING` | 设为 `1` 禁用所有模型的 prompt 缓存（优先于单模型设置） |
| `DISABLE_PROMPT_CACHING_HAIKU` | 设为 `1` 禁用 Haiku 模型的 prompt 缓存 |
| `DISABLE_PROMPT_CACHING_OPUS` | 设为 `1` 禁用 Opus 模型的 prompt 缓存 |
| `DISABLE_PROMPT_CACHING_SONNET` | 设为 `1` 禁用 Sonnet 模型的 prompt 缓存 |
| `DISABLE_TELEMETRY` | 设为 `1` 退出 Statsig 遥测（Statsig 事件不含代码、文件路径或 bash 命令等用户数据） |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | 设为 `false` 禁用 Claude Code 中的 [claude.ai MCP 服务器](./mcp#use-mcp-servers-from-claudeai)。已登录用户默认启用 |
| `ENABLE_TOOL_SEARCH` | 控制 [MCP 工具搜索](./mcp#scale-with-mcp-tool-search)。不设：默认启用，但当 `ANTHROPIC_BASE_URL` 指向非第一方主机时禁用。可选值：`true`（始终包含代理）、`auto`（在 10% 上下文时启用）、`auto:N`（自定义阈值，如 `auto:5` 为 5%）、`false`（禁用） |
| `FORCE_AUTOUPDATE_PLUGINS` | 设为 `true` 强制插件自动更新，即使通过 `DISABLE_AUTOUPDATER` 禁用了主自动更新程序 |
| `HTTP_PROXY` | 指定 HTTP 代理服务器 |
| `HTTPS_PROXY` | 指定 HTTPS 代理服务器 |
| `IS_DEMO` | 设为 `true` 启用演示模式：在 UI 中隐藏邮箱和组织、跳过入门引导并隐藏内部命令。适用于直播或录屏 |
| `MAX_MCP_OUTPUT_TOKENS` | MCP 工具响应中允许的最大 token 数。输出超过 10,000 token 时 Claude Code 显示警告（默认 25000） |
| `MAX_THINKING_TOKENS` | 覆盖[扩展思维](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) token 预算。上限为模型的[最大输出 token](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) 减一。设为 `0` 完全禁用思维。在有自适应推理的模型（Opus 4.6、Sonnet 4.6）上，预算会被忽略，除非通过 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` 禁用自适应推理 |
| `MCP_CLIENT_SECRET` | 需要[预配置凭据](./mcp#use-pre-configured-oauth-credentials)的 MCP 服务器的 OAuth 客户端密钥。添加服务器时用 `--client-secret` 可避免交互式提示 |
| `MCP_OAUTH_CALLBACK_PORT` | 固定 OAuth 重定向回调的端口，作为使用[预配置凭据](./mcp#use-pre-configured-oauth-credentials)添加 MCP 服务器时 `--callback-port` 的替代 |
| `MCP_TIMEOUT` | MCP 服务器启动超时（毫秒） |
| `MCP_TOOL_TIMEOUT` | MCP 工具执行超时（毫秒） |
| `NO_PROXY` | 绕过代理直连的域名和 IP 列表 |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | 覆盖[技能工具](./skills#control-who-invokes-a-skill)中技能元数据的字符预算。预算按上下文窗口 2% 动态缩放，回退值 16,000 字符。保留旧名称以向后兼容 |
| `USE_BUILTIN_RIPGREP` | 设为 `0` 使用系统安装的 `rg` 而非 Claude Code 自带的 |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU` | 使用 Vertex AI 时覆盖 Claude 3.5 Haiku 的区域 |
| `VERTEX_REGION_CLAUDE_3_7_SONNET` | 使用 Vertex AI 时覆盖 Claude 3.7 Sonnet 的区域 |
| `VERTEX_REGION_CLAUDE_4_0_OPUS` | 使用 Vertex AI 时覆盖 Claude 4.0 Opus 的区域 |
| `VERTEX_REGION_CLAUDE_4_0_SONNET` | 使用 Vertex AI 时覆盖 Claude 4.0 Sonnet 的区域 |
| `VERTEX_REGION_CLAUDE_4_1_OPUS` | 使用 Vertex AI 时覆盖 Claude 4.1 Opus 的区域 |

## 另请参阅

* [设置](./settings)：在 `settings.json` 中配置环境变量，让它们应用到每个会话
* [CLI 参考](./cli-reference)：启动时 flag
* [网络配置](./network-config)：代理和 TLS 设置
