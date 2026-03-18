---
title: "在 VS Code 中使用 Claude Code"
order: 17
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "安装并配置 VS Code 的 Claude Code 扩展。通过内联差异、@-提及、计划审查和键盘快捷键获得 AI 编码帮助。"
sourceUrl: "https://code.claude.com/docs/en/vs-code.md"
sourceTitle: "Use Claude Code in VS Code"
tags: []
---
# 在 VS Code 中使用 Claude Code

> 安装并配置 VS Code 的 Claude Code 扩展。通过内联差异、@-提及、计划审查和键盘快捷键获得 AI 编码帮助。

![VS Code 编辑器，右侧打开 Claude Code 扩展面板，显示与 Claude 的对话](https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8)

VS Code 扩展为 Claude Code 提供本机图形界面，直接集成到您的 IDE 中。这是在 VS Code 中使用 Claude Code 的推荐方法。

通过该扩展，您可以在接受之前查看和编辑 Claude 的计划、自动接受所做的编辑、@-提及您选择的特定行范围的文件、访问对话历史记录以及在单独的选项卡或窗口中打开多个对话。

## 先决条件

安装之前，请确保您拥有：

* VS Code 1.98.0 或更高版本
* Anthropic 帐户（您将在首次打开扩展程序时登录）。如果您使用的是 Amazon Bedrock 或 Google Vertex AI 等第三方提供商，请参阅[使用第三方提供商](#use-third-party-providers)。

**提示**

该扩展包括 CLI（命令行界面），您可以从 VS Code 的集成终端访问它以获取高级功能。有关详细信息，请参阅[VS Code 扩展与 Claude Code CLI](#vs-code-extension-vs-claude-code-cli)。

## 安装扩展

单击您的 IDE 的链接直接安装：

* [为 VS Code 安装](vscode:extension/anthropic.claude-code)
* [安装光标](cursor:extension/anthropic.claude-code)

或者在 VS Code 中，按 `Cmd+Shift+X` (Mac) 或 `Ctrl+Shift+X` (Windows/Linux) 打开“扩展”视图，搜索“Claude Code”，然后单击“**安装**”。

**注意**

如果安装后未出现扩展，请重新启动 VS Code 或从命令面板运行“开发人员：重新加载窗口”。

## 开始吧

安装完成后，您可以通过 VS Code 界面开始使用 Claude Code：

### 打开 Claude Code 面板

在整个 VS Code 中，Spark 图标表示 Claude Code： ![Spark 图标](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505)

打开 Claude 的最快方法是单击 **编辑器工具栏**（编辑器右上角）中的 Spark 图标。仅当您打开文件时才会出现该图标。

    ![VS Code 编辑器在编辑器工具栏中显示 Spark 图标](https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02)

其他打开Claude Code的方法：

* **活动栏**：单击左侧边栏中的 Spark 图标可打开会话列表。单击任何会话将其作为完整编辑器选项卡打开，或启动一个新选项卡。该图标始终在活动栏中可见。
* **命令面板**：`Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)，键入“Claude Code”，然后选择“在新选项卡中打开”等选项
* **状态栏**：单击窗口右下角的**✱ Claude Code**。即使没有文件打开，此功能也有效。

首次打开面板时，会出现 **学习 Claude Code** 清单。单击 **显示** 来完成每个项目，或使用 X 将其关闭。要稍后重新打开它，请在扩展 → Claude Code 下的 VS Code 设置中取消选中 **隐藏入职**。

您可以拖动 Claude 面板将其重新定位到 VS Code 中的任意位置。有关详细信息，请参阅[自定义您的工作流程](#customize-your-workflow)。

  
### 发送提示请求 Claude 帮助您处理代码或文件，无论是解释某些内容如何工作、调试问题还是进行更改。

**提示**

Claude 自动查看您选择的文本。按 `Option+K` (Mac) / `Alt+K` (Windows/Linux) 还可在提示中插入@提及引用（如 `@file.ts#5-10`）。

下面是询问文件中特定行的示例：

    ![VS Code 编辑器在 Python 文件中选择了第 2-3 行，Claude Code 面板显示了有关带有 @-mention 引用的这些行的问题](https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd)

  
### 查看更改

当 Claude 想要编辑文件时，它会显示原始更改和建议更改的并排比较，然后请求许可。您可以接受、拒绝或告诉 Claude 该怎么做。

    ![VS Code 显示 Claude 提议的更改的差异，并询问是否进行编辑的权限提示](https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c)

有关可以使用 Claude Code 执行哪些操作的更多想法，请参阅[常见工作流程](./common-workflows)。

**提示**

从命令面板运行“Claude Code：打开演练”，以引导了解基础知识。

## 使用提示框

提示框支持多种功能：

* **权限模式**：点击提示框底部的模式指示灯可切换模式。在正常模式下，Claude 在执行每个操作之前都会请求许可。在计划模式下，Claude 描述它将执行的操作并在进行更改之前等待批准。 VS Code 会自动将计划作为完整的降价文档打开，您可以在其中添加内联注释以在 Claude 开始之前提供反馈。在自动接受模式下，Claude 无需询问即可进行编辑。在 `claudeCode.initialPermissionMode` 下的 VS Code 设置中设置默认值。
* **命令菜单**：单击 `/` 或键入 `/` 打开命令菜单。选项包括附加文件、切换模型、切换扩展思维和查看计划使用情况 (`/usage`)。自定义部分提供对 MCP 服务器、挂钩、内存、权限和插件的访问。带有终端图标的项目在集成终端中打开。
* **上下文指示器**：提示框显示您正在使用 Claude 的上下文窗口的大小。 Claude 会在需要时自动压缩，或者您也可以手动运行 `/compact`。
* **扩展思维**：让Claude花更多的时间推理复杂的问题。通过命令菜单 (`/`) 将其打开。详情请参见【延伸思考】(./common-workflows#use-extended-thinking-thinking-mode)。
* **多行输入**：按`Shift+Enter`添加新行而不发送。这也适用于问题对话框的“其他”自由文本输入。

### 参考文件和文件夹

使用 @-mentions 提供有关特定文件或文件夹的 Claude 上下文。当您键入 `@` 后跟文件或文件夹名称时，Claude 会读取该内容并可以回答有关该内容的问题或对其进行更改。 Claude Code 支持模糊匹配，因此您可以输入部分名称来查找您需要的内容：

```text
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

对于大型 PDF，您可以要求 Claude 读取特定页面而不是整个文件：单个页面、第 1-10 页等范围或第 3 页以上的开放式范围。当您在编辑器中选择文本时，Claude 可以自动看到突出显示的代码。提示框页脚显示选择了多少行。按 `Option+K` (Mac) / `Alt+K` (Windows/Linux) 插入带有文件路径和行号的@提及（例如 `@app.ts#5-10`）。单击选择指示器可切换 Claude 是否可以看到突出显示的文本 - 斜线图标表示所选内容对 Claude 隐藏。

您还可以按住 `Shift` 的同时将文件拖到提示框中以将其添加为附件。单击任意附件上的 X 可将其从上下文中删除。

### 恢复过去的对话

单击 Claude Code 面板顶部的下拉菜单可访问您的对话历史记录。您可以按关键字搜索或按时间浏览（今天、昨天、最近 7 天等）。单击任何对话即可恢复该对话并显示完整的消息历史记录。将鼠标悬停在会话上可显示重命名和删除操作：重命名以为其提供描述性标题，或删除以将其从列表中删除。有关恢复会话的更多信息，请参阅[常见工作流程](./common-workflows#resume-previous-conversations)。

### 从 Claude.ai 恢复远程会话

如果您在网络上使用 [Claude Code](./claude-code-on-the-web)，则可以直接在 VS Code 中恢复这些远程会话。这需要使用 **Claude.ai 订阅**，而不是 Anthropic 控制台登录。

### 打开过去的对话

单击 Claude Code 面板顶部的 **过去的对话** 下拉列表。

  
### 选择远程选项卡

该对话框显示两个选项卡：本地和远程。单击 **远程** 查看来自 claude.ai 的会话。

  
### 选择要恢复的会话

浏览或搜索您的远程会话。单击任意会话即可下载并在本地继续对话。

**注意**

只有使用 GitHub 存储库启动的 Web 会话才会出现在“远程”选项卡中。恢复加载本地对话历史记录；更改不会同步回 claude.ai。

## 定制您的工作流程

启动并运行后，您可以重新定位 Claude 面板、运行多个会话或切换到终端模式。

### 选择 Claude 居住的地方

您可以拖动 Claude 面板将其重新定位到 VS Code 中的任意位置。抓住面板的选项卡或标题栏并将其拖动到：

* **辅助侧边栏**：窗口的右侧。在您编码时保持 Claude 可见。
* **主侧边栏**：左侧边栏，带有资源管理器、搜索等图标。
* **编辑器区域**：将 Claude 作为文件旁边的选项卡打开。对于副任务很有用。

**提示**

使用侧边栏进行主要 Claude 会话，并打开其他选项卡来执行辅助任务。 Claude 会记住您的首选位置。活动栏会话列表图标与 Claude 面板分开：会话列表始终在活动栏中可见，而 Claude 面板图标仅在面板停靠到左侧边栏时才出现。

### 运行多个对话

使用命令面板中的 **在新选项卡中打开** 或 **在新窗口中打开** 启动其他对话。每个对话都保留自己的历史记录和上下文，使您可以并行处理不同的任务。使用选项卡时，火花图标上的小彩色点指示状态：蓝色表示权限请求正在等待，橙色表示 Claude 在选项卡隐藏时已完成。

### 切换到终端模式

默认情况下，扩展程序会打开图形聊天面板。如果您喜欢 CLI 风格的界面，请打开 [使用终端设置](vscode://settings/claudeCode.useTerminal) 并选中该框。

您还可以打开 VS Code 设置（Mac 上的 `Cmd+,` 或 Windows/Linux 上的 `Ctrl+,`），转至扩展 → Claude Code，然后选中 **使用终端**。

## 管理插件

VS Code 扩展包括用于安装和管理[插件](./plugins) 的图形界面。在提示框中输入`/plugins`，打开**管理插件**界面。

### 安装插件

插件对话框显示两个选项卡：**插件**和**市场**。

在插件选项卡中：

* **安装的插件**显示在顶部，并带有切换开关以启用或禁用它们
* **您配置的市场中的可用插件**显示在下面
* 搜索按名称或描述过滤插件
* 在任何可用插件上单击“**安装**”

安装插件时，选择安装范围：

* **为您安装**：可用于您的所有项目（用户范围）
* **为此项目安装**：与项目合作者共享（项目范围）
* **本地安装**：仅适用于您，仅在此存储库中（本地范围）

### 管理市场

切换到 **Marketplaces** 选项卡以添加或删除插件源：

* 输入 GitHub 存储库、URL 或本地路径以添加新市场
* 单击刷新图标可更新市场的插件列表
* 单击垃圾桶图标可删除市场

进行更改后，横幅会提示您重新启动 Claude Code 以应用更新。

**注意**

VS Code 中的插件管理在底层使用相同的 CLI 命令。您在扩展中配置的插件和市场也可以在 CLI 中使用，反之亦然。

有关插件系统的更多信息，请参阅[插件](./plugins)和[插件市场](./plugin-marketplaces)。

## 使用 Chrome 自动执行浏览器任务

将 Claude 连接到 Chrome 浏览器，以测试 Web 应用程序、使用控制台日志进行调试以及自动化浏览器工作流程，而无需离开 VS Code。这需要 [Chrome 扩展中的 Claude](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 版本 1.0.36 或更高版本。

在提示框中键入 `@browser`，然后输入您希望 Claude 执行的操作：

```text
@browser go to localhost:3000 and check the console for errors
```

您还可以打开附件菜单来选择特定的浏览器工具，例如打开新选项卡或阅读页面内容。

Claude 为浏览器任务打开新选项卡并共享​​浏览器的登录状态，以便它可以访问您已登录的任何网站。

有关设置说明、完整功能列表以及故障排除，请参阅[将 Claude Code 与 Chrome 结合使用](./chrome)。

## VS Code 命令和快捷键

打开命令面板（Mac 上的 `Cmd+Shift+P` 或 Windows/Linux 上的 `Ctrl+Shift+P`）并键入“Claude Code”以查看 Claude Code 扩展的所有可用 VS Code 命令。某些快捷键取决于哪个面板“聚焦”（接收键盘输入）。当光标位于代码文件中时，编辑器将获得焦点。当光标位于 Claude 的提示框中时，Claude 获得焦点。使用 `Cmd+Esc` / `Ctrl+Esc` 在它们之间切换。

**注意**

这些是用于控制扩展的 VS Code 命令。并非所有内置 Claude Code 命令都在扩展中可用。有关详细信息，请参阅 [VS Code 扩展与 Claude Code CLI](#vs-code-extension-vs-claude-code-cli)。

|命令|快捷方式|描述 |
| -------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
|焦点输入| `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux) |在编辑器和 Claude 之间切换焦点 |
|在侧边栏打开 | - |在左侧边栏中打开 Claude |
|在终端中打开 | - |在终端模式下打开Claude |
|在新选项卡中打开 | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) |作为编辑器选项卡打开新对话 |
|在新窗口中打开 | - |在单独的窗口中打开新对话 |
|新对话 | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux) |开始新对话（需要 Claude 保持专注）|
|插入@-提及参考| `Option+K` (Mac) / `Alt+K` (Windows/Linux) |插入对当前文件和选择的引用（需要编辑器聚焦）|
|显示日志 | - |查看扩展调试日志 |
|退出 | - |退出您的 Anthropic 帐户 |

## 配置设置

该扩展有两种类型的设置：

* **VS Code 中的扩展设置**：控制 VS Code 中的扩展的行为。使用 `Cmd+,` (Mac) 或 `Ctrl+,` (Windows/Linux) 打开，然后转到扩展 → Claude Code。您还可以键入 `/` 并选择 **常规配置** 以打开设置。
* **`~/.claude/settings.json` 中的 Claude Code 设置**：在扩展和 CLI 之间共享。用于允许的命令、环境变量、挂钩和 MCP 服务器。有关详细信息，请参阅[设置](./settings)。

**提示**

将 `"$schema": "https://json.schemastore.org/claude-code-settings.json"` 添加到 `settings.json`，以便直接在 VS Code 中对所有可用设置进行自动完成和内联验证。### 扩展设置

|设置|默认|描述 |
| --------------------------------- | ---------| --------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel` | `default` |新对话的模型。使用 `/model` 更改每个会话。                                                    |
| `useTerminal` | `false` |以终端模式而不是图形面板启动 Claude |
| `initialPermissionMode` | `default` |控制审批提示：`default`（每次询问）、`plan`、`acceptEdits` 或 `bypassPermissions` |
| `preferredLocation` | `panel` | Claude 在哪里打开：`sidebar`（右）或 `panel`（新选项卡）|
| `autosave` | `true` |在 Claude 读取或写入文件之前自动保存文件 |
| `useCtrlEnterToSend` | `false` |使用 Ctrl/Cmd+Enter 而不是 Enter 发送提示 |
| `enableNewConversationShortcut` | `true` |启用 Cmd/Ctrl+N 开始新对话 |
| `hideOnboarding` | `false` |隐藏入职清单（毕业帽图标）|
| `respectGitIgnore` | `true` |从文件搜索中排除 .gitignore 模式 |
| `environmentVariables` | `[]` |设置Claude进程的环境变量。使用 Claude Code 设置代替共享配置。             |
| `disableLoginPrompt` | `false` |跳过身份验证提示（对于第三方提供商设置）|
| `allowDangerouslySkipPermissions` | `false` |绕过权限提示。 **使用时请格外小心。** 请参阅[权限模式](./permissions#permission-modes) |
| `claudeProcessWrapper` | - |用于启动Claude进程的可执行路径|

## VS Code 扩展与 Claude Code CLI

Claude Code 可用作 VS Code 扩展（图形面板）和 CLI（终端中的命令行界面）。某些功能仅在 CLI 中可用。如果您需要仅 CLI 功能，请在 VS Code 的集成终端中运行 `claude`。|特色 |命令行 | VS Code 扩展 |
| ------------------- | ------------------- | ------------------------------------------------------------------------------------------------ |
|命令与技能| [全部](./commands) |子集（输入 `/` 查看可用）|
| MCP 服务器配置 |是的 |部分（通过 CLI 添加服务器；在聊天面板中使用 `/mcp` 管理现有服务器）|
|检查站|是的 |是的 |
| `!` bash 快捷方式 |是的 |没有 |
|制表符补全 |是的 |没有 |

### 使用检查点倒带

VS Code 扩展支持检查点，可跟踪 Claude 的文件编辑并让您回退到之前的状态。将鼠标悬停在任何消息上即可显示快退按钮，然后从三个选项中进行选择：

* **从这里分叉对话**：从此消息开始一个新的对话分支，同时保持所有代码更改不变
* **将代码倒回到此处**：将文件更改恢复到对话中的这一点，同时保留完整的对话历史记录
* **分叉对话并倒回代码**：启动一个新的对话分支并将文件更改恢复到此时

有关检查点工作原理及其限制的完整详细信息，请参阅[检查点](./checkpointing)。

### 在 VS Code 中运行 CLI

要在 VS Code 中使用 CLI，请打开集成终端 (`` Ctrl+` `` on Windows/Linux or `` Cmd+` `` on Mac) and run `claude`。CLI 自动与您的 IDE 集成，以提供差异查看和诊断共享等功能。

如果使用外部终端，请在 Claude Code 内部运行 `/ide`，将其连接到 VS Code。

### 在扩展和 CLI 之间切换

分机和 CLI 共享相同的对话历史记录。要在 CLI 中继续分机对话，请在终端中运行 `claude --resume`。这将打开一个交互式选择器，您可以在其中搜索并选择您的对话。

### 在提示中包含终端输出

使用 `@terminal:name` 在提示中引用终端输出，其中 `name` 是终端的标题。这使 Claude 无需复制粘贴即可查看命令输出、错误消息或日志。

### 监控后台进程

当 Claude 运行长时间运行的命令时，扩展会在状态栏中显示进度。但是，与 CLI 相比，后台任务的可见性有限。为了获得更好的可见性，请让 Claude 输出命令，以便您可以在 VS Code 的集成终端中运行它。

### 使用 MCP 连接到外部工具

MCP (Model Context Protocol) 服务器使 Claude 能够访问外部工具、数据库和 API。

要添加 MCP 服务器，请打开集成终端 (`` Ctrl+` `` or `` Cmd+` ``) 并运行：

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

配置完成后，要求 Claude 使用这些工具（例如“查看 PR #456”）。要在不离开 VS Code 的情况下管理 MCP 服务器，请在聊天面板中键入 `/mcp`。 MCP 管理对话框允许您启用或禁用服务器、重新连接到服务器以及管理 OAuth 身份验证。有关可用服务器，请参阅 [MCP 文档](./mcp)。

## 使用 git

Claude Code 与 git 集成，可直接在 VS Code 中帮助完成版本控制工作流程。要求 Claude 提交更改、创建拉取请求或跨分支工作。

### 创建提交和拉取请求

Claude 可以根据您的工作暂存更改、编写提交消息并创建拉取请求：

```text
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

创建拉取请求时，Claude 会根据实际代码更改生成描述，并可以添加有关测试或实施决策的上下文。

### 使用 git 工作树进行并行任务

使用 `--worktree` (`-w`) 标志在具有自己的文件和分支的隔离工作树中启动 Claude：

```bash
claude --worktree feature-auth
```

每个工作树在共享 git 历史记录的同时维护独立的文件状态。这可以防止 Claude 实例在处理不同任务时相互干扰。有关更多详细信息，请参阅[使用 Git 工作树运行并行会话](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)。

## 使用第三方提供商

默认情况下，Claude Code 直接连接到 Anthropic 的 API。如果您的组织使用 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 来访问 Claude，请将扩展配置为使用您的提供商：

### 禁用登录提示

打开[禁用登录提示设置](vscode://settings/claudeCode.disableLoginPrompt)并选中该框。

您还可以打开 VS Code 设置（Mac 上的 `Cmd+,` 或 Windows/Linux 上的 `Ctrl+,`），搜索“Claude Code 登录”，然后选中 **禁用登录提示**。

  
### 配置您的提供商

请遵循您的提供商的设置指南：

* [Amazon Bedrock 上的 Claude Code](./amazon-bedrock)
* [Claude Code 于 Google Vertex AI](./google-vertex-ai)
* [Claude Code 于 Microsoft Foundry](./microsoft-foundry)

这些指南涵盖了在 `~/.claude/settings.json` 中配置您的提供程序，这可确保您的设置在 VS Code 扩展和 CLI 之间共享。

## 安全和隐私

您的代码保持私密。 Claude Code 处理您的代码以提供帮助，但不使用它来训练模型。有关数据处理以及如何选择退出日志记录的详细信息，请参阅[数据和隐私](./data-usage)。

启用自动编辑权限后，Claude Code 可以修改 VS Code 可以自动执行的 VS Code 配置文件（例如 `settings.json` 或 `tasks.json`）。要降低使用不受信任的代码时的风险：

* 为不受信任的工作区启用 [VS Code 限制模式](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode)
* 使用手动批准模式而不是自动接受编辑
* 在接受变更之前仔细审查变更

## 修复常见问题

### 扩展程序无法安装

* 确保您有兼容版本的 VS Code（1.98.0 或更高版本）
* 检查VS Code是否有安装扩展的权限
* 尝试直接从 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) 安装

### Spark 图标不可见

当您打开文件时，Spark 图标会出现在**编辑器工具栏**（编辑器的右上角）中。如果您没有看到它：1. **打开文件**：该图标需要打开文件。仅打开一个文件夹是不够的。
2. **检查VS Code版本**：需要1.98.0或更高版本（帮助→关于）
3. **重新启动 VS Code**：从命令面板运行“开发人员：重新加载窗口”
4. **禁用冲突的扩展**：暂时禁用其他AI扩展（Cline、Continue等）
5. **检查工作区信任**：扩展在受限模式下不起作用

或者，单击 **状态栏**（右下角）中的“✱ Claude Code”。即使没有打开文件，这也可以工作。您还可以使用 **命令面板** (`Cmd+Shift+P` / `Ctrl+Shift+P`) 并输入“Claude Code”。

### Claude Code 从不回应

如果 Claude Code 没有响应您的提示：

1. **检查您的互联网连接**：确保您有稳定的互联网连接
2. **开始新对话**：尝试开始新对话以查看问题是否仍然存在
3. **尝试 CLI**：从终端运行 `claude` 以查看是否收到更详细的错误消息

如果问题仍然存在，请[在 GitHub 上提交问题](https://github.com/anthropics/claude-code/issues)，并提供有关错误的详细信息。

## 卸载扩展

要卸载 Claude Code 扩展：

1. 打开扩展视图（Mac 上的 `Cmd+Shift+X` 或 Windows/Linux 上的 `Ctrl+Shift+X`）
2. 搜索“Claude Code”
3. 单击“**卸载**”

要同时删除扩展数据并重置所有设置：

```bash
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

如需其他帮助，请参阅[故障排除指南](./troubleshooting)。

## 后续步骤

现在您已在 VS Code 中设置了 Claude Code：

* [探索常见工作流程](./common-workflows) 以充分利用 Claude Code
* [设置 MCP 服务器](./mcp)，通过外部工具扩展 Claude 的功能。使用 CLI 添加服务器，然后在聊天面板中使用 `/mcp` 进行管理。
* [配置 Claude Code 设置](./settings) 自定义允许的命令、挂钩等。这些设置在扩展和 CLI 之间共享。
