---
title: "开发容器"
order: 37
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "了解适合需要一致、安全环境的团队的 Claude Code 开发容器。"
sourceUrl: "https://code.claude.com/docs/en/devcontainer.md"
sourceTitle: "Development containers"
tags: []
---
# 开发容器

> 了解适合需要一致、安全环境的团队的 Claude Code 开发容器。

参考 [devcontainer setup](https://github.com/anthropics/claude-code/tree/main/.devcontainer) 和关联的 [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) 提供了一个预配置的开发容器，您可以按原样使用，也可以根据需要进行自定义。此开发容器可与 Visual Studio Code [开发容器扩展](https://code.visualstudio.com/docs/devcontainers/containers) 和类似工具配合使用。

容器的增强安全措施（隔离和防火墙规则）允许您运行 `claude --dangerously-skip-permissions` 绕过权限提示进行无人值守操作。

**警告**

虽然开发容器提供了实质性的保护，但没有任何系统能够完全免受所有攻击。
使用 `--dangerously-skip-permissions` 执行时，开发容器不会阻止恶意项目泄露开发容器中可访问的任何内容，包括 Claude Code 凭据。
我们建议在使用受信任的存储库进行开发时仅使用开发容器。
始终保持良好的安全实践并监控 Claude 的活动。

## 主要特点

* **生产就绪 Node.js**：基于 Node.js 20 构建，具有基本的开发依赖项
* **设计安全**：自定义防火墙仅限制网络访问必要的服务
* **开发人员友好的工具**：包括 git、具有生产力增强功能的 ZSH、fzf 等
* **无缝 VS Code 集成**：预配置的扩展和优化的设置
* **会话持久性**：在容器重新启动之间保留命令历史记录和配置
* **随处可用**：与 macOS、Windows 和 Linux 开发环境兼容

## 入门分 4 步

1. 安装 VS Code 和远程 - 容器扩展
2. 克隆 [Claude Code 参考实现](https://github.com/anthropics/claude-code/tree/main/.devcontainer) 存储库
3. 打开VS Code中的存储库
4. 出现提示时，单击“在容器中重新打开”（或使用命令面板：Cmd+Shift+P →“远程容器：在容器中重新打开”）

## 配置细目

devcontainer 设置由三个主要组件组成：

* [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json)：控制容器设置、扩展和卷安装
* [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): 定义容器镜像和安装的工具
* [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): 建立网络安全规则

## 安全特性

容器通过其防火墙配置实现了多层安全方法：

* **精确访问控制**：仅限制到白名单域的出站连接（npm 注册表、GitHub、Claude API 等）
* **允许的出站连接**：防火墙允许出站 DNS 和 SSH 连接
* **默认拒绝策略**：阻止所有其他外部网络访问
* **启动验证**：容器初始化时验证防火墙规则
* **隔离**：创建与主系统分离的安全开发环境

## 自定义选项

devcontainer 配置旨在适应您的需求：* 根据您的工作流程添加或删除 VS Code 扩展
* 修改不同硬件环境的资源分配
* 调整网络访问权限
* 自定义 shell 配置和开发人员工具

## 示例用例

### 保护客户工作

使用开发容器隔离不同的客户端项目，确保代码和凭据永远不会在环境之间混合。

### 团队入职

新的团队成员可以在几分钟内获得完全配置的开发环境，并预安装所有必要的工具和设置。

### 一致的 CI/CD 环境

在 CI/CD 管道中镜像您的开发容器配置，以确保开发和生产环境匹配。

## 相关资源

* [VS Code 开发容器文档](https://code.visualstudio.com/docs/devcontainers/containers)
* [Claude Code 安全最佳实践](./security)
* [企业网络配置](./network-config)
