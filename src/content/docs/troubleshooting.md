---
title: "故障排除"
order: 30
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "发现 Claude Code 安装和使用常见问题的解决方案。"
sourceUrl: "https://code.claude.com/docs/en/troubleshooting.md"
sourceTitle: "Troubleshooting"
tags: []
---
# 故障排除

> 发现 Claude Code 安装和使用常见问题的解决方案。

## 解决安装问题

**提示**

如果您想完全跳过终端，[Claude Code 桌面应用程序](./desktop-quickstart) 可让您通过图形界面安装和使用 Claude Code。下载 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs) 或 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs) 并开始编码，无需任何命令行设置。

查找您看到的错误消息或症状：

|你所看到的|解决方案 |
| :---------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `command not found: claude` 或 `'claude' is not recognized` | [修复您的路径](#command-not-found-claude-after-installation) |
| `syntax error near unexpected token '<'` | [安装脚本返回 HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `curl: (56) Failure writing output to destination` | [先下载脚本，然后运行](#curl-56-failure-writing-output-to-destination) |
|在 Linux 上安装期间出现 `Killed` | [为低内存服务器添加交换空间](#install-killed-on-low-memory-linux-servers) |
| `TLS connect error` 或 `SSL/TLS secure channel` | [更新CA证书](#tls-or-ssl-connection-errors) |
| `Failed to fetch version` 或无法到达下载服务器 | [检查网络和代理设置](#check-network-connectivity) |
| `irm is not recognized` 或 `&& is not valid` | [使用适合您的 shell 的正确命令](#windows-irm-or--not-recognized) |
| `Claude Code on Windows requires git-bash` | [安装或配置 Git Bash](#windows-claude-code-on-windows-requires-git-bash) |
| `Error loading shared library` | [您的系统的二进制变体错误](#linux-wrong-binary-variant-installed-muslglibc-mismatch) |
| Linux 上的 `Illegal instruction` | [架构不匹配](#illegal-instruction-on-linux) |
| macOS 上的 `dyld: cannot load` 或 `Abort trap` | [二进制不兼容](#dyld-cannot-load-on-macos) |
| `Invoke-Expression: Missing argument in parameter list` | [安装脚本返回 HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `App unavailable in region` | Claude Code 在您所在的国家/地区不可用。请参阅[支持的国家/地区](https://www.anthropic.com/supported-countries)。 |
| `unable to get local issuer certificate` | [配置企业CA证书](#tls-or-ssl-connection-errors) |
| `OAuth error` 或 `403 Forbidden` | [修复身份验证](#authentication-issues) |

如果您的问题未列出，请完成这些诊断步骤。

## 调试安装问题

### 检查网络连接

安装程序从 `storage.googleapis.com` 下载。验证您可以到达它：

```bash
curl -sI https://storage.googleapis.com
```如果失败，您的网络可能会阻止连接。常见原因：

* 公司防火墙或代理阻止 Google Cloud Storage
* 区域网络限制：尝试 VPN 或替代网络
* TLS/SSL 问题：更新系统的 CA 证书，或检查是否配置了 `HTTPS_PROXY`

如果您使用公司代理，请在安装前将 `HTTPS_PROXY` 和 `HTTP_PROXY` 设置为您的代理地址。如果您不知道代理 URL，请向 IT 团队询问，或者检查浏览器的代理设置。

此示例设置两个代理变量，然后通过代理运行安装程序：

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### 验证你的路径

如果安装成功，但在运行 `claude` 时出现 `command not found` 或 `not recognized` 错误，则安装目录不在您的 PATH 中。您的 shell 会在 PATH 列出的目录中搜索程序，安装程序会将 `claude` 放置在 macOS/Linux 上的 `~/.local/bin/claude` 或 Windows 上的 `%USERPROFILE%\.local\bin\claude.exe` 处。

通过列出您的 PATH 条目并过滤 `local/bin`，检查安装目录是否在您的 PATH 中：

### macOS/Linux

```bash
echo $PATH | tr ':' '\n' | grep local/bin
```

如果没有输出，则说明该目录丢失。将其添加到您的 shell 配置中：

```bash
# Zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Bash (Linux default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

或者，关闭并重新打开您的终端。

验证修复是否有效：

```bash
claude --version
```

  
### Windows PowerShell

```powershell
$env:PATH -split ';' | Select-String 'local\\bin'
```

如果没有输出，请将安装目录添加到您的用户路径：

```powershell
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
```

重新启动终端以使更改生效。

验证修复是否有效：

```powershell
claude --version
```

  
### Windows CMD

```batch
echo %PATH% | findstr /i "local\bin"
```

如果没有输出，请打开系统设置，转到环境变量，然后将 `%USERPROFILE%\.local\bin` 添加到用户路径变量中。重新启动您的终端。

验证修复是否有效：

```batch
claude --version
```

### 检查安装冲突

多个 Claude Code 安装可能会导致版本不匹配或意外行为。检查安装了什么：

### macOS/Linux

列出在您的 PATH 中找到的所有 `claude` 二进制文件：

```bash
which -a claude
```

检查本机安装程序和 npm 版本是否存在：

```bash
ls -la ~/.local/bin/claude
```

```bash
ls -la ~/.claude/local/
```

```bash
npm -g ls @anthropic-ai/claude-code 2>/dev/null
```

  
### Windows PowerShell

```powershell
where.exe claude
Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
```

如果您发现多个安装，请仅保留一个。建议在 `~/.local/bin/claude` 进行本机安装。删除任何额外的安装：

卸载 npm 全局安装：

```bash
npm uninstall -g @anthropic-ai/claude-code
```

删除 macOS 上的 Homebrew 安装：

```bash
brew uninstall --cask claude-code
```

### 检查目录权限

安装程序需要对 `~/.local/bin/` 和 `~/.claude/` 具有写入权限。如果安装失败并出现权限错误，请检查这些目录是否可写：

```bash
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

如果任一目录不可写，请创建安装目录并将您的用户设置为所有者：

```bash
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### 验证二进制文件是否有效

如果已安装 `claude` 但在启动时崩溃或挂起，请运行这些检查以缩小原因范围。

确认二进制文件存在并且可执行：

```bash
ls -la $(which claude)
```

在 Linux 上，检查是否缺少共享库。如果 `ldd` 显示缺少库，您可能需要安装系统软件包。在 Alpine Linux 和其他基于 musl 的发行版上，请参阅 [Alpine Linux 设置](./setup#alpine-linux-and-musl-based-distributions)。

```bash
ldd $(which claude) | grep "not found"
```

运行快速健全性检查以确保二进制文件可以执行：

```bash
claude --version
```## 常见安装问题

这些是最常遇到的安装问题及其解决方案。

### 安装脚本返回 HTML 而不是 shell 脚本

运行安装命令时，您可能会看到以下错误之一：

```text
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

在 PowerShell 上，同样的问题显示为：

```text
Invoke-Expression: Missing argument in parameter list.
```

这意味着安装 URL 返回 HTML 页面而不是安装脚本。如果 HTML 页面显示“应用程序在该地区不可用”，则 Claude Code 在您所在的国家/地区不可用。请参阅[支持的国家/地区](https://www.anthropic.com/supported-countries)。

否则，这种情况可能会由于网络问题、区域路由或临时服务中断而发生。

**解决方案：**

1. **使用替代安装方法**：

   在 macOS 或 Linux 上，通过 Homebrew 安装：

   ```bash 
   brew install --cask claude-code
   ```

   在 Windows 上，通过 WinGet 安装：

   ```powershell 
   winget install Anthropic.ClaudeCode
   ```

2. **几分钟后重试**：问题通常是暂时的。等待并再次尝试原始命令。

### 安装后`command not found: claude`

安装已完成，但 `claude` 无法工作。确切的错误因平台而异：

|平台|错误信息 |
| :---------- | :--------------------------------------------------------------------- |
| macOS | `zsh: command not found: claude` |
| Linux | `bash: claude: command not found` |
| Windows 命令 | `'claude' is not recognized as an internal or external command` |
| PowerShell | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

这意味着安装目录不在 shell 的搜索路径中。请参阅[验证您的路径](#verify-your-path) 了解每个平台上的修复程序。

### `curl: (56) Failure writing output to destination`

`curl ... | bash` 命令下载脚本并将其直接传递到 Bash 以使用管道 (`|`) 执行。此错误意味着在脚本下载完成之前连接中断。常见原因包括网络中断、下载中途受阻或系统资源限制。

**解决方案：**

1. **检查网络稳定性**：Claude Code 二进制文件托管在 Google Cloud Storage 上。测试你是否可以达到它：
   ```bash 
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   如果命令以静默方式完成，则表明您的连接正常，并且问题可能是间歇性的。重试安装命令。如果您看到错误，则您的网络可能阻止下载。

2. **尝试替代安装方法**：

   在 macOS 或 Linux 上：

   ```bash 
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell 
   winget install Anthropic.ClaudeCode
   ```

### TLS 或 SSL 连接错误

`curl: (35) TLS connect error`、`schannel: next InitializeSecurityContext failed` 或 PowerShell 的 `Could not establish trust relationship for the SSL/TLS secure channel` 等错误表示 TLS 握手失败。

**解决方案：**

1. **更新您的系统 CA 证书**：

   在 Ubuntu/Debian 上：

   ```bash 
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   在 macOS 上通过 Homebrew：

   ```bash 
   brew install ca-certificates
   ```

2. **在 Windows 上，在运行安装程序之前在 PowerShell 中启用 TLS 1.2**：
   ```powershell 
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **检查代理或防火墙干扰**：执行 TLS 检查的企业代理可能会导致这些错误，包括 `unable to get local issuer certificate`。将 `NODE_EXTRA_CA_CERTS` 设置为您的公司 CA 证书捆绑包：
   ```bash 
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   如果您没有证书文件，请向您的 IT 团队索要证书文件。您还可以尝试直接连接以确认代理是原因。

### `Failed to fetch version from storage.googleapis.com`安装程序无法访问下载服务器。这通常意味着 `storage.googleapis.com` 在您的网络上被阻止。

**解决方案：**

1. **直接测试连通性**：
   ```bash 
   curl -sI https://storage.googleapis.com
   ```

2. **如果位于代理后面**，请设置 `HTTPS_PROXY`，以便安装程序可以通过它进行路由。有关详细信息，请参阅[代理配置](./network-config#proxy-configuration)。
   ```bash 
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **如果在受限网络上**，请尝试不同的网络或 VPN，或使用替代安装方法：

   在 macOS 或 Linux 上：

   ```bash 
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell 
   winget install Anthropic.ClaudeCode
   ```

### Windows：无法识别 `irm` 或 `&&`

如果您看到 `'irm' is not recognized` 或 `The token '&&' is not valid`，则说明您在 shell 中运行了错误的命令。

* **无法识别 `irm`**：您使用的是 CMD，而不是 PowerShell。您有两个选择：

  在开始菜单中搜索“PowerShell”打开PowerShell，然后运行原始安装命令：

  ```powershell 
  irm https://claude.ai/install.ps1 | iex
  ```

  或者留在 CMD 中并使用 CMD 安装程序：

  ```batch 
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` 无效**：您位于 PowerShell 但运行了 CMD 安装程序命令。使用 PowerShell 安装程序：
  ```powershell 
  irm https://claude.ai/install.ps1 | iex
  ```

### 在低内存 Linux 服务器上安装被终止

如果您在 VPS 或云实例上安装期间看到 `Killed`：

```text
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

由于系统内存不足，Linux OOM Killer 终止了该进程。 Claude Code 需要至少 4 GB 的可用 RAM。

**解决方案：**

1. **如果您的服务器 RAM 有限，请添加交换空间**。交换使用磁盘空间作为溢出内存，即使物理 RAM 较低也可以完成安装。

   创建一个 2 GB 交换文件并启用它：

   ```bash 
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   然后重试安装：

   ```bash 
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **安装前关闭其他进程**以释放内存。

3. **如果可能，使用更大的实例**。 Claude Code 需要至少 4 GB RAM。

### 安装在 Docker 中挂起

在 Docker 容器中安装 Claude Code 时，以 root 身份安装到 `/` 可能会导致挂起。

**解决方案：**

1. **在运行安装程序之前设置工作目录**。从 `/` 运行时，安装程​​序会扫描整个文件系统，这会导致内存使用过多。设置 `WORKDIR` 将扫描限制为小目录：
   ```dockerfile 
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **如果使用 Docker 桌面，则增加 Docker 内存限制**：
   ```bash 
   docker build --memory=4g .
   ```

### Windows：Claude Desktop 覆盖 `claude` CLI 命令

如果您安装了旧版本的 Claude Desktop，它可能会在 `WindowsApps` 目录中注册 `Claude.exe`，该目录的 PATH 优先级高于 Claude Code CLI。运行 `claude` 将打开桌面应用程序而不是 CLI。

将 Claude Desktop 更新到最新版本以修复此问题。

### Windows：“Windows 上的 Claude Code 需要 git-bash”

本机 Windows 上的 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win)，其中包括 Git Bash。

**如果未安装 Git**，请从 [git-scm.com/downloads/win](https://git-scm.com/downloads/win) 下载并安装它。在安装过程中，选择“添加到路径”。安装后重新启动终端。

**如果已经安装了 Git** 但 Claude Code 仍然找不到它，请在您的 [settings.json 文件](./settings) 中设置路径：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```如果您的 Git 安装在其他位置，请通过在 PowerShell 中运行 `where.exe git` 来查找路径，并使用该目录中的 `bin\bash.exe` 路径。

### Linux：安装了错误的二进制变体（musl/glibc 不匹配）

如果您在安装后看到有关缺少共享库（例如 `libstdc++.so.6` 或 `libgcc_s.so.1`）的错误，则安装程序可能为您的系统下载了错误的二进制变体。

```text
Error loading shared library libstdc++.so.6: No such file or directory
```

这种情况可能发生在安装了 musl 交叉编译包的基于 glibc 的系统上，导致安装程序将系统误检测为 musl。

**解决方案：**

1. **检查您的系统使用哪个 libc**：
   ```bash 
   ldd /bin/ls | head -1
   ```
   如果它显示 `linux-vdso.so` 或对 `/lib/x86_64-linux-gnu/` 的引用，则说明您使用的是 glibc。如果显示 `musl`，则说明您处于 musl 状态。

2. **如果您使用的是 glibc 但获得了 musl 二进制文件**，请删除安装并重新安装。您还可以从位于 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` 的 GCS 存储桶手动下载正确的二进制文件。使用 `ldd /bin/ls` 和 `ls /lib/libc.musl*` 的输出提交 [GitHub 问题](https://github.com/anthropics/claude-code/issues)。

3. **如果您实际上使用的是 musl** (Alpine Linux)，请安装所需的软件包：
   ```bash 
   apk add libgcc libstdc++ ripgrep
   ```

### `Illegal instruction` 于 Linux

如果安装程序打印 `Illegal instruction` 而不是 OOM `Killed` 消息，则下载的二进制文件与您的 CPU 架构不匹配。这种情况通常发生在接收 x86 二进制文件的 ARM 服务器上，或者缺乏所需指令集的旧 CPU 上。

```text
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**解决方案：**

1. **验证您的架构**：
   ```bash 
   uname -m
   ```
   `x86_64` 表示 64 位 Intel/AMD，`aarch64` 表示 ARM64。如果二进制文件不匹配，请使用输出[提交 GitHub 问题](https://github.com/anthropics/claude-code/issues)。

2. **尝试替代安装方法**，同时解决架构问题：
   ```bash 
   brew install --cask claude-code
   ```

### `dyld: cannot load` 于 macOS

如果您在安装过程中看到 `dyld: cannot load` 或 `Abort trap: 6`，则二进制文件与您的 macOS 版本或硬件不兼容。

```text
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**解决方案：**

1. **检查您的 macOS 版本**：Claude Code 需要 macOS 13.0 或更高版本。打开 Apple 菜单并选择“关于本机”以检查您的版本。

2. **如果您使用的是旧版本，请更新 macOS**。该二进制文件使用旧版 macOS 不支持的加载命令。

3. **尝试 Homebrew** 作为替代安装方法：
   ```bash 
   brew install --cask claude-code
   ```

### Windows 安装问题：WSL 中的错误

您在 WSL 中可能会遇到以下问题：

**操作系统/平台检测问题**：如果您在安装过程中收到错误，WSL 可能正在使用 Windows `npm`。尝试：

* 安装前运行 `npm config set os linux`
* 与 `npm install -g @anthropic-ai/claude-code --force --no-os-check` 一起安装。请勿使用 `sudo`。

**找不到节点错误**：如果您在运行 `claude` 时看到 `exec: node: not found`，则您的 WSL 环境可能正在使用 Node.js 的 Windows 安装。您可以使用 `which npm` 和 `which node` 来确认这一点，它们应该指向以 `/usr/` 而不是 `/mnt/c/` 开头的 Linux 路径。要解决此问题，请尝试通过 Linux 发行版的包管理器或通过 [`nvm`](https://github.com/nvm-sh/nvm) 安装 Node。**nvm 版本冲突**：如果您在 WSL 和 Windows 中都安装了 nvm，则在 WSL 中切换 Node 版本时可能会遇到版本冲突。发生这种情况是因为 WSL 默认导入 Windows PATH，导致 Windows nvm/npm 优先于 WSL 安装。

您可以通过以下方式识别此问题：

* 运行 `which npm` 和 `which node` - 如果它们指向 Windows 路径（以 `/mnt/c/` 开头），则正在使用 Windows 版本
* 在 WSL 中使用 nvm 切换 Node 版本后遇到功能损坏的情况

要解决此问题，请修复 Linux PATH，以确保 Linux 节点/npm 版本优先：

**主要解决方案：确保 nvm 已正确加载到您的 shell 中**

最常见的原因是 nvm 未加载到非交互式 shell 中。将以下内容添加到您的 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）：

```bash
# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

或者直接在当前会话中运行：

```bash
source ~/.nvm/nvm.sh
```

**替代方案：调整 PATH 顺序**

如果 nvm 已正确加载，但 Windows 路径仍然优先，您可以在 shell 配置中显式地将 Linux 路径添加到 PATH 之前：

```bash
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

**警告**

避免通过 `appendWindowsPath = false` 禁用 Windows PATH 导入，因为这会破坏从 WSL 调用 Windows 可执行文件的能力。同样，如果您将 Windows 用于 Windows 开发，请避免从 Windows 中卸载 Node.js。

### WSL2 沙箱设置

[沙盒](./sandboxing) 在 WSL2 上受支持，但需要安装其他软件包。如果您在运行 `/sandbox` 时看到类似“Sandbox require socat and bubblewrap”的错误，请安装依赖项：

### Ubuntu/Debian

```bash
sudo apt-get install bubblewrap socat
```

  
### 软呢帽

```bash
sudo dnf install bubblewrap socat
```

WSL1 不支持沙箱。如果您看到“沙盒需要 WSL2”，则需要升级到 WSL2 或在没有沙盒的情况下运行 Claude Code。

### 安装过程中出现权限错误

如果本机安装程序因权限错误而失败，则目标目录可能不可写。请参阅[检查目录权限](#check-directory-permissions)。

如果您之前使用 npm 安装并遇到了 npm 特定的权限错误，请切换到本机安装程序：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

## 权限和身份验证

这些部分解决登录失败、令牌问题和权限提示行为。

### 重复权限提示

如果您发现自己重复批准相同的命令，您可以允许特定工具
使用 `/permissions` 命令未经批准即可运行。请参阅[权限文档](./permissions#manage-permissions)。

### 身份验证问题

如果您遇到身份验证问题：

1. 运行`/logout`完全注销
2. 关闭Claude Code
3. 使用`claude`重新启动并再次完成身份验证过程

如果登录期间浏览器未自动打开，请按 `c` 将 OAuth URL 复制到剪贴板，然后手动将其粘贴到浏览器中。

### OAuth 错误：代码无效

如果您看到 `OAuth error: Invalid code. Please make sure the full code was copied`，则登录代码已过期或在复制粘贴过程中被截断。

**解决方案：*** 浏览器打开后按回车键重试并快速完成登录
* 如果浏览器没有自动打开，请输入 `c` 复制完整的 URL
* 如果使用远程/SSH 会话，浏览器可能会在错误的计算机上打开。复制终端中显示的 URL 并在本地浏览器中打开它。

### 403 登录后禁止

如果登录后看到 `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}`：

* **Claude Pro/Max 用户**：在 [claude.ai/settings](https://claude.ai/settings) 验证您的订阅是否有效
* **控制台用户**：确认您的帐户具有管理员分配的“Claude Code”或“开发人员”角色
* **代理背后**：公司代理可能会干扰 API 请求。有关代理设置，请参阅[网络配置](./network-config)。

### 有效订阅的“该组织已被禁用”

如果您在拥有有效的 Claude 订阅的情况下看到 `API Error: 400 ... "This organization has been disabled"`，则 `ANTHROPIC_API_KEY` 环境变量将覆盖您的订阅。当您的 shell 配置文件中仍然设置了来自前雇主或项目的旧 API 密钥时，通常会发生这种情况。

当 `ANTHROPIC_API_KEY` 存在并且您已批准它时，Claude Code 将使用该密钥而不是您订阅的 OAuth 凭据。在非交互模式 (`-p`) 下，密钥存在时始终使用。有关完整解析顺序，请参阅[身份验证优先级](./authentication#authentication-precedence)。

要使用您的订阅，请取消设置环境变量并将其从 shell 配置文件中删除：

```bash
unset ANTHROPIC_API_KEY
claude
```

检查 `~/.zshrc`、`~/.bashrc` 或 `~/.profile` 中的 `export ANTHROPIC_API_KEY=...` 线路并将其删除以使更改永久生效。在 Claude Code 内运行 `/status` 以确认哪种身份验证方法处于活动状态。

### OAuth 在 WSL2 中登录失败

如果 WSL 无法打开 Windows 浏览器，则 WSL2 中基于浏览器的登录可能会失败。设置 `BROWSER` 环境变量：

```bash
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

或者手动复制 URL：出现登录提示时，按 `c` 复制 OAuth URL，然后将其粘贴到 Windows 浏览器中。

### “未登录”或令牌已过期

如果 Claude Code 在会话后提示您重新登录，则您的 OAuth 令牌可能已过期。

运行 `/login` 重新进行身份验证。如果这种情况经常发生，请检查您的系统时钟是否准确，因为令牌验证取决于正确的时间戳。

## 配置文件位置

Claude Code 将配置存储在多个位置：|文件|目的|
| :---------------------------- | :-------------------------------------------------------------------------------------------------------- |
| `~/.claude/settings.json` |用户设置（权限、挂钩、模型覆盖）|
| `.claude/settings.json` |项目设置（签入源代码管理）|
| `.claude/settings.local.json` |本地项目设置（未提交）|
| `~/.claude.json` |全局状态（主题、OAuth、MCP 服务器）|
| `.mcp.json` |项目 MCP 服务器（已签入源代码管理） |
| `managed-mcp.json` | [托管 MCP 服务器](./mcp#managed-mcp-configuration) |
|托管设置 | [托管设置](./settings#settings-files)（服务器管理、MDM/操作系统级策略或基于文件）|

在 Windows 上，`~` 指的是您的用户主目录，例如 `C:\Users\YourName`。

有关配置这些文件的详细信息，请参阅[设置](./settings)和[MCP](./mcp)。

### 重置配置

要将 Claude Code 重置为默认设置，您可以删除配置文件：

```bash
# Reset all user settings and state
rm ~/.claude.json
rm -rf ~/.claude/

# Reset project-specific settings
rm -rf .claude/
rm .mcp.json
```

**警告**

这将删除您的所有设置、MCP 服务器配置和会话历史记录。

## 性能和稳定性

这些部分涵盖与资源使用、响应能力和搜索行为相关的问题。

### CPU 或内存使用率过高

Claude Code 设计用于大多数开发环境，但在处理大型代码库时可能会消耗大量资源。如果您遇到性能问题：

1. 定期使用`/compact`来减少上下文大小
2. 在主要任务之间关闭并重新启动 Claude Code
3. 考虑将大型构建目录添加到 `.gitignore` 文件中

### 命令挂起或冻结

如果 Claude Code 似乎没有响应：

1. 按Ctrl+C尝试取消当前操作
2. 如果没有响应，您可能需要关闭终端并重新启动

### 搜索和发现问题

如果搜索工具 `@file` 提到自定义代理和自定义技能不起作用，请安装系统 `ripgrep`：

```bash
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

然后在您的[环境](./env-vars)中设置`USE_BUILTIN_RIPGREP=0`。

### WSL 上的搜索结果缓慢或不完整

[在 WSL 上跨文件系统工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems) 时的磁盘读取性能损失可能会导致在 WSL 上使用 Claude Code 时匹配次数少于预期。搜索仍然有效，但返回的结果比本机文件系统少。

**注意**

在这种情况下，`/doctor` 将显示搜索正常。

**解决方案：**

1. **提交更具体的搜索**：通过指定目录或文件类型来减少搜索的文件数量：“在auth-service包中搜索JWT验证逻辑”或“在JS文件中查找md5哈希的使用”。2. **将项目移动到 Linux 文件系统**：如果可能，请确保您的项目位于 Linux 文件系统 (`/home/`)，而不是 Windows 文件系统 (`/mnt/c/`)。

3. **改用本机 Windows**：考虑在 Windows 上本机运行 Claude Code，而不是通过 WSL，以获得更好的文件系统性能。

## IDE 集成问题

如果 Claude Code 无法连接到 IDE 或在 IDE 终端中行为异常，请尝试以下解决方案。

### JetBrains IDE 在 WSL2 上未检测到

如果您在带有 JetBrains IDE 的 WSL2 上使用 Claude Code 并收到“未检测到可用的 IDE”错误，这可能是由于 WSL2 的网络配置或 Windows 防火墙阻止了连接。

#### WSL2 网络模式

WSL2 默认使用 NAT 网络，这可以防止 IDE 检测。您有两个选择：

**选项 1：配置 Windows 防火墙**（推荐）

1. 找到您的 WSL2 IP 地址：
   ```bash 
   wsl hostname -I
   # Example output: 172.21.123.45
   ```

2. 以管理员身份打开 PowerShell 并创建防火墙规则：
   ```powershell 
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   根据步骤 1 中的 WSL2 子网调整 IP 范围。

3. 重新启动 IDE 和 Claude Code

**选项 2：切换到镜像网络**

添加到 Windows 用户目录中的 `.wslconfig`：

```ini
[wsl2]
networkingMode=mirrored
```

然后使用 PowerShell 中的 `wsl --shutdown` 重新启动 WSL。

**注意**

这些网络问题仅影响 WSL2。 WSL1 直接使用主机的网络，不需要这些配置。

有关其他 JetBrains 配置提示，请参阅 [JetBrains IDE 指南](./jetbrains#plugin-settings)。

### 报告 Windows IDE 集成问题

如果您在 Windows 上遇到 IDE 集成问题，请使用以下信息[创建问题](https://github.com/anthropics/claude-code/issues)：

* 环境类型：本机 Windows (Git Bash) 或 WSL1/WSL2
* WSL 网络模式（如果适用）：NAT 或镜像
* IDE名称和版本
* Claude Code 扩展/插件版本
* Shell类型：Bash、Zsh、PowerShell等

### 退出键在 JetBrains IDE 终端中不起作用

如果您在 JetBrains 终端中使用 Claude Code，并且 `Esc` 键未按预期中断代理，这可能是由于与 JetBrains 的默认快捷键发生键绑定冲突。

要解决此问题：

1. 进入设置 → 工具 → 终端
2. 要么：
   * 取消选中“使用 Escape 将焦点移至编辑器”，或者
   * 单击“配置终端键绑定”并删除“将焦点切换到编辑器”快捷方式
3. 应用更改

这允许 `Esc` 密钥正确中断 Claude Code 操作。

## Markdown 格式问题

Claude Code 有时会生成代码围栏上缺少语言标记的 Markdown 文件，这可能会影响 GitHub、编辑器和文档工具中的语法突出显示和可读性。

### 代码块中缺少语言标签

如果您在生成的 markdown 中注意到这样的代码块：

```
`markdown
```
函数示例() {
  返回“你好”；
}
```text
```
`

而不是正确标记的块，例如：

```
`markdown
```javascript
函数示例() {
  返回“你好”；
}
```text
```
`

**解决方案：**

1. **要求 Claude 添加语言标签**：请求“为该 markdown 文件中的所有代码块添加适当的语言标签”。2. **使用后处理挂钩**：设置自动格式化挂钩来检测和添加缺失的语言标签。有关 PostToolUse 格式化挂钩的示例，请参阅[编辑后自动格式化代码](./hooks-guide#auto-format-code-after-edits)。

3. **手动验证**：生成 Markdown 文件后，检查其代码块格式是否正确，并在需要时请求更正。

### 间距和格式不一致

如果生成的 markdown 有过多的空行或不一致的间距：

**解决方案：**

1. **请求格式更正**：要求 Claude“修复此 Markdown 文件中的间距和格式问题”。

2. **使用格式化工具**：设置挂钩以在生成的 Markdown 文件上运行 `prettier` 等 Markdown 格式化程序或自定义格式化脚本。

3. **指定格式首选项**：在提示或项目 [内存](./memory) 文件中包含格式要求。

### 减少 Markdown 格式问题

为了尽量减少格式问题：

* **在请求中明确**：要求“带有语言标记代码块的正确格式的降价”
* **使用项目约定**：在 [`CLAUDE.md`](./memory) 中记录您喜欢的 Markdown 样式
* **设置验证挂钩**：使用后处理挂钩自动验证并修复常见的格式问题

## 获得更多帮助

如果您遇到此处未涵盖的问题：

1. 在 Claude Code 中使用 `/feedback` 命令直接向 Anthropic 报告问题
2. 检查 [GitHub 存储库](https://github.com/anthropics/claude-code) 中的已知问题
3. 运行 `/doctor` 来诊断问题。它检查：
   * 安装类型、版本和搜索功能
   * 自动更新状态和可用版本
   * 无效的设置文件（格式错误的 JSON、类型不正确）
   * MCP服务器配置错误
   * 按键绑定配置问题
   * 上下文使用警告（大型 CLAUDE.md 文件、高 MCP 令牌使用、无法访问的权限规则）
   * 插件和代理加载错误
4. 直接向 Claude 询问其功能和特性 - Claude 具有对其文档的内置访问权限
