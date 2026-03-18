---
title: "企业部署概述"
order: 31
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "了解 Claude Code 如何与各种第三方服务和基础设施集成以满足企业部署要求。"
sourceUrl: "https://code.claude.com/docs/en/third-party-integrations.md"
sourceTitle: "Enterprise deployment overview"
tags: []
---
# 企业部署概述

> 了解 Claude Code 如何与各种第三方服务和基础设施集成以满足企业部署要求。

组织可以直接通过 Anthropic 或通过云提供商部署 Claude Code。此页面可帮助您选择正确的配置。

## 比较部署选项

对于大多数组织来说，Claude for Teams 或 Claude for Enterprise 可提供最佳体验。团队成员只需一次订阅、集中计费即可在网络上访问 Claude Code 和 Claude，无需进行基础设施设置。

**Claude for Teams** 是自助服务，包括协作功能、管理工具和计费管理。最适合需要快速入门的小型团队。

**Claude for Enterprise** 添加了 SSO 和域捕获、基于角色的权限、合规性 API 访问以及托管策略设置，用于部署组织范围内的 Claude Code 配置。最适合具有安全性和合规性要求的大型组织。

了解有关[团队计划](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) 和[企业计划](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan) 的更多信息。

如果您的组织有特定的基础架构要求，请比较以下选项：

  
    
      特点
      Claude 适用于团队/企业
      Anthropic 控制台
      Amazon Bedrock
      Google Vertex AI
      Microsoft Foundry
    
  

  
    
      最适合
      大多数组织（推荐）
      个人开发者
      AWS 原生部署
      GCP 原生部署
      Azure 本机部署
    

    
      计费
      **团队：** \$150/席位（高级），可使用现收现付
**企业：** [联系销售人员](https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise)
      现收现付
      通过 AWS 付费
      通过 GCP 现收现付
      通过 Azure 付费
    

    
      地区
      支持的[国家/地区](https://www.anthropic.com/supported-countries)
      支持的[国家/地区](https://www.anthropic.com/supported-countries)
      多个 AWS [区域](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)
      多个 GCP [区域](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)
      多个 Azure [区域](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)
    

    
      提示缓存
      默认启用
      默认启用
      默认启用
      默认启用
      默认启用
    

    
      认证
      Claude.ai SSO 或电子邮件
      API密钥
      API 密钥或 AWS 凭证
      GCP 凭据
      API 密钥或 Microsoft Entra ID
    

    
      成本追踪
      使用情况仪表板
      使用情况仪表板
      AWS 成本管理器
      GCP 结算
      Azure 成本管理
    

    
      包括网络上的 Claude
      是的
      否
      否
      否
      否
    

    
      企业特色
      团队管理、SSO、使用情况监控
      无
      IAM 策略、CloudTrail
      IAM 角色、云审核日志
      RBAC 策略、Azure Monitor
    
  

选择部署选项以查看设置说明：

* [Claude 适用于团队或企业](./authentication#claude-for-teams-or-enterprise)
* [Anthropic 控制台](./authentication#claude-console-authentication)
* [Amazon Bedrock](./amazon-bedrock)
* [Google Vertex AI](./google-vertex-ai)
* [Microsoft Foundry](./microsoft-foundry)

## 配置代理和网关大多数组织可以直接使用云提供商，无需额外配置。但是，如果您的组织有特定的网络或管理要求，您可能需要配置公司代理或 LLM 网关。这些是可以一起使用的不同配置：

* **企业代理**：通过 HTTP/HTTPS 代理路由流量。如果您的组织需要所有出站流量都通过代理服务器进行安全监控、合规性或网络策略实施，请使用此选项。使用 `HTTPS_PROXY` 或 `HTTP_PROXY` 环境变量进行配置。了解更多信息[企业网络配置](./network-config)。
* **LLM 网关**：位于 Claude Code 和云提供商之间的一项服务，用于处理身份验证和路由。如果您需要跨团队集中使用情况跟踪、自定义速率限制或预算或集中身份验证管理，请使用此选项。使用 `ANTHROPIC_BASE_URL`、`ANTHROPIC_BEDROCK_BASE_URL` 或 `ANTHROPIC_VERTEX_BASE_URL` 环境变量进行配置。了解更多信息 [LLM 网关配置](./llm-gateway)。

以下示例显示要在 shell 或 shell 配置文件中设置的环境变量（`.bashrc`、`.zshrc`）。其他配置方法请参见[设置](./settings)。

### Amazon Bedrock

### 公司代理

通过设置以下[环境变量](./env-vars)，通过公司代理路由 Bedrock 流量：

```bash
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'
```

  
### 法学硕士网关

通过设置以下[环境变量](./env-vars)，通过 LLM 网关路由 Bedrock 流量：

```bash
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configure LLM gateway
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
```

### Microsoft Foundry

### 公司代理

通过设置以下[环境变量](./env-vars)，通过公司代理路由 Foundry 流量：

```bash
# Enable Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'
```

  
### 法学硕士网关

通过设置以下[环境变量](./env-vars)，通过 LLM 网关路由 Foundry 流量：

```bash
# Enable Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Configure LLM gateway
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # If gateway handles Azure auth
```

### Google Vertex AI

### 公司代理

通过设置以下[环境变量](./env-vars)，通过公司代理路由 Vertex AI 流量：

```bash
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'
```

  
### 法学硕士网关

通过设置以下[环境变量](./env-vars)，通过 LLM 网关路由 Vertex AI 流量：

```bash
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configure LLM gateway
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
```

**提示**

使用 Claude Code 中的 `/status` 验证您的代理和网关配置是否正确应用。

## 组织的最佳实践

### 投资于文档和内存

我们强烈建议投资文档，以便 Claude Code 了解您的代码库。组织可以在多个级别部署 CLAUDE.md 文件：

* **组织范围**：部署到 `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) 等系统目录，以实现公司范围的标准
* **存储库级**：在存储库根目录中创建 `CLAUDE.md` 文件，其中包含项目架构、构建命令和贡献指南。将这些检查到源代码管理中，以便所有用户受益

在[内存和 CLAUDE.md 文件](./memory) 中了解更多信息。

### 简化部署

如果您有自定义开发环境，我们发现创建“一键式”安装 Claude Code 的方式是在整个组织中提高采用率的关键。

### 从指导使用开始鼓励新用户尝试 Claude Code 进行代码库问答，或者较小的错误修复或功能请求。请 Claude Code 制定计划。检查 Claude 的建议，如果偏离轨道，请提供反馈。随着时间的推移，随着用户更好地理解这种新范例，他们将更有效地让 Claude Code 更代理地运行。

### 云提供商的 Pin 模型版本

如果您通过 [Bedrock](./amazon-bedrock)、[Vertex AI](./google-vertex-ai) 或 [Foundry](./microsoft-foundry) 进行部署，请使用 `ANTHROPIC_DEFAULT_OPUS_MODEL`、`ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 固定特定型号版本。如果不固定，Claude Code 别名将解析为最新版本，当 Anthropic 发布尚未在您的帐户中启用的新模型时，这可能会破坏用户。详情请参见[型号配置](./model-config#pin-models-for-third-party-deployments)。

### 配置安全策略

安全团队可以配置 Claude Code 可以执行和不允许执行的操作的托管权限，这些权限不能被本地配置覆盖。 [了解更多](./security)。

### 利用 MCP 进行集成

MCP 是向 Claude Code 提供更多信息的好方法，例如连接到票证管理系统或错误日志。我们建议由一个中心团队配置 MCP 服务器并将 `.mcp.json` 配置检查到代码库中，以便所有用户都能受益。 [了解更多](./mcp)。

在 Anthropic，我们相信 Claude Code 能够推动每个 Anthropic 代码库的开发。我们希望您和我们一样喜欢使用 Claude Code。

## 后续步骤

选择部署选项并为您的团队配置访问权限后：

1. **向您的团队推出**：共享安装说明并让团队成员[安装 Claude Code](./setup) 并使用其凭据进行身份验证。
2. **设置共享配置**：在您的存储库中创建一个 [CLAUDE.md 文件](./memory)，以帮助 Claude Code 了解您的代码库和编码标准。
3. **配置权限**：查看[安全设置](./security) 以定义 Claude Code 在您的环境中可以执行和不能执行的操作。
