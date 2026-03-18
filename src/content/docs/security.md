---
title: "安全"
order: 40
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "了解 Claude Code 的安全保障措施和安全使用的最佳实践。"
sourceUrl: "https://code.claude.com/docs/en/security.md"
sourceTitle: "Security"
tags: []
---
# 安全

> Claude Code 的安全防护机制与安全使用最佳实践。

## 安全理念

### 安全基础

代码安全至关重要。Claude Code 以安全为核心设计，基于 Anthropic 的全面安全体系构建。更多信息和合规资源（SOC 2 Type II 报告、ISO 27001 认证等）请访问 [Anthropic 信任中心](https://trust.anthropic.com)。

### 基于权限的架构

Claude Code 默认采用严格的只读权限。需要额外操作（编辑文件、运行测试、执行命令）时，Claude Code 会请求明确许可。你可以选择单次批准或设为自动允许。

我们把 Claude Code 设计得透明且安全。例如，执行 bash 命令前必须先经你批准，让你拥有直接控制权。用户和组织可以自行配置权限策略。

详细权限配置请参阅[权限](./permissions)。

### 内置防护

为降低 Agent 系统的风险，Claude Code 提供了以下防护：

* **沙箱化 Bash 工具**：[沙箱](./sandboxing)化的 bash 命令具有文件系统和网络隔离，在保障安全的同时减少权限提示。通过 `/sandbox` 启用，可定义 Claude Code 自主工作的边界
* **写入限制**：Claude Code 只能写入启动目录及其子目录——未经允许无法修改父目录中的文件。虽然 Claude Code 可以读取工作目录外的文件（方便访问系统库和依赖），但写入操作严格限制在项目范围内
* **减少权限疲劳**：支持按用户、按代码库或按组织将常用安全命令加入白名单
* **批量接受编辑模式**：可批量接受多个编辑，同时保留有副作用的命令的权限提示

### 用户责任

Claude Code 只拥有你授予它的权限。批准前请务必审查代码和命令的安全性。

## 防范 prompt 注入

Prompt 注入是一种攻击手段，攻击者试图通过插入恶意文本来操控 AI 助手的行为。Claude Code 内置了多层防护：

### 核心防护

* **权限系统**：敏感操作需要明确批准
* **上下文感知分析**：通过分析完整请求检测潜在有害指令
* **输入净化**：处理用户输入以防止命令注入
* **命令黑名单**：默认阻止从网络获取任意内容的高风险命令，如 `curl` 和 `wget`。明确允许时请注意[权限模式的限制](./permissions#tool-specific-permission-rules)

### 隐私保护

我们实施了多项数据保护措施：
* 敏感信息有限留期（详见[隐私中心](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data)）
* 限制对用户会话数据的访问
* 用户可控制数据训练偏好。消费者用户可随时更改[隐私设置](https://claude.ai/settings/privacy)

完整详情请查看[商业服务条款](https://www.anthropic.com/legal/commercial-terms)（适用于 Team、Enterprise 和 API 用户）、[消费者条款](https://www.anthropic.com/legal/consumer-terms)（适用于 Free、Pro 和 Max 用户）以及[隐私政策](https://www.anthropic.com/legal/privacy)。

### 额外防护

* **网络请求审批**：发起网络请求的工具默认需要用户批准
* **隔离上下文窗口**：Web fetch 使用独立的上下文窗口，避免注入潜在恶意 prompt
* **信任验证**：首次运行代码库和新 MCP 服务器时需要信任验证
  * 注意：使用 `-p` 标志非交互运行时，信任验证被跳过
* **命令注入检测**：可疑的 bash 命令即使之前已加入白名单，也需要手动批准
* **默认拒绝**：无法匹配的命令默认需要手动批准
* **自然语言描述**：复杂的 bash 命令会附带解释说明
* **安全凭据存储**：API 密钥和 token 经过加密。参阅[凭据管理](./authentication#credential-management)

**警告**

**Windows WebDAV 安全风险**：在 Windows 上运行 Claude Code 时，建议不要启用 WebDAV，也不要让 Claude Code 访问可能包含 WebDAV 子目录的路径（如 `\\*`）。WebDAV 已被 [Microsoft 弃用](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features#:~:text=The%20Webclient%20\(WebDAV\)%20service%20is%20deprecated)，存在安全风险。启用 WebDAV 可能允许 Claude Code 绕过权限系统向远程主机发起网络请求。

**处理不可信内容的最佳实践**：

1. 批准前先审查建议的命令
2. 避免将不可信内容直接传给 Claude
3. 验证对关键文件的修改建议
4. 使用虚拟机 (VM) 执行脚本和工具调用，尤其是与外部 Web 服务交互时
5. 使用 `/feedback` 报告可疑行为

**警告**

这些防护可以显著降低风险，但没有任何系统能做到绝对安全。使用任何 AI 工具时，请始终保持良好的安全习惯。

## MCP 安全

Claude Code 允许用户配置 Model Context Protocol (MCP) 服务器。允许的 MCP 服务器列表在源代码中配置，作为工程师检入源码控制的 Claude Code 设置的一部分。

建议你编写自己的 MCP 服务器或使用可信提供商的 MCP 服务器。你可以为 MCP 服务器配置 Claude Code 权限。Anthropic 不管理或审核任何第三方 MCP 服务器。

## IDE 安全

关于在 IDE 中运行 Claude Code 的更多信息，请参阅 [VS Code 安全与隐私](./vs-code#security-and-privacy)。

## 云端执行安全

在 Web 上使用 [Claude Code](./claude-code-on-the-web) 时，有额外的安全控制：

* **隔离虚拟机**：每个云端会话都在 Anthropic 管理的隔离 VM 中运行
* **网络访问控制**：网络访问默认受限，可配置为禁用或仅允许特定域名
* **凭据保护**：认证通过安全代理处理，沙箱内使用有限范围的凭据，再转换为你实际的 GitHub 认证 token
* **分支限制**：Git push 操作仅限当前工作分支
* **审计日志**：云端环境中的所有操作都会记录日志，用于合规和审计
* **自动清理**：会话结束后云端环境自动销毁

更多云端执行的细节请参阅 [Web 版 Claude Code](./claude-code-on-the-web)。

[Remote Control](./remote-control) 会话的工作方式不同：Web 界面连接的是在你本地机器上运行的 Claude Code 进程。所有代码执行和文件访问都在本地完成，数据通过 TLS 经由 Anthropic API 传输，和本地 Claude Code 会话一样。不涉及云端 VM 或沙箱。连接使用多个短期、有限范围的凭据，每个凭据只限于特定用途并独立过期，以限制单个凭据泄露的影响范围。

## 安全最佳实践

### 处理敏感代码

* 批准前审查所有建议的变更
* 对敏感仓库使用项目级权限配置
* 考虑使用 [devcontainer](./devcontainer) 获得额外隔离
* 定期用 `/permissions` 审核你的权限设置

### 团队安全

* 使用[托管设置](./settings#settings-files)强制执行组织标准
* 通过版本控制共享已批准的权限配置
* 对团队成员进行安全最佳实践培训
* 通过 [OpenTelemetry 指标](./monitoring-usage)监控 Claude Code 使用情况
* 使用 [`ConfigChange` hook](./hooks#configchange) 在会话中审计或阻止设置变更

### 报告安全问题

如果你发现 Claude Code 中的安全漏洞：

1. 请勿公开披露
2. 通过 [HackerOne 项目](https://hackerone.com/anthropic-vdp/reports/new?type=team&report_type=vulnerability)提交报告
3. 附上详细的复现步骤
4. 在公开前给我们时间修复

## 相关资源

* [沙箱](./sandboxing) - bash 命令的文件系统和网络隔离
* [权限](./permissions) - 配置权限与访问控制
* [监控](./monitoring-usage) - 跟踪和审计 Claude Code 活动
* [开发容器](./devcontainer) - 安全隔离的环境
* [Anthropic 信任中心](https://trust.anthropic.com) - 安全认证与合规
