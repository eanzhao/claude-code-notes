---
title: "LLM网关配置"
order: 36
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "了解如何配置 Claude Code 以与 LLM 网关解决方案配合使用。涵盖网关要求、身份验证配置、模型选择和特定于提供商的端点设置。"
sourceUrl: "https://code.claude.com/docs/en/llm-gateway.md"
sourceTitle: "LLM gateway configuration"
tags: []
---
#LLM网关配置

> 了解如何配置 Claude Code 以与 LLM 网关解决方案配合使用。涵盖网关要求、身份验证配置、模型选择和特定于提供商的端点设置。

LLM 网关在 Claude Code 和模型提供商之间提供集中代理层，通常提供：

* **集中身份验证** - 单点 API 密钥管理
* **使用情况跟踪** - 监控跨团队和项目的使用情况
* **成本控制** - 实施预算和费率限制
* **审核日志** - 跟踪所有模型交互以确保合规性
* **模型路由** - 在提供者之间切换，无需更改代码

## 网关要求

对于与 Claude Code 配合使用的 LLM 网关，必须满足以下要求：

**API格式**

网关必须向客户端至少公开以下 API 格式之一：

1. **Anthropic 消息**：`/v1/messages`、`/v1/messages/count_tokens`
   * 必须转发请求标头：`anthropic-beta`、`anthropic-version`

2. **Bedrock 调用模型**：`/invoke`、`/invoke-with-response-stream`
   * 必须保留请求正文字段：`anthropic_beta`、`anthropic_version`

3. **Vertex 原始预测**：`:rawPredict`、`:streamRawPredict`、`/count-tokens:rawPredict`
   * 必须转发请求标头：`anthropic-beta`、`anthropic-version`

未能转发标头或保留正文字段可能会导致功能减少或无法使用 Claude Code 功能。

**注意**

Claude Code 根据 API 格式确定启用哪些功能。在 Bedrock 或 Vertex 中使用 Anthropic 消息格式时，您可能需要设置环境变量 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`。

## 配置

### 型号选择

默认情况下，Claude Code 将使用所选 API 格式的标准模型名称。

如果您已在网关中配置自定义模型名称，请使用[模型配置](./model-config) 中记录的环境变量来匹配您的自定义名称。

## LiteLLM 配置

**注意**

LiteLLM 是第三方代理服务。 Anthropic 不认可、维护或审核 LiteLLM 的安全性或功能。本指南仅供参考，可能会过时。请自行决定使用。

### 先决条件

* Claude Code更新至最新版本
* LiteLLM代理服务器已部署且可访问
* 通过您选择的提供商访问 Claude 型号

### LiteLLM 基本设置

**配置 Claude Code**：

#### 身份验证方法

##### 静态 API 密钥

使用固定 API 密钥的最简单方法：

```bash
# Set in environment
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Or in Claude Code settings
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

该值将作为 `Authorization` 标头发送。

##### 带有帮助程序的动态 API 密钥

对于轮换密钥或每用户身份验证：

1. 创建 API 密钥帮助程序脚本：

```bash
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. 配置 Claude Code 设置以使用帮助程序：

```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. 设置令牌刷新间隔：

```bash
# Refresh every hour (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

该值将作为 `Authorization` 和 `X-Api-Key` 标头发送。 `apiKeyHelper` 的优先级低于 `ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_API_KEY`。

#### 统一端点（推荐）

使用 LiteLLM 的 [Anthropic 格式端点](https://docs.litellm.ai/docs/anthropic_unified)：

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**统一端点相对于直通端点的优势：**

* 负载均衡
* 后备方案
* 对成本跟踪和最终用户跟踪的一致支持

#### 特定于提供商的传递端点（替代）##### Claude API 通过 LiteLLM

使用[直通端点](https://docs.litellm.ai/docs/pass_through/anthropic_completion)：

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock 通过 LiteLLM

使用[直通端点](https://docs.litellm.ai/docs/pass_through/bedrock)：

```bash
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI 通过 LiteLLM

使用[直通端点](https://docs.litellm.ai/docs/pass_through/vertex_ai)：

```bash
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

有关更多详细信息，请参阅 [LiteLLM 文档](https://docs.litellm.ai/)。

## 其他资源

* [LiteLLM 文档](https://docs.litellm.ai/)
* [Claude Code 设置](./settings)
* [企业网络配置](./network-config)
* [第三方集成概述](./third-party-integrations)
