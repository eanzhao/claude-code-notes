---
title: "Claude Code GitHub Actions"
order: 12
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "了解如何使用 Claude Code 将 Claude Code 集成到您的开发工作流程中"
sourceUrl: "https://code.claude.com/docs/en/github-actions.md"
sourceTitle: "Claude Code GitHub Actions"
group: "Platforms and integrations > Code review & CI/CD"
groupLabel: "代码评审与 CI/CD"
tags: []
---
# Claude Code GitHub Actions

> 将 Claude Code 集成到你的 GitHub 开发工作流中

Claude Code GitHub Actions 为你的 GitHub 工作流带来 AI 驱动的自动化。只需在任意 PR 或 issue 中 @claude，Claude 就能分析代码、创建 pull request、实现功能、修复 bug，同时遵循你的项目规范。如果你需要在每个 PR 上自动发布审查（无需手动触发），请参阅 [GitHub 代码审查](./code-review)。

**注意**

Claude Code GitHub Actions 基于 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 构建，用于将 Claude Code 以编程方式集成到你的应用中。你可以用 SDK 在 GitHub Actions 之外构建自定义的自动化工作流。

**说明**

**Claude Opus 4.6 已上线。** Claude Code GitHub Actions 默认使用 Sonnet。要使用 Opus 4.6，请将[模型参数](#breaking-changes-reference)配置为 `claude-opus-4-6`。

## 为什么用 Claude Code GitHub Actions？

* **即时创建 PR**：描述你的需求，Claude 创建包含所有必要改动的完整 PR
* **自动化代码实现**：一条命令就能把 issue 变成可运行的代码
* **遵循你的规范**：Claude 尊重你的 `CLAUDE.md` 规则和现有代码模式
* **设置简单**：用安装器和 API 密钥，几分钟就能上手
* **默认安全**：你的代码留在 GitHub 的 runner 上

## Claude 能做什么？

Claude Code 提供了强大的 GitHub Actions，可以改变你的开发方式：

### Claude Code Action

这个 GitHub Action 让你在 GitHub Actions 工作流中运行 Claude Code。你可以基于它构建任何自定义工作流。

[查看仓库 →](https://github.com/anthropics/claude-code-action)

## 设置

## 快速设置

最简单的方式是在终端中通过 Claude Code 来设置。打开 Claude 并运行 `/install-github-app`。

这个命令会引导你完成 GitHub App 安装和所需 secret 的配置。

**注意**

* 你必须是仓库管理员才能安装 GitHub App 和添加 secret
* GitHub App 需要 contents、issues 和 pull requests 的读写权限
* 此快速设置方式仅适用于直接使用 Claude API 的用户。如果你使用 AWS Bedrock 或 Google Vertex AI，请参阅[与 AWS Bedrock 和 Google Vertex AI 一起使用](#using-with-aws-bedrock-%26-google-vertex-ai)部分。

## 手动设置

如果 `/install-github-app` 命令失败或你更喜欢手动配置，按以下步骤操作：

1. **安装 Claude GitHub App** 到你的仓库：[https://github.com/apps/claude](https://github.com/apps/claude)

   Claude GitHub App 需要以下仓库权限：

   * **Contents**：读写（修改仓库文件）
   * **Issues**：读写（回复 issue）
   * **Pull requests**：读写（创建 PR 和推送变更）

   更多安全和权限详情，参见[安全文档](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)。
2. **添加 ANTHROPIC\_API\_KEY** 到你的仓库 secret（[了解如何在 GitHub Actions 中使用 secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)）
3. **复制工作流文件** [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) 到仓库的 `.github/workflows/` 目录

**提示**

完成设置后，在 issue 或 PR 评论中 @claude 来测试。

## 从 Beta 版升级

**警告**

Claude Code GitHub Actions v1.0 引入了破坏性变更，从 Beta 版升级到 v1.0 需要更新工作流文件。

如果你当前使用的是 Beta 版，建议更新工作流到 GA 版本。新版本简化了配置，同时增加了自动模式检测等新功能。

### 主要变更

所有 Beta 用户升级时需要对工作流文件做以下改动：

1. **更新 action 版本**：`@beta` 改为 `@v1`
2. **移除模式配置**：删除 `mode: "tag"` 或 `mode: "agent"`（现在自动检测）
3. **更新 prompt 输入**：`direct_prompt` 改为 `prompt`
4. **迁移 CLI 选项**：`max_turns`、`model`、`custom_instructions` 等统一放到 `claude_args` 中

### 破坏性变更对照表

| 旧 Beta 版输入 | 新 v1.0 输入 |
| -------------------- | -------------------------------------------------- |
| `mode` | *（已移除 - 自动检测）* |
| `direct_prompt` | `prompt` |
| `override_prompt` | `prompt` 配合 GitHub 变量 |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns` | `claude_args: --max-turns` |
| `model` | `claude_args: --model` |
| `allowed_tools` | `claude_args: --allowedTools` |
| `disallowed_tools` | `claude_args: --disallowedTools` |
| `claude_env` | `settings` JSON 格式 |

### 升级前后对比

**Beta 版：**

```yaml
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Follow our coding standards"
    max_turns: "10"
    model: "claude-sonnet-4-6"
```

**正式版（v1.0）：**

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --append-system-prompt "Follow our coding standards"
      --max-turns 10
      --model claude-sonnet-4-6
```

**提示**

现在 action 会根据你的配置自动检测是运行交互模式（响应 `@claude` 提及）还是自动化模式（直接运行 prompt）。

## 示例用法

Claude Code GitHub Actions 可以帮你完成各种任务。[示例目录](https://github.com/anthropics/claude-code-action/tree/main/examples)包含了适用于不同场景的现成工作流。

### 基本工作流

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

### 使用 skill

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this pull request for code quality, correctness, and security. Analyze the diff, then post your findings as review comments."
          claude_args: "--max-turns 5"
```

### 带 prompt 的自定义自动化

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model opus"
```

### 常见用法

在 issue 或 PR 评论中：

```text
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude 会自动分析上下文并做出相应回复。

## 最佳实践

### CLAUDE.md 配置

在仓库根目录创建 `CLAUDE.md` 文件，定义代码风格指南、审查标准、项目规则和首选模式。这个文件指导 Claude 了解你的项目规范。

### 安全注意事项

**警告**

绝不要把 API 密钥直接提交到仓库。

全面的安全指南（包括权限、认证和最佳实践），请参阅 [Claude Code Action 安全文档](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)。

始终使用 GitHub Secrets 存放 API 密钥：

* 把 API 密钥添加为名为 `ANTHROPIC_API_KEY` 的仓库 secret
* 在工作流中引用它：`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* 将 action 权限限制到最小必要范围
* 合并前审查 Claude 的建议

始终使用 GitHub Secrets（如 `${{ secrets.ANTHROPIC_API_KEY }}`），不要在工作流文件中硬编码 API 密钥。

### 优化性能

使用 issue 模板提供上下文，保持 `CLAUDE.md` 简洁聚焦，为工作流配置合理的超时时间。

### CI 成本

使用 Claude Code GitHub Actions 时，注意相关成本：

**GitHub Actions 成本：**

* Claude Code 在 GitHub 托管的 runner 上运行，会消耗你的 GitHub Actions 分钟数
* 详细的定价和分钟限制，参见 [GitHub 计费文档](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)

**API 成本：**

* 每次 Claude 交互根据 prompt 和回复长度消耗 API token
* token 用量取决于任务复杂度和代码库大小
* 当前 token 费率参见 [Claude 定价页面](https://claude.com/platform/api)

**成本优化建议：**

* 用明确的 `@claude` 指令减少不必要的 API 调用
* 在 `claude_args` 中配置合理的 `--max-turns` 防止过度迭代
* 设置工作流级超时，避免任务失控
* 考虑用 GitHub 的并发控制限制并行运行数

## 配置示例

Claude Code Action v1 通过统一参数简化了配置：

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

主要特性：

* **统一 prompt 接口** - 所有指令都用 `prompt`
* **Skill 支持** - 直接在 prompt 中调用已安装的 [skill](./skills)
* **CLI 直通** - 通过 `claude_args` 传入任何 Claude Code CLI 参数
* **灵活的触发器** - 适用于任何 GitHub 事件

完整的工作流文件请访问[示例目录](https://github.com/anthropics/claude-code-action/tree/main/examples)。

**提示**

回复 issue 或 PR 评论时，Claude 自动响应 @claude 提及。对于其他事件，用 `prompt` 参数提供指令。

## 与 AWS Bedrock 和 Google Vertex AI 一起使用

在企业环境中，你可以将 Claude Code GitHub Actions 与自己的云基础设施配合使用。这样可以控制数据驻留和计费，同时保持相同的功能。

### 前置条件

在配置云提供商之前，你需要：

#### Google Cloud Vertex AI：

1. 启用了 Vertex AI 的 Google Cloud 项目
2. 为 GitHub Actions 配置好 Workload Identity Federation
3. 具有所需权限的服务账号
4. GitHub App（推荐）或使用默认的 GITHUB\_TOKEN

#### AWS Bedrock：

1. 启用了 Amazon Bedrock 的 AWS 账号
2. AWS 中配置好的 GitHub OIDC 身份提供商
3. 具有 Bedrock 权限的 IAM 角色
4. GitHub App（推荐）或使用默认的 GITHUB\_TOKEN

### 创建自定义 GitHub App（推荐第三方提供商使用）

使用 Vertex AI 或 Bedrock 等第三方提供商时，为了更好的控制和安全性，建议创建你自己的 GitHub App：

1. 前往 [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
2. 填写基本信息：
   * **GitHub App name**：选一个唯一名称（如 "YourOrg Claude Assistant"）
   * **Homepage URL**：你组织的网站或仓库 URL
3. 配置应用设置：
   * **Webhooks**：取消"Active"勾选（此集成不需要）
4. 设置所需权限：
   * **Repository permissions**：
     * Contents：Read and write
     * Issues：Read and write
     * Pull requests：Read and write
5. 点击"Create GitHub App"
6. 创建完成后，点击"Generate a private key"，保存下载的 `.pem` 文件
7. 在应用设置页面记下 App ID
8. 将应用安装到你的仓库：
   * 在应用设置页面，点击左侧边栏的"Install App"
   * 选择你的账号或组织
   * 选择"Only select repositories"并选择具体仓库
   * 点击"Install"
9. 把私钥添加为仓库 secret：
   * 前往仓库的 Settings → Secrets and variables → Actions
   * 用 `.pem` 文件内容创建名为 `APP_PRIVATE_KEY` 的 secret
10. 添加 App ID 为 secret：

* 用你的 GitHub App ID 创建名为 `APP_ID` 的 secret

**注意**

这个应用会配合 [actions/create-github-app-token](https://github.com/actions/create-github-app-token) action 在工作流中生成认证 token。

**如果你使用 Claude API 或不想自建 GitHub App**：使用官方 Anthropic 应用：

1. 从这里安装：[https://github.com/apps/claude](https://github.com/apps/claude)
2. 无需额外认证配置


### 配置云提供商认证

选择你的云提供商并设置安全认证：

### AWS Bedrock

**配置 AWS 让 GitHub Actions 无需存储凭证即可安全认证。**

> **安全提示**：使用仓库级配置，只授予最小必要权限。

**所需步骤：**

1. **启用 Amazon Bedrock**：
   * 在 Amazon Bedrock 中申请 Claude 模型的访问权限
   * 如果使用跨区域模型，在所有需要的区域申请访问权限

2. **设置 GitHub OIDC 身份提供商**：
   * Provider URL：`https://token.actions.githubusercontent.com`
   * Audience：`sts.amazonaws.com`

3. **为 GitHub Actions 创建 IAM 角色**：
   * 可信实体类型：Web identity
   * 身份提供商：`token.actions.githubusercontent.com`
   * 权限：`AmazonBedrockFullAccess` 策略
   * 为你的具体仓库配置信任策略

**所需的值：**

设置完成后你需要：

* **AWS\_ROLE\_TO\_ASSUME**：你创建的 IAM 角色的 ARN

**提示**

OIDC 比静态 AWS 访问密钥更安全，因为凭证是临时的且会自动轮换。

详细的 OIDC 设置说明参见 [AWS 文档](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)。

### Google Vertex AI

**配置 Google Cloud 让 GitHub Actions 无需存储凭证即可安全认证。**

> **安全提示**：使用仓库级配置，只授予最小必要权限。

**所需步骤：**

1. **在 Google Cloud 项目中启用 API**：
   * IAM Credentials API
   * Security Token Service (STS) API
   * Vertex AI API

2. **创建 Workload Identity Federation 资源**：
   * 创建 Workload Identity Pool
   * 添加 GitHub OIDC Provider：
     * Issuer：`https://token.actions.githubusercontent.com`
     * 配置仓库和 owner 的属性映射
     * **安全建议**：使用仓库级的属性条件

3. **创建服务账号**：
   * 只授予 `Vertex AI User` 角色
   * **安全建议**：为每个仓库创建专用服务账号

4. **配置 IAM 绑定**：
   * 允许 Workload Identity Pool 模拟服务账号
   * **安全建议**：使用仓库级的 principal set

**所需的值：**

设置完成后你需要：

* **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**：完整的 provider 资源名称
* **GCP\_SERVICE\_ACCOUNT**：服务账号邮箱

**提示**

Workload Identity Federation 不需要下载服务账号密钥，安全性更高。

详细设置说明参见 [Google Cloud Workload Identity Federation 文档](https://cloud.google.com/iam/docs/workload-identity-federation)。


### 添加所需的 secret

将以下 secret 添加到你的仓库（Settings → Secrets and variables → Actions）：

#### Claude API（直连）：

1. **API 认证**：
   * `ANTHROPIC_API_KEY`：来自 [console.anthropic.com](https://console.anthropic.com) 的 Claude API 密钥

2. **GitHub App（如果用自建的）**：
   * `APP_ID`：你的 GitHub App ID
   * `APP_PRIVATE_KEY`：私钥（.pem）内容

#### Google Cloud Vertex AI

1. **GCP 认证**：
   * `GCP_WORKLOAD_IDENTITY_PROVIDER`
   * `GCP_SERVICE_ACCOUNT`

2. **GitHub App（如果用自建的）**：
   * `APP_ID`：你的 GitHub App ID
   * `APP_PRIVATE_KEY`：私钥（.pem）内容

#### AWS Bedrock

1. **AWS 认证**：
   * `AWS_ROLE_TO_ASSUME`

2. **GitHub App（如果用自建的）**：
   * `APP_ID`：你的 GitHub App ID
   * `APP_PRIVATE_KEY`：私钥（.pem）内容


### 创建工作流文件

创建与云提供商集成的 GitHub Actions 工作流文件。以下示例展示了 AWS Bedrock 和 Google Vertex AI 的完整配置：

### AWS Bedrock 工作流

**前置条件：**

* 已启用 AWS Bedrock 并有 Claude 模型访问权限
* 已在 AWS 中配置 GitHub 为 OIDC 身份提供商
* 已创建信任 GitHub Actions 的、具有 Bedrock 权限的 IAM 角色

**所需的 GitHub secret：**

| Secret 名称 | 说明 |
| -------------------- | ------------------------------------------------- |
| `AWS_ROLE_TO_ASSUME` | 用于 Bedrock 访问的 IAM 角色 ARN |
| `APP_ID` | 你的 GitHub App ID（来自应用设置） |
| `APP_PRIVATE_KEY` | 你为 GitHub App 生成的私钥 |

```yaml
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    env:
      AWS_REGION: us-west-2
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-west-2

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_bedrock: "true"
          claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'
```

**提示**

Bedrock 的模型 ID 格式包含区域前缀（如 `us.anthropic.claude-sonnet-4-6`）。

### Google Vertex AI 工作流

**前置条件：**

* 在 GCP 项目中启用了 Vertex AI API
* 已为 GitHub 配置 Workload Identity Federation
* 有具备 Vertex AI 权限的服务账号

**所需的 GitHub secret：**

| Secret 名称 | 说明 |
| -------------------------------- | ------------------------------------------------- |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider 资源名称 |
| `GCP_SERVICE_ACCOUNT` | 具有 Vertex AI 访问权限的服务账号邮箱 |
| `APP_ID` | 你的 GitHub App ID（来自应用设置） |
| `APP_PRIVATE_KEY` | 你为 GitHub App 生成的私钥 |

```yaml
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          use_vertex: "true"
          claude_args: '--model claude-sonnet-4@20250514 --max-turns 10'
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
```

**提示**

Project ID 会从 Google Cloud 认证步骤中自动获取，无需硬编码。

## 故障排查

### Claude 不响应 @claude 命令

确认 GitHub App 已正确安装，工作流已启用，API 密钥已设置在仓库 secret 中，并且评论用的是 `@claude`（不是 `/claude`）。

### CI 不在 Claude 的提交上运行

确保你使用的是 GitHub App 或自定义应用（不是 action 用户），检查工作流触发器包含必要的事件，验证应用权限包含 CI 触发所需的权限。

### 认证错误

确认 API 密钥有效且权限足够。对于 Bedrock/Vertex，检查凭证配置并确保 secret 名称在工作流中正确。

## 高级配置

### Action 参数

Claude Code Action v1 使用简化的配置：

| 参数 | 说明 | 必填 |
| ------------------- | ------------------------------------------------------------------ | -------- |
| `prompt` | Claude 指令（纯文本或 [skill](./skills) 名称） | 否* |
| `claude_args` | 传给 Claude Code 的 CLI 参数 | 否 |
| `anthropic_api_key` | Claude API 密钥 | 是** |
| `github_token` | 用于 API 访问的 GitHub token | 否 |
| `trigger_phrase` | 自定义触发短语（默认："@claude"） | 否 |
| `use_bedrock` | 使用 AWS Bedrock 替代 Claude API | 否 |
| `use_vertex` | 使用 Google Vertex AI 替代 Claude API | 否 |

\*prompt 可选——省略时，Claude 响应 issue/PR 评论中的触发短语\
\*\*直接使用 Claude API 时必填，Bedrock/Vertex 不需要

#### 传递 CLI 参数

`claude_args` 接受任何 Claude Code CLI 参数：

```yaml
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

常用参数：

* `--max-turns`：最大对话轮数（默认：10）
* `--model`：使用的模型（如 `claude-sonnet-4-6`）
* `--mcp-config`：MCP 配置文件路径
* `--allowed-tools`：逗号分隔的允许工具列表
* `--debug`：启用调试输出

### 其他集成方式

虽然 `/install-github-app` 是推荐方式，你还可以：

* **自定义 GitHub App**：适合需要品牌用户名或自定义认证流程的组织。用所需权限（contents、issues、pull requests）创建自己的 GitHub App，在工作流中用 actions/create-github-app-token 生成 token。
* **手动 GitHub Actions**：直接配置工作流，最大灵活性
* **MCP 配置**：动态加载 Model Context Protocol 服务器

认证、安全和高级配置的详细指南，参见 [Claude Code Action 文档](https://github.com/anthropics/claude-code-action/blob/main/docs)。

### 自定义 Claude 的行为

有两种方式配置 Claude 的行为：

1. **CLAUDE.md**：在仓库根目录的 `CLAUDE.md` 文件中定义编码标准、审查标准和项目规则。Claude 在创建 PR 和回复请求时会遵循这些规则。详见[记忆文档](./memory)。
2. **自定义 prompt**：用工作流文件中的 `prompt` 参数提供特定于工作流的指令。可以针对不同工作流或任务定制 Claude 的行为。

Claude 在创建 PR 和回复请求时会遵循这些规则。
