---
title: "Claude Code 上 Amazon Bedrock"
order: 32
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "了解如何通过 Amazon Bedrock 配置 Claude Code，包括设置、IAM 配置和故障排除。"
sourceUrl: "https://code.claude.com/docs/en/amazon-bedrock.md"
sourceTitle: "Claude Code on Amazon Bedrock"
tags: []
---
# Claude Code 于 Amazon Bedrock

> 了解如何通过 Amazon Bedrock 配置 Claude Code，包括设置、IAM 配置和故障排除。

## 先决条件

在使用 Bedrock 配置 Claude Code 之前，请确保您拥有：

* 启用了 Bedrock 访问的 AWS 账户
* 在基岩中访问所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 安装并配置 AWS CLI（可选 - 仅当您没有其他获取凭证的机制时才需要）
* 适当的 IAM 权限

**注意**

如果您要将 Claude Code 部署给多个用户，请[固定您的模型版本](#4-pin-model-versions)，以防止 Anthropic 发布新模型时出现损坏。

## 设置

### 1.提交用例详细信息

Anthropic 模型的首次用户需要在调用模型之前提交用例详细信息。每个帐户执行一次此操作。

1. 确保您拥有正确的 IAM 权限（请参阅下面的更多信息）
2. 导航至[Amazon Bedrock控制台](https://console.aws.amazon.com/bedrock/)
3. 选择**聊天/文本游乐场**
4. 选择任意 Anthropic 型号，系统将提示您填写用例表

### 2.配置AWS凭证

Claude Code 使用默认的 AWS 开发工具包凭证链。使用以下方法之一设置您的凭据：

**选项 A：AWS CLI 配置**

```bash
aws configure
```

**选项 B：环境变量（访问密钥）**

```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**选项 C：环境变量（SSO 配置文件）**

```bash
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**选项 D：AWS 管理控制台凭证**

```bash
aws login
```

[了解更多](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)关于`aws login`。

**选项 E：基岩 API 密钥**

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 密钥提供更简单的身份验证方法，无需完整的 AWS 凭证。 [了解有关 Bedrock API 密钥的更多信息](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)。

#### 高级凭证配置

Claude Code 支持 AWS SSO 和企业身份提供商的自动凭证刷新。将这些设置添加到 Claude Code 设置文件中（有关文件位置，请参阅[设置](./settings)）。

当 Claude Code 检测到您的 AWS 凭证已过期（根据其时间戳在本地或当 Bedrock 返回凭证错误时），它将自动运行您配置的 `awsAuthRefresh` 和/或 `awsCredentialExport` 命令以在重试请求之前获取新凭证。

##### 配置示例

```json
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### 配置设置解释

**`awsAuthRefresh`**：将此用于修改 `.aws` 目录的命令，例如更新凭据、SSO 缓存或配置文件。命令的输出显示给用户，但不支持交互式输入。这对于基于浏览器的 SSO 流程非常有效，其中 CLI 显示 URL 或代码，并且您可以在浏览器中完成身份验证。

**`awsCredentialExport`**：仅当您无法修改 `.aws` 并且必须直接返回凭据时才使用此选项。输出以静默方式捕获，不会向用户显示。该命令必须按以下格式输出 JSON：

```json
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3.配置Claude Code

设置以下环境变量以启用 Bedrock：

```bash
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku)
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

为 Claude Code 启用 Bedrock 时，请记住以下几点：* `AWS_REGION` 是必需的环境变量。 Claude Code 不会从 `.aws` 配置文件中读取此设置。
* 使用 Bedrock 时，`/login` 和 `/logout` 命令被禁用，因为身份验证是通过 AWS 凭证处理的。
* 您可以使用环境变量的设置文件，例如 `AWS_PROFILE`，您不想泄漏到其他进程。有关详细信息，请参阅[设置](./settings)。

### 4. 引脚型号版本

**警告**

为每个部署固定特定的模型版本。如果您在未固定的情况下使用模型别名（`sonnet`、`opus`、`haiku`），Claude Code 可能会尝试使用您的 Bedrock 帐户中不可用的较新模型版本，从而在 Anthropic 发布更新时破坏现有用户。

将这些环境变量设置为特定的基岩模型 ID：

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

这些变量使用跨区域推理配置文件 ID（带有 `us.` 前缀）。如果您使用不同的区域前缀或应用程序推理配置文件，请进行相应调整。有关当前和旧版型号 ID，请参阅[型号概述](https://platform.claude.com/docs/en/about-claude/models/overview)。有关环境变量的完整列表，请参阅[模型配置](./model-config#pin-models-for-third-party-deployments)。

当未设置固定变量时，Claude Code 使用这些默认模型：

|型号类型|默认值|
| ：-------------- | :-------------------------------------------------------- |
|主要型号| `global.anthropic.claude-sonnet-4-6` |
|小型/快速型号 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

要进一步自定义模型，请使用以下方法之一：

```bash
# Using inference profile ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

**注意**

[提示缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 可能并非在所有区域都可用。

#### 将每个模型版本映射到推理配置文件

`ANTHROPIC_DEFAULT_*_MODEL` 环境变量为每个模型系列配置一个推理配置文件。如果您的组织需要在 `/model` 选择器中公开同一系列的多个版本（每个版本都路由到自己的应用程序推理配置文件 ARN），请改用[设置文件](./settings#settings-files) 中的 `modelOverrides` 设置。

此示例将三个 Opus 版本映射到不同的 ARN，以便用户可以在它们之间进行切换，而无需绕过组织的推理配置文件：

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

当用户在 `/model` 中选择这些版本之一时，Claude Code 将使用映射的 ARN 调用 Bedrock。没有覆盖的版本会回退到内置基岩模型 ID 或启动时发现的任何匹配的推理配置文件。有关覆盖如何与 `availableModels` 和其他模型设置交互的详细信息，请参阅[覆盖每个版本的模型 ID](./model-config#override-model-ids-per-version)。

## IAM 配置

创建具有 Claude Code 所需权限的 IAM 策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

对于更严格的权限，您可以将资源限制为特定的推理配置文件 ARN。

有关详细信息，请参阅[Bedrock IAM 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)。

**注意**

为 Claude Code 创建专用 AWS 账户以简化成本跟踪和访问控制。

## AWS 护栏[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) 可让您对 Claude Code 实施内容过滤。在 [Amazon Bedrock 控制台](https://console.aws.amazon.com/bedrock/) 中创建 Guardrail，发布版本，然后将 Guardrail 标头添加到您的[设置文件](./settings)。如果您使用跨区域推理配置文件，请在 Guardrail 上启用跨区域推理。

配置示例：

```json
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## 故障排除

如果您遇到区域问题：

* 检查型号可用性：`aws bedrock list-inference-profiles --region your-region`
* 切换到支持的区域：`export AWS_REGION=us-east-1`
* 考虑使用推理配置文件进行跨区域访问

如果您收到错误“不支持按需吞吐量”：

* 将模型指定为[推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

Claude Code 使用 Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)，不支持 Converse API。

## 其他资源

* [基岩文档](https://docs.aws.amazon.com/bedrock/)
* [基岩定价](https://aws.amazon.com/bedrock/pricing/)
* [基岩推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Amazon Bedrock 上的 Claude Code：快速设置指南](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)- [Claude Code 监控实施 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
