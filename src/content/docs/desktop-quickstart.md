---
title: "开始使用桌面应用程序"
order: 9
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "在桌面上安装 Claude Code 并开始您的第一个编码会话"
sourceUrl: "https://code.claude.com/docs/en/desktop-quickstart.md"
sourceTitle: "Get started with the desktop app"
group: "Platforms and integrations > Claude Code on desktop"
groupLabel: "桌面端与图形界面"
tags: []
---
# 开始使用桌面应用

> 安装 Claude Code 桌面应用，开始你的第一次编码

桌面应用为 Claude Code 提供了图形界面：可视化 diff 审查、实时应用预览、带自动合并的 GitHub PR 监控、基于 Git worktree 隔离的并行 session、定时任务，以及远程运行任务。不需要终端。

本页会带你完成安装并启动第一个 session。如果你已经装好了，请看[使用 Claude Code 桌面版](./desktop)了解完整功能。

![Claude Code 桌面界面显示选中的代码选项卡，带有提示框，权限模式选择器设置为询问权限、模型选择器、文件夹选择器和本地环境选项](https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce)

  ![深色模式下的 Claude Code 桌面界面显示选中的“代码”选项卡，带有提示框，权限模式选择器设置为询问权限、模型选择器、文件夹选择器和本地环境选项](https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8)
桌面应用有三个选项卡：

* **Chat**：普通对话，没有文件访问权限，类似 claude.ai。
* **Cowork**：自主后台 agent，在云端虚拟机中运行任务。你做别的事时它能独立工作。
* **Code**：交互式编码助手，直接访问本地文件。你实时审查并批准每一处更改。

Chat 和 Cowork 的介绍见 [Claude Desktop 支持文章](https://support.claude.com/en/collections/16163169-claude-desktop)。本页聚焦 **Code** 选项卡。

**注意**

Claude Code 需要 [Pro、Max、Teams 或 Enterprise 订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=desktop_quickstart_pricing)。

## 安装

### 下载应用

下载适合你平台的 Claude。

### [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)

Intel 和 Apple Silicon 通用版本


### [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs)

x64 处理器

Windows ARM64 请[点这里下载](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs)。

暂不支持 Linux。


### 登录

从应用程序文件夹（macOS）或开始菜单（Windows）启动 Claude，用你的 Anthropic 账号登录。


### 打开 Code 选项卡

点击顶部中间的 **Code** 选项卡。如果提示你升级，需要先[订阅付费套餐](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=desktop_quickstart_upgrade)。如果提示在线登录，完成登录后重启应用。如果看到 403 错误，参见[身份验证问题排查](./desktop#403-or-authentication-errors-in-the-code-tab)。

桌面应用已内置 Claude Code，无需单独安装 Node.js 或 CLI。如果你想在终端里用 `claude` 命令，需要另外安装 CLI，参见 [CLI 入门](./quickstart)。

## 开始第一个 session

打开 Code 选项卡后，选个项目，给 Claude 点事做。

### 选择环境和文件夹

选择 **本地** 让 Claude 在你的电脑上运行，直接操作你的文件。点击 **选择文件夹** 选中你的项目目录。

**提示**

从一个你熟悉的小项目开始，这是了解 Claude Code 最快的方式。Windows 上必须安装 [Git](https://git-scm.com/downloads/win) 才能正常使用本地 session。大多数 Mac 自带 Git。

你也可以选择：
* **远程**：在 Anthropic 的云端运行 session，关掉应用也会继续执行。远程 session 使用和 [Claude Code 网页版](./claude-code-on-the-web) 相同的基础设施。
* **SSH**：通过 SSH 连接远程机器（你自己的服务器、云虚拟机或开发容器）。远程机器上必须安装 Claude Code。


### 选择模型

从发送按钮旁边的下拉列表选择模型。参见[模型](./model-config#available-models)了解 Opus、Sonnet 和 Haiku 的对比。session 开始后不能换模型。


### 告诉 Claude 做什么

输入你想让 Claude 做的事：

* `Find a TODO comment and fix it`
* `Add tests for the main function`
* `Create a CLAUDE.md with instructions for this codebase`

[Session](./desktop#work-in-parallel-with-sessions) 是你和 Claude 围绕代码展开的一次对话。每个 session 各自跟踪上下文和改动，互不干扰。


### 审查并接受更改

默认情况下，Code 选项卡以[请求权限模式](./desktop#choose-a-permission-mode)启动——Claude 提出修改建议，等你批准后才会应用。你会看到：

1. [Diff 视图](./desktop#review-changes-with-diff-view)精确展示每个文件的改动
2. 接受/拒绝按钮，逐项审批
3. Claude 根据你的要求实时更新

如果你拒绝某项更改，Claude 会问你希望怎么改。在你接受之前，文件不会被修改。

## 下一步

你已经完成了第一次编辑。完整功能参见 [使用 Claude Code 桌面版](./desktop)，下面是一些值得尝试的事情。

**随时打断和纠正。** 你可以随时打断 Claude。如果方向不对，点停止按钮或直接输入纠正内容按 **Enter**。Claude 会立即停下来，按你的新指示调整。不用等它跑完，也不用重新开始。

**给 Claude 更多上下文。** 在输入框里输入 `@filename` 可以把特定文件拉进对话，用附件按钮添加图片和 PDF，或者直接把文件拖进输入框。Claude 得到的上下文越多，结果越好。参见[添加文件和上下文](./desktop#add-files-and-context-to-prompts)。

**用 skill 处理重复任务。** 输入 `/` 或点 **+** → **斜杠命令** 浏览[内置命令](./commands)、[自定义 skill](./skills) 和插件 skill。Skill 是可复用的 prompt，需要时随时调用，比如代码审查清单或部署步骤。

**提交前检查改动。** Claude 编辑文件后会出现 `+12 -1` 这样的指示器。点击它打开 [diff 视图](./desktop#review-changes-with-diff-view)，逐文件查看修改，还能对特定行添加评论。Claude 会读取你的评论并据此修改。点 **Review Code** 让 Claude 自己审查 diff 并留下行内建议。

**调整控制力度。** [权限模式](./desktop#choose-a-permission-mode)决定了你的控制程度。请求权限（默认）每次编辑前都需要你批准；自动接受编辑会自动应用文件修改，加快迭代；计划模式让 Claude 只制定方案不动文件，适合大型重构前先理清思路。

**用插件扩展功能。** 点输入框旁的 **+** 按钮，选择 **插件** 来浏览和安装各种[插件](./desktop#install-plugins)，可以添加 skill、agent、MCP server 等。

**预览你的应用。** 点 **预览** 下拉菜单，直接在桌面应用里运行开发服务器。Claude 能查看运行中的应用、测试接口、检查日志并迭代修复。参见[预览应用](./desktop#preview-your-app)。

**跟踪 PR。** 打开 PR 后，Claude Code 会监控 CI 检查结果，自动修复失败的检查，或在所有检查通过后自动合并。参见[监控 PR 状态](./desktop#monitor-pull-request-status)。

**定时运行 Claude。** 设置[定时任务](./desktop#schedule-recurring-tasks)让 Claude 定期自动运行：每天早上做代码审查、每周检查依赖更新，或者从连接的工具中提取简报。

**准备好了就扩展规模。** 从侧边栏开启[并行 session](./desktop#work-in-parallel-with-sessions)，同时处理多个任务，每个都在独立的 Git worktree 中。把[耗时任务发到云端](./desktop#run-long-running-tasks-remotely)，关掉应用也能继续跑；或者[在网页版或 IDE 中接着做](./desktop#continue-in-another-surface)。[连接外部工具](./desktop#extend-claude-code)如 GitHub、Slack、Linear，把工作流串起来。

## 从 CLI 过来的？

桌面版和 CLI 跑的是同一个引擎，只是多了图形界面。你可以在同一个项目上同时用两者，它们共享配置（CLAUDE.md 文件、MCP server、hook、skill 和设置）。功能对比、CLI 标志对应关系以及桌面版暂不支持的功能，参见 [CLI 对比](./desktop#coming-from-the-cli)。

## 继续探索

* [使用 Claude Code 桌面版](./desktop)：权限模式、并行 session、diff 视图、连接器和企业配置
* [问题排查](./desktop#troubleshooting)：常见错误和设置问题的解决方案
* [最佳实践](./best-practices)：写好 prompt、用好 Claude Code 的技巧
* [常用工作流](./common-workflows)：调试、重构、测试等实操教程
