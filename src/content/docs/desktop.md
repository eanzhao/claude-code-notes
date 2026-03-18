---
title: "使用 Claude Code 桌面版"
order: 10
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "充分利用 Claude Code Desktop：包括 Git 隔离的并行会话、可视化 diff 审查、应用预览、PR 监控、权限模式、连接器和企业配置。"
sourceUrl: "https://code.claude.com/docs/en/desktop.md"
sourceTitle: "Use Claude Code Desktop"
group: "Platforms and integrations > Claude Code on desktop"
groupLabel: "桌面端与图形界面"
tags: []
---
# 使用 Claude Code 桌面版

> 充分利用 Claude Code 桌面版：基于 Git 隔离的并行 session、可视化 diff 审查、应用预览、PR 监控、权限模式、连接器和企业配置。

Claude Desktop 应用中的 Code 选项卡让你通过图形界面而非终端使用 Claude Code。

桌面版在标准 Claude Code 体验之上增加了：

* 带行内评论的[可视化 diff 审查](#review-changes-with-diff-view)
* 连接开发服务器的[实时应用预览](#preview-your-app)
* 支持自动修复和自动合并的 [GitHub PR 监控](#monitor-pull-request-status)
* 基于 Git worktree 自动隔离的[并行 session](#work-in-parallel-with-sessions)
* 按计划定期运行 Claude 的[定时任务](#schedule-recurring-tasks)
* 对接 GitHub、Slack、Linear 等的[连接器](#connect-external-tools)
* 本地、[SSH](#ssh-sessions) 和[云端](#run-long-running-tasks-remotely)环境

**提示**

刚接触桌面版？先看[快速开始](./desktop-quickstart)安装应用并完成第一次编辑。

本页涵盖[使用代码](#work-with-code)、[管理 session](#manage-sessions)、[扩展 Claude Code](#extend-claude-code)、[定时任务](#schedule-recurring-tasks)和[环境配置](#environment-configuration)。还包括 [CLI 对比](#coming-from-the-cli)和[问题排查](#troubleshooting)。

## 开始一个 session

发送第一条消息之前，在输入区域配置四项内容：

* **环境**：选择 Claude 在哪里运行。选 **本地** 在你的电脑上跑，选 **远程** 用 Anthropic 托管的云 session，或选 [**SSH 连接**](#ssh-sessions) 连到你管理的远程机器。参见[环境配置](#environment-configuration)。
* **项目文件夹**：选择 Claude 工作的文件夹或仓库。远程 session 可以添加[多个仓库](#run-long-running-tasks-remotely)。
* **模型**：从发送按钮旁的下拉列表选择[模型](./model-config#available-models)。session 开始后模型锁定，不能更换。
* **权限模式**：从[模式选择器](#choose-a-permission-mode)选择 Claude 的自主程度。session 进行中可以随时切换。

输入任务按 **Enter** 开始。每个 session 独立跟踪各自的上下文和改动。

## 写代码

给 Claude 提供合适的上下文，控制它的自主程度，审查它的改动。

### 使用输入框

输入你要 Claude 做的事，按 **Enter** 发送。Claude 会读取项目文件、做出修改，并根据你的[权限模式](#choose-a-permission-mode)运行命令。你可以随时打断 Claude：点停止按钮，或直接输入纠正内容按 **Enter**。Claude 会立即停下来按你的新指示调整。

输入框旁边的 **+** 按钮可以访问文件附件、[skill](#use-skills)、[连接器](#connect-external-tools)和[插件](#install-plugins)。

### 添加文件和上下文

输入框支持两种方式引入外部上下文：
* **@提及文件**：输入 `@` 加文件名，把文件加入对话上下文，Claude 就能读取和引用这个文件。
* **附加文件**：用附件按钮添加图片、PDF 等文件，或直接拖进输入框。适合分享报错截图、设计稿或参考文档。

### 选择权限模式

权限模式决定 Claude 在 session 中有多大自主权：编辑文件前要不要问你、运行命令前要不要问你、还是都不问。你可以用发送按钮旁的模式选择器随时切换。建议从”请求权限”开始，熟悉 Claude 的行为后再切换到”自动接受编辑”或”计划模式”。

| 模式 | 设置键 | 行为 |
| ---------------------- | ------------------- | —————————————————————————————————————————————————————————————————————————————————————————
| **请求权限** | `default` | Claude 在编辑文件或运行命令之前都会询问。你能看到 diff 并逐项接受或拒绝。推荐新手使用。                                                                                                                                                                                                                            |
| **自动接受编辑** | `acceptEdits` | Claude 自动应用文件编辑，但运行终端命令前仍会询问。适合你信任文件改动、想加快迭代的场景。                                                                                                                                                                                                                  |
| **计划模式** | `plan` | Claude 分析代码并制定方案，但不修改文件也不运行命令。适合复杂任务，先看方案再动手。                                                                                                                                                                                                    |
| **绕过权限** | `bypassPermissions` | Claude 运行时不弹权限提示，等同于 CLI 中的 `--dangerously-skip-permissions`。需在设置 → Claude Code → “允许绕过权限模式”中开启。仅在沙箱容器或虚拟机中使用。参见[权限模式](./permissions#permission-modes)了解哪些检查会跳过。企业管理员可以禁用此选项。 |`dontAsk` 权限模式仅在 [CLI](./permissions#permission-modes) 中可用。

**提示：最佳实践**

复杂任务建议先用计划模式，让 Claude 制定方案。方案确认后再切到”自动接受编辑”或”请求权限”。参见[先探索、再规划、再编码](./best-practices#explore-first-then-plan-then-code)。

远程 session 支持自动接受编辑和计划模式。请求权限不可用，因为远程 session 默认自动接受文件编辑；绕过权限也不可用，因为远程环境本身就在沙箱中。

企业管理员可以限制可用的权限模式，详见[企业配置](#enterprise-configuration)。

### 预览应用

Claude 可以启动开发服务器并打开内嵌浏览器来验证改动。前端 Web 应用和后端服务器都适用：Claude 能测试 API 接口、查看服务器日志，并迭代修复发现的问题。通常 Claude 编辑项目文件后会自动启动服务器，你也可以随时让它预览。默认开启[自动验证](#auto-verify-changes)，每次编辑后自动检查。

在预览面板中，你可以：

* 直接在内嵌浏览器中与运行中的应用交互
* 看 Claude 自动验证自己的改动：截屏、检查 DOM、点击元素、填写表单、修复问题
* 从 session 工具栏的 **预览** 下拉菜单启动或停止服务器
* 在下拉菜单中选择 **持久化 session**，服务器重启时保留 cookie 和 localStorage，免得开发时反复登录
* 编辑服务器配置或一键停止所有服务器

Claude 会根据项目自动生成初始服务器配置。如果你的应用使用自定义的开发命令，编辑 `.claude/launch.json` 来匹配你的设置。完整参考见[配置预览服务器](#configure-preview-servers)。

要清除保存的 session 数据，在设置 → Claude Code 中关闭 **保留预览 session**。要完全禁用预览，在设置 → Claude Code 中关闭 **预览**。

### 用 diff 视图审查改动

Claude 改完代码后，diff 视图让你在创建 PR 之前逐文件审查修改。

当 Claude 修改文件时，会出现一个统计指示器，显示增减行数，如 `+12 -1`。点击它打开 diff 查看器，左侧是文件列表，右侧是每个文件的具体改动。

要对某一行评论，点击 diff 中的任意行打开评论框，输入反馈按 **Enter** 添加。写完多条评论后一次性提交：

* **macOS**：按 **Cmd+Enter**
* **Windows**：按 **Ctrl+Enter**

Claude 会读取你的评论并做出相应修改，新的改动会以新 diff 的形式展示。

### 让 Claude 审查代码

在 diff 视图中，点击右上角工具栏的 **Review Code**，让 Claude 在提交前审查改动。Claude 会检查当前 diff 并直接在 diff 视图中留下评论。你可以回复评论或让 Claude 修改。

审查聚焦于高价值问题：编译错误、明显的逻辑错误、安全漏洞和 bug。不会标记代码风格、格式、已有问题或 linter 能捕获的东西。

### 监控 PR 状态

打开 PR 后，session 中会出现 CI 状态栏。Claude Code 通过 GitHub CLI 轮询检查结果并展示失败信息。

* **自动修复**：开启后，Claude 会自动读取失败输出并尝试修复未通过的 CI 检查。
* **自动合并**：开启后，所有检查通过后 Claude 会自动合并 PR（使用 squash 方式）。需要先[在 GitHub 仓库设置中启用](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository)自动合并。

用 CI 状态栏中的 **自动修复** 和 **自动合并** 开关来控制。CI 跑完后 Claude Code 还会发桌面通知。

**注意**

PR 监控需要在你的电脑上安装并认证 [GitHub CLI (`gh`)](https://cli.github.com/)。如果没装 `gh`，桌面版会在你第一次创建 PR 时提示安装。

## 管理 session

每个 session 是一次独立的对话，有自己的上下文和改动。你可以并行运行多个 session，或把任务发到云端。

### 并行 session

点侧边栏的 **+ 新 session** 可以并行处理多个任务。对于 Git 仓库，每个 session 通过 [Git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 获得项目的独立副本，一个 session 中的改动不会影响其他 session，直到你提交。

Worktree 默认存储在 `/.claude/worktrees/` 下。你可以在设置 → Claude Code → “Worktree 位置”中改为自定义目录。还可以设置分支前缀，自动添加到每个 worktree 的分支名前面，方便管理 Claude 创建的分支。完成后要删除 worktree，把鼠标悬停在侧边栏的 session 上，点归档图标。

**注意**

Session 隔离需要 [Git](https://git-scm.com/downloads)。大多数 Mac 自带 Git，终端里运行 `git --version` 检查。Windows 上 Code 选项卡必须有 Git 才能工作：[下载 Git for Windows](https://git-scm.com/downloads/win)，安装后重启应用。遇到 Git 错误可以试试用 Cowork session 来排查。

用侧边栏顶部的过滤图标按状态（活跃、已归档）和环境（本地、云端）筛选 session。要重命名 session 或查看上下文使用情况，点活跃 session 顶部工具栏中的 session 标题。上下文快满时 Claude 会自动压缩对话并继续工作。你也可以输入 `/compact` 提前触发压缩、释放上下文空间。压缩机制详见[上下文窗口](./how-claude-code-works#the-context-window)。

### 把耗时任务放到云端运行

大型重构、跑测试套件、迁移等耗时任务，启动 session 时选 **远程** 而非 **本地**。远程 session 在 Anthropic 的云端运行，关掉应用甚至关机都不影响。随时回来查看进度或调整方向。你也可以在 [claude.ai/code](https://claude.ai/code) 或 Claude iOS 应用中查看远程 session。

远程 session 还支持多仓库。选择云环境后，点仓库旁的 **+** 按钮添加其他仓库，每个仓库有独立的分支选择器。适合跨多个代码库的任务，比如同时更新共享库和它的使用方。

远程 session 的工作机制详见[网页版 Claude Code](./claude-code-on-the-web)。

### 在其他界面继续

**继续** 菜单在 session 工具栏右下角（VS Code 图标），让你把 session 迁移到其他界面：

* **网页版 Claude Code**：把本地 session 发到云端继续运行。桌面版会推送你的分支、生成对话摘要，并创建带完整上下文的远程 session。之后你可以选择归档本地 session 或保留。需要干净的 worktree，不适用于 SSH session。
* **IDE**：在当前工作目录下用支持的 IDE 打开项目。

## 扩展 Claude Code

连接外部服务、添加可重用工作流程、自定义 Claude 的行为以及配置预览服务器。

### 连接外部工具

对于本地和 [SSH](#ssh-sessions) 会话，请单击提示框旁边的 **+** 按钮，然后选择 **连接器** 以添加 Google 日历、Slack、GitHub、Linear、Notion 等集成。您可以在会话之前或会话期间添加连接器。连接器不可用于远程会话。

要管理或断开连接器，请转至桌面应用程序中的“设置”→“连接器”，或从提示框中的“连接器”菜单中选择“**管理连接器**”。

连接后，Claude 可以读取您的日历、发送消息、创建问题并直接与您的工具交互。您可以询问 Claude 您的会话中配置了哪些连接器。

连接器是具有图形设置流程的 [MCP 服务器](./mcp)。使用它们与支持的服务快速集成。对于连接器中未列出的集成，请通过 [设置文件](./mcp#installing-mcp-servers) 手动添加 MCP 服务器。您还可以[创建自定义连接器](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)。

### 使用技能

[技能](./skills) 扩展了 Claude 的功能。 Claude 会在相关时自动加载它们，或者您可以直接调用它们：在提示框中键入 `/` 或单击 **+** 按钮并选择 **斜线命令** 来浏览可用的内容。这包括[内置命令](./commands)、您的[自定义技能](./skills#create-custom-skills)、代码库中的项目技能以及任何[已安装的插件](./plugins)中的技能。选择一个，它会在输入字段中突出显示。在其后输入您的任务并照常发送。

### 安装插件[插件](./plugins) 是可重复使用的软件包，可将技能、代理、挂钩、MCP 服务器和 LSP 配置添加到 Claude Code。您可以从桌面应用程序安装插件，而无需使用终端。

对于本地和 [SSH](#ssh-sessions) 会话，单击提示框旁边的 **+** 按钮，然后选择 **插件** 以查看已安装的插件及其命令。要添加插件，请从子菜单中选择 **添加插件** 以打开插件浏览器，其中显示您配置的[市场](./plugin-marketplaces) 中的可用插件，包括官方 Anthropic 市场。选择**管理插件**以启用、禁用或卸载插件。

插件的范围可以是您的用户帐户、特定项目或仅限本地。插件不可用于远程会话。有关完整的插件参考（包括创建您自己的插件），请参阅 [插件](./plugins)。

### 配置预览服务器

Claude 会自动检测您的开发服务器设置，并将配置存储在您启动会话时选择的文件夹根目录下的 `.claude/launch.json` 中。预览使用此文件夹作为其工作目录，因此如果您选择父文件夹，则不会自动检测具有自己的开发服务器的子文件夹。要使用子文件夹的服务器，请直接在该文件夹中启动会话或手动添加配置。

要自定义服务器的启动方式，例如使用 `yarn dev` 而不是 `npm run dev` 或更改端口，请手动编辑文件或单击预览下拉列表中的 **编辑配置** 以在代码编辑器中将其打开。该文件支持带有注释的 JSON。

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

您可以定义多个配置来运行同一项目中的不同服务器，例如前端和 API。请参阅下面的[示例](#examples)。

#### 自动验证更改

启用 `autoVerify` 后，Claude 在编辑文件后自动验证代码更改。在完成响应之前，它会截取屏幕截图、检查错误并确认更改工作。

默认情况下自动验证处于开启状态。通过将 `"autoVerify": false` 添加到 `.claude/launch.json` 来按项目禁用它，或从 **预览** 下拉菜单中切换它。

```json
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

禁用后，预览工具仍然可用，您可以随时要求 Claude 进行验证。自动验证使其在每次编辑后自动进行。

#### 配置字段

`configurations` 数组中的每个条目接受以下字段：|领域 |类型 |描述 |
| ------------------- | ---------| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` |字符串|该服务器的唯一标识符 |
| `runtimeExecutable` |字符串|要运行的命令，例如 `npm`、`yarn` 或 `node` |
| `runtimeArgs` |字符串\[] |传递给 `runtimeExecutable` 的参数，例如 `["run", "dev"]` |
| `port` |数量 |您的服务器侦听的端口。默认为 3000 |
| `cwd` |字符串|相对于项目根目录的工作目录。默认为项目根目录。使用 `${workspaceFolder}` 显式引用项目根目录 |
| `env` |对象|其他环境变量作为键值对，例如 `{ "NODE_ENV": "development" }`。不要在此处放置机密，因为该文件已提交到您的存储库。您的 shell 配置文件中设置的秘密会自动继承。 |
| `autoPort` |布尔 |如何处理端口冲突。见下文 |
| `program` |字符串|使用 `node` 运行的脚本。请参阅[何时使用 `program` 与 `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable) |
| `args` |字符串\[] |参数传递至 `program`。仅在设置 `program` 时使用 |

##### 何时使用 `program` 与 `runtimeExecutable`

将 `runtimeExecutable` 与 `runtimeArgs` 结合使用，通过包管理器启动开发服务器。例如，`"runtimeExecutable": "npm"` 与 `"runtimeArgs": ["run", "dev"]` 一起运行 `npm run dev`。当您想要直接使用 `node` 运行独立脚本时，请使用 `program`。例如，`"program": "server.js"` 运行 `node server.js`。使用 `args` 传递附加标志。

#### 端口冲突

`autoPort` 字段控制当您的首选端口已在使用时会发生什么：

* **`true`**：Claude 自动查找并使用空闲端口。适用于大多数开发服务器。
* **`false`**：Claude 失败并出现错误。当您的服务器必须使用特定端口（例如 OAuth 回调或 CORS 允许列表）时，请使用此端口。
* **未设置（默认）**：Claude 询问服务器是否需要该确切端口，然后保存您的答案。

当 Claude 选择不同的端口时，它会通过 `PORT` 环境变量将分配的端口传递到您的服务器。

#### 示例

这些配置显示了不同项目类型的常见设置：

### Next.js

此配置使用 Yarn 在端口 3000 上运行 Next.js 应用程序：

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "web",
      "runtimeExecutable": "yarn",
      "runtimeArgs": ["dev"],
      "port": 3000
    }
  ]
}
```

  
### 多个服务器

对于具有前端和 API 服务器的 monorepo，定义多个配置。前端使用 `autoPort: true`，因此如果使用 3000，它会选择一个空闲端口，而 API 服务器恰好需要端口 8080：

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "frontend",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "cwd": "apps/web",
      "port": 3000,
      "autoPort": true
    },
    {
      "name": "api",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start"],
      "cwd": "server",
      "port": 8080,
      "env": { "NODE_ENV": "development" },
      "autoPort": false
    }
  ]
}
```

  
### Node.js 脚本

要直接运行 Node.js 脚本而不是使用包管理器命令，请使用 `program` 字段：

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "server",
      "program": "server.js",
      "args": ["--verbose"],
      "port": 4000
    }
  ]
}
```

## 安排重复任务

计划任务会按照您选择的时间和频率自动启动新的本地会话。将它们用于重复性工作，例如每日代码审查、依赖项更新检查或从日历和收件箱中提取的早间简报。

任务在您的计算机上运行，​​因此桌面应用程序必须打开并且您的计算机必须处于唤醒状态才能启动任务。有关错过的运行和追赶行为的详细信息，请参阅[计划任务的运行方式](#how-scheduled-tasks-run)。

**注意**

默认情况下，计划任务会根据工作目录所处的任何状态运行，包括未提交的更改。在提示输入中启用工作树切换，为每个运行提供自己独立的 Git 工作树，与 [并行会话](#work-in-parallel-with-sessions) 的工作方式相同。

要创建计划任务，请单击边栏中的“**计划**”，然后单击“**+ 新任务**”。配置这些字段：|领域|描述 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|名称 |任务的标识符。转换为小写短横线并用作磁盘上的文件夹名称。在您的任务中必须是唯一的。                                                                                        |
|描述 |任务列表中显示简短摘要。                                                                                                                                                                                    |
|提示|任务运行时发送到 Claude 的指令。编写此内容的方式与在提示框中编写任何消息的方式相同。提示输入还包括模型、权限模式、工作文件夹和工作树的控件。 |
|频率|任务运行的频率。请参阅下面的[频率选项](#frequency-options)。                                                                                                                                              |

您还可以通过在任何会话中描述您想要的内容来创建任务。例如，“设置每日代码审查，每天早上 9 点运行。”

### 频率选项

* **手动**：无计划，仅在您单击 **立即运行** 时运行。对于保存按需触发的提示很有用
* **每小时**：每小时运行。每个任务从整点开始会有最多 10 分钟的固定偏移量，以错开 API 流量
* **每日**：显示时间选择器，默认为当地时间上午 9:00
* **工作日**：与每日相同，但跳过周六和周日
* **每周**：显示时间选择器和日期选择器

对于选择器未提供的时间间隔（每 15 分钟一次、每月第一天等），请在任何桌面会话中要求 Claude 设置计划。使用通俗易懂的语言；例如，“安排一个任务每 6 小时运行一次所有测试”。

### 计划任务如何运行

计划任务在您的计算机上本地运行。 Desktop 在应用程序打开时每分钟检查一次计划，并在任务到期时启动新的会话，独立于您打开的任何手动会话。每个任务在计划时间后都会有最多 10 分钟的固定延迟，以错开 API 流量。延迟是确定性的：相同的任务总是以相同的偏移量开始。

当任务触发时，您会收到桌面通知，并且新会话会出现在侧边栏中的 **计划** 部分下。打开它以查看 Claude 执行了哪些操作、查看更改或响应权限提示。该会话的工作方式与其他会话类似：Claude 可以编辑文件、运行命令、创建提交和打开拉取请求。任务仅在桌面应用程序运行并且您的计算机处于唤醒状态时运行。如果您的计算机在预定时间内处于睡眠状态，则运行将被跳过。要防止空闲睡眠，请在**桌面应用程序 → 常规**下的“设置”中启用**保持计算机唤醒**。合上笔记本电脑的盖子仍会使其进入睡眠状态。

### 错过的跑步

当应用程序启动或计算机唤醒时，Desktop 会检查每个任务在过去 7 天内是否错过了任何运行。如果是这样，Desktop 会针对最近错过的时间开始一次追赶运行，并丢弃任何较旧的运行。错过六天的每日任务在唤醒时运行一次。当追赶运行开始时，桌面会显示通知。

编写提示时请记住这一点。如果您的计算机整天处于睡眠状态，则计划于上午 9 点执行的任务可能会在晚上 11 点运行。如果时间很重要，请在提示本身中添加护栏，例如：“仅审查今天的提交。如果是下午 5 点之后，请跳过审查，只发布错过的内容的摘要。”

### 计划任务的权限

每个任务都有自己的权限模式，您可以在创建或编辑任务时设置该权限模式。 `~/.claude/settings.json` 中的允许规则也适用于计划任务会话。如果任务在询问模式下运行并且需要运行它没有权限的工具，则运行将停止，直到您批准为止。该会话在侧边栏中保持打开状态，以便您稍后可以回答。

为了避免停顿，请在创建任务后单击“**立即运行**”，注意权限提示，然后为每个任务选择“始终允许”。该任务的未来运行会自动批准相同的工具，而无需提示。您可以从任务的详细信息页面查看和撤销这些批准。

### 管理计划任务

单击 **计划** 列表中的任务以打开其详细信息页面。从这里您可以：

* **立即运行**：立即启动任务，无需等待下一个预定时间
* **切换重复**：暂停或恢复计划运行而不删除任务
* **编辑**：更改提示、频率、文件夹或其他设置
* **查看历史记录**：查看过去的每一次运行，包括由于计算机处于睡眠状态而跳过的运行
* **查看允许的权限**：从 **始终允许** 面板查看并撤销为此任务保存的工具批准
* **删除**：删除任务并存档其创建的所有会话

您还可以通过在任何桌面会话中询问 Claude 来管理任务。例如，“暂停我的依赖项审核任务”、“删除站立准备任务”或“显示我的计划任务”。

要编辑磁盘上的任务提示，请打开 `~/.claude/scheduled-tasks/<task-name>/SKILL.md`（或在 [`CLAUDE_CONFIG_DIR`](./env-vars) 下，如果已设置）。该文件对 `name` 和 `description` 使用 YAML frontmatter，并以提示符作为正文。更改将在下次运行时生效。计划、文件夹、模型和启用状态不在此文件中：通过编辑表单更改它们或询问 Claude。

## 环境配置

[启动会话](#start-a-session) 时选择的环境决定 Claude 的执行位置以及连接方式：* **本地**：在您的计算机上运行，可以直接访问您的文件
* **远程**：在 Anthropic 的云基础设施上运行。即使您关闭应用程序，会话也会继续。
* **SSH**：在您通过 SSH 连接的远程计算机上运行，例如您自己的服务器、云虚拟机或开发容器

### 本地会话

本地会话从 shell 继承环境变量。如果您需要其他变量，请在 shell 配置文件中设置它们，例如 `~/.zshrc` 或 `~/.bashrc`，然后重新启动桌面应用程序。有关支持的变量的完整列表，请参阅[环境变量](./env-vars)。

[扩展思维](./common-workflows#use-extended-thinking-thinking-mode) 默认启用，可提高复杂推理任务的性能，但会使用额外的标记。要完全禁用思考，请在 shell 配置文件中设置 `MAX_THINKING_TOKENS=0`。在 Opus 上，除了 `0` 之外，`MAX_THINKING_TOKENS` 都会被忽略，因为自适应推理反而控制思维深度。

### 远程会话

即使您关闭应用程序，远程会话也会在后台继续。使用量计入您的[订阅计划限制](./costs)，无需单独支付计算费用。

您可以创建具有不同网络访问级别和环境变量的自定义云环境。启动远程会话时选择环境下拉列表，然后选择 **添加环境**。有关配置网络访问和环境变量的详细信息，请参阅[云环境](./claude-code-on-the-web#cloud-environment)。

### SSH 会话

SSH 会话允许您在远程计算机上运行 Claude Code，同时使用桌面应用程序作为界面。这对于使用位于云虚拟机、开发容器或具有特定硬件或依赖项的服务器上的代码库非常有用。

要添加 SSH 连接，请在启动会话之前单击环境下拉列表，然后选择 **+ 添加 SSH 连接**。该对话框要求：

* **名称**：此连接的友好标签
* **SSH 主机**：`user@hostname` 或 `~/.ssh/config` 中定义的主机
* **SSH 端口**：如果留空则默认为 22，或者使用 SSH 配置中的端口
* **身份文件**：您的私钥的路径，例如 `~/.ssh/id_rsa`。留空以使用默认密钥或您的 SSH 配置。

添加后，连接将显示在环境下拉列表中。选择它以在该计算机上启动会话。 Claude 在远程计算机上运行，​​可以访问其文件和工具。

Claude Code 必须安装在远程计算机上。连接后，SSH 会话支持权限模式、连接器、插件和 MCP 服务器。

## 企业配置

使用 Teams 或 Enterprise 计划的组织可以通过管理控制台控件、托管设置文件和设备管理策略来管理桌面应用程序行为。

### 管理控制台控件

这些设置是通过[管理设置控制台](https://claude.ai/admin-settings/claude-code)配置的：

* **启用或禁用“代码”选项卡**：控制组织中的用户是否可以在桌面应用程序中访问 Claude Code
* **禁用绕过权限模式**：防止组织中的用户启用绕过权限模式
* **在网络上禁用 Claude Code**：为您的组织启用或禁用远程会话

### 托管设置托管设置会覆盖项目和用户设置，并在桌面生成 CLI 会话时应用。您可以在组织的[托管设置](./settings#settings-precedence) 文件中设置这些密钥，或通过管理控制台远程推送它们。

|关键|描述 |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` |设置为 `"disable"` 以防止用户启用绕过权限模式。请参阅[托管设置](./permissions#managed-only-settings)。 |

有关仅托管设置（包括 `allowManagedPermissionRulesOnly` 和 `allowManagedHooksOnly`）的完整列表，请参阅[仅托管设置](./permissions#managed-only-settings)。

通过管理控制台上传的远程管理设置当前仅适用于 CLI 和 IDE 会话。对于特定于桌面的限制，请使用上面的管理控制台控件。

### 设备管理策略

IT 团队可以通过 macOS 上的 MDM 或 Windows 上的组策略来管理桌面应用程序。可用策略包括启用或禁用 Claude Code 功能、控制自动更新以及设置自定义部署 URL。

* **macOS**：使用 Jamf 或 Kandji 等工具通过 `com.anthropic.Claude` 首选项域进行配置
* **Windows**：通过 `SOFTWARE\Policies\Claude` 处的注册表进行配置

### 身份验证和 SSO

企业组织可以要求所有用户进行 SSO。有关计划级别的详细信息，请参阅[身份验证](./authentication)；有关 SAML 和 OIDC 配置，请参阅[设置 SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)。

### 数据处理

Claude Code 在本地会话中本地处理您的代码，或在远程会话中在 Anthropic 的云基础设施上处理您的代码。对话和代码上下文被发送到 Anthropic 的 API 进行处理。有关数据保留、隐私和合规性的详细信息，请参阅[数据处理](./data-usage)。

### 部署

桌面可以通过企业部署工具进行分发：

* **macOS**：使用 `.dmg` 安装程序通过 Jamf 或 Kandji 等 MDM 进行分发
* **Windows**：通过 MSIX 包或 `.exe` 安装程序进行部署。有关企业部署选项（包括静默安装），请参阅[为 Windows 部署 Claude Desktop](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows)

有关代理设置、防火墙白名单和 LLM 网关等网络配置，请参阅[网络配置](./network-config)。

有关完整的企业配置参考，请参阅[企业配置指南](https://support.claude.com/en/articles/12622667-enterprise-configuration)。

## 来自 CLI？

如果您已使用 Claude Code CLI，则桌面将运行具有图形界面的相同底层引擎。您可以在同一台计算机上甚至在同一个项目上同时运行这两者。每个都维护单独的会话历史记录，但它们通过 CLAUDE.md 文件共享配置和项目内存。

要将 CLI 会话移至桌面，请在终端中运行 `/desktop`。 Claude 保存您的会话并在桌面应用程序中打开它，然后退出 CLI。此命令仅适用于 macOS 和 Windows。

**提示**何时使用桌面与 CLI：当您需要在侧边栏中进行可视化差异审查、文件附件或会话管理时，请使用桌面。当您需要脚本、自动化、第三方提供商或更喜欢终端工作流程时，请使用 CLI。

### CLI 标志等效项

下表显示了常见 CLI 标志的桌面应用程序等效项。未列出的标志没有桌面等效项，因为它们是为脚本或自动化而设计的。

|命令行 |桌面等效 |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet` |在开始会话之前，发送按钮旁边的模型下拉菜单 |
| `--resume`、`--continue` |单击侧边栏中的会话 |
| `--permission-mode` |发送按钮旁边的模式选择器 |
| `--dangerously-skip-permissions` |绕过权限模式。在设置→Claude Code→“允许绕过权限模式”中启用。企业管理员可以禁用此设置。 |
| `--add-dir` |在远程会话中使用 **+** 按钮添加多个存储库 |
| `--allowedTools`、`--disallowedTools` |不适用于桌面 |
| `--verbose` |无法使用。检查系统日志：macOS 上的 Console.app、事件查看器 → Windows 日志 → Windows 上的应用程序 |
| `--print`、`--output-format` |无法使用。桌面仅是交互式的。                                                                                              |
| `ANTHROPIC_MODEL` 环境变量 |发送按钮旁边的模型下拉菜单 |
| `MAX_THINKING_TOKENS` 环境变量 |在外壳配置文件中设置；适用于本地会话。请参见[环境配置](#environment-configuration)。                            |

### 共享配置

桌面和 CLI 读取相同的配置文件，因此您的设置会保留：* **[CLAUDE.md](./memory)** 项目中的文件由两者使用
* **[MCP 服务器](./mcp)** 在 `~/.claude.json` 或 `.mcp.json` 中配置可在两者中工作
* **设置中定义的[挂钩](./hooks)**和**[技能](./skills)**适用于两者
* **`~/.claude.json` 和 `~/.claude/settings.json` 中的[设置](./settings)** 是共享的。 `settings.json` 中的权限规则、允许的工具和其他设置适用于桌面会话。
* **模型**：Sonnet、Opus 和 Haiku 均可用。在 Desktop 中，在开始会话之前，从发送按钮旁边的下拉列表中选择模型。您无法在活动会话期间更改模型。

**注意**

**MCP 服务器：桌面聊天应用程序与 Claude Code**：为 `claude_desktop_config.json` 中的 Claude Desktop 聊天应用程序配置的 MCP 服务器与 Claude Code 分开，不会出现在“代码”选项卡中。要在 Claude Code 中使用 MCP 服务器，请在 `~/.claude.json` 或项目的 `.mcp.json` 文件中配置它们。有关详细信息，请参阅 [MCP 配置](./mcp#installing-mcp-servers)。

### 功能比较

此表比较了 CLI 和桌面之间的核心功能。有关 CLI 标志的完整列表，请参阅 [CLI 参考](./cli-reference)。|特色 |命令行 |桌面|
| ---------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
|权限模式|所有模式，包括 `dontAsk` |通过“设置”|询问权限、自动接受编辑、计划模式和绕过权限
| `--dangerously-skip-permissions` | CLI 标志 |绕过权限模式。在设置→Claude Code→“允许绕过权限模式”中启用|
| [第三方提供商](./third-party-integrations) |Bedrock、Vertex、Foundry |无法使用。 Desktop直接连接Anthropic的API。                                |
| [MCP 服务器](./mcp) |在设置文件中配置 |用于本地和 SSH 会话或设置文件的连接器 UI
| [插件](./plugins) | `/plugin` 命令 |插件管理器 UI |
| @提及文件 |基于文本|具有自动完成功能 |
|文件附件 |不可用 |图片、PDF |
|会话隔离| [`--worktree`](./cli-reference) 标志 |自动工作树|
|多次会议 |独立终端 |侧边栏选项卡 |
|重复性任务 | cron 作业、CI 管道 | [计划任务](#schedule-recurring-tasks) |
|脚本编写和自动化| [`--print`](./cli-reference)、[Agent SDK](./headless) |不可用 |

### 桌面版中不可用的内容

以下功能仅在 CLI 或 VS Code 扩展中可用：* **第三方提供商**：桌面直接连接到 Anthropic 的 API。请改用带有 Bedrock、Vertex 或 Foundry 的 [CLI](./quickstart)。
* **Linux**：桌面应用程序仅适用于 macOS 和 Windows。
* **内联代码建议**：Desktop 不提供自动完成式建议。它通过对话提示和显式代码更改来工作。
* **代理团队**：多代理编排可通过 [CLI](./agent-teams) 和 [Agent SDK](./headless) 进行，而不是在桌面中进行。

## 故障排除

### 检查您的版本

要查看您正在运行的桌面应用程序的版本：

* **macOS**：点击菜单栏中的**Claude**，然后点击**关于Claude**
* **Windows**：单击“**帮助**”，然后单击“**关于**”

单击版本号将其复制到剪贴板。

### 403 或“代码”选项卡中的身份验证错误

如果您在使用“代码”选项卡时看到 `Error 403: Forbidden` 或其他身份验证失败：

1. 从应用程序菜单注销并重新登录。这是最常见的修复方法。
2. 确认您有有效的付费订阅：Pro、Max、Teams 或 Enterprise。
3. 如果 CLI 工作但 Desktop 不工作，请完全退出桌面应用程序，而不仅仅是关闭窗口，然后重新打开并再次登录。
4. 检查您的互联网连接和代理设置。

### 启动时出现空白或卡住的屏幕

如果应用程序打开但显示空白或无响应的屏幕：

1. 重新启动应用程序。
2. 检查待处理的更新。该应用程序在启动时自动更新。
3. 在 Windows 上，检查事件查看器中 **Windows 日志 → 应用程序** 下的崩溃日志。

###“加载会话失败”

如果您看到 `Failed to load session`，则所选文件夹可能不再存在、Git 存储库可能需要未安装的 Git LFS，或者文件权限可能会阻止访问。尝试选择其他文件夹或重新启动应用程序。

### 会话未找到已安装的工具

如果 Claude 找不到 `npm`、`node` 等工具或其他 CLI 命令，请验证这些工具在常规终端中是否正常工作，检查 shell 配置文件是否正确设置 PATH，然后重新启动桌面应用程序以重新加载环境变量。

### Git 和 Git LFS 错误

在 Windows 上，“代码”选项卡需要 Git 才能启动本地会话。如果您看到“需要 Git”，请安装 [Git for Windows](https://git-scm.com/downloads/win) 并重新启动应用程序。

如果您看到“此存储库需要 Git LFS，但尚未安装”，请从 [git-lfs.com](https://git-lfs.com/) 安装 Git LFS，运行 `git lfs install`，然后重新启动应用程序。

### MCP 服务器无法在 Windows 上运行

如果 MCP 服务器切换不响应或服务器无法在 Windows 上连接，请检查服务器是否在您的设置中正确配置，重新启动应用程序，验证服务器进程是否在任务管理器中运行，并查看服务器日志是否有连接错误。

### 应用程序不会退出

* **macOS**：按 Cmd+Q。如果应用程序没有响应，请使用 Cmd+Option+Esc 强制退出，选择 Claude，然后单击强制退出。
* **Windows**：使用任务管理器并按 Ctrl+Shift+Esc 结束 Claude 进程。

### Windows 特定问题* **安装后路径未更新**：打开一个新的终端窗口。 PATH 更新仅适用于新的终端会话。
* **并发安装错误**：如果您看到有关正在进行的另一安装的错误，但实际上没有，请尝试以管理员身份运行安装程序。
* **ARM64**：完全支持 Windows ARM64 设备。

### Cowork 选项卡在 Intel Mac 上不可用

Cowork 选项卡需要 macOS 上的 Apple Silicon（M1 或更高版本）。在 Windows 上，Cowork 可在所有支持的硬件上使用。 “聊天”和“代码”选项卡在 Intel Mac 上正常工作。

### 在 CLI 中打开时“分支尚不存在”

远程会话可以创建本地计算机上不存在的分支。单击会话工具栏中的分支名称进行复制，然后在本地获取：

```bash
git fetch origin <branch-name>
git checkout <branch-name>
```

### 还卡住了吗？

* 在 [GitHub 问题](https://github.com/anthropics/claude-code/issues) 上搜索或提交错误
* 访问[Claude支持中心](https://support.claude.com/)

提交错误时，请包括您的桌面应用程序版本、操作系统、确切的错误消息和相关日志。在 macOS 上，检查 Console.app。在 Windows 上，检查事件查看器 → Windows 日志 → 应用程序。
