---
title: "使用快速模式加快响应速度"
order: 53
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "通过切换快速模式，在 Claude Code 中获得更快的 Opus 4.6 响应。"
sourceUrl: "https://code.claude.com/docs/en/fast-mode.md"
sourceTitle: "Speed up responses with fast mode"
tags: []
---
# 使用快速模式加快响应速度

> 通过切换快速模式，在 Claude Code 中获得更快的 Opus 4.6 响应。

**注意**

快速模式处于[研究预览](#research-preview)。功能、定价和可用性可能会根据反馈而变化。

快速模式是 Claude Opus 4.6 的高速配置，使模型速度提高 2.5 倍，但每个令牌的成本更高。当您需要速度进行交互式工作（例如快速迭代或实时调试）时，请使用 `/fast` 将其打开，而当成本比延迟更重要时，请关闭它。

快速模式并不是一个不同的模型。它使用相同的 Opus 4.6 和不同的 API 配置，优先考虑速度而不是成本效率。您可以获得相同的质量和功能，但响应速度更快。

**注意**

快速模式需要 Claude Code v2.1.36 或更高版本。使用 `claude --version` 检查您的版本。

要知道什么：

* 使用 `/fast` 在 Claude Code CLI 中打开快速模式。也可通过 Claude Code VS Code 扩展中的 `/fast` 获得。
* Opus 4.6 的快速模式定价为 30 美元/150 MTok。
* 适用于订阅计划（Pro/Max/Team/Enterprise）和 Claude 控制台的所有 Claude Code 用户。
* 对于订阅计划（Pro/Max/Team/Enterprise）的 Claude Code 用户，快速模式仅可通过额外使用使用，不包含在订阅费率限制中。

本页介绍如何[切换快速模式](#toggle-fast-mode)、其[成本权衡](#understand-the-cost-tradeoff)、[何时使用](#decide-when-to-use-fast-mode)、[要求](#requirements)、[每会话选择加入](#require-per-session-opt-in)和[速率限制行为](#handle-rate-limits)。

## 切换快速模式

通过以下任一方式切换快速模式：

* 输入 `/fast` 并按 Tab 键切换打开或关闭
* 在您的[用户设置文件]中设置`"fastMode": true`(./settings)

默认情况下，快速模式在会话中持续存在。管理员可以配置快速模式来重置每个会话。有关详细信息，请参阅[需要每个会话选择加入](#require-per-session-opt-in)。

为了获得最佳成本效率，请在会话开始时启用快速模式，而不是在会话中切换。有关详细信息，请参阅[了解成本权衡](#understand-the-cost-tradeoff)。

当您启用快速模式时：

* 如果您使用的是其他模型，Claude Code 会自动切换到 Opus 4.6
* 您将看到一条确认消息：“快速模式开启”
* 当快速模式处于活动状态时，提示旁边会出现一个小 `↯` 图标
* 随时再次运行`/fast`来检查快速模式是否打开或关闭

当您再次使用 `/fast` 禁用快速模式时，您仍使用 Opus 4.6。该模型不会恢复为之前的模型。要切换到不同模型，请使用 `/model`。

## 了解成本权衡

快速模式的每代币定价高于标准 Opus 4.6：

|模式|输入（MTok）|输出（MTok）|
| -------------------- | ------------ | ------------- |
| Opus 4.6 上的快速模式 | 30 美元 | 150 美元 |

快速模式定价在整个 1M 代币上下文窗口中保持平稳。

当您在对话中切换到快速模式时，您需要为整个对话上下文支付完整的快速模式未缓存输入令牌价格。这比从一开始就启用快速模式的成本更高。

## 决定何时使用快速模式快速模式最适合响应延迟比成本更重要的交互式工作：

* 代码变更快速迭代
* 实时调试会话
* 时间紧迫、期限紧迫的工作

标准模式更适合：

* 速度较不重要的长时间自主任务
* 批处理或 CI/CD 管道
* 成本敏感的工作负载

### 快速模式与努力水平

快速模式和工作量级别都会影响响应速度，但有所不同：

|设置|效果|
| ---------------------- | -------------------------------------------------------------------------------- |
| **快速模式** |同型号品质，更低延迟，更高成本 |
| **降低工作量** |思考时间更少，反应更快，但复杂任务的质量可能会降低 |

您可以将两者结合起来：使用[工作量级别]较低的快速模式(./model-config#adjust-effort-level)，以最大速度完成简单的任务。

## 要求

快速模式需要满足以下所有条件：

* **不适用于第三方云提供商**：快速模式不适用于 Amazon Bedrock、Google Vertex AI 或 Microsoft Azure Foundry。快速模式可通过 Anthropic 控制台 API 以及使用额外使用量的 Claude 订阅计划使用。
* **启用额外使用量**：您的帐户必须启用额外使用量，这允许超出您的计划包含的使用量进行计费。对于个人帐户，请在[控制台计费设置](https://platform.claude.com/settings/organization/billing) 中启用此功能。对于 Teams 和 Enterprise，管理员必须为组织启用额外的使用。

**注意**

即使您的计划中有剩余使用量，快速模式使用量也会直接按额外使用量计费。这意味着快速模式令牌不计入您的计划包含的使用量，并且从第一个令牌开始按快速模式费率收费。

* **团队和企业的管理员启用**：默认情况下，团队和企业组织禁用快速模式。管理员必须明确[启用快速模式](#enable-fast-mode-for-your-organization)，用户才能访问它。

**注意**

如果您的管理员尚未为您的组织启用快速模式，`/fast` 命令将显示“您的组织已禁用快速模式”。

### 为您的组织启用快速模式

管理员可以在以下位置启用快速模式：

* **控制台**（API 客户）：[Claude Code 首选项](https://platform.claude.com/claude-code/preferences)
* **Claude AI**（团队和企业）：[管理设置 > Claude Code](https://claude.ai/admin-settings/claude-code)

完全禁用快速模式的另一个选项是设置 `CLAUDE_CODE_DISABLE_FAST_MODE=1`。请参阅[环境变量](./env-vars)。

### 需要每个会话选择加入

默认情况下，快速模式在会话中持续存在：如果用户启用快速模式，它将在以后的会话中保持开启状态。 [团队](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=fast_mode_teams#team-&-enterprise) 或[企业](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=fast_mode_enterprise) 计划的管理员可以通过在[托管设置](./settings#settings-files) 或[服务器管理设置](./server-managed-settings) 中将 `fastModePerSessionOptIn` 设置为 `true` 来防止出现这种情况。这会导致每个会话在快速模式关闭的情况下启动，要求用户使用 `/fast` 显式启用它。

```json
{
  "fastModePerSessionOptIn": true
}
```这对于控制用户运行多个并发会话的组织的成本很有用。当需要速度时，用户仍然可以使用 `/fast` 启用快速模式，但它会在每个新会话开始时重置。用户的快速模式首选项仍会保存，因此删除此设置将恢复默认的持久行为。

## 处理速率限制

快速模式具有与标准 Opus 4.6 不同的速率限制。当您达到快速模式速率限制或用完额外使用积分时：

1. 快速模式自动回退到标准Opus 4.6
2. `↯`图标变为灰色表示冷却
3. 您继续以标准速度和定价工作
4. 冷却时间结束后，快速模式自动重新启用

要手动禁用快速模式而不是等待冷却，请再次运行 `/fast`。

## 研究预览

快速模式是一项研究预览功能。这意味着：

* 该功能可能会根据反馈进行更改
* 供货情况和价格可能会发生变化
* 底层 API 配置可能会演变

通过常用的 Anthropic 支持渠道报告问题或反馈。

## 另请参阅

* [模型配置](./model-config)：切换模型并调整努力程度
* [有效管理成本](./costs)：跟踪代币使用情况并降低成本
* [状态线配置](./statusline)：显示模型和上下文信息
