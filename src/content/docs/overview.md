---
title: "Claude Code 概述"
order: 1
section: "getting-started"
sectionLabel: "快速入门"
sectionOrder: 1
summary: "Claude Code 是一个 AI 编程助手，能读懂你的代码、编辑文件、运行命令，还能和你的开发工具无缝配合。终端、IDE、桌面应用、浏览器都能用。"
sourceUrl: "https://code.claude.com/docs/en/overview.md"
sourceTitle: "Claude Code overview"
tags: []
---
# Claude Code 概述

> Claude Code 是一个 AI 编程助手，能读懂你的代码、编辑文件、运行命令，还能和你的开发工具无缝配合。终端、IDE、桌面应用、浏览器都能用。

Claude Code 是一个 AI 编程助手，帮你写功能、修 bug、自动化开发任务。它能理解你的整个代码库，跨文件、跨工具协作完成工作。

## 开始使用

选一个你喜欢的环境就能开始。大多数环境需要 [Claude 订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_pricing) 或 [Anthropic 控制台](https://console.anthropic.com/) 账号。终端 CLI 和 VS Code 还支持[第三方服务商](./third-party-integrations)。

### 终端

功能完整的 CLI，直接在终端里用 Claude Code。从命令行就能编辑文件、运行命令、管理整个项目。

安装方式（任选一种）：

### 原生安装（推荐）

    **macOS、Linux、WSL：**

    ```bash         
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell：**

    ```powershell         
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD：**

    ```batch         
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows 需要先安装 [Git for Windows](https://git-scm.com/downloads/win)。**


**说明**

原生安装会在后台自动更新，始终保持最新版本。

### Homebrew

```bash
brew install --cask claude-code
```

**说明**

Homebrew 安装不会自动更新，需要定期运行 `brew upgrade claude-code` 来获取新功能和安全补丁。

### WinGet

```powershell
winget install Anthropic.ClaudeCode
```

**说明**

WinGet 安装不会自动更新，需要定期运行 `winget upgrade Anthropic.ClaudeCode` 来获取新功能和安全补丁。

    然后在任意项目中启动 Claude Code：

    ```bash 
    cd your-project
    claude
    ```

    首次使用会提示你登录，登录完就能开始了。[继续快速入门 →](./quickstart)


**提示**

更多安装选项、手动更新或卸载方法，见[高级设置](./setup)。遇到问题请看[故障排除](./troubleshooting)。

  
### VS Code

VS Code 扩展直接在编辑器里提供 inline diff、@-mention、计划审查和对话历史。

* [为 VS Code 安装](vscode:extension/anthropic.claude-code)
* [为 Cursor 安装](cursor:extension/anthropic.claude-code)

也可以在扩展视图里搜”Claude Code”（Mac: `Cmd+Shift+X`，Windows/Linux: `Ctrl+Shift+X`）。装好后打开命令面板（`Cmd+Shift+P` / `Ctrl+Shift+P`），输入”Claude Code”，选择**在新标签页中打开**。

[开始使用 VS Code →](./vs-code#get-started)

  
### 桌面应用

独立应用，可以在 IDE 和终端之外使用 Claude Code。支持可视化 diff 查看、并行多 session、定时任务和云端 session。

下载安装：

* [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)（Intel 和 Apple 芯片）
* [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs)（x64）
* [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs)（仅支持远程 session）

安装后启动 Claude，登录，点 **Code** 标签页开始写代码。需要[付费订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_desktop_pricing)。

[了解更多桌面应用功能 →](./desktop-quickstart)

  
### 网页端

在浏览器中运行 Claude Code，无需本地设置。你可以启动长时间运行的任务，完成后再回来查看；也可以处理本地没有的仓库，或者并行跑多个任务。桌面浏览器和 Claude iOS 应用都可以使用。

从 [claude.ai/code](https://claude.ai/code) 开始编码。

[开始使用网页端 →](./claude-code-on-the-web#getting-started)

  
### JetBrains

支持 IntelliJ IDEA、PyCharm、WebStorm 等 JetBrains IDE 的插件，提供交互式 diff 查看和选中代码上下文共享。

从 JetBrains Marketplace 安装 [Claude Code 插件](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，重启 IDE 即可。

[开始使用 JetBrains →](./jetbrains)

## 你能用它做什么

下面是一些典型用法：

### 自动化那些你一直拖着没做的事

Claude Code 帮你处理那些耗时又琐碎的活：给没测试的代码补测试、修 lint 错误、解决合并冲突、更新依赖、写 release notes。

```bash
claude "write tests for the auth module, run them, and fix any failures"
```

  
### 写功能、修 bug

用自然语言描述你想要什么。Claude Code 会制定方案，跨多个文件写代码，然后验证是否可行。

修 bug 时，直接贴报错信息或描述现象就行。Claude Code 会在代码库中追踪问题，定位根因并实施修复。更多例子见[常见工作流](./common-workflows)。

  
### 提交代码、创建 PR

Claude Code 直接和 Git 配合。它能 stage 改动、写 commit message、建分支、开 PR。

```bash
claude "commit my changes with a descriptive message"
```

在 CI 里，你还可以用 [GitHub Actions](./github-actions) 或 [GitLab CI/CD](./gitlab-ci-cd) 自动做代码审查和 issue 分类。

  
### 用 MCP 接入外部工具

[Model Context Protocol (MCP)](./mcp) 是把 AI 工具连接到外部数据源的开放标准。通过 MCP，Claude Code 可以读 Google Drive 里的设计文档、更新 Jira ticket、从 Slack 拉数据，或者使用你自己写的工具。

  
### 用指令、skill 和 hook 做定制

[`CLAUDE.md`](./memory) 是放在项目根目录的 Markdown 文件，Claude Code 每次启动 session 时都会读。你可以在里面写编码规范、架构决策、偏好的库、review 检查项等。Claude 还会在工作过程中自动构建[记忆](./memory#auto-memory)，自动保存构建命令、调试经验等信息，不需要你手动写。

创建[自定义命令](./skills)可以把可复用的工作流打包成你的团队都能用的 skill，比如 `/review-pr` 或 `/deploy-staging`。

[Hook](./hooks) 让你在 Claude Code 操作前后运行 shell 命令，比如每次编辑文件后自动格式化，或者提交前跑 lint。

  
### 跑多 agent 协作，或构建自定义 agent

启动[多个 Claude Code agent](./sub-agents) 同时处理任务的不同部分。主 agent 负责协调、分配子任务、合并结果。

如果需要完全自定义的工作流，[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 允许你基于 Claude Code 的工具和能力构建自己的 agent，完全控制编排、工具访问和权限。

### 用 CLI 做管道、脚本和自动化

Claude Code 是可组合的，遵循 Unix 哲学。你可以把日志 pipe 给它，在 CI 里跑它，或者和其他工具串联：

```bash
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

完整的命令和参数列表见 [CLI 参考](./cli-reference)。

  
### 随时随地工作

Session 不绑定在某一个环境里，你可以随时在不同环境之间切换：

* 离开电脑后，用 [Remote Control](./remote-control) 在手机或任何浏览器上继续工作
* 在 [web](./claude-code-on-the-web) 或 [iOS 应用](https://apps.apple.com/app/claude-by-anthropic/id6473753684)上启动长时间任务，然后用 `/teleport` 拉到你的终端里
* 用 `/desktop` 把终端 session 转到[桌面应用](./desktop)里做可视化 diff review
* 在 [Slack](./slack) 里 @Claude 发 bug 报告，它会直接帮你开 PR

## 在各个环境中使用 Claude Code

所有环境连的都是同一个 Claude Code 引擎，你的 CLAUDE.md、设置、MCP server 在所有环境中通用。

除了前面说的[终端](./quickstart)、[VS Code](./vs-code)、[JetBrains](./jetbrains)、[桌面应用](./desktop)和[网页端](./claude-code-on-the-web)，Claude Code 还集成了 CI/CD、聊天和浏览器工作流：

|我想... |推荐方式|
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
|在手机或其他设备上继续本地 session | [Remote Control](./remote-control) |
|在本地开任务，到手机上继续 | [网页端](./claude-code-on-the-web) 或 [Claude iOS 应用](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
|自动化 PR review 和 issue 分类 | [GitHub Actions](./github-actions) 或 [GitLab CI/CD](./gitlab-ci-cd) |
|每个 PR 自动做 code review | [GitHub Code Review](./code-review) |
|从 Slack 的 bug 报告直接生成 PR | [Slack](./slack) |
|调试线上 Web 应用 | [Chrome](./chrome) |
|构建自定义 agent | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |

## 下一步

装好 Claude Code 后，这些指南帮你进一步了解：

* [快速入门](./quickstart)：一步步完成你的第一个实际任务，从探索代码库到提交修复
* [指令与记忆](./memory)：通过 CLAUDE.md 和自动记忆给 Claude 设定持久指令
* [常见工作流](./common-workflows) 和 [最佳实践](./best-practices)：把 Claude Code 用好的各种模式
* [设置](./settings)：根据你的工作流定制 Claude Code
* [故障排除](./troubleshooting)：常见问题的解决方案
* [code.claude.com](https://code.claude.com/)：演示、定价和产品详情
