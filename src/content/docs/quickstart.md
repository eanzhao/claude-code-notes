---
title: "快速入门"
order: 2
section: "getting-started"
sectionLabel: "快速入门"
sectionOrder: 1
summary: "欢迎来到 Claude Code！"
sourceUrl: "https://code.claude.com/docs/en/quickstart.md"
sourceTitle: "Quickstart"
tags: []
---
# 快速入门

> 欢迎来到Claude Code！

几分钟就能上手 AI 辅助编程。看完这篇，你就知道怎么用 Claude Code 做常见的开发任务了。

## 开始之前

确保你有：

* 一个终端或命令提示符
  * 没用过终端？看看[终端指南](https://code.claude.com/docs/en/terminal-guide)
* 一个代码项目
* [Claude 订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=quickstart_prereq)（Pro、Max、Teams 或 Enterprise）、[Claude 控制台](https://console.anthropic.com/) 账号，或通过[支持的云服务商](./third-party-integrations)访问

**注意**

本指南主要覆盖终端 CLI。Claude Code 也可以在 [网页端](https://claude.ai/code)、[桌面应用](./desktop)、[VS Code](./vs-code)、[JetBrains IDE](./jetbrains)、[Slack](./slack) 中使用，也支持通过 [GitHub Actions](./github-actions) 和 [GitLab](./gitlab-ci-cd) 接入 CI/CD。请参阅[所有使用入口](./overview#use-claude-code-everywhere)。

## 步骤 1：安装 Claude Code

安装方式（任选一种）：

### 原生安装（推荐）

**macOS、Linux、WSL：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows 命令：**

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

## 第 2 步：登录账号

Claude Code 需要登录才能使用。用 `claude` 命令启动交互式 session 时会提示你登录：

```bash
claude
# 首次使用会提示登录
```

```bash
/login
# 按提示操作，用你的账号登录
```

支持以下账号类型：

* [Claude Pro、Max、Teams 或 Enterprise](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=quickstart_login)（推荐）
* [Claude 控制台](https://console.anthropic.com/)（用预充值额度访问 API）。首次登录时会自动在控制台创建”Claude Code”工作区，方便统一跟踪费用。
* [Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry](./third-party-integrations)（企业云服务商）

登录后凭据会保存下来，不需要再次登录。之后想切换账号，用 `/login` 命令。

## 第 3 步：开始你的第一个 session

在任意项目目录打开终端，启动 Claude Code：

```bash
cd /path/to/your/project
claude
```

你会看到 Claude Code 欢迎界面，包含 session 信息、最近的对话和最新更新。输入 `/help` 查看可用命令，输入 `/resume` 继续之前的对话。

**提示**

登录（第 2 步）后，凭据会保存在你的系统里。更多细节见[凭据管理](./authentication#credential-management)。

## 第 4 步：问第一个问题

先从了解你的代码库开始。试试这些：

```text
what does this project do?
```

Claude 会分析你的文件并给出概要。也可以问更具体的问题：

```text
what technologies does this project use?
```

```text
where is the main entry point?
```

```text
explain the folder structure
```

你也可以直接问 Claude 它自己会什么：

```text
what can Claude Code do?
```

```text
how do I create custom skills in Claude Code?
```

```text
can Claude Code work with Docker?
```

**注意**

Claude Code 会按需读取你的项目文件，不需要你手动添加上下文。

## 第 5 步：做第一次代码修改

让 Claude Code 动手写点代码。试个简单任务：

```text
add a hello world function to the main file
```

Claude Code 会：

1. 找到合适的文件
2. 展示建议的改动
3. 征求你的同意
4. 执行编辑

**注意**

Claude Code 修改文件前一定会征求许可。你可以逐个批准，也可以为当前 session 开启”全部接受”模式。

## 第 6 步：用 Claude Code 操作 Git

Claude Code 让 Git 操作变成对话式的：

```text
what files have I changed?
```

```text
commit my changes with a descriptive message
```

更复杂的 Git 操作也行：

```text
create a new branch called feature/quickstart
```

```text
show me the last 5 commits
```

```text
help me resolve merge conflicts
```

## 第 7 步：修 bug 或加功能

Claude 很擅长调试和写功能。

用自然语言描述你想要什么：

```text
add input validation to the user registration form
```

或者修复现有问题：

```text
there's a bug where users can submit empty forms - fix it
```

Claude Code 会：

* 找到相关代码
* 理解上下文
* 实施修复
* 跑测试（如果有的话）

## 第 8 步：试试其他常见工作流

Claude 还能做很多事：

**重构代码**

```text
refactor the authentication module to use async/await instead of callbacks
```

**编写测试**

```text
write unit tests for the calculator functions
```

**更新文档**

```text
update the README with installation instructions
```

**Code review**

```text
review my changes and suggest improvements
```

**提示**

像跟同事说话一样跟 Claude 交流。描述你想做什么，它会帮你搞定。

## 基本命令

以下是日常使用中最重要的命令：

|命令|它有什么作用 |示例|
| ------------------- | ------------------------------------------------------ | ----------------------------------- |
| `claude` |启动交互模式 | `claude` |
| `claude "task"` |运行一次性任务 | `claude "fix the build error"` |
| `claude -p "query"` |运行一次性查询，然后退出 | `claude -p "explain this function"` |
| `claude -c` |继续当前目录中的最近对话 | `claude -c` |
| `claude -r` |恢复之前的对话 | `claude -r` |
| `claude commit` |创建 Git 提交 | `claude commit` |
| `/clear` |清除通话记录 | `/clear` |
| `/help` |显示可用命令 | `/help` |
| `exit` 或 Ctrl+C |退出 Claude Code | `exit` |

有关命令的完整列表，请参阅 [CLI 参考](./cli-reference)。

## 给初学者的专业提示

有关更多信息，请参阅[最佳实践](./best-practices) 和[常见工作流程](./common-workflows)。

### 具体说明您的要求

而不是：“修复错误”

尝试：“修复用户输入错误凭据后看到空白屏幕的登录错误”### 使用分步说明

将复杂的任务分解为步骤：

```text
1. create a new database table for user profiles
2. create an API endpoint to get and update user profiles
3. build a webpage that allows users to see and edit their information
```

  
### 让Claude先探索一下

在进行更改之前，让 Claude 了解您的代码：

```text
analyze the database schema
```

```text
build a dashboard showing products that are most frequently returned by our UK customers
```

  
### 使用快捷方式节省时间

* 按 `?` 查看所有可用的键盘快捷键
* 使用 Tab 完成命令
* 按 ↑ 查看命令历史记录
* 输入 `/` 查看所有命令和技能

## 接下来是什么？

现在您已经了解了基础知识，接下来探索更多高级功能：

### [Claude Code 的工作原理](/en/how-claude-code-works)

了解代理循环、内置工具以及 Claude Code 如何与您的项目交互

  
### [最佳实践](/en/best-practices)

通过有效的提示和项目设置获得更好的结果

  
### [常用工作流程](/en/common-workflows)

常见任务的分步指南

  
### [扩展 Claude Code](/en/features-overview)

使用 CLAUDE.md、技能、挂钩、MCP 等进行定制

## 获取帮助

* **在 Claude Code** 中：键入 `/help` 或询问“我如何...”
* **文档**：你在这里！浏览其他指南
* **社区**：加入我们的 [Discord](https://www.anthropic.com/discord) 获取提示和支持
