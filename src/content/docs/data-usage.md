---
title: "数据使用情况"
order: 42
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "了解 Anthropic 的 Claude 数据使用政策"
sourceUrl: "https://code.claude.com/docs/en/data-usage.md"
sourceTitle: "Data usage"
tags: []
---
# 数据使用情况

> 了解 Anthropic 针对 Claude 的数据使用政策

## 数据政策

### 数据训练政策

**消费者用户（免费、Pro 和 Max 套餐）**：
我们为您提供选择，允许您的数据用于改进未来的 Claude 模型。当此设置启用时（包括当您从这些帐户使用 Claude Code 时），我们将使用来自 Free、Pro 和 Max 帐户的数据来训练新模型。

**商业用户**：（团队和企业计划、API、第 3 方平台和 Claude Gov）维持现有政策：Anthropic 不会使用根据商业条款发送到 Claude Code 的代码或提示来训练生成模型，除非客户选择向我们提供其数据以进行模型改进（例如，[开发者合作伙伴计划](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)）。

### 开发合作伙伴计划

如果您明确选择向我们提供培训材料的方法，例如通过[开发合作伙伴计划](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)，我们可能会使用提供的这些材料来培训我们的模型。组织管理员可以明确选择加入其组织的开发合作伙伴计划。请注意，此程序仅适用于 Anthropic 第一方 API，不适用于 Bedrock 或 Vertex 用户。

### 使用 `/feedback` 命令的反馈

如果您选择使用 `/feedback` 命令向我们发送有关 Claude Code 的反馈，我们可能会使用您的反馈来改进我们的产品和服务。通过 `/feedback` 共享的成绩单将保留 5 年。

### 会议质量调查

当您看到“Claude 此会话进展如何？”时Claude Code 中的提示，响应此调查（包括选择“驳回”），仅记录您的数字评级（1、2、3 或驳回）。作为本次调查的一部分，我们不会收集或存储任何对话记录、输入、输出或其他会话数据。与赞成/反对反馈或 `/feedback` 报告不同，此会话质量调查是一个简单的产品满意度指标。您对此调查的回答不会影响您的数据训练偏好，也不能用于训练我们的人工智能模型。

要禁用这些调查，请设置 `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`。当设置 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时，该测量也会被禁用。要控制频率而不是禁用，请在设置文件中将 [`feedbackSurveyRate`](./settings#available-settings) 设置为 `0` 和 `1` 之间的概率。

### 数据保留

Anthropic 根据您的帐户类型和偏好保留 Claude Code 数据。

**消费者用户（免费、Pro 和 Max 套餐）**：

* 允许数据用于模型改进的用户：5年保留期以支持模型开发和安全改进
* 不允许数据用于模型改进的用户：30天保留期
* 可以随时在 [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) 更改隐私设置。

**商业用户（团队、企业和 API）**：* 标准：30天保留期
* [零数据保留](./zero-data-retention)：适用于企业版 Claude 上的 Claude Code。 ZDR 在每个组织的基础上启用；每个新组织必须由您的客户团队单独启用 ZDR
* 本地缓存：Claude Code 客户端可以在本地存储会话长达 30 天，以启用会话恢复（可配置）

您可以随时删除 Web 会话上的各个 Claude Code。删除会话将永久删除该会话的事件数据。有关如何删除会话的说明，请参阅[管理会话](./claude-code-on-the-web#managing-sessions)。

请访问我们的[隐私中心](https://privacy.anthropic.com/) 了解有关数据保留实践的更多信息。

有关完整详细信息，请查看我们的[商业服务条款](https://www.anthropic.com/legal/commercial-terms)（适用于 Team、Enterprise 和 API 用户）或[消费者条款](https://www.anthropic.com/legal/consumer-terms)（适用于 Free、Pro 和 Max 用户）和[隐私政策](https://www.anthropic.com/legal/privacy)。

## 数据访问

对于所有第一方用户，您可以详细了解为 [本地 Claude Code](#local-claude-code-data-flow-and-dependencies) 和 [远程 Claude Code](#cloud-execution-data-flow-and-dependencies) 记录的数据。 [Remote Control](./remote-control) 会话遵循本地数据流，因为所有执行都发生在您的计算机上。请注意，对于远程 Claude Code，Claude 将访问您在其中启动 Claude Code 会话的存储库。 Claude 不会访问您已连接但尚未启动会话的存储库。

## 本地 Claude Code：数据流和依赖关系

下图显示了 Claude Code 在安装和正常操作过程中如何连接到外部服务。实线表示所需的连接，而虚线表示可选或用户启动的数据流。

![显示 Claude Code 外部连接的图表：安装/更新连接到 NPM，用户请求连接到 Anthropic 服务，包括控制台身份验证、公共 api 以及可选的 Statsig、Sentry 和错误报告](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce)

Claude Code 是从 [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code) 安装的。 Claude Code 在本地运行。为了与 LLM 交互，Claude Code 通过网络发送数据。该数据包括所有用户提示和模型输出。数据在传输过程中通过 TLS 加密，静态时不加密。 Claude Code 与最流行的 VPN 和 LLM 代理兼容。

Claude Code 基于 Anthropic 的 API 构建。有关我们的 API 安全控制的详细信息，包括我们的 API 日志记录程序，请参阅 [Anthropic 信任中心](https://trust.anthropic.com) 中提供的合规性工件。

### 云执行：数据流和依赖关系

在 Web 上使用 [Claude Code](./claude-code-on-the-web) 时，会话在 Anthropic 管理的虚拟机中运行，而不是在本地运行。在云环境中：* **代码和数据存储：** 您的存储库已克隆到隔离的虚拟机。代码和会话数据受您帐户类型的保留和使用政策的约束（请参阅上面的数据保留部分）
* **凭证：** GitHub 身份验证通过安全代理处理；您的 GitHub 凭证永远不会进入沙箱
* **网络流量：** 所有出站流量都通过安全代理进行审核日志记录和滥用预防
* **会话数据：** 提示、代码更改和输出遵循与本地 Claude Code 使用相同的数据策略

有关云执行的安全详细信息，请参阅[安全](./security#cloud-execution-security)。

## 遥测服务

Claude Code 从用户计算机连接到 Statsig 服务，以记录延迟、可靠性和使用模式等操作指标。此日志记录不包含任何代码或文件路径。数据在传输过程中使用 TLS 加密，静态时使用 256 位 AES 加密。请参阅 [Statsig 安全文档](https://www.statsig.com/trust/security) 了解更多信息。要选择退出 Statsig 遥测，请设置 `DISABLE_TELEMETRY` 环境变量。

Claude Code 从用户计算机连接到 Sentry 以记录操作错误。数据在传输过程中使用 TLS 加密，静态时使用 256 位 AES 加密。请参阅 [Sentry 安全文档](https://sentry.io/security/) 了解更多信息。要选择退出错误日志记录，请设置 `DISABLE_ERROR_REPORTING` 环境变量。

当用户运行 `/feedback` 命令时，包括代码的完整对话历史记录的副本将发送到 Anthropic。数据在传输过程中和静态时均被加密。或者，在我们的公共存储库中创建一个 Github 问题。要选择退出，请设置 `DISABLE_FEEDBACK_COMMAND` 环境变量。

## API 提供者的默认行为

默认情况下，使用 Bedrock、Vertex 或 Foundry 时会禁用错误报告、遥测和错误报告。会话质量调查是例外，无论提供商如何，都会出现。您可以通过设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 立即选择退出所有非必要流量，包括调查。以下是完整的默认行为：|服务 | Claude API |Vertex API |Bedrock API |Foundry API |
| ------------------------------------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Statsig（指标）** |默认开启。
`DISABLE_TELEMETRY=1` 禁用。                   |默认关闭。
`CLAUDE_CODE_USE_VERTEX` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_BEDROCK` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。
| **Sentry（错误）** |默认开启。
`DISABLE_ERROR_REPORTING=1` 禁用。             |默认关闭。
`CLAUDE_CODE_USE_VERTEX` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_BEDROCK` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。
| **Claude API（`/feedback` 报告）** |默认开启。
`DISABLE_FEEDBACK_COMMAND=1` 禁用。            |默认关闭。
`CLAUDE_CODE_USE_VERTEX` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_BEDROCK` 必须为 1。默认关闭。
`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。
| **会议质量调查** |默认开启。
`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 |默认开启。
`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 |默认开启。
`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 |默认开启。
`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 |

所有环境变量都可以检查到 `settings.json`（[阅读更多](./settings)）。
