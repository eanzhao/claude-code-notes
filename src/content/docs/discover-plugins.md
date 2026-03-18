---
title: "通过市场发现并安装预构建的插件"
order: 23
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "从市场查找并安装插件，以使用新命令、代理和功能扩展 Claude Code。"
sourceUrl: "https://code.claude.com/docs/en/discover-plugins.md"
sourceTitle: "Discover and install prebuilt plugins through marketplaces"
tags: []
---
# 通过市场发现并安装预构建插件

> 从市场查找并安装插件，以使用新命令、代理和功能扩展 Claude Code。

插件通过技能、代理、挂钩和 MCP 服务器扩展 Claude Code。插件市场是帮助您发现和安装这些扩展的目录，而无需您自己构建它们。

想要创建和分销您自己的市场？请参阅[创建和分发插件市场](./plugin-marketplaces)。

## 市场如何运作

市场是其他人创建和共享的插件目录。使用市场的过程分为两步：

### 添加市场

这会将目录注册到 Claude Code，以便您可以浏览可用的内容。尚未安装任何插件。

  
### 安装单独的插件

浏览目录并安装您想要的插件。

可以将其想象为添加应用程序商店：添加商店使您可以浏览其集合，但您仍然可以选择单独下载哪些应用程序。

## Anthropic 官方市场

当您启动 Claude Code 时，官方 Anthropic 市场 (`claude-plugins-official`) 将自动可用。运行 `/plugin` 并转到 **发现** 选项卡以浏览可用的内容。

要从官方市场安装插件：

```shell
/plugin install plugin-name@claude-plugins-official
```

**注意**

官方市场由 Anthropic 维护。要将插件提交到官方市场，请使用应用内提交表单之一：

* **Claude.ai**：[claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **控制台**：[platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

要独立分发插件，请[创建您自己的市场](./plugin-marketplaces) 并与用户共享。

官方市场包括几类插件：

### 代码智能

代码智能插件启用 Claude Code 的内置 LSP 工具，使 Claude 能够在编辑后立即跳转到定义、查找引用并查看类型错误。这些插件配置[语言服务器协议](https://microsoft.github.io/language-server-protocol/) 连接，这与支持 VS Code 代码智能的技术相同。

这些插件需要在您的系统上安装语言服务器二进制文件。如果您已经安装了语言服务器，当您打开项目时，Claude可能会提示您安装相应的插件。

|语言 |插件 |需要二进制 |
| :--------- | :------------------ | :---------------------------- |
| C/C++ | `clangd-lsp` | `clangd` |
| C# | `csharp-lsp` | `csharp-ls` |
|去 | `gopls-lsp` | `gopls` |
|爪哇 | `jdtls-lsp` | `jdtls` |
|科特林 | `kotlin-lsp` | `kotlin-language-server` |
|卢阿 | `lua-lsp` | `lua-language-server` |
| PHP | `php-lsp` | `intelephense` |
|蟒蛇 | `pyright-lsp` | `pyright-langserver` |
|铁锈| `rust-analyzer-lsp` | `rust-analyzer` |
|斯威夫特 | `swift-lsp` | `sourcekit-lsp` |
|打字稿 | `typescript-lsp` | `typescript-language-server` |您还可以为其他语言[创建您自己的 LSP 插件](./plugins-reference#lsp-servers)。

**注意**

如果安装插件后在 `/plugin` 错误选项卡中看到 `Executable not found in $PATH`，请安装上表中所需的二进制文件。

#### Claude 从代码智能插件中获得什么

安装代码智能插件并且其语言服务器二进制文件可用后，Claude 获得两项功能：

* **自动诊断**：Claude 进行每次文件编辑后，语言服务器都会分析更改并自动报告错误和警告。 Claude 无需运行编译器或 linter 即可发现类型错误、缺少导入和语法问题。如果 Claude 出现错误，它会立即注意到并修复该问题。除了安装插件之外，不需要任何配置。当“找到诊断”指示器出现时，您可以通过按 **Ctrl+O** 来查看内联诊断。
* **代码导航**：Claude 可以使用语言服务器跳转到定义、查找引用、在悬停时获取类型信息、列出符号、查找实现以及跟踪调用层次结构。这些操作为 Claude 提供比基于 grep 的搜索更精确的导航，但可用性可能因语言和环境而异。

如果遇到问题，请参阅[代码智能故障排除](#code-intelligence-issues)。

### 外部集成

这些插件捆绑了预配置的 [MCP 服务器](./mcp)，因此您可以将 Claude 连接到外部服务，而无需手动设置：

* **源代码控制**：`github`、`gitlab`
* **项目管理**：`atlassian`（Jira/Confluence）、`asana`、`linear`、`notion`
* **设计**：`figma`
* **基础设施**：`vercel`、`firebase`、`supabase`
* **通讯**：`slack`
* **监控**：`sentry`

### 开发工作流程

为常见开发任务添加命令和代理的插件：

* **commit-commands**：Git 提交工作流程，包括提交、推送和 PR 创建
* **pr-review-toolkit**：用于审查拉取请求的专业代理
* **agent-sdk-dev**：用于使用 Claude 进行构建的工具 Agent SDK
* **plugin-dev**：用于创建自己的插件的工具包

### 输出样式

自定义 Claude 的响应方式：

* **解释性输出风格**：关于实施选择的教育见解
**学习输出风格**：用于技能培养的交互式学习模式

## 尝试一下：添加演示市场

Anthropic 还维护一个[演示插件市场](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`)，其中包含示例插件，展示插件系统的可能性。与官方市场不同，您需要手动添加此市场。

### 添加市场

从 Claude Code 中，运行 `anthropics/claude-code` 市场的 `plugin marketplace add` 命令：

```shell
/plugin marketplace add anthropics/claude-code
```

这将下载市场目录并使其插件可供您使用。

  
### 浏览可用插件

运行 `/plugin` 打开插件管理器。这将打开一个带有四个选项卡的选项卡式界面，您可以使用 **Tab** （或 **Shift+Tab** 向后退）循环浏览：* **发现**：浏览所有市场中的可用插件
* **已安装**：查看和管理您已安装的插件
* **市场**：添加、删除或更新您添加的市场
* **错误**：查看任何插件加载错误

转到 **发现** 选项卡以查看您刚刚添加的市场中的插件。

  
### 安装插件

选择一个插件以查看其详细信息，然后选择安装范围：

* **用户范围**：在所有项目中为您自己安装
* **项目范围**：为此存储库上的所有协作者安装
* **本地范围**：仅在此存储库中为您自己安装

例如，选择 **commit-commands** （一个添加 git 工作流程命令的插件）并将其安装到您的用户范围。

您也可以直接从命令行安装：

```shell
/plugin install commit-commands@anthropics-claude-code
```

请参阅[配置范围](./settings#configuration-scopes) 了解有关范围的更多信息。

  
### 使用你的新插件

安装后，运行 `/reload-plugins` 激活插件。插件命令由插件名称命名，因此 **commit-commands** 提供诸如 `/commit-commands:commit` 之类的命令。

通过更改文件并运行来尝试一下：

```shell
/commit-commands:commit
```

这会暂存您的更改、生成提交消息并创建提交。

每个插件的工作方式都不同。检查 **发现** 选项卡或其主页中的插件描述，以了解它提供的命令和功能。

本指南的其余部分涵盖了添加市场、安装插件和管理配置的所有方法。

## 添加市场

使用 `/plugin marketplace add` 命令添加来自不同来源的市场。

**提示**

**快捷方式**：您可以使用 `/plugin market` 代替 `/plugin marketplace`，使用 `rm` 代替 `remove`。

* **GitHub 存储库**：`owner/repo` 格式（例如 `anthropics/claude-code`）
* **Git URL**：任何 git 存储库 URL（GitLab、Bitbucket、自托管）
* **本地路径**：`marketplace.json` 文件的目录或直接路径
* **远程 URL**：托管 `marketplace.json` 文件的直接 URL

### 从 GitHub 添加

添加包含使用 `owner/repo` 格式的 `.claude-plugin/marketplace.json` 文件的 GitHub 存储库，其中 `owner` 是 GitHub 用户名或组织，`repo` 是存储库名称。

例如，`anthropics/claude-code` 指的是 `anthropics` 拥有的 `claude-code` 存储库：

```shell
/plugin marketplace add anthropics/claude-code
```

### 从其他 Git 主机添加

通过提供完整的 URL 添加任何 git 存储库。这适用于任何 Git 主机，包括 GitLab、Bitbucket 和自托管服务器：

使用 HTTPS：

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git
```

使用 SSH：

```shell
/plugin marketplace add git@gitlab.com:company/plugins.git
```

要添加特定分支或标签，请附加 `#`，后跟 ref：

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### 从本地路径添加

添加包含 `.claude-plugin/marketplace.json` 文件的本地目录：

```shell
/plugin marketplace add ./my-marketplace
```

您还可以添加 `marketplace.json` 文件的直接路径：

```shell
/plugin marketplace add ./path/to/marketplace.json
```

### 从远程 URL 添加

通过 URL 添加远程 `marketplace.json` 文件：

```shell
/plugin marketplace add https://example.com/marketplace.json
```

**注意**

与基于 Git 的市场相比，基于 URL 的市场有一些限制。如果您在安装插件时遇到“路径未找到”错误，请参阅[疑难解答](./plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)。

## 安装插件

添加市场后，您可以直接安装插件（默认安装到用户范围）：

```shell
/plugin install plugin-name@marketplace-name
```要选择不同的[安装范围](./settings#configuration-scopes)，请使用交互式 UI：运行 `/plugin`，转到 **发现** 选项卡，然后在插件上按 **Enter**。您将看到以下选项：

* **用户范围**（默认）：在所有项目中为您自己安装
* **项目范围**：为此存储库上的所有协作者安装（添加到 `.claude/settings.json`）
* **本地范围**：仅在此存储库中为您自己安装（不与协作者共享）

您还可能会看到具有 **托管** 范围的插件 - 这些插件由管理员通过 [托管设置](./settings#settings-files) 安装，并且无法修改。

运行 `/plugin` 并转到 **已安装** 选项卡以查看按范围分组的插件。

**警告**

在安装插件之前，请确保您信任该插件。 Anthropic 无法控制插件中包含的 MCP 服务器、文件或其他软件，也无法验证它们是否按预期工作。检查每个插件的主页以获取更多信息。

## 管理已安装的插件

运行 `/plugin` 并转到 **已安装** 选项卡以查看、启用、禁用或卸载您的插件。键入以按插件名称或描述过滤列表。

您还可以使用直接命令管理插件。

禁用插件而不卸载：

```shell
/plugin disable plugin-name@marketplace-name
```

重新启用已禁用的插件：

```shell
/plugin enable plugin-name@marketplace-name
```

完全删除插件：

```shell
/plugin uninstall plugin-name@marketplace-name
```

`--scope` 选项允许您使用 CLI 命令定位特定范围：

```shell
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### 应用插件更改而不重新启动

当您在会话期间安装、启用或禁用插件时，运行 `/reload-plugins` 以获取所有更改而无需重新启动：

```shell
/reload-plugins
```

Claude Code 重新加载所有活动插件，并显示重新加载的命令、技能、代理、挂钩、插件 MCP 服务器和插件 LSP 服务器的计数。

## 管理市场

您可以通过交互式 `/plugin` 界面或使用 CLI 命令来管理市场。

### 使用交互界面

运行 `/plugin` 并转到 **Marketplaces** 选项卡以：

* 查看您添加的所有市场及其来源和状态
* 添加新市场
* 更新市场列表以获取最新的插件
* 删除您不再需要的市场

### 使用 CLI 命令

您还可以使用直接命令管理市场。

列出所有配置的市场：

```shell
/plugin marketplace list
```

从市场刷新插件列表：

```shell
/plugin marketplace update marketplace-name
```

删除市场：

```shell
/plugin marketplace remove marketplace-name
```

**警告**

删除市场将卸载您从其中安装的所有插件。

### 配置自动更新

Claude Code 可以在启动时自动更新市场及其安装的插件。当为市场启用自动更新时，Claude Code 会刷新市场数据并将已安装的插件更新到最新版本。如果更新了任何插件，您将看到一条通知，提示您运行 `/reload-plugins`。

通过 UI 切换各个市场的自动更新：

1. 运行`/plugin`打开插件管理器
2. 选择**市场**
3. 从列表中选择一个市场
4. 选择**启用自动更新**或**禁用自动更新**

官方 Anthropic 市场默认启用自动更新。第三方和本地开发市场默认禁用自动更新。要完全禁用 Claude Code 和所有插件的所有自动更新，请设置 `DISABLE_AUTOUPDATER` 环境变量。有关详细信息，请参阅[自动更新](./setup#auto-updates)。

要在禁用 Claude Code 自动更新的同时保持插件自动更新处于启用状态，请设置 `FORCE_AUTOUPDATE_PLUGINS=true` 和 `DISABLE_AUTOUPDATER`：

```shell
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

当您想要手动管理 Claude Code 更新但仍接收自动插件更新时，这非常有用。

## 配置团队市场

团队管理员可以通过将市场配置添加到 `.claude/settings.json` 来为项目设置自动市场安装。当团队成员信任存储库文件夹时，Claude Code 会提示他们安装这些市场和插件。

将 `extraKnownMarketplaces` 添加到项目的 `.claude/settings.json` 中：

```json
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

有关包括 `extraKnownMarketplaces` 和 `enabledPlugins` 在内的完整配置选项，请参阅[插件设置](./settings#plugin-settings)。

## 安全

插件和市场是高度可信的组件，可以使用您的用户权限在您的计算机上执行任意代码。仅安装插件并从您信任的来源添加市场。组织可以使用[托管市场限制](./plugin-marketplaces#managed-marketplace-restrictions) 来限制允许用户添加哪些市场。

## 故障排除

### /plugin 命令无法识别

如果您看到“未知命令”或 `/plugin` 命令未出现：

1. **检查您的版本**：运行 `claude --version`。插件需要 1.0.33 或更高版本。
2. **更新Claude Code**：
   * **Homebrew**：`brew upgrade claude-code`
   * **npm**：`npm update -g @anthropic-ai/claude-code`
   * **本机安装程序**：从 [安装程序](./setup) 重新运行安装命令
3. **重新启动 Claude Code**：更新后，重新启动终端并再次运行 `claude`。

### 常见问题

* **市场未加载**：验证 URL 是否可访问以及路径中是否存在 `.claude-plugin/marketplace.json`
* **插件安装失败**：检查插件源 URL 是否可访问且存储库是否公开（或者您有权访问）
* **安装后找不到文件**：插件被复制到缓存，因此引用插件目录之外的文件的路径将不起作用
* **插件技能不出现**：用`rm -rf ~/.claude/plugins/cache`清除缓存，重新启动Claude Code，然后重新安装插件。

有关详细的故障排除解决方案，请参阅市场指南中的[故障排除](./plugin-marketplaces#troubleshooting)。调试工具请参见[调试和开发工具](./plugins-reference#debugging-and-development-tools)。

### 代码情报问题

* **语言服务器未启动**：验证二进制文件是否已安装并且在 `$PATH` 中可用。有关详细信息，请检查 `/plugin` 错误选项卡。
* **高内存使用率**：`rust-analyzer` 和 `pyright` 等语言服务器可能会在大型项目中消耗大量内存。如果您遇到内存问题，请使用 `/plugin disable ` 禁用该插件，并改用 Claude 的内置搜索工具。
* **单一存储库中的误报诊断**：如果工作区配置不正确，语言服务器可能会报告内部包未解决的导入错误。这些不会影响 Claude 编辑代码的能力。

## 后续步骤* **构建您自己的插件**：请参阅 [插件](./plugins) 创建技能、代理和挂钩
* **创建市场**：请参阅[创建插件市场](./plugin-marketplaces) 将插件分发给您的团队或社区
* **技术参考**：完整规格请参阅[插件参考](./plugins-reference)
