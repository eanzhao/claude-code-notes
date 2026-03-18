---
title: "以编程方式运行 Claude Code"
order: 28
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "使用 Agent SDK 通过 CLI、Python 或 TypeScript 以编程方式运行 Claude Code。"
sourceUrl: "https://code.claude.com/docs/en/headless.md"
sourceTitle: "Run Claude Code programmatically"
tags: []
---
# 以编程方式运行 Claude Code

> 使用 Agent SDK 通过 CLI、Python 或 TypeScript 以编程方式运行 Claude Code。

[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 为您提供与 Claude Code 相同的工具、代理循环和上下文管理。它可用作脚本和 CI/CD 的 CLI，或用作完全编程控制的 [Python](https://platform.claude.com/docs/en/agent-sdk/python) 和 [TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript) 包。

**注意**

CLI 以前称为“无头模式”。 `-p` 标志和所有 CLI 选项的工作方式相同。

要从 CLI 以编程方式运行 Claude Code，请传递 `-p` 以及提示符和任何 [CLI 选项](./cli-reference)：

```bash
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

本页介绍通过 CLI (`claude -p`) 使用 Agent SDK。有关具有结构化输出、工具批准回调和本机消息对象的 Python 和 TypeScript SDK 包，请参阅[完整的 Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview)。

## 基本用法

将 `-p`（或 `--print`）标志添加到任何 `claude` 命令中以非交互方式运行它。所有 [CLI 选项](./cli-reference) 均适用于 `-p`，包括：

* `--continue` 用于[继续对话](#continue-conversations)
* `--allowedTools` 用于[自动批准工具](#auto-approve-tools)
* `--output-format` 用于[结构化输出](#get-structured-output)

此示例向 Claude 询问有关您的代码库的问题并打印响应：

```bash
claude -p "What does the auth module do?"
```

## 示例

这些示例重点介绍了常见的 CLI 模式。

### 获取结构化输出

使用 `--output-format` 控制如何返回响应：

* `text`（默认）：纯文本输出
* `json`：结构化 JSON，包含结果、会话 ID 和元数据
* `stream-json`：换行符分隔的 JSON 用于实时流式传输

此示例返回带有会话元数据的项目摘要 JSON，文本结果位于 `result` 字段中：

```bash
claude -p "Summarize this project" --output-format json
```

要获得符合特定架构的输出，请将 `--output-format json` 与 `--json-schema` 和 [JSON 架构](https://json-schema.org/) 定义结合使用。响应包括有关请求的元数据（会话 ID、使用情况等）以及 `structured_output` 字段中的结构化输出。

此示例提取函数名称并将它们作为字符串数组返回：

```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

**提示**

使用 [jq](https://jqlang.github.io/jq/) 等工具来解析响应并提取特定字段：

```bash
# Extract the text result
claude -p "Summarize this project" --output-format json | jq -r '.result'

# Extract structured output
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

### 流响应

将 `--output-format stream-json` 与 `--verbose` 和 `--include-partial-messages` 结合使用以接收生成的令牌。每行都是代表一个事件的 JSON 对象：

```bash
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

以下示例使用 [jq](https://jqlang.github.io/jq/) 过滤文本增量并仅显示流文本。 `-r` 标志输出原始字符串（无引号），并且 `-j` 不带换行符连接，因此令牌连续流动：

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

当 API 请求因可重试错误而失败时，Claude Code 在重试之前会发出 `system/api_retry` 事件。您可以使用它来显示重试进度或实现自定义退避逻辑。|领域 |类型 |描述 |
| ---------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` | `"system"` |消息类型 |
| `subtype` | `"api_retry"` |将其识别为重试事件 |
| `attempt` |整数 |当前尝试次数，从 1 开始 |
| `max_retries` |整数 |允许的总重试次数 |
| `retry_delay_ms` |整数 |距离下一次尝试还有多少毫秒 |
| `error_status` |整数或 null | HTTP 状态代码，或 `null` 表示没有 HTTP 响应的连接错误 |
| `error` |字符串|错误类别：`authentication_failed`、`billing_error`、`rate_limit`、`invalid_request`、`server_error`、`max_output_tokens` 或 `unknown` |
| `uuid` |字符串|唯一的事件标识符|
| `session_id` |字符串|事件所属的会话 |

有关使用回调和消息对象的编程流式传输，请参阅 Agent SDK 文档中的[实时流式响应](https://platform.claude.com/docs/en/agent-sdk/streaming-output)。

### 自动批准工具

使用 `--allowedTools` 让 Claude 在没有提示的情况下使用某些工具。此示例运行测试套件并修复故障，允许 Claude 执行 Bash 命令并读取/编辑文件，而无需请求许可：

```bash
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

### 创建提交

此示例审查分阶段的更改并使用适当的消息创建提交：

```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

`--allowedTools` 标志使用[权限规则语法](./settings#permission-rule-syntax)。尾随 ` *` 启用前缀匹配，因此 `Bash(git diff *)` 允许以 `git diff` 开头的任何命令。 `*` 之前的空格很重要：没有它，`Bash(git diff*)` 也会匹配 `git diff-index`。

**注意**

用户调用的[技能](./skills)（例如`/commit`）和[内置命令](./commands)仅在交互模式下可用。在 `-p` 模式下，描述您想要完成的任务。

### 自定义系统提示符使用 `--append-system-prompt` 添加指令，同时保留 Claude Code 的默认行为。此示例将 PR 差异通过管道传输到 Claude 并指示其检查安全漏洞：

```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

请参阅 [系统提示标志](./cli-reference#system-prompt-flags) 了解更多选项，包括 `--system-prompt` 以完全替换默认提示。

### 继续对话

使用 `--continue` 继续最近的对话，或使用 `--resume` 和会话 ID 继续特定对话。此示例运行审核，然后发送后续提示：

```bash
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

如果您正在运行多个对话，请捕获会话 ID 以恢复特定对话：

```bash
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## 后续步骤

* [Agent SDK 快速入门](https://platform.claude.com/docs/en/agent-sdk/quickstart)：使用 Python 或 TypeScript 构建您的第一个代理
* [CLI 参考](./cli-reference)：所有 CLI 标志和选项
* [GitHub Actions](./github-actions)：在 GitHub 工作流程中使用 Agent SDK
* [GitLab CI/CD](./gitlab-ci-cd)：在 GitLab 管道中使用 Agent SDK
