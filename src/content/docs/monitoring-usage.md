---
title: "监控"
order: 44
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "了解如何为 Claude Code 启用和配置 OpenTelemetry。"
sourceUrl: "https://code.claude.com/docs/en/monitoring-usage.md"
sourceTitle: "Monitoring"
tags: []
---
# 监控

> 了解如何为 Claude Code 启用和配置 OpenTelemetry。

通过 OpenTelemetry (OTel) 导出遥测数据，跟踪整个组织中的 Claude Code 使用情况、成本和工具活动。 Claude Code 通过标准指标协议将指标导出为时间序列数据，并通过日志/事件协议将事件导出。配置您的指标和日志后端以满足您的监控要求。

## 快速开始

使用环境变量配置 OpenTelemetry：

```bash
# 1. Enable telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choose exporters (both are optional - configure only what you need)
export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console

# 3. Configure OTLP endpoint (for OTLP exporter)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Set authentication (if required)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. For debugging: reduce export intervals
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)

# 6. Run Claude Code
claude
```

**注意**

指标的默认导出间隔为 60 秒，日志的默认导出间隔为 5 秒。在设置过程中，您可能希望使用较短的间隔来进行调试。请记住重置这些以供生产使用。

有关完整配置选项，请参阅 [OpenTelemetry 规范](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options)。

## 管理员配置

管理员可以通过[托管设置文件](./settings#settings-files) 为所有用户配置 OpenTelemetry 设置。这允许对整个组织的遥测设置进行集中控制。有关如何应用设置的详细信息，请参阅[设置优先级](./settings#settings-precedence)。

托管设置配置示例：

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

**注意**

托管设置可以通过 MDM（移动设备管理）或其他设备管理解决方案进行分发。托管设置文件中定义的环境变量具有高优先级，并且不能被用户覆盖。

## 配置详细信息

### 常用配置变量|环境变量 |描述 |示例值 |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `CLAUDE_CODE_ENABLE_TELEMETRY` |启用遥测收集（必需）| `1` |
| `OTEL_METRICS_EXPORTER` |指标导出器类型，以逗号分隔 | `console`、`otlp`、`prometheus` |
| `OTEL_LOGS_EXPORTER` |日志/事件导出器类型，以逗号分隔 | `console`、`otlp` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP 导出器协议，适用于所有信号 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` |所有信号的 OTLP 收集器端点 | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` |指标协议，覆盖常规设置 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | OTLP 指标端点，覆盖常规设置 | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` |日志协议，覆盖常规设置 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | OTLP 记录端点，覆盖常规设置 | `http://localhost:4318/v1/logs` |
| `OTEL_EXPORTER_OTLP_HEADERS` | OTLP 的身份验证标头 | `Authorization=Bearer token` |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` |用于 mTLS 身份验证的客户端密钥 |客户端密钥文件的路径 |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | mTLS 身份验证的客户端证书 |客户端证书文件的路径 |
| `OTEL_METRIC_EXPORT_INTERVAL` |导出间隔（以毫秒为单位）（默认值：60000）| `5000`、`60000` |
| `OTEL_LOGS_EXPORT_INTERVAL` |日志导出间隔（以毫秒为单位）（默认值：5000）| `1000`、`10000` || `OTEL_LOG_USER_PROMPTS` |启用用户提示内容的日志记录（默认：禁用） | `1` 启用 |
| `OTEL_LOG_TOOL_DETAILS` |启用在工具事件中记录 MCP 服务器/工具名称和技能名称（默认值：禁用） | `1` 启用 |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` |指标临时性首选项（默认值：`delta`）。如果您的后端需要累积临时性，请设置为 `cumulative` | `delta`、`cumulative` |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` |刷新动态标头的时间间隔（默认：1740000ms / 29 分钟） | `900000` |### 指标基数控制

以下环境变量控制哪些属性包含在指标中以管理基数：

|环境变量 |描述 |默认值 |禁用示例 |
| ----------------------------------- | ----------------------------------------------------------- | ------------- | ------------------ |
| `OTEL_METRICS_INCLUDE_SESSION_ID` |在指标中包含 session.id 属性 | `true` | `false` |
| `OTEL_METRICS_INCLUDE_VERSION` |在指标中包含 app.version 属性 | `false` | `true` |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` |在指标中包含 user.account\_uuid 属性 | `true` | `false` |

这些变量有助于控制指标的基数，这会影响指标后端的存储要求和查询性能。较低的基数通常意味着更好的性能和更低的存储成本，但用于分析的数据粒度更少。

### 动态标头

对于需要动态身份验证的企业环境，您可以配置脚本来动态生成标头：

#### 设置配置

添加到您的 `.claude/settings.json`：

```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### 脚本要求

该脚本必须输出有效的 JSON 以及表示 HTTP 标头的字符串键值对：

```bash
#!/bin/bash
# Example: Multiple headers
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### 刷新行为

标头帮助程序脚本在启动时运行，并在此后定期运行以支持令牌刷新。默认情况下，该脚本每 29 分钟运行一次。使用 `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` 环境变量自定义间隔。

### 多团队组织支持

拥有多个团队或部门的组织可以使用 `OTEL_RESOURCE_ATTRIBUTES` 环境变量添加自定义属性来区分不同的组：

```bash
# Add custom attributes for team identification
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

这些自定义属性将包含在所有指标和事件中，使您能够：

* 按团队或部门过滤指标
* 跟踪每个成本中心的成本
* 创建特定于团队的仪表板
* 为特定团队设置警报

**警告**

**OTEL\_RESOURCE\_ATTRIBUTES 的重要格式要求：**

`OTEL_RESOURCE_ATTRIBUTES` 环境变量使用逗号分隔的 key=value 对，并具有严格的格式要求：

* **不允许空格**：值不能包含空格。例如，`user.organizationName=My Company` 无效
* **格式**：必须是逗号分隔的键=值对：`key1=value1,key2=value2`
* **允许的字符**：仅限 US-ASCII 字符，不包括控制字符、空格、双引号、逗号、分号和反斜杠
* **特殊字符**：超出允许范围的字符必须进行百分比编码

**示例：**

```bash
# ❌ Invalid - contains spaces
export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

# ✅ Valid - use underscores or camelCase instead
export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

# ✅ Valid - percent-encode special characters if needed
export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
```

注意：将值括在引号中不会转义空格。例如，`org.name="My Company"` 会生成文字值 `"My Company"`（包含引号），而不是 `My Company`。

### 配置示例

在运行 `claude` 之前设置这些环境变量。每个块显示不同导出器或部署场景的完整配置：

```bash
# Console debugging (1-second intervals)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Multiple exporters
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Different endpoints/backends for metrics and logs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Metrics only (no events/logs)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Events/logs only (no metrics)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## 可用指标和事件

### 标准属性

所有指标和事件都共享这些标准属性：|属性|描述 |控制者 |
| ------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| `session.id` |唯一会话标识符 | `OTEL_METRICS_INCLUDE_SESSION_ID`（默认值：true）|
| `app.version` |当前 Claude Code 版本 | `OTEL_METRICS_INCLUDE_VERSION`（默认值：假）|
| `organization.id` |组织 UUID（经过身份验证后）|可用时始终包含在内 |
| `user.account_uuid` |帐户 UUID（经过身份验证后）| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（默认值：true）|
| `user.id` |匿名设备/安装标识符，根据 Claude Code 安装生成 |始终包含在内 |
| `user.email` |用户电子邮件地址（通过 OAuth 进行身份验证时）|可用时始终包含在内 |
| `terminal.type` |终端类型，例如 `iTerm.app`、`vscode`、`cursor` 或 `tmux` |检测到时始终包含 |

### 指标

Claude Code 导出以下指标：

|指标名称 |描述 |单位|
| -------------------------------------------------- | ----------------------------------------------------------- | ------ |
| `claude_code.session.count` |已启动的 CLI 会话计数 |计数|
| `claude_code.lines_of_code.count` |修改的代码行数 |计数|
| `claude_code.pull_request.count` |创建的拉取请求数量 |计数|
| `claude_code.commit.count` |创建的 git 提交数量 |计数|
| `claude_code.cost.usage` | Claude Code 会话的成本 |美元 |
| `claude_code.token.usage` |使用的代币数量 |代币 |
| `claude_code.code_edit_tool.decision` |代码编辑工具权限决策计数|计数|
| `claude_code.active_time.total` |总活跃时间（秒）| s |

### 指标详细信息

每个指标都包含上面列出的标准属性。下面列出了具有附加上下文特定属性的指标。

#### 会话计数器

在每次会话开始时增加。

**属性**：

* 所有[标准属性](#standard-attributes)

#### 代码行计数器

添加或删除代码时增加。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：（`"added"`、`"removed"`）

#### 拉取请求计数器

通过 Claude Code 创建拉取请求时增加。

**属性**：

* 所有[标准属性](#standard-attributes)

#### 提交计数器

通过 Claude Code 创建 git 提交时增加。

**属性**：

* 所有[标准属性](#standard-attributes)

#### 成本计数器

每次 API 请求后递增。

**属性**：* 所有[标准属性](#standard-attributes)
* `model`：型号标识符（例如“claude-sonnet-4-6”）

#### 令牌计数器

每次 API 请求后递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：（`"input"`、`"output"`、`"cacheRead"`、`"cacheCreation"`）
* `model`：型号标识符（例如“claude-sonnet-4-6”）

#### 代码编辑工具决策计数器

当用户接受或拒绝编辑、写入或 NotebookEdit 工具使用时增加。

**属性**：

* 所有[标准属性](#standard-attributes)
* `tool_name`：工具名称（`"Edit"`、`"Write"`、`"NotebookEdit"`）
* `decision`：用户决定（`"accept"`、`"reject"`）
* `source`：决策源 - `"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`
* `language`：编辑文件的编程语言，例如 `"TypeScript"`、`"Python"`、`"JavaScript"` 或 `"Markdown"`。对于无法识别的文件扩展名，返回 `"unknown"`。

#### 活动时间计数器

跟踪积极使用 Claude Code 所花费的实际时间，不包括空闲时间。该指标在用户交互（打字、读取响应）和 CLI 处理（工具执行、AI 响应生成）期间递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：`"user"`用于键盘交互，`"cli"`用于工具执行和AI响应

### 活动

Claude Code 通过 OpenTelemetry 日志/事件导出以下事件（当配置 `OTEL_LOGS_EXPORTER` 时）：

#### 事件关联属性

当用户提交提示时，Claude Code 可能会进行多个 API 调用并运行多个工具。 `prompt.id` 属性允许您将所有这些事件绑定回触发它们的单个提示。

|属性 |描述 |
| ----------- | ------------------------------------------------------------------------------------------------ |
| `prompt.id` | UUID v4 标识符链接处理单个用户提示时产生的所有事件 |

要跟踪单个提示触发的所有活动，请按特定 `prompt.id` 值过滤事件。这将返回处理该提示时发生的 user\_prompt 事件、任何 api\_request 事件以及任何 tool\_result 事件。

**注意**

`prompt.id` 有意从指标中排除，因为每个提示都会生成一个唯一的 ID，这将创建数量不断增加的时间序列。仅将其用于事件级分析和审计跟踪。

#### 用户提示事件

当用户提交提示时记录。

**事件名称**：`claude_code.user_prompt`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：单调递增计数器，用于在会话中排序事件
* `prompt_length`: 提示的长度
* `prompt`：提示内容（默认已编辑，通过`OTEL_LOG_USER_PROMPTS=1`启用）

#### 工具结果事件

当工具完成执行时记录。

**事件名称**：`claude_code.tool_result`

**属性**：* 所有[标准属性](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：单调递增计数器，用于在会话中排序事件
* `tool_name`：工具名称
* `success`: `"true"` 或 `"false"`
* `duration_ms`：执行时间（以毫秒为单位）
* `error`：错误消息（如果失败）
* `decision_type`：`"accept"` 或 `"reject"`
* `decision_source`：决策源 - `"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`
* `tool_result_size_bytes`：工具结果的大小（以字节为单位）
* `mcp_server_scope`：MCP 服务器范围标识符（对于 MCP 工具）
* `tool_parameters`：JSON 包含工具特定参数的字符串（如果可用）
  * 对于 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description`、`dangerouslyDisableSandbox` 和 `git_commit_id`（`git commit` 命令成功时的提交 SHA）
  * 对于 MCP 工具（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：包括 `mcp_server_name`、`mcp_tool_name`
  * 对于技能工具（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：包括 `skill_name`

#### API请求事件

记录对 Claude 的每个 API 请求。

**事件名称**：`claude_code.api_request`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：单调递增计数器，用于在会话中排序事件
* `model`：使用的型号（例如“claude-sonnet-4-6”）
* `cost_usd`：预计成本（美元）
* `duration_ms`：请求持续时间（以毫秒为单位）
* `input_tokens`：输入令牌数量
* `output_tokens`：输出令牌数量
* `cache_read_tokens`：从缓存读取的令牌数量
* `cache_creation_tokens`：用于创建缓存的令牌数量
* `speed`：`"fast"` 或 `"normal"`，指示快速模式是否处于活动状态

#### API 错误事件

当对 Claude 的 API 请求失败时记录。

**事件名称**：`claude_code.api_error`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：单调递增计数器，用于在会话中排序事件
* `model`：使用的型号（例如“claude-sonnet-4-6”）
* `error`：错误消息
* `status_code`：HTTP 状态代码作为字符串，或 `"undefined"` 表示非 HTTP 错误
* `duration_ms`：请求持续时间（以毫秒为单位）
* `attempt`：尝试编号（用于重试请求）
* `speed`：`"fast"` 或 `"normal"`，指示快速模式是否处于活动状态

#### 工具决策事件

当做出工具权限决定（接受/拒绝）时记录。

**事件名称**：`claude_code.tool_decision`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：单调递增计数器，用于在会话中排序事件
* `tool_name`：工具名称（例如“读取”、“编辑”、“写入”、“NotebookEdit”）
* `decision`：`"accept"` 或 `"reject"`
* `source`：决策源 - `"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`

## 解释指标和事件数据

导出的指标和事件支持一系列分析：

### 使用情况监控|公制|分析机会 |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `claude_code.token.usage` |按 `type`（输入/输出）、用户、团队或模型细分 |
| `claude_code.session.count` |跟踪一段时间内的采用率和参与度 |
| `claude_code.lines_of_code.count` |通过跟踪代码添加/删除来衡量生产力 |
| `claude_code.commit.count` 和 `claude_code.pull_request.count` |了解对开发工作流程的影响 |

### 成本监控

`claude_code.cost.usage` 指标有助于：

* 跟踪团队或个人的使用趋势
* 识别高使用率会话以进行优化

**注意**

成本指标是近似值。有关官方账单数据，请咨询您的 API 提供商（Claude 控制台、AWS Bedrock 或 Google Cloud Vertex）。

### 警报和分段

要考虑的常见警报：

* 成本飙升
* 异常的代币消耗
* 来自特定用户的高会话量

所有指标均可按 `user.account_uuid`、`organization.id`、`session.id`、`model` 和 `app.version` 进行分段。

###事件分析

事件数据提供了有关 Claude Code 交互的详细见解：

**工具使用模式**：分析工具结果事件以识别：

* 最常用的工具
* 工具成功率
* 平均工具执行时间
* 按工具类型划分的错误模式

**性能监控**：跟踪 API 请求持续时间和工具执行时间以识别性能瓶颈。

## 后端注意事项

您对指标和日志后端的选择决定了您可以执行的分析类型：

### 对于指标

* **时间序列数据库（例如 Prometheus）**：速率计算、聚合指标
* **列式存储（例如ClickHouse）**：复杂查询，独特的用户分析
* **功能齐全的可观测平台（例如 Honeycomb、Datadog）**：高级查询、可视化、警报

### 对于事件/日志

* **日志聚合系统（例如Elasticsearch、Loki）**：全文搜索、日志分析
* **列式存储（例如ClickHouse）**：结构化事件分析
* **功能齐全的可观测平台（例如 Honeycomb、Datadog）**：指标和事件之间的关联

对于需要每日/每周/每月活跃用户 (DAU/WAU/MAU) 指标的组织，请考虑支持高效唯一值查询的后端。

## 服务信息

所有指标和事件均使用以下资源属性导出：

* `service.name`: `claude-code`
* `service.version`：当前 Claude Code 版本
* `os.type`：操作系统类型（例如，`linux`、`darwin`、`windows`）
* `os.version`：操作系统版本字符串
* `host.arch`：主机架构（例如，`amd64`、`arm64`）
* `wsl.version`：WSL 版本号（仅在 Linux 的 Windows 子系统上运行时出现）
* 仪表名称：`com.anthropic.claude_code`

## 投资回报率衡量资源有关衡量 Claude Code 投资回报的综合指南，包括遥测设置、成本分析、生产力指标和自动报告，请参阅 [Claude Code 投资回报率衡量指南](https://github.com/anthropics/claude-code-monitoring-guide)。该存储库提供了即用型 Docker Compose 配置、Prometheus 和 OpenTelemetry 设置以及用于生成与 Linear 等工具集成的生产力报告的模板。

## 安全和隐私

* 遥测是可选的，需要显式配置
* 原始文件内容和代码片段不包含在指标或事件中。工具执行事件包括`tool_parameters`字段中的bash命令和文件路径，其中可能包含敏感值。如果您的命令可能包含机密，请配置您的遥测后端以过滤或编辑 `tool_parameters`
* 当通过 OAuth 进行身份验证时，`user.email` 包含在遥测属性中。如果这是您的组织所关心的问题，请与您的遥测后端合作来过滤或编辑此字段
* 默认不收集用户提示内容。仅记录提示长度。要包含提示内容，请设置 `OTEL_LOG_USER_PROMPTS=1`
* MCP 服务器/工具名称和技能名称默认情况下不会记录，因为它们可能会泄露用户特定的配置。要包含它们，请设置 `OTEL_LOG_TOOL_DETAILS=1`

## 在 Amazon Bedrock 上监控 Claude Code

有关 Amazon Bedrock 的详细 Claude Code 使用情况监控指南，请参阅 [Claude Code 监控实施 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)。
