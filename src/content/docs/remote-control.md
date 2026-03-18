---
title: "使用 Remote Control 从任何设备继续本地会话"
order: 14
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "使用 Remote Control 从您的手机、平板电脑或任何浏览器继续本地 Claude Code 会话。可与 claude.ai/code 和 Claude 移动应用程序配合使用。"
sourceUrl: "https://code.claude.com/docs/en/remote-control.md"
sourceTitle: "Continue local sessions from any device with Remote Control"
tags: []
---
# 使用 Remote Control 从任何设备继续本地会话

> 使用 Remote Control 从您的手机、平板电脑或任何浏览器继续本地 Claude Code 会话。可与 claude.ai/code 和 Claude 移动应用程序配合使用。

**注意**

Remote Control 适用于所有计划。团队和企业管理员必须首先在 [管理设置](https://claude.ai/admin-settings/claude-code) 中启用 Claude Code。

Remote Control 将 [claude.ai/code](https://claude.ai/code) 或适用于 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 和 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的 Claude 应用程序连接到在您的计算机上运行的 Claude Code 会话。在办公桌上开始一项任务，然后从沙发上的手机或另一台计算机上的浏览器中拿起它。

当您在计算机上启动 Remote Control 会话时，Claude 始终在本地运行，因此不会将任何内容移动到云端。使用 Remote Control，您可以：

* **远程使用完整的本地环境**：您的文件系统、[MCP 服务器](./mcp)、工具和项目配置均保持可用
* **同时在两个表面上工作**：对话在所有连接的设备上保持同步，因此您可以从终端、浏览器和手机互换发送消息
* **避免中断**：如果您的笔记本电脑处于睡眠状态或网络中断，会话会在您的计算机恢复在线时自动重新连接

与在云基础设施上运行的[网络上的 Claude Code](./claude-code-on-the-web) 不同，Remote Control 会话直接在您的计算机上运行并与本地文件系统交互。 Web 和移动界面只是本地会话的一个窗口。

**注意**

Remote Control 需要 Claude Code v2.1.51 或更高版本。使用 `claude --version` 检查您的版本。

本页面介绍设置、如何启动和连接到会话，以及 Remote Control 与网络上的 Claude Code 的比较。

## 要求

在使用 Remote Control 之前，请确认您的环境满足以下条件：

* **订阅**：适用于 Pro、Max、Team 和 Enterprise 计划。团队和企业管理员必须首先在 [管理设置](https://claude.ai/admin-settings/claude-code) 中启用 Claude Code。不支持 API 密钥。
* **身份验证**：运行 `claude` 并使用 `/login` 通过 claude.ai 登录（如果您尚未登录）。
* **工作空间信任**：在项目目录中运行 `claude` 至少一次以接受工作空间信任对话框。

## 启动 Remote Control 会话

您可以启动专用 Remote Control 服务器、在启用 Remote Control 的情况下启动交互式会话，或者连接已在运行的会话。

### 服务器模式

    导航到您的项目目录并运行：

    ```bash 
    claude remote-control
    ```

    该进程在您的终端中以服务器模式保持运行，等待远程连接。它会显示可用于[从其他设备连接](#connect-from-another-device) 的会话 URL，并且您可以按空格键显示二维码以便从手机快速访问。当远程会话处于活动状态时，终端会显示连接状态和工具活动。

    可用标志：|旗帜|描述 |
    | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | `--name "My Project"` |设置在 claude.ai/code 的会话列表中可见的自定义会话标题。                                                                                                                                                                                                                                                                                                        |
    | `--spawn <mode>` |如何创建并发会话。在运行时按 `w` 进行切换。
• `same-dir`（默认）：所有会话共享当前工作目录，因此如果编辑相同的文件，它们可能会发生冲突。
• `worktree`：每个按需会话都有自己的[git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)。需要 git 存储库。 |
    | `--capacity <N>` |最大并发会话数。默认值为 32。
    | `--verbose` |显示详细的连接和会话日志。                                                                                                                                                                                                                                                                                                                                       |
    | `--sandbox` / `--no-sandbox` |启用或禁用[沙盒](./sandboxing) 以进行文件系统和网络隔离。默认关闭。                                                                                                                                                                                                                                                                             |

  
### 互动环节

要在启用 Remote Control 的情况下启动正常的交互式 Claude Code 会话，请使用 `--remote-control` 标志（或 `--rc`）：

```bash
claude --remote-control
```

可以选择传递会话名称：

```bash
claude --remote-control "My Project"
```这为您在终端中提供了完整的交互式会话，您也可以通过 claude.ai 或 Claude 应用程序进行控制。与 `claude remote-control`（服务器模式）不同，您可以在本地键入消息，同时也可以远程进行会话。

  
### 来自现有会话

如果您已处于 Claude Code 会话中并希望远程继续该会话，请使用 `/remote-control`（或 `/rc`）命令：

```text
/remote-control
```

传递名称作为参数来设置自定义会话标题：

```text
/remote-control My Project
```

这将启动 Remote Control 会话，该会话会继承您当前的对话历史记录，并显示可用于[从其他设备连接](#connect-from-another-device) 的会话 URL 和 QR 代码。 `--verbose`、`--sandbox` 和 `--no-sandbox` 标志不适用于此命令。

### 从另一台设备连接

一旦 Remote Control 会话处于活动状态，您可以通过多种方式从其他设备进行连接：

* **在任何浏览器中打开会话 URL**，直接转到 [claude.ai/code](https://claude.ai/code) 上的会话。 `claude remote-control` 和 `/remote-control` 都会在终端中显示此 URL。
* **扫描会话 URL 旁边显示的二维码**，直接在 Claude 应用程序中打开它。对于 `claude remote-control`，按空格键可切换 QR 码显示。
* **打开 [claude.ai/code](https://claude.ai/code) 或 Claude 应用程序**，然后在会话列表中按名称查找会话。 Remote Control 会话在线时显示带有绿色状态点的计算机图标。

远程会话的名称取自 `--name` 参数（或传递给 `/remote-control` 的名称）、您的最后一条消息、`/rename` 值或“Remote Control 会话”（如果没有对话历史记录）。如果环境已有一个活动会话，系统会询问您是否继续该会话还是开始一个新会话。

如果您还没有 Claude 应用程序，请使用 Claude Code 内的 `/mobile` 命令显示 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 或 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的下载二维码。

### 为所有会话启用 Remote Control

默认情况下，仅当您显式运行 `claude remote-control`、`claude --remote-control` 或 `/remote-control` 时，Remote Control 才会激活。要为每个交互式会话自动启用它，请在 Claude Code 内运行 `/config`，并将 **为所有会话启用 Remote Control** 设置为 `true`。将其设置回 `false` 以禁用。

启用此设置后，每个交互式 Claude Code 进程都会注册一个远程会话。如果您运行多个实例，每个实例都会获得自己的环境和会话。要从单个进程运行多个并发会话，请改用带有 `--spawn` 的服务器模式。

## 连接和安全

您的本地 Claude Code 会话仅发出出站 HTTPS 请求，并且从不打开计算机上的入站端口。当您启动 Remote Control 时，它会向 Anthropic API 注册并轮询工作。当您从其他设备连接时，服务器会通过流连接在 Web 或移动客户端与本地会话之间路由消息。

所有流量都通过 TLS 上的 Anthropic API 传输，其传输安全性与任何 Claude Code 会话相同。该连接使用多个短期凭据，每个凭据都有一个目的并独立过期。

## 网络上的 Remote Control 与 Claude CodeRemote Control 和 [网络上的 Claude Code](./claude-code-on-the-web) 都使用 claude.ai/code 接口。主要区别在于会话运行的位置：Remote Control 在您的计算机上执行，因此您的本地 MCP 服务器、工具和项目配置保持可用。 Web 上的 Claude Code 在 Anthropic 托管的云基础设施中执行。

当您正在本地工作并希望通过另一台设备继续工作时，请使用 Remote Control。当您想要在没有任何本地设置的情况下启动任务、处理未克隆的存储库或并行运行多个任务时，请在 Web 上使用 Claude Code。

## 限制

* **每个交互进程一个远程会话**：在服务器模式之外，每个 Claude Code 实例一次支持一个远程会话。将服务器模式与 `--spawn` 结合使用，从单个进程运行多个并发会话。
* **终端必须保持打开状态**：Remote Control 作为本地进程运行。如果关闭终端或停止 `claude` 进程，会话就会结束。再次运行 `claude remote-control` 以开始新的操作。
* **长时间网络中断**：如果您的计算机处于唤醒状态，但无法连接到网络的时间超过大约 10 分钟，则会话超时并且进程退出。再次运行 `claude remote-control` 以启动新会话。

## 故障排除

如果您的终端显示 `Remote credentials fetch failed — see debug log`，则 Claude Code 无法从 Anthropic API 获取短期凭证来建立 Remote Control 连接。要查看完整的错误详细信息，请使用 `--verbose` 标志重新运行：

```bash
claude remote-control --verbose
```

常见原因：

* 未登录：运行 `claude` 并使用 `/login` 对您的 claude.ai 帐户进行身份验证。 Remote Control 不支持 API 密钥身份验证。
* 网络或代理问题：防火墙或代理可能会阻止出站 HTTPS 请求。 Remote Control 需要访问端口 443 上的 Anthropic API。
* 会话创建失败：如果您还看到 `Session creation failed — see debug log`，则失败发生在安装的早期阶段。检查您的订阅（Pro、Max、Team 或 Enterprise）是否处于活动状态。

## 相关资源

* [网络上的 Claude Code](./claude-code-on-the-web)：在 Anthropic 托管的云环境中而不是在您的计算机上运行会话
* [身份验证](./authentication)：设置 `/login` 并管理 claude.ai 的凭据
* [CLI 参考](./cli-reference)：标志和命令的完整列表，包括 `claude remote-control`
* [安全](./security)：Remote Control 会话如何适应 Claude Code 安全模型
* [数据使用](./data-usage)：本地和远程会话期间哪些数据流经 Anthropic API
