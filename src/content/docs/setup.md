---
title: "高级设置"
order: 38
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "Claude Code 的系统要求、特定于平台的安装、版本管理和卸载。"
sourceUrl: "https://code.claude.com/docs/en/setup.md"
sourceTitle: "Advanced setup"
tags: []
---
# 高级设置

> Claude Code 的系统要求、平台安装指南、版本管理与卸载。

本页涵盖系统要求、各平台安装细节、更新和卸载。如果你想看首次使用的引导教程，请参阅[快速入门](./quickstart)。如果你从未用过终端，请参阅[终端指南](https://code.claude.com/docs/en/terminal-guide)。

## 系统要求

Claude Code 支持以下平台和配置：

* **操作系统**：
  * macOS 13.0+
  * Windows 10 1809+ 或 Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **硬件**：4 GB+ RAM
* **网络**：需要联网。详见[网络配置](./network-config#network-access-requirements)。
* **Shell**：Bash、Zsh、PowerShell 或 CMD。Windows 上需要安装 [Git for Windows](https://git-scm.com/downloads/win)。
* **地区**：[Anthropic 支持的国家/地区](https://www.anthropic.com/supported-countries)

### 额外依赖

* **ripgrep**：通常已包含在 Claude Code 中。如果搜索功能异常，请参阅[搜索问题排查](./troubleshooting#search-and-discovery-issues)。

## 安装 Claude Code

**提示**

更喜欢图形界面？[桌面应用](./desktop-quickstart)可以让你不用终端也能使用 Claude Code。下载 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs) 或 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs) 版本。

刚接触终端？请参阅[终端指南](https://code.claude.com/docs/en/terminal-guide)获取分步说明。

安装 Claude Code 可以选择以下方式：

### 原生安装（推荐）

**macOS、Linux、WSL：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD：**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Windows 需要先安装 [Git for Windows](https://git-scm.com/downloads/win)。**

**说明**

原生安装会自动后台更新，始终保持最新版本。


### Homebrew

```bash
brew install --cask claude-code
```

**说明**

Homebrew 安装不会自动更新。请定期运行 `brew upgrade claude-code` 获取最新功能和安全补丁。


### WinGet

```powershell
winget install Anthropic.ClaudeCode
```

**说明**

WinGet 安装不会自动更新。请定期运行 `winget upgrade Anthropic.ClaudeCode` 获取最新功能和安全补丁。

安装完成后，在项目目录中打开终端并启动 Claude Code：

```bash
claude
```

如果安装过程中遇到问题，请参阅[故障排除指南](./troubleshooting)。

### Windows 设置

Windows 上的 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win) 或 WSL。你可以从 PowerShell、CMD 或 Git Bash 启动 `claude`。Claude Code 内部使用 Git Bash 执行命令，不需要以管理员身份运行 PowerShell。

**选项 1：原生 Windows + Git Bash**

安装 [Git for Windows](https://git-scm.com/downloads/win)，然后从 PowerShell 或 CMD 运行安装命令。

如果 Claude Code 找不到你的 Git Bash，可以在 [settings.json](./settings) 中指定路径：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**选项 2：WSL**

WSL 1 和 WSL 2 均可使用。WSL 2 支持[沙箱](./sandboxing)以增强安全性，WSL 1 不支持沙箱。

### Alpine Linux 及基于 musl 的发行版

Alpine 和其他基于 musl/uClibc 的发行版，原生安装需要 `libgcc`、`libstdc++` 和 `ripgrep`。先用包管理器安装它们，然后设置 `USE_BUILTIN_RIPGREP=0`。

在 Alpine 上安装所需包：

```bash
apk add libgcc libstdc++ ripgrep
```

然后在 [`settings.json`](./settings#available-settings) 中将 `USE_BUILTIN_RIPGREP` 设为 `0`：

```json
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## 验证安装

安装完成后，确认 Claude Code 工作正常：

```bash
claude --version
```

要做更详细的安装和配置检查，运行 [`claude doctor`](./troubleshooting#get-more-help)：

```bash
claude doctor
```

## 登录认证

Claude Code 需要 Pro、Max、Teams、Enterprise 或 Console 账户。免费的 Claude.ai 账户不包含 Claude Code 使用权限。你也可以配合第三方 API 提供商使用，如 [Amazon Bedrock](./amazon-bedrock)、[Google Vertex AI](./google-vertex-ai) 或 [Microsoft Foundry](./microsoft-foundry)。

安装后运行 `claude`，按照浏览器提示完成登录。所有账户类型和团队配置详见[认证](./authentication)。

## 更新 Claude Code

原生安装会自动后台更新。你可以[配置发布通道](#configure-release-channel)来控制更新节奏——立即获取更新或按延迟的稳定计划更新，也可以完全[禁用自动更新](#disable-auto-updates)。Homebrew 和 WinGet 安装需要手动更新。

### 自动更新

Claude Code 启动时检查更新，运行时也会定期检查。更新在后台下载安装，下次启动时生效。

**注意**

Homebrew 和 WinGet 安装不会自动更新。请用 `brew upgrade claude-code` 或 `winget upgrade Anthropic.ClaudeCode` 手动更新。

**已知问题：** Claude Code 可能会在包管理器中尚未发布新版本时就通知你更新。如果升级失败，请稍后重试。

Homebrew 升级后会在磁盘上保留旧版本。定期运行 `brew cleanup claude-code` 回收磁盘空间。

### 配置发布通道

用 `autoUpdatesChannel` 设置控制自动更新和 `claude update` 使用哪个版本通道：

* `"latest"`（默认）：新功能发布后立即获取
* `"stable"`：使用大约一周前的版本，跳过有严重回归的版本

通过 `/config` → **自动更新通道** 配置，或添加到 [settings.json](./settings)：

```json
{
  "autoUpdatesChannel": "stable"
}
```

企业部署可以使用[托管设置](./permissions#managed-settings)在整个组织内统一发布通道。

### 禁用自动更新

在 [`settings.json`](./settings#available-settings) 的 `env` 中将 `DISABLE_AUTOUPDATER` 设为 `"1"`：

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### 手动更新

要立即应用更新而不等待后台检查，运行：

```bash
claude update
```

## 高级安装选项

这些选项用于版本固定、从 npm 迁移以及验证二进制完整性。

### 安装指定版本

原生安装程序支持指定版本号或发布通道（`latest` 或 `stable`）。安装时选择的通道会成为自动更新的默认通道。详见[配置发布通道](#configure-release-channel)。

安装最新版本（默认）：

### macOS、Linux、WSL

```bash
curl -fsSL https://claude.ai/install.sh | bash
```


### Windows PowerShell

```powershell
irm https://claude.ai/install.ps1 | iex
```


### Windows CMD

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

安装稳定版本：

### macOS、Linux、WSL

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable
```


### Windows PowerShell

```powershell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
```


### Windows CMD

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
```

安装特定版本号：

### macOS、Linux、WSL

```bash
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```


### Windows PowerShell

```powershell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
```


### Windows CMD

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
```

### 已弃用的 npm 安装

npm 安装已弃用。原生安装更快、无需额外依赖，且支持自动后台更新。请尽量使用[原生安装](#install-claude-code)。

#### 从 npm 迁移到原生安装

如果你之前用 npm 安装了 Claude Code，请切换到原生安装：

```bash
# Install the native binary
curl -fsSL https://claude.ai/install.sh | bash

# Remove the old npm installation
npm uninstall -g @anthropic-ai/claude-code
```

你也可以在现有 npm 安装中运行 `claude install` 来安装原生二进制文件，然后删除 npm 版本。

#### 用 npm 安装

如果因兼容性原因需要 npm 安装，必须先安装 [Node.js 18+](https://nodejs.org/en/download)，然后全局安装：

```bash
npm install -g @anthropic-ai/claude-code
```

**警告**

不要使用 `sudo npm install -g`，这会导致权限问题和安全风险。如果遇到权限错误，请参阅[权限错误排查](./troubleshooting#permission-errors-during-installation)。

### 二进制完整性与代码签名

你可以通过 SHA256 校验和和代码签名验证 Claude Code 二进制文件的完整性。

* 各平台的 SHA256 校验和发布在 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`。将 `{VERSION}` 替换为版本号，如 `2.0.30`。
* 已签名的二进制文件分发到以下平台：
  * **macOS**：由 "Anthropic PBC" 签名并经 Apple 公证
  * **Windows**：由 "Anthropic, PBC" 签名

## 卸载 Claude Code

根据你的安装方式选择对应的卸载步骤。

### 原生安装

删除 Claude Code 二进制文件和版本文件：

### macOS、Linux、WSL

```bash
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```


### Windows PowerShell

```powershell
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

### Homebrew 安装

卸载 Homebrew cask：

```bash
brew uninstall --cask claude-code
```

### WinGet 安装

卸载 WinGet 包：

```powershell
winget uninstall Anthropic.ClaudeCode
```

### npm

卸载全局 npm 包：

```bash
npm uninstall -g @anthropic-ai/claude-code
```

### 删除配置文件

**警告**

删除配置文件会清除你的所有设置、已允许的工具、MCP 服务器配置和会话历史。

删除 Claude Code 的设置和缓存数据：

### macOS、Linux、WSL

```bash
# Remove user settings and state
rm -rf ~/.claude
rm ~/.claude.json

# Remove project-specific settings (run from your project directory)
rm -rf .claude
rm -f .mcp.json
```


### Windows PowerShell

```powershell
# Remove user settings and state
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Remove project-specific settings (run from your project directory)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```
