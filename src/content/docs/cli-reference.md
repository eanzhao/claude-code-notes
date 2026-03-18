---
title: "CLI 参考"
order: 57
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "Claude Code 命令行界面的完整参考，包括命令和标志。"
sourceUrl: "https://code.claude.com/docs/en/cli-reference.md"
sourceTitle: "CLI reference"
tags: []
---
# CLI 参考

> Claude Code 命令行界面的完整参考，包括命令和 flag。

## CLI 命令

你可以用以下命令启动会话、通过管道传入内容、恢复对话以及管理更新：

| 命令 | 说明 | 示例 |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude` | 启动交互式会话 | `claude` |
| `claude "query"` | 带初始提示启动交互式会话 | `claude "explain this project"` |
| `claude -p "query"` | 以 SDK 模式查询后退出 | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | 通过管道传入内容 | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | 继续当前目录中最近的对话 | `claude -c` |
| `claude -c -p "query"` | 以 SDK 模式继续对话 | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | 按 ID 或名称恢复会话 | `claude -r "auth-refactor" "Finish this PR"` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude auth login` | 登录 Anthropic 账户。可用 `--email` 预填邮箱，`--sso` 强制 SSO 认证 | `claude auth login --email user@example.com --sso` |
| `claude auth logout` | 退出 Anthropic 账户 | `claude auth logout` |
| `claude auth status` | 以 JSON 格式显示认证状态。加 `--text` 可输出人类可读格式。已登录时退出码为 0，未登录为 1 | `claude auth status` |
| `claude agents` | 列出所有已配置的[子代理](./sub-agents)，按来源分组 | `claude agents` |
| `claude mcp` | 配置 Model Context Protocol (MCP) 服务器 | 详见 [Claude Code MCP 文档](./mcp) |
| `claude remote-control` | 启动 [Remote Control](./remote-control) 服务器，让你从 Claude.ai 或 Claude 客户端控制 Claude Code。以服务器模式运行（无本地交互式会话）。详见[服务器模式 flag](./remote-control#server-mode) | `claude remote-control --name "My Project"` |

## CLI flag

你可以用以下命令行 flag 自定义 Claude Code 的行为：

| flag | 说明 | 示例 |
| :------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `--add-dir` | 添加额外的工作目录供 Claude 访问（会验证每个路径是否为有效目录） | `claude --add-dir ../apps ../lib` |
| `--agent` | 为当前会话指定代理（覆盖 `agent` 设置） | `claude --agent my-custom-agent` |
| `--agents` | 通过 JSON 动态定义自定义子代理。字段名与子代理 [frontmatter](./sub-agents#supported-frontmatter-fields) 相同，另有 `prompt` 字段用于代理说明 | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | 启用权限绕过选项但不立即激活。可与 `--permission-mode` 组合使用（请谨慎使用） | `claude --permission-mode plan --allow-dangerously-skip-permissions` |
| `--allowedTools` | 无需提示即可执行的工具。模式匹配语法详见[权限规则语法](./settings#permission-rule-syntax)。如要限制可用工具，请改用 `--tools` | `"Bash(git log *)" "Bash(git diff *)" "Read"` |
| `--append-system-prompt` | 在默认 system prompt 末尾追加自定义文本 | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | 从文件加载额外的 system prompt 文本并追加到默认 prompt | `claude --append-system-prompt-file ./extra-rules.txt` |
| `--betas` | API 请求中包含的 Beta 标头（仅限 API 密钥用户） | `claude --betas interleaved-thinking` |
| `--chrome` | 启用 [Chrome 浏览器集成](./chrome)，用于 Web 自动化和测试 | `claude --chrome` |
| `--continue`、`-c` | 加载当前目录中最近的对话 | `claude --continue` |
| `--dangerously-skip-permissions` | 跳过权限提示（请谨慎使用）。详见[权限模式](./permissions#permission-modes) | `claude --dangerously-skip-permissions` |
| `--debug` | 启用调试模式，可选按类别过滤（如 `"api,hooks"` 或 `"!statsig,!file"`） | `claude --debug "api,mcp"` |
| `--disable-slash-commands` | 禁用本次会话的所有技能和命令 | `claude --disable-slash-commands` |
| `--disallowedTools` | 从模型上下文中移除、禁止使用的工具 | `"Bash(git log *)" "Bash(git diff *)" "Edit"` |
| `--effort` | 设置当前会话的[工作量级别](./model-config#adjust-effort-level)。可选值：`low`、`medium`、`high`、`max`（仅限 Opus 4.6）。仅当前会话有效，不会保存 | `claude --effort high` |
| `--fallback-model` | 当默认模型过载时自动回退到指定模型（仅限打印模式） | `claude -p --fallback-model sonnet "query"` |
| `--fork-session` | 恢复时创建新的会话 ID，而非复用原会话 ID（与 `--resume` 或 `--continue` 搭配使用） | `claude --resume abc123 --fork-session` |
| `--from-pr` | 恢复关联到特定 GitHub PR 的会话。接受 PR 号或 URL。通过 `gh pr create` 创建的会话会自动关联 | `claude --from-pr 123` |
| `--ide` | 如果只有一个可用的 IDE，启动时自动连接 | `claude --ide` |
| `--init` | 运行初始化 hook 并启动交互模式 | `claude --init` |
| `--init-only` | 运行初始化 hook 后退出（不进入交互式会话） | `claude --init-only` |
| `--include-partial-messages` | 在输出中包含部分流事件（需要 `--print` 和 `--output-format=stream-json`） | `claude -p --output-format stream-json --include-partial-messages "query"` |
| `--input-format` | 指定打印模式的输入格式（可选：`text`、`stream-json`） | `claude -p --output-format json --input-format stream-json` |
| `--json-schema` | 代理完成工作后，获取符合 JSON Schema 的验证输出（仅限打印模式，详见[结构化输出](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)） | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"` |
| `--maintenance` | 运行维护 hook 后退出 | `claude --maintenance` |
| `--max-budget-usd` | 停止前 API 调用的最大花费金额（仅限打印模式） | `claude -p --max-budget-usd 5.00 "query"` |
| `--max-turns` | 限制代理轮次数（仅限打印模式）。达到限制时退出并报错。默认无限制 | `claude -p --max-turns 3 "query"` |
| `--mcp-config` | 从 JSON 文件或字符串加载 MCP 服务器（空格分隔） | `claude --mcp-config ./mcp.json` |
| `--model` | 设置当前会话的模型，可用别名（`sonnet` 或 `opus`）或模型全名 | `claude --model claude-sonnet-4-6` |
| `--name`、`-n` | 设置会话显示名称（在 `/resume` 中显示）和终端标题。可通过 `claude --resume <name>` 恢复指定会话。会话中可用 [`/rename`](./commands) 改名，名称会显示在提示栏上 | `claude -n "my-feature-work"` |
| `--no-chrome` | 在本次会话中禁用 [Chrome 浏览器集成](./chrome) | `claude --no-chrome` |
| `--no-session-persistence` | 禁用会话持久化，会话不会保存到磁盘、也无法恢复（仅限打印模式） | `claude -p --no-session-persistence "query"` |
| `--output-format` | 指定打印模式的输出格式（可选：`text`、`json`、`stream-json`） | `claude -p "query" --output-format json` |
| `--permission-mode` | 以指定的[权限模式](./permissions#permission-modes)启动 | `claude --permission-mode plan` |
| `--permission-prompt-tool` | 指定在非交互模式下处理权限提示的 MCP 工具 | `claude -p --permission-prompt-tool mcp_auth_tool "query"` |
| `--plugin-dir` | 仅为本次会话从目录加载插件。每个 flag 接受一个路径，多个目录需重复使用：`--plugin-dir A --plugin-dir B` | `claude --plugin-dir ./my-plugins` |
| `--print`、`-p` | 打印响应后退出，不进入交互模式（编程用法详见 [Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview)） | `claude -p "query"` |
| `--remote` | 用指定的任务描述在 claude.ai 上创建一个[远程会话](./claude-code-on-the-web) | `claude --remote "Fix the login bug"` |
| `--remote-control`、`--rc` | 启动带 [Remote Control](./remote-control#interactive-session) 的交互式会话，让你同时可以从 claude.ai 或 Claude 客户端控制它。可选传入会话名称 | `claude --remote-control "My Project"` |
| `--resume`、`-r` | 按 ID 或名称恢复特定会话，或显示交互式选择器 | `claude --resume auth-refactor` |
| `--session-id` | 使用特定的会话 ID（必须是有效的 UUID） | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"` |
| `--setting-sources` | 要加载的设置源，逗号分隔（`user`、`project`、`local`） | `claude --setting-sources user,project` |
| `--settings` | 设置 JSON 文件的路径或 JSON 字符串，用于加载额外设置 | `claude --settings ./settings.json` |
| `--strict-mcp-config` | 仅使用 `--mcp-config` 中的 MCP 服务器，忽略其他所有 MCP 配置 | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--system-prompt` | 用自定义文本替换整个 system prompt | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | 从文件加载 system prompt，替换默认 prompt | `claude --system-prompt-file ./custom-prompt.txt` |
| `--teleport` | 在本地终端中恢复[远程会话](./claude-code-on-the-web) | `claude --teleport` |
| `--teammate-mode` | 设置[代理团队](./agent-teams)队友的显示方式：`auto`（默认）、`in-process` 或 `tmux`。详见[设置代理团队](./agent-teams#set-up-agent-teams) | `claude --teammate-mode in-process` |
| `--tools` | 限制 Claude 可使用的内置工具。用 `""` 禁用全部，`"default"` 使用默认，或指定工具名如 `"Bash,Edit,Read"` | `claude --tools "Bash,Edit,Read"` |
| `--verbose` | 启用详细日志，显示完整的逐轮输出 | `claude --verbose` |
| `--version`、`-v` | 输出版本号 | `claude -v` |
| `--worktree`、`-w` | 在 `<repo>/.claude/worktrees/<name>` 的隔离 [git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中启动 Claude。不指定名称则自动生成 | `claude -w feature-auth` |

### System prompt flag

Claude Code 提供四个用于自定义 system prompt 的 flag。四种方式在交互和非交互模式下都可以使用。

| flag | 行为 | 示例 |
| :---------------------------- | :------------------------------------------ | :------------------------------------------------------ |
| `--system-prompt` | 替换整个默认 prompt | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | 用文件内容替换 | `claude --system-prompt-file ./prompts/review.txt` |
| `--append-system-prompt` | 追加到默认 prompt | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | 将文件内容追加到默认 prompt | `claude --append-system-prompt-file ./style-rules.txt` |

`--system-prompt` 和 `--system-prompt-file` 互斥。追加 flag 可以和任一替换 flag 组合使用。

大多数情况下建议使用追加 flag。追加方式保留了 Claude Code 的内置能力，同时加入你的要求。只有当你需要完全控制 system prompt 时，才使用替换 flag。

## 另请参阅

* [Chrome 扩展](./chrome) - 浏览器自动化和 Web 测试
* [交互模式](./interactive-mode) - 快捷键、输入模式和交互功能
* [快速入门指南](./quickstart) - Claude Code 入门
* [常用工作流程](./common-workflows) - 高级工作流程和模式
* [设置](./settings) - 配置选项
* [Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview) - 编程用法和集成
