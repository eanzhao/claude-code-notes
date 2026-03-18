---
title: "Claude Code GitLab CI/CD"
order: 13
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "了解如何使用 GitLab CI/CD 将 Claude Code 集成到您的开发工作流程中"
sourceUrl: "https://code.claude.com/docs/en/gitlab-ci-cd.md"
sourceTitle: "Claude Code GitLab CI/CD"
group: "Platforms and integrations > Code review & CI/CD"
groupLabel: "代码评审与 CI/CD"
tags: []
---
# Claude Code GitLab CI/CD

> 将 Claude Code 集成到你的 GitLab 开发工作流中

**说明**

Claude Code for GitLab CI/CD 目前处于 Beta 阶段。功能和特性可能会随着体验改进而演进。

此集成由 GitLab 维护。如需帮助，请参见 [GitLab issue](https://gitlab.com/gitlab-org/gitlab/-/issues/573776)。

**注意**

此集成基于 [Claude Code CLI 和 Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 构建，支持在 CI/CD 任务和自定义自动化工作流中以编程方式使用 Claude。

## 为什么将 Claude Code 与 GitLab 搭配使用？

* **即时创建 MR**：描述你的需求，Claude 提交包含完整改动和说明的 MR
* **自动化实现**：一条命令或一个 @提及就能把 issue 变成可运行的代码
* **理解项目上下文**：Claude 遵循你的 `CLAUDE.md` 规则和现有代码模式
* **设置简单**：在 `.gitlab-ci.yml` 中加一个 job，配一个 masked CI/CD 变量就行
* **企业级就绪**：可选 Claude API、AWS Bedrock 或 Google Vertex AI，满足数据驻留和采购需求
* **默认安全**：运行在你的 GitLab runner 上，受你的分支保护和审批规则约束

## 工作原理

Claude Code 通过 GitLab CI/CD 在隔离的 job 中运行 AI 任务，并通过 MR 提交结果：

1. **事件驱动编排**：GitLab 监听你选择的触发器（例如在 issue、MR 或审查线程中 @claude 的评论）。Job 从线程和仓库收集上下文，构建 prompt，然后运行 Claude Code。

2. **提供商抽象**：选择适合你环境的提供商：
   * Claude API（SaaS）
   * AWS Bedrock（基于 IAM 的访问，支持跨区域）
   * Google Vertex AI（GCP 原生，Workload Identity Federation）

3. **沙盒执行**：每次交互在带有严格网络和文件系统规则的容器中运行。Claude Code 强制执行工作区级权限来限制写入。所有变更都走 MR 流程，审查者可以看到 diff，审批规则照常生效。

选择就近的区域端点来减少延迟，满足数据主权要求，同时复用现有的云协议。

## Claude 能做什么？

Claude Code 支持强大的 CI/CD 工作流，改变你的开发方式：

* 根据 issue 描述或评论创建和更新 MR
* 分析性能回归并建议优化方案
* 直接在分支上实现功能，然后开 MR
* 修复测试或审查中发现的 bug 和回归问题
* 回复后续评论，迭代改进

## 设置

### 快速设置

最快的上手方式是在 `.gitlab-ci.yml` 中加一个最简 job，然后把 API 密钥设为 masked 变量。

1. **添加 masked CI/CD 变量**
   * 前往 **Settings** → **CI/CD** → **Variables**
   * 添加 `ANTHROPIC_API_KEY`（按需设为 masked、protected）

2. **在 `.gitlab-ci.yml` 中添加 Claude job**

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Adjust rules to fit how you want to trigger the job:
  # - manual runs
  # - merge request events
  # - web/API triggers when a comment contains '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    # Optional: start a GitLab MCP server if your setup provides one
    - /bin/gitlab-mcp-server || true
    # Use AI_FLOW_* variables when invoking via web/API triggers with context payloads
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

添加 job 和 `ANTHROPIC_API_KEY` 变量后，从 **CI/CD** → **Pipelines** 手动运行 job 来测试，或通过 MR 触发，让 Claude 在分支中提交更新，需要时会自动开 MR。

**注意**

要在 AWS Bedrock 或 Google Vertex AI 上运行（而非 Claude API），请参阅下面的[与 AWS Bedrock 和 Google Vertex AI 一起使用](#using-with-aws-bedrock--google-vertex-ai)部分。

### 手动设置（推荐生产环境使用）

如果你需要更精细的控制或企业级提供商：

1. **配置提供商访问**：
   * **Claude API**：创建 `ANTHROPIC_API_KEY` 并存为 masked CI/CD 变量
   * **AWS Bedrock**：配置 GitLab → AWS OIDC 并为 Bedrock 创建 IAM 角色
   * **Google Vertex AI**：为 GitLab → GCP 配置 Workload Identity Federation

2. **添加 GitLab API 操作的项目凭证**：
   * 默认使用 `CI_JOB_TOKEN`，或创建具有 `api` scope 的 Project Access Token
   * 如果使用 PAT，存为 `GITLAB_ACCESS_TOKEN`（masked）

3. **在 `.gitlab-ci.yml` 中添加 Claude job**（参见下方示例）

4. **（可选）启用 @提及驱动的触发器**：
   * 添加"Comment (note)"类型的项目 Webhook 到你的事件监听器
   * 当评论包含 `@claude` 时，监听器通过 pipeline trigger API 调用，传递 `AI_FLOW_INPUT` 和 `AI_FLOW_CONTEXT` 等变量

## 示例用法

### 把 issue 变成 MR

在 issue 评论中：

```text
@claude implement this feature based on the issue description
```

Claude 分析 issue 和代码库，在分支中写入改动，并开 MR 供审查。

### 获取实现建议

在 MR 讨论中：

```text
@claude suggest a concrete approach to cache the results of this API call
```

Claude 提出方案，添加合适的缓存代码，并更新 MR。

### 快速修 bug

在 issue 或 MR 评论中：

```text
@claude fix the TypeError in the user dashboard component
```

Claude 定位 bug，实现修复，更新分支或开新 MR。

## 与 AWS Bedrock 和 Google Vertex AI 一起使用

在企业环境中，你可以完全在自己的云基础设施上运行 Claude Code，保持相同的开发体验。

### AWS Bedrock

### 前置条件

配置之前你需要：

1. 有 Amazon Bedrock 权限的 AWS 账号，可以访问所需的 Claude 模型
2. GitLab 在 AWS IAM 中配置为 OIDC 身份提供商
3. 具有 Bedrock 权限的 IAM 角色，信任策略限定到你的 GitLab 项目/ref
4. GitLab 角色 assume 所需的 CI/CD 变量：
   * `AWS_ROLE_TO_ASSUME`（角色 ARN）
   * `AWS_REGION`（Bedrock 区域）

### 设置步骤

配置 AWS 让 GitLab CI job 通过 OIDC assume IAM 角色（无静态密钥）。

**所需步骤：**

1. 启用 Amazon Bedrock 并申请目标 Claude 模型的访问权限
2. 为 GitLab 创建 IAM OIDC Provider（如果还没有的话）
3. 创建被 GitLab OIDC Provider 信任的 IAM 角色，限定到你的项目和受保护的 ref
4. 附加 Bedrock 调用 API 所需的最小权限

**需要存为 CI/CD 变量的值：**

* `AWS_ROLE_TO_ASSUME`
* `AWS_REGION`

在 Settings → CI/CD → Variables 中添加：

```yaml
# For AWS Bedrock:
- AWS_ROLE_TO_ASSUME
- AWS_REGION
```

用下方的 AWS Bedrock job 示例，在运行时将 GitLab job token 换取临时 AWS 凭证。


### Google Vertex AI

### 前置条件

配置之前你需要：

1. 一个 Google Cloud 项目：
   * 启用了 Vertex AI API
   * Workload Identity Federation 配置为信任 GitLab OIDC
2. 只授予所需 Vertex AI 角色的专用服务账号
3. WIF 所需的 GitLab CI/CD 变量：
   * `GCP_WORKLOAD_IDENTITY_PROVIDER`（完整资源名称）
   * `GCP_SERVICE_ACCOUNT`（服务账号邮箱）

### 设置步骤

配置 Google Cloud 让 GitLab CI job 通过 Workload Identity Federation 模拟服务账号。

**所需步骤：**

1. 启用 IAM Credentials API、STS API 和 Vertex AI API
2. 为 GitLab OIDC 创建 Workload Identity Pool 和 Provider
3. 创建具有 Vertex AI 角色的专用服务账号
4. 授予 WIF principal 模拟服务账号的权限

**需要存为 CI/CD 变量的值：**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`
* `GCP_SERVICE_ACCOUNT`

在 Settings → CI/CD → Variables 中添加：

```yaml
# For Google Vertex AI:
- GCP_WORKLOAD_IDENTITY_PROVIDER
- GCP_SERVICE_ACCOUNT
- CLOUD_ML_REGION (for example, us-east5)
```

用下方的 Google Vertex AI job 示例进行认证，无需存储密钥。

## 配置示例

以下是可直接使用的代码片段，按你的流水线需要调整。

### 基本 .gitlab-ci.yml（Claude API）

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code will use ANTHROPIC_API_KEY from CI/CD variables
```

### AWS Bedrock job 示例（OIDC）

**前置条件：**

* Amazon Bedrock 有你选择的 Claude 模型访问权限
* GitLab OIDC 在 AWS 中配置完毕，角色信任你的 GitLab 项目和 ref
* 具有 Bedrock 权限的 IAM 角色（建议最小权限）

**所需的 CI/CD 变量：**

* `AWS_ROLE_TO_ASSUME`：用于 Bedrock 访问的 IAM 角色 ARN
* `AWS_REGION`：Bedrock 区域（如 `us-west-2`）

```yaml
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Exchange GitLab OIDC token for AWS credentials
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

**注意**

Bedrock 的模型 ID 包含区域前缀（如 `us.anthropic.claude-sonnet-4-6`）。如果你的工作流支持，可通过 job 配置或 prompt 传入所需模型。

### Google Vertex AI job 示例（Workload Identity Federation）

**前置条件：**

* GCP 项目中启用了 Vertex AI API
* Workload Identity Federation 配置为信任 GitLab OIDC
* 具有 Vertex AI 权限的服务账号

**所需的 CI/CD 变量：**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`：完整的 Provider 资源名称
* `GCP_SERVICE_ACCOUNT`：服务账号邮箱
* `CLOUD_ML_REGION`：Vertex 区域（如 `us-east5`）

```yaml
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git && apt-get clean
    - curl -fsSL https://claude.ai/install.sh | bash
    # Authenticate to Google Cloud via WIF (no downloaded keys)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Review and update code as requested'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

**注意**

使用 Workload Identity Federation 不需要存储服务账号密钥。建议使用仓库级的信任条件和最小权限服务账号。

## 最佳实践

### CLAUDE.md 配置

在仓库根目录创建 `CLAUDE.md` 文件，定义编码标准、审查标准和项目规则。Claude 在运行时会读取这个文件，提交改动时遵循你的约定。

### 安全注意事项

**绝不要把 API 密钥或云凭证提交到仓库**。始终使用 GitLab CI/CD 变量：

* 把 `ANTHROPIC_API_KEY` 添加为 masked 变量（按需设为 protected）
* 尽量使用提供商特定的 OIDC（无长期密钥）
* 限制 job 权限和网络出口
* 像审查其他贡献者的代码一样审查 Claude 的 MR

### 优化性能

* 保持 `CLAUDE.md` 聚焦简洁
* 提供清晰的 issue/MR 描述以减少迭代次数
* 配置合理的 job 超时以避免任务失控
* 在 runner 中尽量缓存 npm 和包安装

### CI 成本

将 Claude Code 与 GitLab CI/CD 搭配使用时，注意相关成本：

* **GitLab runner 运行时间**：
  * Claude 在 GitLab runner 上运行，消耗计算时间
  * 详情参见 GitLab 各版本的 runner 计费说明

* **API 成本**：
  * 每次 Claude 交互根据 prompt 和回复大小消耗 token
  * Token 用量取决于任务复杂度和代码库大小
  * 详情参见 [Anthropic 定价](https://platform.claude.com/docs/en/about-claude/pricing)

* **成本优化建议**：
  * 用明确的 `@claude` 指令减少不必要的对话轮次
  * 设置合理的 `max_turns` 和 job 超时值
  * 限制并发来控制并行运行数

## 安全和治理

* 每个 job 都在隔离容器中运行，网络访问受限
* Claude 的改动走 MR 流程，审查者可以看到每个 diff
* 分支保护和审批规则同样适用于 AI 生成的代码
* Claude Code 使用工作区级权限限制写入范围
* 费用在你的控制之下，因为你用自己的提供商凭证

## 故障排查

### Claude 不响应 @claude 命令

* 确认 pipeline 被正确触发（手动、MR 事件或通过评论事件监听器/webhook）
* 确保 CI/CD 变量（`ANTHROPIC_API_KEY` 或云提供商配置）已设置且未被 mask 规则屏蔽
* 检查评论包含 `@claude`（不是 `/claude`），且你的 @提及触发器已配置

### Job 无法发评论或开 MR

* 确保 `CI_JOB_TOKEN` 对项目有足够权限，或使用具有 `api` scope 的 Project Access Token
* 检查 `--allowedTools` 中是否启用了 `mcp__gitlab` 工具
* 确认 job 运行在 MR 上下文中，或通过 `AI_FLOW_*` 变量提供了足够上下文

### 认证错误

* **Claude API**：确认 `ANTHROPIC_API_KEY` 有效且未过期
* **Bedrock/Vertex**：验证 OIDC/WIF 配置、角色模拟和 secret 名称；确认区域和模型可用

## 高级配置

### 常用参数和变量

Claude Code 支持以下常用输入：

* `prompt` / `prompt_file`：通过 `-p` 提供内联指令或通过文件提供
* `max_turns`：限制来回迭代次数
* `timeout_minutes`：限制总执行时间
* `ANTHROPIC_API_KEY`：Claude API 必需（Bedrock/Vertex 不需要）
* 提供商特定的环境变量：`AWS_REGION`、Vertex 的项目/区域变量

**注意**

具体的 flag 和参数可能因 `@anthropic-ai/claude-code` 版本而异。在 job 中运行 `claude --help` 查看支持的选项。

### 自定义 Claude 的行为

有两种主要方式来引导 Claude：

1. **CLAUDE.md**：定义编码标准、安全要求和项目约定。Claude 在运行时读取此文件并遵循你的规则。
2. **自定义 prompt**：通过 job 中的 `prompt`/`prompt_file` 传入任务特定的指令。对不同任务使用不同的 prompt（如审查、实现、重构）。
