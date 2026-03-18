---
title: "Claude Code 上 Microsoft Foundry"
order: 34
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "了解如何通过 Microsoft Foundry 配置 Claude Code，包括设置、配置和故障排除。"
sourceUrl: "https://code.claude.com/docs/en/microsoft-foundry.md"
sourceTitle: "Claude Code on Microsoft Foundry"
tags: []
---
# Claude Code 于 Microsoft Foundry

> 了解如何通过 Microsoft Foundry 配置 Claude Code，包括设置、配置和故障排除。

## 先决条件

在使用 Microsoft Foundry 配置 Claude Code 之前，请确保您拥有：

* 可访问 Microsoft Foundry 的 Azure 订阅
* 创建 Microsoft Foundry 资源和部署的 RBAC 权限
* 安装并配置 Azure CLI（可选 - 仅当您没有其他获取凭据的机制时才需要）

**注意**

如果您要将 Claude Code 部署给多个用户，请[固定您的模型版本](#4-pin-model-versions)，以防止 Anthropic 发布新模型时出现损坏。

## 设置

### 1.配置Microsoft Foundry资源

首先，在 Azure 中创建 Claude 资源：

1. 导航至 [Microsoft Foundry 门户](https://ai.azure.com/)
2. 创建一个新资源，记下您的资源名称
3. 为 Claude 模型创建部署：
   * Claude 作品
   * Claude 十四行诗
   * Claude 俳句

### 2.配置Azure凭据

Claude Code 支持 Microsoft Foundry 的两种身份验证方法。选择最适合您的安全要求的方法。

**选项 A：API 密钥身份验证**

1. 导航到 Microsoft Foundry 门户中的资源
2. 转到 **端点和键** 部分
3. 复制**API密钥**
4. 设置环境变量：

```bash
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**选项 B：Microsoft Entra ID 身份验证**

如果未设置 `ANTHROPIC_FOUNDRY_API_KEY`，Claude Code 将自动使用 Azure SDK [默认凭据链](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview)。
这支持多种用于验证本地和远程工作负载的方法。

在本地环境中，您通常可以使用 Azure CLI：

```bash
az login
```

**注意**

使用 Microsoft Foundry 时，`/login` 和 `/logout` 命令将被禁用，因为身份验证是通过 Azure 凭据处理的。

### 3.配置Claude Code

设置以下环境变量以启用 Microsoft Foundry：

```bash
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. 引脚型号版本

**警告**

为每个部署固定特定的模型版本。如果您在未固定的情况下使用模型别名（`sonnet`、`opus`、`haiku`），Claude Code 可能会尝试使用您的 Foundry 帐户中不可用的较新模型版本，从而在 Anthropic 发布更新时破坏现有用户。创建 Azure 部署时，选择特定模型版本，而不是“自动更新到最新版本”。

设置模型变量以匹配您在步骤 1 中创建的部署名称：

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

有关当前和旧版型号 ID，请参阅[型号概述](https://platform.claude.com/docs/en/about-claude/models/overview)。有关环境变量的完整列表，请参阅[模型配置](./model-config#pin-models-for-third-party-deployments)。

## Azure RBAC 配置

`Azure AI User` 和 `Cognitive Services User` 默认角色包括调用 Claude 模型所需的所有权限。

要获得更多限制性权限，请使用以下内容创建自定义角色：

```json
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

有关详细信息，请参阅 [Microsoft Foundry RBAC 文档](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry)。

## 故障排除

如果收到错误“无法从 azureADTokenProvider 获取令牌：ChainedTokenCredential 身份验证失败”：

* 在环境中配置Entra ID，或设置`ANTHROPIC_FOUNDRY_API_KEY`。

## 其他资源* [Microsoft Foundry 文档](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry 型号](https://ai.azure.com/explore/models)
* [Microsoft Foundry 定价](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
