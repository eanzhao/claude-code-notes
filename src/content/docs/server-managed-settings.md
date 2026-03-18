---
title: "配置服务器管理的设置（公开测试版）"
order: 41
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "通过服务器提供的设置为您的组织集中配置 Claude Code，无需设备管理基础设施。"
sourceUrl: "https://code.claude.com/docs/en/server-managed-settings.md"
sourceTitle: "Configure server-managed settings (public beta)"
tags: []
---
# 配置服务器管理设置（公开测试版）

> 通过服务器提供的设置为您的组织集中配置 Claude Code，无需设备管理基础设施。

服务器管理设置允许管理员通过 Claude.ai 上基于 Web 的界面集中配置 Claude Code。当用户使用其组织凭据进行身份验证时，Claude Code 客户端会自动接收这些设置。

此方法专为没有设备管理基础设施或需要管理非托管设备上的用户设置的组织而设计。

**注意**

服务器管理的设置处于公开测试阶段，可供 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=server_settings_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=server_settings_enterprise) 客户使用。功能可能会在正式发布之前发生变化。

## 要求

要使用服务器管理的设置，您需要：

* Claude（适用于团队）或 Claude（适用于企业计划）
* Claude Code version 2.1.38 or later for Claude for Teams, or version 2.1.30 or later for Claude for Enterprise
* 网络访问`api.anthropic.com`

## 在服务器管理和端点管理设置之间进行选择

Claude Code 支持两种集中配置方法。服务器管理的设置从 Anthropic 的服务器提供配置。 [端点管理的设置](./settings#settings-files) 通过本机操作系统策略（macOS 托管首选项、Windows 注册表）或托管设置文件直接部署到设备。

|方法|最适合 |安全模型|
| ：------------------------------------------------------------------------ | :-------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| **服务器管理的设置** |没有 MDM 的组织或非托管设备上的用户 |身份验证时从 Anthropic 服务器传送的设置 |
| **[端点管理的设置](./settings#settings-files)** |拥有 MDM 或端点管理的组织 |通过 MDM 配置文件、注册表策略或托管设置文件部署到设备的设置 |

如果您的设备已注册 MDM 或端点管理解决方案，则端点管理的设置可提供更强的安全保证，因为可以保护设置文件免遭操作系统级别的用户修改。

## 配置服务器管理的设置

### 打开管理控制台

在 [Claude.ai](https://claude.ai) 中，导航至 **管理设置 > Claude Code > 托管设置**。

  
### 定义您的设置

将您的配置添加为 JSON。支持所有[`settings.json` 中可用的设置](./settings#available-settings)，包括[仅限托管设置](./permissions#managed-only-settings)，例如 `disableBypassPermissionsMode`。

此示例强制执行权限拒绝列表并防止用户绕过权限：

```json
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "disableBypassPermissionsMode": "disable"
  }
}
```

  
### 保存并部署保存您的更改。 Claude Code 客户端会在下次启动或每小时轮询周期收到更新的设置。

### 验证设置交付

要确认设置已应用，请要求用户重新启动 Claude Code。如果配置包含触发[安全审批对话框](#security-approval-dialogs) 的设置，则用户在启动时会看到一条描述托管设置的提示。您还可以通过让用户运行 `/permissions` 查看其有效的权限规则来验证托管权限规则是否处于活动状态。

### 访问控制

以下角色可以管理服务器管理的设置：

* **主要业主**
* **业主**

限制对受信任人员的访问，因为设置更改适用于组织中的所有用户。

### 当前限制

服务器管理的设置在测试期间具有以下限制：

* 设置统一应用于组织中的所有用户。尚不支持按组配置。
* [MCP 服务器配置](./mcp#managed-mcp-configuration) 无法通过服务器管理的设置进行分发。

## 设置传递

### 设置优先级

服务器管理的设置和[端点管理的设置](./settings#settings-files) 均占据 Claude Code [设置层次结构](./settings#settings-precedence) 中的最高层。没有其他设置级别可以覆盖它们，包括命令行参数。当两者都存在时，服务器管理的设置优先，并且不使用端点管理的设置。

### 获取和缓存行为

Claude Code 在启动时从 Anthropic 的服务器获取设置，并在活动会话期间每小时轮询更新。

**首次启动时没有缓存设置：**

* Claude Code 异步获取设置
* 如果获取失败，Claude Code 将继续，无需托管设置
* 在设置加载之前有一个短暂的窗口，其中尚未强制执行限制

**使用缓存设置进行后续启动：**

* 缓存设置在启动时立即应用
* Claude Code 在后台获取新设置
* 缓存的设置在网络故障时仍然存在

Claude Code 无需重新启动即可自动应用设置更新，但 OpenTelemetry 配置等高级设置除外，这些设置需要完全重新启动才能生效。

### 安全批准对话框

某些可能带来安全风险的设置需要用户明确批准才能应用：

* **Shell命令设置**：执行shell命令的设置
* **自定义环境变量**：不在已知安全白名单中的变量
* **钩子配置**：任何钩子定义

当这些设置存在时，用户会看到一个安全对话框，解释正在配置的内容。用户必须批准才能继续。如果用户拒绝设置，Claude Code 将退出。

**注意**

在带有 `-p` 标志的非交互模式下，Claude Code 会跳过安全对话框并在未经用户批准的情况下应用设置。

## 平台可用性

服务器管理的设置需要直接连接到 `api.anthropic.com`，并且在使用第三方模型提供程序时不可用：

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* 通过 `ANTHROPIC_BASE_URL` 或 [LLM 网关](./llm-gateway) 的自定义 API 端点

## 审计日志记录设置更改的审核日志事件可通过合规性 API 或审核日志导出获得。请联系您的 Anthropic 客户团队以获取访问权限。

审核事件包括执行的操作类型、执行操作的帐户和设备以及对先前值和新值的引用。

## 安全考虑

服务器管理的设置提供集中策略实施，但它们作为客户端控制运行。在非托管设备上，具有 admin 或 sudo 访问权限的用户可以修改 Claude Code 二进制文件、文件系统或网络配置。

|场景 |行为 |
| :------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------- |
|用户编辑缓存的设置文件 |被篡改的文件在启动时应用，但正确的设置会在下一次服务器获取时恢复 |
|用户删除缓存的设置文件 |发生首次启动行为：通过短暂的非强制窗口异步获取设置 |
| API 不可用 |如果可用，则应用缓存设置，否则在下一次成功提取之前不会强制执行托管设置 |
|用户通过不同的组织进行身份验证 |不会为托管组织之外的帐户提供设置 |
|用户设置非默认 `ANTHROPIC_BASE_URL` |使用第三方 API 提供商时会绕过服务器管理的设置 |

要检测运行时配置更改，请使用 [`ConfigChange` 挂钩](./hooks#configchange) 记录修改或在未经授权的更改生效之前阻止它们。

为了获得更强的执行保证，请在注册 MDM 解决方案的设备上使用[端点管理的设置](./settings#settings-files)。

## 另请参阅

管理 Claude Code 配置的相关页面：

* [设置](./settings)：完整的配置参考，包括所有可用设置
* [端点托管设置](./settings#settings-files)：IT 部署到设备的托管设置
* [验证](./authentication): 设置用户访问 Claude Code
* [安全](./security)：安全保障措施和最佳实践
