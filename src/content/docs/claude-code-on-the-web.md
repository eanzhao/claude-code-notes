---
title: "网络上的 Claude Code"
order: 15
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "在安全的云基础设施上异步运行 Claude Code 任务"
sourceUrl: "https://code.claude.com/docs/en/claude-code-on-the-web.md"
sourceTitle: "Claude Code on the web"
tags: []
---
# 网络上的 Claude Code

> 在安全的云基础设施上异步运行 Claude Code 任务

**注意**

网络上的 Claude Code 目前处于研究预览阶段。

## 网络上的 Claude Code 是什么？

网络上的 Claude Code 允许开发人员从 Claude 应用程序启动 Claude Code。这非常适合：

* **回答问题**：询问代码架构以及功能如何实现
* **错误修复和日常任务**：明确定义的任务，不需要频繁指导
* **并行工作**：并行解决多个错误修复
* **存储库不在本地计算机上**：处理您未在本地签出的代码
* **后端更改**：Claude Code 可以编写测试，然后编写代码来通过这些测试

Claude Code 还可在适用于 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 和 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的 Claude 应用程序上使用，用于随时随地启动任务并监控正在进行的工作。

您可以使用 `--remote` [从终端在网络上启动新任务](#from-terminal-to-web)，或[将网络会话传送回您的终端](#from-web-to-terminal) 以在本地继续。要在您自己的计算机而不是云基础架构上运行 Claude Code 时使用 Web 界面，请参阅 [Remote Control](./remote-control)。

## 谁可以在网络上使用 Claude Code？

网络上的 Claude Code 可在研究预览中用于：

* **专业用户**
* **最大用户数**
* **团队用户**
* **拥有高级席位或聊天 + Claude Code 席位的企业用户**

## 开始使用

1. 访问[claude.ai/code](https://claude.ai/code)
2. 连接您的 GitHub 帐户
3. 在您的存储库中安装 Claude GitHub 应用程序
4. 选择您的默认环境
5. 提交您的编码任务
6. 在 diff 视图中查看更改，迭代注释，然后创建拉取请求

## 它是如何工作的

当您在 Web 上的 Claude Code 上启动任务时：

1. **存储库克隆**：您的存储库被克隆到 Anthropic 管理的虚拟机
2. **环境设置**：Claude 使用您的代码准备一个安全的云环境，然后运行您的[设置脚本](#setup-scripts)（如果已配置）
3. **网络配置**：根据您的设置配置互联网访问
4. **任务执行**：Claude 分析代码、进行更改、运行测试并检查其工作
5. **完成**：完成后您会收到通知，并且可以创建包含更改的 PR
6. **结果**：更改被推送到分支，准备创建拉取请求

## 使用 diff 视图查看更改

差异视图可让您在创建拉取请求之前准确查看 Claude 更改的内容。不要单击“创建 PR”来查看 GitHub 中的更改，而是直接在应用程序中查看差异并使用 Claude 进行迭代，直到更改准备就绪。

当 Claude 对文件进行更改时，会出现差异统计指示器，显示添加和删除的行数（例如 `+12 -1`）。选择此指示器可打开差异查看器，该查看器在左侧显示文件列表，在右侧显示每个文件的更改。

从差异视图中，您可以：

*逐个文件查看更改
* 对具体变更发表评论以请求修改
* 根据您所看到的内容继续使用 Claude 进行迭代这使您可以通过多轮反馈来完善更改，而无需创建 PR 草稿或切换到 GitHub。

## 在网络和终端之间移动任务

您可以从终端在网络上启动新任务，或将网络会话拉入终端以在本地继续。即使您关闭笔记本电脑，Web 会话仍然存在，并且您可以从任何地方（包括 Claude 移动应用程序）监控它们。

**注意**

会话切换是单向的：您可以将 Web 会话拉入终端，但无法将现有终端会话推送到 Web。 `--remote` 标志为您当前的存储库创建一个*新的* Web 会话。

### 从终端到网络

使用 `--remote` 标志从命令行启动 Web 会话：

```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

这会在 claude.ai 上创建一个新的网络会话。该任务在云中运行，而您继续在本地工作。使用 `/tasks` 检查进度，或在 claude.ai 或 Claude 移动应用程序上打开会话直接交互。从那里您可以引导 Claude、提供反馈或回答问题，就像任何其他对话一样。

#### 远程任务提示

**本地规划，远程执行**：对于复杂的任务，在计划模式下启动 Claude 以协作处理该方法，然后将工作发送到网络：

```bash
claude --permission-mode plan
```

在计划模式下，Claude 只能读取文件并探索代码库。一旦您对计划感到满意，就启动远程会话以进行自主执行：

```bash
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

此模式使您可以控制策略，同时让 Claude 在云中自主执行。

**并行运行任务**：每个 `--remote` 命令都会创建自己独立运行的 Web 会话。您可以启动多个任务，它们将在单独的会话中同时运行：

```bash
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

使用 `/tasks` 监视所有会话。会话完成后，您可以从 Web 界面创建 PR 或将会话[传送](#from-web-to-terminal) 到您的终端以继续工作。

### 从网络到终端

有多种方法可以将网络会话拉入终端：

* **使用 `/teleport`**：从 Claude Code 中运行 `/teleport`（或 `/tp`）以查看 Web 会话的交互式选择器。如果您有未提交的更改，系统会提示您先隐藏它们。
* **使用 `--teleport`**：从命令行运行 `claude --teleport` 以获取交互式会话选择器，或运行 `claude --teleport <session-id>` 以直接恢复特定会话。
* **来自 `/tasks`**：运行 `/tasks` 查看您的后台会话，然后按 `t` 传送到一个
* **从 Web 界面**：单击“在 CLI 中打开”复制可粘贴到终端的命令

当您传送会话时，Claude 会验证您是否位于正确的存储库中，从远程会话中获取并签出分支，并将完整的对话历史记录加载到您的终端中。

#### 传送的要求

Teleport 在恢复会话之前会检查这些要求。如果不满足任何要求，您将看到错误或提示解决问题。|要求 |详情 |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
|清理 git 状态 |您的工作目录必须没有未提交的更改。如果需要，传送会提示您隐藏更改。              |
|正确的存储库 |您必须从同一存储库的签出运行 `--teleport`，而不是分支。                                          |
|分行可用 |来自 Web 会话的分支必须已推送到远程。 Teleport 会自动获取并检查它。 |
|同一帐户 |您必须通过网络会话中使用的同一 Claude.ai 帐户进行身份验证。                                       |

### 分享会

要共享会话，请根据帐户切换其可见性
类型如下。之后，按原样共享会话链接。打开您的
共享会话将在加载时看到会话的最新状态，但是
收件人页面不会实时更新。

#### 从企业或团队帐户共享

对于企业和团队帐户，两个可见性选项是**私人**
和**团队**。团队可见性使会议对您的其他成员可见
Claude.ai 组织。默认情况下启用存储库访问验证，
基于连接到收件人帐户的 GitHub 帐户。您的帐户的
所有具有访问权限的收件人都可以看到显示名称。 [Slack 中的 Claude](./slack)
会话会自动与团队可见性共享。

#### 从 Max 或 Pro 帐户共享

对于 Max 和 Pro 帐户，两个可见性选项是 **私人**
和**公开**。公共可见性使会话对任何登录的用户都可见
进入 claude.ai。

在共享之前检查您的会话中是否存在敏感内容。会话可能包含
来自私人 GitHub 存储库的代码和凭据。存储库访问
默认情况下不启用验证。

启用存储库访问验证和/或在共享中隐藏您的姓名
通过转至设置 > Claude Code > 共享设置来进行会话。

## 管理会话

### 存档会话

您可以存档会话以保持会话列表井井有条。存档会话在默认会话列表中隐藏，但可以通过筛选存档会话来查看。

要存档会话，请将鼠标悬停在侧栏中的会话上，然后单击存档图标。

### 删除会话

删除会话将永久删除该会话及其数据。此操作无法撤消。您可以通过两种方式删除会话：

* **从侧边栏**：筛选已存档的会话，然后将鼠标悬停在要删除的会话上并单击删除图标
* **从会话菜单**：打开会话，单击会话标题旁边的下拉菜单，然后选择 **删除**

在删除会话之前，系统会要求您确认。

## 云环境

### 默认图片

我们通过预装的通用工具链和语言生态系统构建和维护通用映像。该图像包括：* 流行的编程语言和运行时
* 常用构建工具和包管理器
* 测试框架和 linter

#### 检查可用工具

要查看您的环境中预安装的内容，请要求 Claude Code 运行：

```bash
check-tools
```

该命令显示：

* 编程语言及其版本
* 可用的包管理器
* 安装的开发工具

#### 特定于语言的设置

通用映像包括以下预配置环境：

* **Python**：带有 pip、poetry 和通用科学库的 Python 3.x
* **Node.js**：带有 npm、yarn、pnpm 和 Bun 的最新 LTS 版本
* **Ruby**：版本 3.1.6、3.2.6、3.3.6（默认：3.3.6），使用 gem、bundler 和 rbenv 进行版本管理
* **PHP**：版本 8.4.14
* **Java**：带有 Maven 和 Gradle 的 OpenJDK
* **Go**：具有模块支持的最新稳定版本
* **Rust**：带货物的 Rust 工具链
* **C++**：GCC 和 Clang 编译器

#### 数据库

通用镜像包含以下数据库：

* **PostgreSQL**：版本 16
* **Redis**：版本 7.0

### 环境配置

当您在网络上的 Claude Code 中启动会话时，会发生以下情况：

1. **环境准备**：我们克隆您的存储库并运行任何配置的[安装脚本](#setup-scripts)。该存储库将使用 GitHub 存储库上的默认分支进行克隆。如果您想查看特定分支，可以在提示中指定。

2. **网络配置**：我们为代理配置互联网访问。默认情况下，Internet 访问受到限制，但您可以根据需要将环境配置为无 Internet 访问或完全访问 Internet。

3. **Claude Code 执行**：Claude Code 运行以完成您的任务，编写代码、运行测试并检查其工作。您可以通过 Web 界面在整个会话过程中指导和操纵 Claude。 Claude 尊重您在 `CLAUDE.md` 中定义的上下文。

4. **结果**：当 Claude 完成其工作时，它将将该分支推送到远程。您将能够为分支创建 PR。

**注意**

Claude 完全通过环境中可用的终端和 CLI 工具进行操作。它使用通用映像中预安装的工具以及您通过挂钩或依赖项管理安装的任何其他工具。

**添加新环境：** 选择当前环境以打开环境选择器，然后选择“添加环境”。这将打开一个对话框，您可以在其中指定环境名称、网络访问级别、环境变量和[安装脚本](#setup-scripts)。

**要更新现有环境：** 选择环境名称右侧的当前环境，然后选择设置按钮。这将打开一个对话框，您可以在其中更新环境名称、网络访问、环境变量和安装脚本。

**要从终端选择默认环境：** 如果您配置了多个环境，请运行 `/remote-env` 以选择在使用 `--remote` 从终端启动 Web 会话时使用哪一个环境。对于单一环境，此命令显示您当前的配置。

**注意**环境变量必须指定为键值对，采用 [`.env` 格式](https://www.dotenv.org/)。例如：

```text
API_KEY=your_api_key
DEBUG=true
```

### 设置脚本

设置脚本是一个 Bash 脚本，在新的云会话启动时、Claude Code 启动之前运行。使用安装脚本安装依赖项、配置工具或准备云环境所需的[默认映像](#default-image) 中未包含的任何内容。

脚本在 Ubuntu 24.04 上以 root 身份运行，因此 `apt install` 和大多数语言包管理器都可以工作。

**提示**

要在将其添加到脚本之前检查已安装的内容，请要求 Claude 在云会话中运行 `check-tools`。

要添加安装脚本，请打开环境设置对话框并在 **安装脚本** 字段中输入您的脚本。

此示例安装 `gh` CLI，该 CLI 不在默认映像中：

```bash
#!/bin/bash
apt update && apt install -y gh
```

安装脚本仅在创建新会话时运行。恢复现有会话时将跳过它们。

如果脚本以非零值退出，则会话无法启动。将 `|| true` 附加到非关键命令，以避免阻塞不稳定安装的会话。

**注意**

安装软件包的安装脚本需要网络访问才能到达注册表。默认网络访问允许连接到[通用包注册表](#default-allowed-domains)，包括 npm、PyPI、RubyGems 和 crates.io。如果您的环境禁用了网络访问，脚本将无法安装软件包。

#### 设置脚本与 SessionStart 挂钩

使用安装脚本来安装云所需但您的笔记本电脑已有的东西，例如语言运行时或 CLI 工具。使用 [SessionStart 挂钩](./hooks#sessionstart) 进行项目设置，该项目应在云和本地的任何地方运行，例如 `npm install`。

两者都在会话开始时运行，但它们属于不同的位置：

|               |设置脚本 | SessionStart 挂钩 |
| ------------- | ------------------------------------------------- | -------------------------------------------------------------------------- |
|附于 |云环境|您的存储库 |
|配置于 |云环境UI | `.claude/settings.json` 在您的存储库中 |
|运行 |在 Claude Code 推出之前，仅限新会话 | Claude Code 启动后，在每个会话中，包括恢复 |
|范围 |仅限云环境 |本地和云端 |

SessionStart 挂钩也可以在本地用户级 `~/.claude/settings.json` 中定义，但用户级设置不会延续到云会话。在云中，只有钩子致力于存储库运行。

### 依赖管理

尚不支持自定义环境映像和快照。使用 [安装脚本](#setup-scripts) 在会话启动时安装软件包，或使用 [SessionStart 挂钩](./hooks#sessionstart) 进行依赖项安装（也应在本地环境中运行）。 SessionStart 挂钩有[已知限制](#dependency-management-limitations)。

要使用安装脚本配置自动依赖项安装，请打开环境设置并添加脚本：```bash 
#!/bin/bash
npm install
pip install -r requirements.txt
```

或者，您可以使用存储库的 `.claude/settings.json` 文件中的 SessionStart 挂钩进行依赖项安装，该依赖项安装也应在本地环境中运行：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

在`scripts/install_pkgs.sh`处创建相应的脚本：

```bash
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

使其可执行：`chmod +x scripts/install_pkgs.sh`

#### 保存环境变量

SessionStart 挂钩可以通过写入 `CLAUDE_ENV_FILE` 环境变量中指定的文件来保留后续 Bash 命令的环境变量。有关详细信息，请参阅挂钩参考中的 [SessionStart 挂钩](./hooks#sessionstart)。

#### 依赖管理限制

* **为所有会话触发钩子**：SessionStart 钩子在本地和远程环境中运行。没有挂钩配置可以将挂钩范围仅限制到远程会话。要跳过本地执行，请检查脚本中的 `CLAUDE_CODE_REMOTE` 环境变量，如上所示。
* **需要网络访问**：安装命令需要网络访问才能到达包注册表。如果您的环境配置为“无互联网”访问，这些挂钩将失败。使用“有限”（默认）或“完全”网络访问。 [默认允许列表](#default-allowed-domains) 包括常见注册表，例如 npm、PyPI、RubyGems 和 crates.io。
* **代理兼容性**：远程环境中的所有出站流量都会通过[安全代理](#security-proxy)。某些包管理器无法与此代理一起正常工作。包子就是一个众所周知的例子。
* **在每次会话启动时运行**：每次会话启动或恢复时都会运行挂钩，从而增加启动延迟。通过在重新安装之前检查依赖项是否已存在，保持安装脚本的快速运行。

## 网络访问和安全

### 网络政策

#### GitHub 代理

为了安全起见，所有 GitHub Actions都通过专用代理服务透明地处理所有 git 交互。在沙箱内，git 客户端使用定制的范围凭证进行身份验证。这个代理：

* 安全地管理 GitHub 身份验证 - git 客户端在沙箱内使用范围内的凭据，代理会验证该凭据并将其转换为您实际的 GitHub 身份验证令牌
* 为了安全起见，将 git Push 操作限制到当前工作分支
* 实现无缝克隆、获取和 PR 操作，同时保持安全边界

#### 安全代理

环境在 HTTP/HTTPS 网络代理后面运行，以实现安全和防止滥用目的。所有出站互联网流量都会通过此代理，该代理提供：

* 防止恶意请求
* 速率限制和滥用预防
* 内容过滤以增强安全性

### 访问级别

默认情况下，网络访问仅限于[允许的域](#default-allowed-domains)。

您可以配置自定义网络访问，包括禁用网络访问。

### 默认允许的域

使用“有限”网络访问时，默认允许以下域：

#### Anthropic 服务

* api.anthropic.com
* statsig.anthropic.com
* 平台.claude.com
* 代码.claude.com
* 克劳德.ai

#### 版本控制* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* 原始\.githubusercontent.com
* pkg-npm.githubusercontent.com
* 对象.githubusercontent.com
* codeload.github.com
* 头像.githubusercontent.com
* camo.githubusercontent.com
*要点.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* 注册表.gitlab.com
* 比特桶.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### 容器注册表

* 注册表-1.docker.io
* auth.docker.io
* 索引.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* 生产.cloudflare.docker.com
* 下载.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* 公共.ecr.aws

#### 云平台

* 云.google.com
* 帐户.google.com
* gcloud.google.com
* \*.googleapis.com
* 存储.googleapis.com
* 计算.googleapis.com
* 容器.googleapis.com
* azure.com
* 门户网站.azure.com
* 微软网站
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* 软件包.microsoft.com
* dotnet.microsoft.com
* 点网
* 视觉工作室.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* 甲骨文网站
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* 下载.oracle.com
* yum.oracle.com

#### 包管理器 - JavaScript/Node

* 注册表.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
*registry.yarnpkg.com

#### 包管理器 - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* 文件.pythonhosted.org
* pythonhosted.org
* 测试.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### 包管理器 - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
*index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* 获取.rvm.io

#### 包管理器 - Rust

* 板条箱.io
* [www.crates.io](http://www.crates.io)
* 索引.crates.io
* 静态.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### 包管理器 - Go

* proxy.golang.org
* sum.golang.org
* 索引.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### 包管理器 - JVM

* maven.org
* repo.maven.org
*central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* 服务.gradle.org
* 插件.gradle.org
* 科特林.org
* [www.kotlin.org](http://www.kotlin.org)
* 春天.io
* repo.spring.io

#### 包管理器 - 其他语言

* packagist.org（PHP 作曲家）
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev（Dart/Flutter）
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
*metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* 斯威夫特.org
* [www.swift.org](http://www.swift.org)#### Linux 发行版

* 存档.ubuntu.com
* 安全.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* 启动板.net
* [www.launchpad.net](http://www.launchpad.net)

#### 开发工具和平台

* dl.k8s.io（Kubernetes）
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
*releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* 哈希公司.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* 连续体.io
* apache.org（阿帕奇）
* [www.apache.org](http://www.apache.org)
* 存档.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* 下载.eclipse.org
*nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### 云服务和监控

* 统计网站
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* 哨兵.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### 内容交付和镜像

* 源福吉网
* \*.sourceforge.net
* 包云.io
* \*.packagecloud.io

#### 架构和配置

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

**注意**

标有 `*` 的域表示通配符子域匹配。例如，`*.gcr.io` 允许访问 `gcr.io` 的任何子域。

### 定制网络访问的安全最佳实践

1. **最小权限原则**：仅启用所需的最低网络访问权限
2. **定期审核**：定期审查允许的域
3. **使用 HTTPS**：始终优先选择 HTTPS 端点而不是 HTTP

## 安全和隔离

网络上的Claude Code提供强大的安全保证：

* **隔离的虚拟机**：每个会话都在隔离的 Anthropic 管理的 VM 中运行
* **网络访问控制**：网络访问默认受到限制，可以禁用

**注意**

在禁用网络访问的情况下运行时，允许 Claude Code 与 Anthropic API 通信，这仍可能允许数据退出隔离的 Claude Code VM。

* **凭据保护**：敏感凭据（例如 git 凭据或签名密钥）永远不会位于 Claude Code 的沙箱内。身份验证是通过使用范围凭据的安全代理进行处理的
* **安全分析**：在创建 PR 之前，在隔离的虚拟机内分析和修改代码

## 定价和费率限制

网络上的 Claude Code 与您帐户内的所有其他 Claude 和 Claude Code 使用情况共享速率限制。并行运行多个任务将按比例消耗更多的速率限制。

## 限制

* **存储库身份验证**：只有当您通过同一帐户的身份验证时，您才能将会话从网络移动到本地
* **平台限制**：网络上的 Claude Code 仅适用于 GitHub 中托管的代码。 GitLab 和其他非 GitHub 存储库不能与云会话一起使用

## 最佳实践1. **自动化环境设置**：在 Claude Code 启动之前使用[设置脚本](#setup-scripts) 安装依赖项并配置工具。对于更高级的场景，请配置 [SessionStart 挂钩](./hooks#sessionstart)。
2. **文件要求**：在 `CLAUDE.md` 文件中明确指定依赖项和命令。如果您有 `AGENTS.md` 文件，则可以使用 `@AGENTS.md` 在 `CLAUDE.md` 中获取该文件，以维护单一事实来源。

## 相关资源

* [挂钩配置](./hooks)
* [设置参考](./settings)
* [安全](./security)
* [数据使用量](./data-usage)
