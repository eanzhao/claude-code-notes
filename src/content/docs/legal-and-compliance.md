---
title: "法律与合规"
order: 65
section: "resources"
sectionLabel: "资源"
sectionOrder: 9
summary: "Claude Code 的法律协议、合规性认证和安全信息。"
sourceUrl: "https://code.claude.com/docs/en/legal-and-compliance.md"
sourceTitle: "Legal and compliance"
tags: []
---
# 法律与合规

> Claude Code 的法律协议、合规认证和安全信息。

## 法律协议

### 许可证

Claude Code 的使用须遵守：

* [商业条款](https://www.anthropic.com/legal/commercial-terms) - 适用于 Teams、Enterprise 和 Claude API 用户
* [消费者服务条款](https://www.anthropic.com/legal/consumer-terms) - 适用于 Free、Pro 和 Max 用户

### 商业协议

无论你是直接使用 Claude API（第一方）还是通过 AWS Bedrock 或 Google Vertex（第三方）访问，你现有的商业协议都适用于 Claude Code 的使用，除非双方另有约定。

## 合规

### 医疗合规 (BAA)

如果客户与 Anthropic 签订了商业伙伴协议 (BAA) 并希望在 Claude Code 上使用，只要客户已执行 BAA 并激活了[零数据保留 (ZDR)](./zero-data-retention)，BAA 将自动扩展覆盖 Claude Code。BAA 适用于该客户通过 Claude Code 的 API 流量。ZDR 按组织级别启用，每个组织必须单独启用 ZDR 才能纳入 BAA 覆盖范围。

## 使用政策

### 可接受使用

Claude Code 的使用须遵守 [Anthropic 使用政策](https://www.anthropic.com/legal/aup)。Pro 和 Max 方案公布的使用限制以 Claude Code 和 Agent SDK 的正常个人使用为前提。

### 认证与凭据使用

Claude Code 通过 OAuth token 或 API 密钥向 Anthropic 服务器认证。这些认证方式有不同的适用范围：

* **OAuth 认证**（适用于 Free、Pro 和 Max 方案）仅限用于 Claude Code 和 Claude.ai。不允许在任何其他产品、工具或服务（包括 [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)）中使用通过 Claude Free、Pro 或 Max 账户获得的 OAuth token，否则违反[消费者服务条款](https://www.anthropic.com/legal/consumer-terms)。
* **开发者**如果构建与 Claude 功能交互的产品或服务（包括使用 [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 的产品），应通过 [Claude Console](https://platform.claude.com/) 或支持的云服务商使用 API 密钥认证。Anthropic 不允许第三方开发者代表其用户提供 Claude.ai 登录或通过 Free、Pro、Max 方案的凭据路由请求。

Anthropic 保留执行这些限制的权利，并可能在不事先通知的情况下采取行动。

如果你对用例允许的认证方式有疑问，请[联系销售](https://www.anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=legal_compliance_contact_sales)。

## 安全与信任

### 信任与安全

更多信息请访问 [Anthropic 信任中心](https://trust.anthropic.com) 和[透明中心](https://www.anthropic.com/transparency)。

### 安全漏洞报告

Anthropic 通过 HackerOne 管理安全项目。[点此报告漏洞](https://hackerone.com/anthropic-vdp/reports/new?type=team&report_type=vulnerability)。

***

&copy; Anthropic PBC. 保留所有权利。使用须遵守适用的 Anthropic 服务条款。
