---
title: "Claude Code 于 Slack"
order: 19
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "直接从 Slack 工作区委派编码任务"
sourceUrl: "https://code.claude.com/docs/en/slack.md"
sourceTitle: "Claude Code in Slack"
tags: []
---
# Slack 中的 Claude Code

> 直接在 Slack 工作区中委派编码任务

Slack 中的 Claude Code 把 Claude Code 的能力直接带到你的 Slack 工作区。在编码相关的对话中 @Claude，Claude 会自动识别意图，在 Web 端创建 Claude Code session，让你无需离开团队对话就能委派开发工作。

这个集成基于已有的 Claude Slack 应用，增加了向 Web 端 Claude Code 智能路由的能力，专门处理编码相关的请求。

## 适用场景

* **Bug 排查和修复**：Slack 频道里一报告 bug，就可以直接让 Claude 去排查和修复。
* **快速代码审查和修改**：让 Claude 根据团队反馈实现小功能或重构代码。
* **协作调试**：团队讨论中提供的关键上下文（如错误复现步骤、用户反馈等），Claude 可以直接利用来辅助调试。
* **并行任务执行**：在 Slack 中发起编码任务后继续做其他事，完成后会收到通知。

## 前置条件

在 Slack 中使用 Claude Code 前，确保满足以下条件：

| 条件 | 说明 |
| :-------------------- | :---------------------------------------------------------------------------------------- |
| Claude 订阅 | Pro、Max、Teams 或 Enterprise，且有 Claude Code 权限（高级席位） |
| Web 端 Claude Code | 必须开启 [Web 端 Claude Code](./claude-code-on-the-web) 的访问权限 |
| GitHub 账号 | 已连接到 Web 端 Claude Code，且至少授权了一个仓库 |
| Slack 认证 | Slack 账号已通过 Claude 应用关联到你的 Claude 账号 |

## 设置 Slack 中的 Claude Code

### 安装 Claude Slack 应用

工作区管理员需要从 Slack 应用市场安装 Claude 应用。前往 [Slack 应用市场](https://slack.com/marketplace/A08SF47R6P4)，点击"Add to Slack"开始安装。


### 关联你的 Claude 账号

应用安装完成后，验证你的 Claude 账号：

1. 在 Slack 的"Apps"区域点击"Claude"，打开 Claude 应用
2. 切换到 App Home 标签页
3. 点击"Connect"将你的 Slack 账号与 Claude 账号关联
4. 在浏览器中完成认证流程


### 配置 Web 端 Claude Code

确保 Web 端 Claude Code 已正确配置：

* 访问 [claude.ai/code](https://claude.ai/code)，用与 Slack 关联的同一账号登录
* 如果还没有连接 GitHub 账号，先完成连接
* 确认至少授权了一个你希望 Claude 使用的仓库


### 选择路由模式

账号关联后，配置 Claude 如何处理 Slack 中的消息。在 Slack 的 Claude App Home 页面找到 **路由模式** 设置。

| 模式 | 行为 |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **仅代码** | Claude 把所有 @提及都路由到 Claude Code session。适合在 Slack 中只用 Claude 做开发任务的团队。 |
| **代码 + 聊天** | Claude 分析每条消息，智能路由到 Claude Code（编码任务）或 Claude 聊天（写作、分析和其他问题）。适合希望用一个 @Claude 入口处理所有工作的团队。 |

**注意**

在"代码 + 聊天"模式下，如果 Claude 把消息路由到了聊天，但你想要 Claude Code session，可以点击"Retry as Code"。反过来也一样，如果路由到了代码但你想要聊天，可以在该线程中选择对应选项。


### 把 Claude 添加到频道

安装后，Claude 不会自动加入任何频道。要在某个频道使用 Claude，需要在该频道中输入 `/invite @Claude` 来邀请它。Claude 只能在已加入的频道中回复 @提及。

## 工作原理

### 自动检测

在 Slack 频道或线程中 @Claude 时，Claude 会自动分析你的消息，判断是否为编码任务。如果检测到编码意图，会将请求路由到 Web 端 Claude Code，而不是当作普通聊天来回复。

你也可以明确告诉 Claude 把请求当作编码任务处理，即使它没有自动检测到。

**注意**

Slack 中的 Claude Code 只在频道（公开或私有）中可用，不支持私信（DM）。

### 上下文收集

**来自线程**：在线程中 @Claude 时，它会收集该线程中所有消息的上下文来理解完整对话。

**来自频道**：在频道中直接 @提及时，Claude 会查看最近的频道消息获取相关上下文。

这些上下文帮助 Claude 理解问题、选择合适的仓库，并决定如何完成任务。

**警告**

在 Slack 中 @Claude 时，Claude 可以访问对话上下文以更好地理解你的请求。Claude 可能会遵循上下文中其他消息的指示，请确保只在受信任的 Slack 对话中使用。

### Session 流程

1. **发起**：你在编码请求中 @Claude
2. **检测**：Claude 分析消息并识别编码意图
3. **创建 session**：在 claude.ai/code 上创建新的 Claude Code session
4. **进度更新**：工作进行中，Claude 会在你的 Slack 线程中发布状态更新
5. **完成**：完成后，Claude @你并提供摘要和操作按钮
6. **审查**：点击"View Session"查看完整记录，或点击"Create PR"创建 pull request

## 界面元素

### App Home

App Home 标签页显示你的连接状态，可以将 Claude 账号与 Slack 连接或断开。

### 消息操作

* **View Session**：在浏览器中打开完整的 Claude Code session，可以查看所有工作内容、继续 session 或提出新请求。
* **Create PR**：直接从 session 的变更创建 pull request。
* **Retry as Code**：如果 Claude 最初以聊天方式回复，但你想要 Claude Code session，点击此按钮重试。
* **Change Repo**：Claude 选错仓库时，允许你选择其他仓库。

### 仓库选择

Claude 会根据 Slack 对话的上下文自动选择仓库。如果有多个仓库可能适用，Claude 可能会显示一个下拉列表让你选择。

## 访问和权限

### 用户级访问

| 访问类型 | 说明 |
| :-------------------- | :-------------------------------------------------------------------------- |
| Claude Code session | 每个用户在自己的 Claude 账号下运行 session |
| 用量和速率限制 | session 消耗计入个人的订阅额度 |
| 仓库访问 | 用户只能访问自己连接的仓库 |
| session 历史 | session 会出现在 claude.ai/code 的 Claude Code 历史记录中 |

### 工作区级访问

Slack 工作区管理员控制 Claude 应用在工作区中的可用性：

| 控制项 | 说明 |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| 应用安装 | 工作区管理员决定是否从 Slack 应用市场安装 Claude 应用 |
| Enterprise Grid 分发 | Enterprise Grid 组织中，组织管理员可以控制哪些工作区有权使用 Claude 应用 |
| 应用移除 | 从工作区移除应用会立即撤销该工作区所有用户的访问权限 |

### 基于频道的访问控制

安装后，Claude 不会自动加入任何频道。用户必须主动邀请 Claude 进入想要使用它的频道：

* **需要邀请**：在频道中输入 `/invite @Claude` 来添加 Claude
* **频道成员控制访问**：Claude 只能在已加入的频道中回复 @提及
* **通过频道控制使用范围**：管理员可以通过控制 Claude 被邀请到哪些频道、以及谁有权访问这些频道来管理使用权限
* **支持私有频道**：Claude 可在公开和私有频道中使用，团队可灵活控制可见性

这种基于频道的模型让团队可以将 Claude Code 的使用限制在特定频道，在工作区级权限之外多加一层访问控制。

## 各端可见的信息

**在 Slack 中**：你会看到状态更新、完成摘要和操作按钮。完整的对话记录会保存下来，随时可查看。

**在 Web 端**：完整的 Claude Code session，包含完整对话历史、所有代码变更、文件操作，以及继续 session 或创建 pull request 的能力。

对于 Enterprise 和 Teams 账号，从 Slack 中的 Claude 创建的 session 会自动对组织可见。详见 [Web 端 Claude Code 的 session 共享](./claude-code-on-the-web#sharing-sessions)。

## 最佳实践

### 写好请求

* **具体明确**：包含文件名、函数名或相关的错误信息。
* **提供上下文**：如果对话中不明确，说明具体的仓库或项目。
* **定义完成标准**：说清楚"做完"是什么样——Claude 需要写测试吗？更新文档？创建 PR？
* **善用线程**：在讨论 bug 或功能时在线程中回复，这样 Claude 可以收集完整的上下文。

### Slack vs Web 的选择

**适合用 Slack 的场景**：Slack 讨论中已经有相关上下文、你想异步发起任务，或者你在和需要了解进展的队友协作。

**适合直接用 Web 的场景**：你需要上传文件、想在开发过程中实时交互，或者在处理更长更复杂的任务。

## 故障排查

### Session 无法启动

1. 确认你的 Claude 账号已在 App Home 中完成连接
2. 检查你是否已开启 Web 端 Claude Code 的访问权限
3. 确保至少有一个 GitHub 仓库已连接到 Claude Code

### 仓库不显示

1. 在 [claude.ai/code](https://claude.ai/code) 的 Web 端 Claude Code 中连接仓库
2. 验证你对该仓库的 GitHub 权限
3. 尝试断开并重新连接你的 GitHub 账号

### 选错了仓库

1. 点击"Change Repo"按钮选择其他仓库
2. 在请求中写明仓库名称，帮助 Claude 更准确地选择

### 认证错误

1. 在 App Home 中断开并重新连接你的 Claude 账号
2. 确保你在浏览器中登录的是正确的 Claude 账号
3. 检查你的 Claude 订阅是否包含 Claude Code 访问权限

### Session 过期

1. 过期的 session 仍然可以在 Web 端 Claude Code 历史记录中查看
2. 你可以在 [claude.ai/code](https://claude.ai/code) 中继续或查阅历史 session

## 当前限制

* **仅支持 GitHub**：目前只支持 GitHub 上的仓库。
* **每次一个 PR**：每个 session 只能创建一个 pull request。
* **受速率限制约束**：session 消耗你个人 Claude 订阅的速率限制。
* **需要 Web 端权限**：用户必须有 Web 端 Claude Code 的访问权限；没有的话只能得到普通的 Claude 聊天回复。

## 相关资源

### [Web 端 Claude Code](/en/claude-code-on-the-web)

了解更多关于 Web 端 Claude Code 的信息


### [Claude 的 Slack 应用](https://claude.com/claude-and-slack)

Claude Slack 应用的通用文档


### [Slack 应用市场](https://slack.com/marketplace/A08SF47R6P4)

从 Slack 应用市场安装 Claude 应用


### [Claude 帮助中心](https://support.claude.com)

获取更多帮助
