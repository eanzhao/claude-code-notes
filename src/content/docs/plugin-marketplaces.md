---
title: "创建和分发插件市场"
order: 47
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "构建和托管插件市场以跨团队和社区分发 Claude Code 扩展。"
sourceUrl: "https://code.claude.com/docs/en/plugin-marketplaces.md"
sourceTitle: "Create and distribute a plugin marketplace"
tags: []
---
# 创建并分发插件市场

> 构建和托管插件市场，以跨团队和社区分发 Claude Code 扩展。

**插件市场**是一个目录，可让您将插件分发给其他人。市场提供集中发现、版本跟踪、自动更新以及对多种源类型（git 存储库、本地路径等）的支持。本指南向您展示如何创建自己的市场以与您的团队或社区共享插件。

想要从现有市场安装插件？请参阅[发现并安装预建插件](./discover-plugins)。

## 概述

创建和分发市场涉及：

1. **创建插件**：使用命令、代理、挂钩、MCP 服务器或 LSP 服务器构建一个或多个插件。本指南假设您已经有要分发的插件；有关如何创建插件的详细信息，请参阅[创建插件](./plugins)。
2. **创建市场文件**：定义一个 `marketplace.json`，其中列出您的插件以及在哪里可以找到它们（请参阅[创建市场文件](#create-the-marketplace-file)）。
3. **托管市场**：推送到 GitHub、GitLab 或其他 git 主机（请参阅[托管和分发市场](#host-and-distribute-marketplaces)）。
4. **与用户共享**：用户使用 `/plugin marketplace add` 添加您的市场并安装各个插件（请参阅[发现并安装插件](./discover-plugins)）。

一旦您的市场上线，您可以通过将更改推送到存储库来更新它。用户使用 `/plugin marketplace update` 刷新其本地副本。

## 演练：创建本地市场

此示例使用一个插件创建一个市场：用于代码审查的 `/quality-review` 技能。您将创建目录结构、添加技能、创建插件清单和市场目录，然后安装并测试它。

### 创建目录结构

```bash
mkdir -p my-marketplace/.claude-plugin
mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
```

  
### 创建技能

创建 `SKILL.md` 文件来定义 `/quality-review` 技能的用途。

```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md
---
description: Review code for bugs, security, and performance
disable-model-invocation: true
---

Review the code I've selected or the recent changes for:
- Potential bugs or edge cases
- Security concerns
- Performance issues
- Readability improvements

Be concise and actionable.
```

  
### 创建插件清单

创建描述该插件的 `plugin.json` 文件。该清单位于 `.claude-plugin/` 目录中。

```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json
{
  "name": "quality-review-plugin",
  "description": "Adds a /quality-review skill for quick code reviews",
  "version": "1.0.0"
}
```

  
### 创建市场文件

创建列出您的插件的市场目录。

```json my-marketplace/.claude-plugin/marketplace.json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "quality-review-plugin",
      "source": "./plugins/quality-review-plugin",
      "description": "Adds a /quality-review skill for quick code reviews"
    }
  ]
}
```

  
### 添加并安装

添加市场并安装插件。

```shell
/plugin marketplace add ./my-marketplace
/plugin install quality-review-plugin@my-plugins
```

  
### 尝试一下

在编辑器中选择一些代码并运行新命令。

```shell
/review
```

要详细了解插件的功能（包括挂钩、代理、MCP 服务器和 LSP 服务器），请参阅[插件](./plugins)。

**注意**

**如何安装插件**：当用户安装插件时，Claude Code 会将插件目录复制到缓存位置。这意味着插件无法使用 `../shared-utils` 等路径引用其目录之外的文件，因为这些文件不会被复制。

如果您需要跨插件共享文件，请使用符号链接（在复制过程中遵循）。有关详细信息，请参阅[插件缓存和文件解析](./plugins-reference#plugin-caching-and-file-resolution)。

## 创建市场文件

在存储库根目录中创建 `.claude-plugin/marketplace.json`。该文件定义您的市场名称、所有者信息以及插件及其来源的列表。每个插件条目至少需要 `name` 和 `source`（从哪里获取）。有关所有可用字段，请参阅下面的[完整架构](#marketplace-schema)。

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## 市场架构

### 必填字段

|领域 |类型 |描述 |示例|
| :-------- | :-----| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `name` |字符串|市场标识符（短横线大小写，无空格）。这是面向公众的：用户在安装插件时会看到它（例如，`/plugin install my-tool@your-marketplace`）。 | `"acme-tools"` |
| `owner` |对象|市场维护者信息（[参见下面的字段](#owner-fields)）|                |
| `plugins` |数组|可用插件列表 |见下文 |

**注意**

**保留名称**：以下市场名称保留供 Anthropic 官方使用，第三方市场不能使用：`claude-code-marketplace`、`claude-code-plugins`、`claude-plugins-official`、`anthropic-marketplace`、`anthropic-plugins`、`agent-skills`、`life-sciences`。冒充官方市场的名称（例如 `official-claude-plugins` 或 `anthropic-tools-v2`）也会被屏蔽。

### 所有者字段

|领域 |类型 |必填|描述 |
| :------ | :-----| :----- | :-------------------------------- |
| `name` |字符串|是的 |维护者或团队的名称 |
| `email` |字符串|没有 |维护者的联系电子邮件 |

### 可选元数据

|领域 |类型 |描述 |
| :-------------------- | :-----| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` |字符串|市场简要描述|
| `metadata.version` |字符串|市场版 |
| `metadata.pluginRoot` |字符串|前缀为相对插件源路径的基目录（例如，`"./plugins"` 允许您编写 `"source": "formatter"` 而不是 `"source": "./plugins/formatter"`）|

## 插件条目`plugins` 数组中的每个插件条目都描述了一个插件以及在哪里可以找到它。您可以包含 [插件清单架构](./plugins-reference#plugin-manifest-schema) 中的任何字段（例如 `description`、`version`、`author`、`commands`、`hooks` 等），以及这些市场特定的字段：`source`、`category`、 `tags` 和 `strict`。

### 必填字段

|领域 |类型 |描述 |
| :----- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` |字符串|插件标识符（短横线大小写，无空格）。这是面向公众的：用户在安装时会看到它（例如，`/plugin install my-plugin@marketplace`）。 |
| `source` |字符串\|对象|从哪里获取插件（请参阅下面的[插件来源](#plugin-sources)）|

### 可选插件字段

**标准元数据字段：**

|领域 |类型 |描述 |
| :------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description` |字符串|插件简介 |
| `version` |字符串|插件版本 |
| `author` |对象|插件作者信息（`name` 必需，`email` 可选）|
| `homepage` |字符串|插件主页或文档 URL |
| `repository` |字符串|源代码存储库 URL |
| `license` |字符串| SPDX 许可证标识符（例如 MIT、Apache-2.0）|
| `keywords` |数组|插件发现和分类标签 |
| `category` |字符串|组织的插件类别 |
| `tags` |数组|可搜索性标签 |
| `strict` |布尔 |控制 `plugin.json` 是否是组件定义的权限（默认值：true）。请参阅下面的[严格模式](#strict-mode)。 |

**组件配置字段：**|领域 |类型 |描述 |
| ：---------- | :------------- | :------------------------------------------------------------ |
| `commands` |字符串\|数组|命令文件或目录的自定义路径 |
| `agents` |字符串\|数组|代理文件的自定义路径 |
| `hooks` |字符串\|对象|自定义钩子配置或钩子文件路径 |
| `mcpServers` |字符串\|对象| MCP 服务器配置或 MCP 配置路径 |
| `lspServers` |字符串\|对象| LSP 服务器配置或 LSP 配置路径 |

## 插件来源

插件源告诉 Claude Code 在哪里获取市场中列出的每个单独的插件。这些设置在 `marketplace.json` 中每个插件条目的 `source` 字段中。

一旦插件被克隆或复制到本地计算机中，它就会被复制到位于 `~/.claude/plugins/cache` 的本地版本化插件缓存中。

|来源 |类型 |领域 |笔记|
| ------------- | ------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
|相对路径| `string`（例如 `"./my-plugin"`）| — |市场存储库中的本地目录。必须以 `./` 开头 |
| `github` |对象| `repo`、`ref?`、`sha?` |                                                                                     |
| `url` |对象| `url`、`ref?`、`sha?` | Git URL 来源 |
| `git-subdir` |对象| `url`、`path`、`ref?`、`sha?` | git 存储库中的子目录。稀疏克隆以最大限度地减少 monorepos 的带宽 |
| `npm` |对象| `package`、`version?`、`registry?` |通过 `npm install` 安装 |
| `pip` |对象| `package`、`version?`、`registry?` |通过 pip 安装 |

**注意**

**市场源与插件源**：这些是控制不同事物的不同概念。

* **市场来源** — 从哪里获取 `marketplace.json` 目录本身。当用户运行 `/plugin marketplace add` 时或在 `extraKnownMarketplaces` 设置中进行设置。支持 `ref`（分支/标签），但不支持 `sha`。
* **插件源** — 从哪里获取市场中列出的单个插件。在 `marketplace.json` 内每个插件条目的 `source` 字段中设置。支持 `ref`（分支/标签）和 `sha`（精确提交）。

例如，在 `acme-corp/plugin-catalog`（市场源）托管的市场可以列出从 `acme-corp/code-formatter`（插件源）获取的插件。市场源和插件源指向不同的存储库并独立固定。

### 相对路径对于同一存储库中的插件，请使用以 `./` 开头的路径：

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

路径相对于市场根目录进行解析，该根目录是包含 `.claude-plugin/` 的目录。在上面的示例中，`./plugins/my-plugin` 指向 `<repo>/plugins/my-plugin`，尽管 `marketplace.json` 位于 `<repo>/.claude-plugin/marketplace.json`。请勿使用 `../` 爬出 `.claude-plugin/`。

**注意**

仅当用户通过 Git（GitHub、GitLab 或 git URL）添加您的市场时，相对路径才有效。如果用户通过直接 URL 将您的市场添加到 `marketplace.json` 文件，则相对路径将无法正确解析。对于基于 URL 的分发，请改用 GitHub、npm 或 git URL 源。有关详细信息，请参阅[故障排除](#plugins-with-relative-paths-fail-in-url-based-marketplaces)。

### GitHub 存储库

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

您可以固定到特定分支、标签或提交：

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

|领域 |类型 |描述 |
| :-----| :-----| :-------------------------------------------------------------------- |
| `repo` |字符串|必需的。 GitHub 存储库采用 `owner/repo` 格式 |
| `ref` |字符串|选修的。 Git 分支或标签（默认为存储库默认分支）|
| `sha` |字符串|选修的。完整的 40 个字符 git commit SHA 以固定到确切的版本 |

### Git 存储库

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

您可以固定到特定分支、标签或提交：

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

|领域|类型 |描述 |
| :----| :-----| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` |字符串|必需的。完整的 git 存储库 URL（`https://` 或 `git@`）。 `.git` 后缀是可选的，因此没有后缀的 Azure DevOps 和 AWS CodeCommit URL 也可以工作 |
| `ref` |字符串|选修的。 Git 分支或标签（默认为存储库默认分支） |
| `sha` |字符串|选修的。完整的 40 个字符 git commit SHA 以固定到确切的版本 |

### Git 子目录

使用 `git-subdir` 指向 git 存储库子目录中的插件。 Claude Code 使用稀疏的部分克隆来仅获取子目录，从而最大限度地减少大型 monorepos 的带宽。

```json
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

您可以固定到特定分支、标签或提交：

```json
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

`url` 字段还接受 GitHub 简写 (`owner/repo`) 或 SSH URL (`git@github.com:owner/repo.git`)。|领域 |类型 |描述 |
| :-----| :-----| :------------------------------------------------------------------------------------------------------------------------ |
| `url` |字符串|必需的。 Git 存储库 URL、GitHub `owner/repo` 简写或 SSH URL |
| `path` |字符串|必需的。包含插件的存储库中的子目录路径（例如，`"tools/claude-plugin"`）|
| `ref` |字符串|选修的。 Git 分支或标签（默认为存储库默认分支） |
| `sha` |字符串|选修的。完整的 40 个字符 git commit SHA 以固定到确切的版本 |

### npm 包

作为 npm 包分发的插件使用 `npm install` 安装。这适用于公共 npm 注册表或您的团队托管的私有注册表中的任何包。

```json
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

要固定到特定版本，请添加 `version` 字段：

```json
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

要从私人或内部注册表安装，请添加 `registry` 字段：

```json
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

|领域 |类型 |描述 |
| :--------- | :-----| :-------------------------------------------------------------------------------------------------------- |
| `package` |字符串|必需的。包名称或范围包（例如，`@org/plugin`）|
| `version` |字符串|选修的。版本或版本范围（例如 `2.1.0`、`^2.0.0`、`~1.5.0`）|
| `registry` |字符串|选修的。自定义 npm 注册表 URL。默认为系统 npm 注册表（通常为 npmjs.org）|

### 高级插件条目

此示例显示了使用许多可选字段的插件条目，包括命令、代理、挂钩和 MCP 服务器的自定义路径：

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

需要注意的关键事项：

* **`commands` 和 `agents`**：您可以指定多个目录或单个文件。路径是相对于插件根目录的。
* **`${CLAUDE_PLUGIN_ROOT}`**：在挂钩和 MCP 服务器配置中使用此变量来引用插件安装目录中的文件。这是必要的，因为插件在安装时会复制到缓存位置。对于应在插件更新中保留的依赖项或状态，请改用 [`${CLAUDE_PLUGIN_DATA}`](./plugins-reference#persistent-data-directory)。
* **`strict: false`**：由于此设置为 false，因此该插件不需要自己的 `plugin.json`。市场准入决定了一切。请参阅下面的[严格模式](#strict-mode)。

### 严格模式

`strict` 字段控制 `plugin.json` 是否是组件定义（命令、代理、挂钩、技能、MCP 服务器、输出样式）的权限。|价值|行为 |
| ：-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true`（默认）| `plugin.json`是权威。市场入口可以用额外的组件来补充它，并且两个来源被合并。                                 |
| `false` |市场进入就是整个定义。如果插件还具有声明组件的 `plugin.json`，则存在冲突并且插件无法加载。 |

**何时使用每种模式：**

* **`strict: true`**：该插件有自己的 `plugin.json` 并管理自己的组件。市场条目可以在顶部添加额外的命令或挂钩。这是默认设置，适用于大多数插件。
* **`strict: false`**：市场运营商想要完全控制。插件存储库提供原始文件，市场条目定义哪些文件作为命令、代理、挂钩等公开。当市场以与插件作者预期不同的方式重组或管理插件组件时非常有用。

## 托管和分发市场

### GitHub 上的主机（推荐）

GitHub提供了最简单的分发方法：

1. **创建存储库**：为您的市场设置新的存储库
2. **添加市场文件**：使用您的插件定义创建 `.claude-plugin/marketplace.json`
3. **与团队共享**：用户使用 `/plugin marketplace add owner/repo` 添加您的市场

**优点**：内置版本控制、问题跟踪和团队协作功能。

### 托管在其他 git 服务上

任何 git 托管服务都可以使用，例如 GitLab、Bitbucket 和自托管服务器。用户添加完整的存储库 URL：

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### 私有存储库

Claude Code 支持从私有存储库安装插件。对于手动安装和更新，Claude Code 使用您现有的 git 凭据帮助程序。如果 `git clone` 适用于您终端中的私有存储库，那么它也适用于 Claude Code。常见的凭据帮助程序包括 GitHub 的 `gh auth login`、macOS 钥匙串和 `git-credential-store`。

后台自动更新在启动时运行，无需凭据帮助程序，因为交互式提示会阻止 Claude Code 启动。要为私人市场启用自动更新，请在您的环境中设置适当的身份验证令牌：

|供应商|环境变量|笔记|
| :-------- | :---------------------------- | :---------------------------------------- |
| GitHub | `GITHUB_TOKEN` 或 `GH_TOKEN` |个人访问令牌或 GitHub 应用程序令牌 |
| GitLab | `GITLAB_TOKEN` 或 `GL_TOKEN` |个人访问令牌或项目令牌 |
|比特桶 | `BITBUCKET_TOKEN` |应用程序密码或存储库访问令牌 |

在 shell 配置中设置令牌（例如 `.bashrc`、`.zshrc`）或在运行 Claude Code 时传递它：

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**注意**对于 CI/CD 环境，将令牌配置为秘密环境变量。 GitHub Actions 自动为同一组织中的存储库提供 `GITHUB_TOKEN`。

### 分发前在本地测试

共享之前在本地测试您的市场：

```shell
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

有关完整的添加命令（GitHub、Git URL、本地路径、远程 URL），请参阅[添加市场](./discover-plugins#add-marketplaces)。

### 需要为您的团队提供市场

您可以配置存储库，以便团队成员在信任项目文件夹时自动提示安装您的市场。将您的市场添加到 `.claude/settings.json`：

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

您还可以指定默认情况下应启用哪些插件：

```json
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

有关完整配置选项，请参阅[插件设置](./settings#plugin-settings)。

### 为容器预填充插件

对于容器映像和 CI 环境，您可以在构建时预先填充插件目录，以便 Claude Code 从可用的市场和插件启动，而无需在运行时克隆任何内容。将 `CLAUDE_CODE_PLUGIN_SEED_DIR` 环境变量设置为指向此目录。

种子目录反映了 `~/.claude/plugins` 的结构：

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>//<version>/...
```

构建种子目录的最简单方法是在映像构建期间运行 Claude Code 一次，安装所需的插件，然后将生成的 `~/.claude/plugins` 目录复制到映像中并将 `CLAUDE_CODE_PLUGIN_SEED_DIR` 指向它。

启动时，Claude Code 会将种子 `known_marketplaces.json` 中找到的市场注册到主要配置中，并使用在 `cache/` 下找到的插件缓存，无需重新克隆。这适用于带有 `-p` 标志的交互模式和非交互模式。

行为详情：

* **只读**：种子目录永远不会被写入。种子市场的自动更新被禁用，因为 git pull 在只读文件系统上会失败。
* **种子条目优先**：种子中声明的市场会在每次启动时覆盖用户配置中的任何匹配条目。要选择退出种子插件，请使用 `/plugin disable` 而不是删除市场。
* **路径解析**：Claude Code 通过在运行时探测 `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` 来定位市场内容，而不是通过信任种子 JSON 中存储的路径。这意味着即使种子安装在与构建位置不同的路径上也能正常工作。
* **由设置组成**：如果 `extraKnownMarketplaces` 或 `enabledPlugins` 声明种子中已存在的市场，则 Claude Code 使用种子副本而不是克隆。

### 托管市场限制

对于需要严格控制插件源的组织，管理员可以使用托管设置中的 [`strictKnownMarketplaces`](./settings#strictknownmarketplaces) 设置来限制允许用户添加哪些插件市场。

当在托管设置中配置 `strictKnownMarketplaces` 时，限制行为取决于该值：|价值|行为 |
| ------------------- | ---------------------------------------------------------------- |
|未定义（默认）|没有限制。用户可以添加任何市场|
|空阵列 `[]` |完全封锁。用户无法添加任何新市场 |
|来源列表|用户只能添加与许可名单完全匹配的市场 |

#### 常用配置

禁用所有市场添加：

```json
{
  "strictKnownMarketplaces": []
}
```

仅允许特定市场：

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

允许使用主机上的正则表达式模式匹配来自内部 git 服务器的所有市场：

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

允许使用路径上的正则表达式模式匹配来自特定目录的基于文件系统的市场：

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

将 `".*"` 用作 `pathPattern`，以允许任何文件系统路径，同时仍使用 `hostPattern` 控制网络源。

**注意**

`strictKnownMarketplaces` 限制用户可以添加的内容，但不会自行注册市场。要在用户不运行 `/plugin marketplace add` 的情况下自动提供允许的市场，请将其与同一 `managed-settings.json` 中的 [`extraKnownMarketplaces`](./settings#extraknownmarketplaces) 配对。请参阅[同时使用两者](./settings#strictknownmarketplaces)。

#### 限制如何运作

在任何网络请求或文件系统操作发生之前，在插件安装过程的早期验证限制。这可以防止未经授权的市场访问尝试。

允许列表对大多数源类型使用精确匹配。对于允许的市场，所有指定字段必须完全匹配：

* 对于 GitHub 源：`repo` 是必需的，并且 `ref` 或 `path` 也必须匹配（如果在允许列表中指定）
* 对于 URL 来源：完整的 URL 必须完全匹配
* 对于 `hostPattern` 源：市场主机与正则表达式模式匹配
* 对于 `pathPattern` 源：市场的文件系统路径与正则表达式模式匹配

由于 `strictKnownMarketplaces` 是在 [托管设置](./settings#settings-files) 中设置的，因此个人用户和项目配置无法覆盖这些限制。

有关完整的配置详细信息，包括所有支持的源类型以及与 `extraKnownMarketplaces` 的比较，请参阅 [strictKnownMarketplaces 参考](./settings#strictknownmarketplaces)。

### 版本解析及发布渠道

插件版本决定缓存路径和更新检测。您可以在插件清单 (`plugin.json`) 或市场条目 (`marketplace.json`) 中指定版本。

**警告**

如果可能，请避免在两个地方都设置版本。插件清单总是默默地获胜，这可能会导致市场版本被忽略。对于相对路径插件，请在市场条目中设置版本。对于所有其他插件源，请在插件清单中设置。

#### 设置发布渠道

为了支持插件的“稳定”和“最新”发布渠道，您可以设置两个指向同一存储库的不同引用或 SHA 的市场。然后，您可以通过[托管设置](./settings#settings-files) 将两个市场分配给不同的用户组。

**警告**插件的 `plugin.json` 必须在每个固定引用或提交处声明不同的 `version`。如果两个引用或提交具有相同的清单版本，Claude Code 会将它们视为相同并跳过更新。

##### 示例

```json
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### 将频道分配给用户组

通过托管设置将每个市场分配给适当的用户组。例如，稳定组收到：

```json
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

抢先体验组收到的是 `latest-tools`：

```json
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## 验证和测试

在分享之前测试您的市场。

验证您的市场 JSON 语法：

```bash
claude plugin validate .
```

或者从 Claude Code 内部：

```shell
/plugin validate .
```

添加市场进行测试：

```shell
/plugin marketplace add ./path/to/marketplace
```

安装测试插件以验证一切正常：

```shell
/plugin install test-plugin@marketplace-name
```

有关完整的插件测试工作流程，请参阅[在本地测试您的插件](./plugins#test-your-plugins-locally)。有关技术故障排除，请参阅[插件参考](./plugins-reference)。

## 故障排除

### 市场未加载

**症状**：无法添加市场或从中查看插件

**解决方案**：

* 验证市场 URL 是否可访问
* 检查指定路径下是否存在`.claude-plugin/marketplace.json`
* 使用 `claude plugin validate` 或 `/plugin validate` 确保 JSON 语法有效且 frontmatter 格式良好
* 对于私有仓库，请确认您有访问权限

### 市场验证错误

从您的市场目录运行 `claude plugin validate .` 或 `/plugin validate .` 以检查问题。验证器检查 `plugin.json`、技能/代理/命令 frontmatter 和 `hooks/hooks.json` 是否存在语法和架构错误。常见错误：

|错误 |原因 |解决方案 |
| :------------------------------------------------ | :---------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` |缺少舱单 |使用必填字段创建 `.claude-plugin/marketplace.json` |
| `Invalid JSON syntax: Unexpected token...` | Marketplace.json 中的 JSON 语法错误 |检查是否缺少逗号、多余逗号或不带引号的字符串 |
| `Duplicate plugin name "x" found in marketplace` |两个插件同名 |为每个插件赋予唯一的 `name` 值 |
| `plugins[0].source: Path contains ".."` |源路径包含 `..` |使用相对于市场根目录的路径，无需 `..`。请参阅[相对路径](#relative-paths) |
| `YAML frontmatter failed to parse: ...` |技能、代理或命令文件中的 YAML 无效 |修复 frontmatter 块中的 YAML 语法。在运行时，该文件加载时没有元数据。     |
| `Invalid JSON syntax: ...` (hooks.json) |畸形的 `hooks/hooks.json` |修复 JSON 语法。格式错误的 `hooks/hooks.json` 会阻止整个插件加载。       |

**警告**（非阻塞）：* `Marketplace has no plugins defined`：向 `plugins` 阵列添加至少一个插件
* `No marketplace description provided`：添加 `metadata.description` 以帮助用户了解您的市场
* `Plugin name "x" is not kebab-case`：插件名称包含大写字母、空格或特殊字符。仅重命名为小写字母、数字和连字符（例如 `my-plugin`）。 Claude Code 接受其他形式，但 Claude.ai 市场同步拒绝它们。

### 插件安装失败

**症状**：市场出现但插件安装失败

**解决方案**：

* 验证插件源 URL 是否可访问
* 检查插件目录是否包含所需文件
* 对于 GitHub 源，确保存储库是公共的或者您有权访问
* 通过克隆/下载手动测试插件源

### 私有仓库认证失败

**症状**：从私有存储库安装插件时出现身份验证错误

**解决方案**：

对于手动安装和更新：

* 验证您已通过 git 提供商的身份验证（例如，针对 GitHub 运行 `gh auth status`）
* 检查您的凭据助手配置是否正确：`git config --global credential.helper`
* 尝试手动克隆存储库以验证您的凭据是否有效

对于后台自动更新：

* 在您的环境中设置适当的令牌：`echo $GITHUB_TOKEN`
* 检查令牌是否具有所需的权限（对存储库的读取权限）
* 对于 GitHub，确保令牌具有私有存储库的 `repo` 范围
* 对于 GitLab，确保令牌至少具有 `read_repository` 范围
* 验证token没有过期

### Git 操作超时

**症状**：插件安装或市场更新失败，并出现超时错误，例如“Git 克隆在 120 秒后超时”或“Git pull 在 120 秒后超时”。

**原因**：Claude Code 对所有 git 操作使用 120 秒超时，包括克隆插件存储库和拉取市场更新。大型存储库或缓慢的网络连接可能会超出此限制。

**解决方案**：使用 `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` 环境变量增加超时。该值以毫秒为单位：

```bash
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
```

### 具有相对路径的插件在基于 URL 的市场中失败

**症状**：通过 URL 添加市场（例如 `https://example.com/marketplace.json`），但具有相对路径源（例如 `"./plugins/my-plugin"`）的插件无法安装，并出现“找不到路径”错误。

**原因**：基于 URL 的市场仅下载 `marketplace.json` 文件本身。他们不从服务器下载插件文件。远程服务器上未下载的市场条目参考文件中的相对路径。

**解决方案**：

* **使用外部源**：更改插件条目以使用 GitHub、npm 或 git URL 源而不是相对路径：
  ```json 
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **使用基于 Git 的市场**：将您的市场托管在 Git 存储库中，并使用 git URL 添加它。基于 Git 的市场克隆整个存储库，使相对路径正常工作。

### 安装后找不到文件

**症状**：插件安装但对文件的引用失败，尤其是插件目录之外的文件**原因**：插件被复制到缓存目录而不是就地使用。引用插件目录之外的文件的路径（例如 `../shared-utils`）将不起作用，因为这些文件不会被复制。

**解决方案**：请参阅[插件缓存和文件解析](./plugins-reference#plugin-caching-and-file-resolution) 了解包括符号链接和目录重组在内的解决方法。

有关其他调试工具和常见问题，请参阅[调试和开发工具](./plugins-reference#debugging-and-development-tools)。

## 另请参阅

* [发现并安装预建插件](./discover-plugins) - 从现有市场安装插件
* [插件](./plugins) - 创建您自己的插件
* [插件参考](./plugins-reference) - 完整的技术规范和架构
* [插件设置](./settings#plugin-settings) - 插件配置选项
* [strictKnownMarketplaces 参考](./settings#strictknownmarketplaces) - 托管市场限制
