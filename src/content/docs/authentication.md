---
title: "验证"
order: 39
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "登录 Claude Code 并配置个人、团队和组织的身份验证。"
sourceUrl: "https://code.claude.com/docs/en/authentication.md"
sourceTitle: "Authentication"
tags: []
---
# 认证

> 登录 Claude Code，配置个人、团队和组织的认证方式。

Claude Code 支持多种认证方式。个人用户可以用 Claude.ai 账户登录；团队可以使用 Claude for Teams/Enterprise、Claude Console，或 Amazon Bedrock、Google Vertex AI、Microsoft Foundry 等云服务商。

## 登录 Claude Code

[安装 Claude Code](./setup#install-claude-code) 后，在终端运行 `claude`。首次启动时会自动打开浏览器窗口供你登录。

如果浏览器没有自动打开，按 `c` 将登录 URL 复制到剪贴板，然后粘贴到浏览器中。

你可以用以下任意账户类型登录：

* **Claude Pro 或 Max 订阅**：用你的 Claude.ai 账户登录。在 [claude.com/pricing](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_pro_max) 订阅。
* **Claude for Teams 或 Enterprise**：用团队管理员邀请你的 Claude.ai 账户登录。
* **Claude Console**：用你的 Console 凭据登录。管理员需要先[邀请你](#claude-console-authentication)。
* **云服务商**：如果你的组织使用 [Amazon Bedrock](./amazon-bedrock)、[Google Vertex AI](./google-vertex-ai) 或 [Microsoft Foundry](./microsoft-foundry)，在运行 `claude` 前设置好环境变量即可，无需浏览器登录。

要登出并重新认证，在 Claude Code 提示符中输入 `/logout`。

如果登录遇到问题，请参阅[认证问题排查](./troubleshooting#authentication-issues)。

## 团队认证设置

团队和组织可以选择以下方式配置 Claude Code 访问权限：

* [Claude for Teams 或 Enterprise](#claude-for-teams-or-enterprise)，推荐大多数团队使用
* [Claude Console](#claude-console-authentication)
* [Amazon Bedrock](./amazon-bedrock)
* [Google Vertex AI](./google-vertex-ai)
* [Microsoft Foundry](./microsoft-foundry)

### Claude for Teams 或 Enterprise

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=authentication_enterprise) 为使用 Claude Code 的组织提供最佳体验，团队成员可以通过统一计费和团队管理在 Web 端和 Claude Code 之间无缝切换。

* **Claude for Teams**：自助服务方案，提供协作功能、管理工具和统一计费。适合小型团队。
* **Claude for Enterprise**：在此基础上增加 SSO、域名捕获、基于角色的权限、合规 API 和托管策略配置。适合有安全合规要求的大型组织。

### 订阅

订阅 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_teams_step#team-&-enterprise) 或联系销售获取 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=authentication_enterprise_step)。


### 邀请团队成员

在管理面板中邀请团队成员。


### 安装并登录

团队成员安装 Claude Code 后用各自的 Claude.ai 账户登录即可。

### Claude Console 认证

如果组织倾向于按 API 用量计费，可以通过 Claude Console 配置访问权限。

### 创建或使用 Console 账户

使用已有的 Claude Console 账户或创建新账户。


### 添加用户

可以通过以下方式添加用户：
* 在 Console 中批量邀请用户：设置 -> 成员 -> 邀请
* [配置 SSO 单点登录](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)


### 分配角色

邀请用户时，分配以下角色之一：

* **Claude Code** 角色：用户只能创建 Claude Code API 密钥
* **Developer** 角色：用户可以创建任何类型的 API 密钥


### 用户完成设置

每位受邀用户需要：

* 接受 Console 邀请
* [检查系统要求](./setup#system-requirements)
* [安装 Claude Code](./setup#install-claude-code)
* 用 Console 账户凭据登录

### 云服务商认证

如果团队使用 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry：

### 按照对应文档配置

参阅 [Bedrock 文档](./amazon-bedrock)、[Vertex 文档](./google-vertex-ai) 或 [Microsoft Foundry 文档](./microsoft-foundry)。


### 分发配置

将环境变量和云凭据生成说明分发给用户。了解更多关于[配置管理](./settings)的信息。


### 安装 Claude Code

用户按照[安装指南](./setup#install-claude-code)安装即可。

## 凭据管理

Claude Code 会安全管理你的认证凭据：

* **存储位置**：macOS 上凭据存储在加密的 macOS 钥匙串中；Linux 和 Windows 上存储在 `~/.claude/.credentials.json`（或 `$CLAUDE_CONFIG_DIR` 指定的目录下）。Linux 上文件权限为 `0600`；Windows 上继承用户配置文件目录的访问控制。
* **支持的认证类型**：Claude.ai 凭据、Claude API 凭据、Azure Auth、Bedrock Auth 和 Vertex Auth。
* **自定义凭据脚本**：[`apiKeyHelper`](./settings#available-settings) 可以配置为一个返回 API 密钥的 shell 脚本。
* **刷新间隔**：默认情况下，`apiKeyHelper` 在 5 分钟后或收到 HTTP 401 响应时重新调用。设置 `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` 环境变量可自定义刷新间隔。
* **慢脚本提醒**：如果 `apiKeyHelper` 超过 10 秒才返回密钥，Claude Code 会在提示栏显示警告。如果频繁看到此提醒，请检查凭据脚本是否可以优化。

`apiKeyHelper`、`ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 仅在终端 CLI 会话中生效。Claude Desktop 和远程会话专门使用 OAuth，不会调用 `apiKeyHelper` 或读取 API 密钥环境变量。

### 认证优先级

当存在多个凭据时，Claude Code 按以下顺序选择：

1. **云服务商凭据**（设置了 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_VERTEX` 或 `CLAUDE_CODE_USE_FOUNDRY` 时）。详见[第三方集成](./third-party-integrations)。
2. **`ANTHROPIC_AUTH_TOKEN` 环境变量**。作为 `Authorization: Bearer` 头发送。通过 [LLM 网关或代理](./llm-gateway)路由时使用此方式，网关使用 Bearer token 而非 Anthropic API 密钥认证。
3. **`ANTHROPIC_API_KEY` 环境变量**。作为 `X-Api-Key` 头发送。配合 [Claude Console](https://platform.claude.com) 的密钥直接访问 Anthropic API。交互模式下会提示你批准或拒绝该密钥，选择会被记住；如需更改，到 `/config` 中切换"使用自定义 API 密钥"开关。非交互模式（`-p`）下，只要密钥存在就直接使用。
4. **[`apiKeyHelper`](./settings#available-settings) 脚本输出**。适用于动态或轮换凭据，比如从密钥管理服务获取的短期 token。
5. **通过 `/login` 获得的订阅 OAuth 凭据**。这是 Claude Pro、Max、Team 和 Enterprise 用户的默认方式。

如果你有有效的 Claude 订阅，但环境中也设置了 `ANTHROPIC_API_KEY`，那么 API 密钥经批准后会优先使用。如果该密钥所属的组织已禁用或过期，可能会导致认证失败。运行 `unset ANTHROPIC_API_KEY` 可回退到订阅认证，用 `/status` 确认当前使用的认证方式。

[Web 版 Claude Code](./claude-code-on-the-web) 始终使用你的订阅凭据。沙箱环境中的 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 不会覆盖它。
