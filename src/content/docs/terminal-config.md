---
title: "优化您的终端设置"
order: 51
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "当您的终端配置正确时，Claude Code 效果最佳。请遵循这些指南来优化您的体验。"
sourceUrl: "https://code.claude.com/docs/en/terminal-config.md"
sourceTitle: "Optimize your terminal setup"
tags: []
---
# 优化你的终端设置

> 当您的终端配置正确时，Claude Code 效果最佳。请遵循这些指南来优化您的体验。

### 主题和外观

Claude 无法控制您终端的主题。这是由您的终端应用程序处理的。您可以随时通过 `/config` 命令将 Claude Code 的主题与您的终端匹配。

要对 Claude Code 界面本身进行其他自定义，您可以配置[自定义状态行](./statusline) 以在终端底部显示上下文信息，例如当前模型、工作目录或 git 分支。

### 换行

您可以通过多种方式在 Claude Code 中输入换行符：

* **快速转义**：键入 `\`，然后按 Enter 键以创建换行符
* **Shift+Enter**：在 iTerm2、WezTerm、Ghostty 和 Kitty 中开箱即用
* **键盘快捷键**：设置键绑定以在其他终端中插入换行符

**为其他终端设置 Shift+Enter**

在 Claude Code 中运行 `/terminal-setup`，以自动为 VS Code、Alacritty、Zed 和 Warp 配置 Shift+Enter。

**注意**

`/terminal-setup` 命令仅在需要手动配置的终端中可见。如果您使用的是 iTerm2、WezTerm、Ghostty 或 Kitty，您将看不到此命令，因为 Shift+Enter 已经可以在本机使用。

**设置 Option+Enter（VS Code、iTerm2 或 macOS Terminal.app）**

**对于 Mac Terminal.app：**

1. 打开设置 → 配置文件 → 键盘
2. 勾选“使用选项作为元键”

**对于 iTerm2：**

1. 打开设置 → 配置文件 → 按键
2. 在常规下，将左/右选项键设置为“Esc+”

**对于 VS Code 终端：**

在 VS Code 设置中设置 `"terminal.integrated.macOptionIsMeta": true`。

### 通知设置

当 Claude 完成工作并等待您的输入时，它会触发通知事件。您可以通过终端将此事件显示为桌面通知，或使用[通知挂钩](./hooks#notification) 运行自定义逻辑。

#### 终端通知

Kitty 和 Ghostty 支持桌面通知，无需额外配置。 iTerm 2 需要设置：

1. 打开 iTerm 2 设置 → 配置文件 → 终端
2. 启用“通知中心警报”
3. 单击“过滤警报”并选中“发送转义序列生成的警报”

如果未显示通知，请验证您的终端应用程序在操作系统设置中是否具有通知权限。

其他终端，包括默认的 macOS 终端，不支持本机通知。请改用[通知挂钩](./hooks#notification)。

#### 通知挂钩

要在通知触发时添加自定义行为（例如播放声音或发送消息），请配置 [通知挂钩](./hooks#notification)。挂钩与终端通知一起运行，而不是作为替代品。

### 处理大量输入

当使用大量代码或长指令时：

* **避免直接粘贴**：Claude Code 可能会难以处理很长的粘贴内容
* **使用基于文件的工作流程**：将内容写入文件并要求 Claude 读取它
* **注意 VS Code 限制**：VS Code 终端特别容易截断长粘贴

### Vim 模式Claude Code 支持 Vim 键绑定的子集，可以使用 `/vim` 启用或通过 `/config` 配置。

支持的子集包括：

* 模式切换：`Esc`（至 NORMAL）、`i`/`I`、`a`/`A`、`o`/`O`（至 INSERT）
* 导航：`h`/`j`/`k`/`l`、`w`/`e`/`b`、`0`/`$`/`^`、 `gg`/`G`、`f`/`F`/`t`/`T` 以及 `;`/`,` 重复
* 编辑：`x`、`dw`/`de`/`db`/`dd`/`D`、`cw`/`ce`/`cb`/`cc`/`C`、 `.`（重复）
* 复制/粘贴：`yy`/`Y`、`yw`/`ye`/`yb`、`p`/`P`
* 文本对象：`iw`/`aw`、`iW`/`aW`、`i"`/`a"`、`i'`/`a'`、`i(`/`a(`、 `i[`/`a[`、`i{`/`a{`
* 压痕：`>>`/`<<`
* 线路操作：`J`（加入线路）

有关完整参考，请参阅[交互模式](./interactive-mode#vim-editor-mode)。
