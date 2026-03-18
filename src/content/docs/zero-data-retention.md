---
title: "零数据保留"
order: 43
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "了解 Claude for Enterprise 上 Claude Code 的零数据保留 (ZDR)，包括范围、禁用的功能以及如何请求启用。"
sourceUrl: "https://code.claude.com/docs/en/zero-data-retention.md"
sourceTitle: "Zero data retention"
tags: []
---
# 零数据保留

> 了解 Claude Enterprise 上的 Claude Code 的零数据保留 (ZDR)，包括范围、禁用的功能以及如何请求启用。

当通过 Claude for Enterprise 使用时，Claude Code 可以使用零数据保留 (ZDR)。启用 ZDR 后，Claude Code 会话期间生成的提示和模型响应将被实时处理，并且在返回响应后不会由 Anthropic 存储，除非需要遵守法律或打击滥用。

Claude 企业版上的 ZDR 使企业客户能够使用具有零数据保留和访问管理功能的 Claude Code：

* 每个用户的成本控制
* [分析](./analytics) 仪表板
* [服务器管理的设置](./server-managed-settings)
* 审核日志

Claude for Enterprise 上的 Claude Code 的 ZDR 仅适用于 Anthropic 的直接平台。对于 AWS Bedrock、Google Vertex AI 或 Microsoft Foundry 上的 Claude 部署，请参阅这些平台的数据保留策略。

## ZDR 范围

ZDR 涵盖了企业版 Claude 上的 Claude Code 推理。

**警告**

ZDR 在每个组织的基础上启用。每个新组织都要求您的 Anthropic 客户团队单独启用 ZDR。 ZDR 不会自动应用于同一帐户下创建的新组织。请联系您的客户团队，为任何新组织启用 ZDR。

### ZDR 涵盖的内容

ZDR 涵盖通过 Claude Code 在 Claude for Enterprise 上进行的模型推理调用。当您在终端中使用 Claude Code 时，Anthropic 不会保留您发送的提示和 Claude 生成的响应。无论使用哪种 Claude 模型，这都适用。

### ZDR 不涵盖的内容

ZDR 不会扩展到以下内容，即使对于启用了 ZDR 的组织也是如此。这些功能遵循[标准数据保留策略](./data-usage#data-retention)：|特色 |详情 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|在 claude.ai 上聊天 | ZDR 不涵盖通过 Claude for Enterprise Web 界面进行的聊天对话。                                                                                                                                                                  |
|联合办公| ZDR 不涵盖 Cowork 会话。                                                                                                                                                                                                                     |
| Claude Code 分析 |不存储提示或模型响应，但收集生产力元数据，例如帐户电子邮件和使用情况统计数据。贡献指标不适用于 ZDR 组织； [分析仪表板](./analytics) 仅显示使用情况指标。 |
|用户和席位管理 |帐户电子邮件和席位分配等管理数据根据标准政策保留。                                                                                                                                                        |
|第三方集成 | ZDR 不涵盖由第三方工具、MCP 服务器或其他外部集成处理的数据。独立审查这些服务的数据处理实践。                                                                                       |

## ZDR 下禁用的功能

当在 Claude for Enterprise 上为 Claude Code 组织启用 ZDR 时，需要存储提示或完成的某些功能将在后端级别自动禁用：

|特色|原因 |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [网络上的 Claude Code](./claude-code-on-the-web) |需要服务器端存储对话历史记录。                   |
|从桌面应用程序进行[远程会话](./desktop#remote-sessions) |需要包含提示和完成的持久会话数据。 |
|反馈提交 (`/feedback`) |提交反馈会将对话数据发送至 Anthropic。               |

无论客户端显示如何，这些功能都会在后端被阻止。如果您在启动过程中看到 Claude Code 终端中的禁用功能，尝试使用它会返回错误，指示组织的策略不允许该操作。如果未来的功能需要存储提示或完成，也可能会被禁用。

## 违反政策的数据保留

即使启用了 ZDR，Anthropic 也可能会根据法律要求保留数据或解决违反使用政策的问题。如果会话被标记为违反策略，Anthropic 可以将关联的输入和输出保留最多 2 年，这与 Anthropic 的标准 ZDR 策略一致。

## 请求 ZDR

要在 Claude for Enterprise 上请求 Claude Code 的 ZDR，请联系您的 Anthropic 客户团队。您的客户团队将在内部提交请求，Anthropic 将在确认资格后在您的组织上审核并启用 ZDR。所有启用操作都会进行审核记录。

如果您当前通过即用即付 API 密钥使用适用于 Claude Code 的 ZDR，则可以转换到适用于企业版的 Claude，以访问管理功能，同时保留适用于 Claude Code 的 ZDR。请联系您的客户团队来协调迁移。
