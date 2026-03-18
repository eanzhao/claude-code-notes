---
title: "JetBrains IDE"
order: 18
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "将 Claude Code 与 JetBrains IDE 结合使用，包括 IntelliJ、PyCharm、WebStorm 等"
sourceUrl: "https://code.claude.com/docs/en/jetbrains.md"
sourceTitle: "JetBrains IDEs"
tags: []
---
# JetBrains IDE

> 将 Claude Code 与 JetBrains IDE 结合使用，包括 IntelliJ、PyCharm、WebStorm 等

Claude Code 通过专用插件与 JetBrains IDE 集成，提供交互式差异查看、选择上下文共享等功能。

## 支持的 IDE

Claude Code 插件适用于大多数 JetBrains IDE，包括：

* IntelliJ IDEA
* 皮查姆
* 安卓工作室
* 网络风暴
* PhpStorm
* 戈兰

## 特点

* **快速启动**：使用 `Cmd+Esc` (Mac) 或 `Ctrl+Esc` (Windows/Linux) 直接从编辑器打开 Claude Code，或单击 UI 中的 Claude Code 按钮
* **差异查看**：代码更改可以直接显示在 IDE 差异查看器中，而不是终端中
* **选择上下文**：IDE 中的当前选择/选项卡自动与 Claude Code 共享
* **文件引用快捷方式**：使用 `Cmd+Option+K` (Mac) 或 `Alt+Ctrl+K` (Linux/Windows) 插入文件引用（例如，@File#L1-99）
* **诊断共享**：在您工作时，IDE 中的诊断错误（lint、语法等）会自动与 Claude 共享

## 安装

### 市场安装

从 JetBrains 市场查找并安装 [Claude Code 插件](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，然后重新启动 IDE。

如果您尚未安装 Claude Code，请参阅[我们的快速入门指南](./quickstart) 了解安装说明。

**注意**

安装插件后，您可能需要完全重新启动 IDE 才能生效。

## 用法

### 从您的 IDE

从 IDE 的集成终端运行 `claude`，所有集成功能都将处于活动状态。

### 来自外部终端

在任何外部终端中使用 `/ide` 命令将 Claude Code 连接到 JetBrains IDE 并激活所有功能：

```bash
claude
```

```text
/ide
```

如果您希望 Claude 能够访问与 IDE 相同的文件，请从与 IDE 项目根目录相同的目录启动 Claude Code。

## 配置

### Claude Code 设置

通过 Claude Code 的设置配置 IDE 集成：

1. 运行`claude`
2. 输入`/config`命令
3. 将diff工具设置为`auto`以进行IDE自动检测

### 插件设置

通过转到 **设置 → 工具 → Claude Code \[Beta]** 配置 Claude Code 插件：

#### 常规设置

* **Claude 命令**：指定运行 Claude 的自定义命令（例如，`claude`、`/usr/local/bin/claude` 或 `npx @anthropic/claude`）
* **抑制未找到 Claude 命令的通知**：跳过有关未找到 Claude 命令的通知
* **启用使用 Option+Enter 进行多行提示**（仅限 macOS）：启用后，Option+Enter 会在 Claude Code 提示中插入新行。如果遇到意外捕获选项密钥的问题，请禁用（需要重新启动终端）
* **启用自动更新**：自动检查并安装插件更新（重新启动时应用）

**提示**

对于 WSL 用户：将 `wsl -d Ubuntu -- bash -lic "claude"` 设置为 Claude 命令（将 `Ubuntu` 替换为您的 WSL 发行版名称）

#### ESC 键配置

如果 ESC 键不会中断 JetBrains 终端中的 Claude Code 操作：1. 转到 **设置 → 工具 → 终端**
2. 要么：
   * 取消选中“使用 Escape 将焦点移至编辑器”，或者
   * 单击“配置终端键绑定”并删除“将焦点切换到编辑器”快捷方式
3. 应用更改

这允许 ESC 键正确中断 Claude Code 操作。

## 特殊配置

### 远程开发

**警告**

使用 JetBrains 远程开发时，必须通过**设置 → 插件（主机）** 在远程主机中安装插件。

该插件必须安装在远程主机上，而不是本地客户端计算机上。

### WSL 配置

**警告**

WSL 用户可能需要额外的配置才能使 IDE 检测正常工作。请参阅我们的 [WSL 故障排除指南](./troubleshooting#jetbrains-ide-not-detected-on-wsl2) 了解详细的设置说明。

WSL 配置可能需要：

* 正确的终端配置
* 联网模式调整
* 防火墙设置更新

## 故障排除

### 插件不工作

* 确保您正在从项目根目录运行 Claude Code
* 检查 IDE 设置中是否启用了 JetBrains 插件
* 完全重新启动IDE（您可能需要多次执行此操作）
* 对于远程开发，请确保插件已安装在远程主机中

### 未检测到 IDE

* 验证插件是否已安装并启用
* 完全重新启动IDE
* 检查您是否正在从集成终端运行 Claude Code
* 对于 WSL 用户，请参阅[WSL 故障排除指南](./troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### 未找到命令

如果单击 Claude 图标显示“未找到命令”：

1. 验证 Claude Code 是否已安装：`npm list -g @anthropic-ai/claude-code`
2. 在插件设置中配置Claude命令路径
3. 对于WSL用户，使用配置部分提到的WSL命令格式

## 安全考虑

当 Claude Code 在启用了自动编辑权限的 JetBrains IDE 中运行时，它可能能够修改可由 IDE 自动执行的 IDE 配置文件。这可能会增加在自动编辑模式下运行 Claude Code 的风险，并允许绕过 Claude Code 的 bash 执行权限提示。

在 JetBrains IDE 中运行时，请考虑：

* 采用手动审批模式进行编辑
* 特别注意确保 Claude 仅在可信提示下使用
* 了解 Claude Code 有权修改哪些文件

如需其他帮助，请参阅我们的[故障排除指南](./troubleshooting)。
