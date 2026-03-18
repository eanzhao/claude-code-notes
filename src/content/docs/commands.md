---
title: "内置命令"
order: 58
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "Claude Code 中提供的内置命令的完整参考。"
sourceUrl: "https://code.claude.com/docs/en/commands.md"
sourceTitle: "Built-in commands"
tags: []
---
# 内置命令

> Claude Code 内置命令的完整参考。

在 Claude Code 中输入 `/` 可以查看所有可用命令，也可以在 `/` 后面输入字母来过滤。并非所有命令对每个用户都可见，有些取决于你的平台、套餐或环境。例如，`/desktop` 仅在 macOS 和 Windows 上出现，`/upgrade` 和 `/privacy-settings` 仅在 Pro 和 Max 套餐中可用，当你的终端原生支持其键绑定时 `/terminal-setup` 会隐藏。

Claude Code 还内置了[捆绑技能](./skills#bundled-skills)，如 `/simplify`、`/batch` 和 `/debug`，输入 `/` 时会和内置命令一起显示。要创建你自己的命令，请参阅[技能](./skills)。

下表中，`<arg>` 表示必填参数，`[arg]` 表示可选参数。

| 命令 | 用途 |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/add-dir ` | 为当前会话添加新的工作目录 |
| `/agents` | 管理[代理](./sub-agents)配置 |
| `/btw <question>` | 快速提个[附带问题](./interactive-mode#side-questions-with-btw)，不会加入对话上下文 |
| `/chrome` | 配置 [Chrome 中的 Claude](./chrome) 设置 |
| `/clear` | 清空对话历史并释放上下文。别名：`/reset`、`/new` |
| `/color [color\|default]` | 设置当前会话的提示栏颜色。可选：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink`、`cyan`。用 `default` 重置 |
| `/compact [instructions]` | 压缩对话，可附带可选的聚焦指令 |
| `/config` | 打开[设置](./settings)界面，调整主题、模型、[输出风格](./output-styles)等偏好。别名：`/settings` |
| `/context` | 以彩色网格可视化当前上下文使用情况，并显示针对上下文密集型工具、内存膨胀和容量警告的优化建议 |
| `/copy [N]` | 复制最后一条助手回复到剪贴板。传入数字 `N` 可复制第 N 条最新回复：`/copy 2` 复制倒数第二条。有代码块时会弹出交互式选择器，让你选择单个代码块或完整回复 |
| `/cost` | 显示 token 使用统计。详见[成本跟踪指南](./costs#using-the-cost-command) |
| `/desktop` | 在 Claude Code 桌面应用中继续当前会话。仅限 macOS 和 Windows。别名：`/app` |
| `/diff` | 打开交互式 diff 查看器，显示未提交的更改和每轮 diff。用左/右箭头在当前 git diff 和单个 Claude 轮次之间切换，用上/下箭头浏览文件 |
| `/doctor` | 诊断并验证你的 Claude Code 安装和设置 |
| `/effort [low\|medium\|high\|max\|auto]` | 设置模型[工作量级别](./model-config#adjust-effort-level)。`low`、`medium`、`high` 在会话间保留。`max` 仅限当前会话且需要 Opus 4.6。`auto` 重置为模型默认值。不带参数则显示当前级别。立即生效，无需等待当前回复完成 |
| `/exit` | 退出 CLI。别名：`/quit` |
| `/export [filename]` | 将当前对话导出为纯文本。指定文件名则直接写入该文件，否则弹出对话框供你复制到剪贴板或保存到文件 |
| `/extra-usage` | 配置额外用量，在达到速率限制时继续工作 |
| `/fast [on\|off]` | 开启或关闭[快速模式](./fast-mode) |
| `/feedback [report]` | 提交关于 Claude Code 的反馈。别名：`/bug` |
| `/branch [name]` | 在当前时刻创建对话的分支。别名：`/fork` |
| `/help` | 显示帮助和可用命令 |
| `/hooks` | 查看工具事件的 [hook](./hooks) 配置 |
| `/ide` | 管理 IDE 集成并显示状态 |
| `/init` | 用 `CLAUDE.md` 指引初始化项目。设置 `CLAUDE_CODE_NEW_INIT=true` 可启用交互式流程，还会遍历技能、hook 和个人内存文件 |
| `/insights` | 生成分析报告，涵盖你的 Claude Code 会话的项目区域、交互模式和痛点 |
| `/install-github-app` | 为仓库设置 [Claude GitHub Actions](./github-actions) 应用。引导你选择仓库并配置集成 |
| `/install-slack-app` | 安装 Claude Slack 应用。会打开浏览器完成 OAuth 流程 |
| `/keybindings` | 打开或创建你的键绑定配置文件 |
| `/login` | 登录 Anthropic 账户 |
| `/logout` | 退出 Anthropic 账户 |
| `/mcp` | 管理 MCP 服务器连接和 OAuth 认证 |
| `/memory` | 编辑 `CLAUDE.md` 内存文件、启用/禁用[自动内存](./memory#auto-memory)，以及查看自动内存条目 |
| `/mobile` | 显示二维码，下载 Claude 移动应用。别名：`/ios`、`/android` |
| `/model [model]` | 选择或切换 AI 模型。对于支持的模型，可用左/右箭头[调整工作量级别](./model-config#adjust-effort-level)。立即生效，无需等待当前回复完成 |
| `/passes` | 与朋友分享一周免费的 Claude Code。仅在你的账户符合条件时可见 |
| `/permissions` | 查看或更新[权限](./permissions#manage-permissions)。别名：`/allowed-tools` |
| `/plan` | 直接从提示进入计划模式 |
| `/plugin` | 管理 Claude Code [插件](./plugins) |
| `/pr-comments [PR]` | 从 GitHub PR 获取并显示评论。自动检测当前分支的 PR，也可传入 PR URL 或编号。需要 `gh` CLI |
| `/privacy-settings` | 查看和更新隐私设置。仅限 Pro 和 Max 套餐 |
| `/release-notes` | 查看完整变更日志，最新版本排在最前面 |
| `/reload-plugins` | 重新加载所有活动的[插件](./plugins)以应用待处理的更改，无需重启。会报告每个重新加载组件的数量并标记加载错误 |
| `/remote-control` | 让此会话可被 claude.ai [远程控制](./remote-control)。别名：`/rc` |
| `/remote-env` | 配置[通过 `--remote` 启动的远程会话](./claude-code-on-the-web#environment-configuration)的默认远程环境 |
| `/rename [name]` | 重命名当前会话并在提示栏上显示名称。不传名称则从对话历史自动生成 |
| `/resume [session]` | 按 ID 或名称恢复对话，或打开会话选择器。别名：`/continue` |
| `/review` | 已弃用。请安装 [`code-review` 插件](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md)：`claude plugin install code-review@claude-code-marketplace` |
| `/rewind` | 将对话和/或代码倒回到某个之前的时间点，或从选定的消息开始总结。详见[检查点](./checkpointing)。别名：`/checkpoint` |
| `/sandbox` | 切换[沙盒模式](./sandboxing)。仅在支持的平台上可用 |
| `/security-review` | 分析当前分支上待提交的更改是否有安全漏洞，检查 git diff 并识别注入、认证问题和数据泄露等风险 |
| `/skills` | 列出可用的[技能](./skills) |
| `/stats` | 可视化每日使用情况、会话历史、连续使用天数和模型偏好 |
| `/status` | 打开设置界面（状态标签页），显示版本、模型、账户和连接信息 |
| `/statusline` | 配置 Claude Code 的[状态栏](./statusline)。描述你想要的样式，或不带参数运行以从 shell 提示符自动配置 |
| `/stickers` | 订购 Claude Code 贴纸 |
| `/tasks` | 列出和管理后台任务 |
| `/terminal-setup` | 配置 Shift+Enter 和其他快捷键的终端键绑定。仅在需要它的终端中可见，如 VS Code、Alacritty 或 Warp |
| `/theme` | 更改颜色主题。包括浅色和深色变体、色盲可访问（道尔顿化）主题以及使用终端调色板的 ANSI 主题 |
| `/upgrade` | 打开升级页面，切换到更高套餐 |
| `/usage` | 显示套餐用量限制和速率限制状态 |
| `/vim` | 在 Vim 和普通编辑模式之间切换 |
| `/voice` | 切换按住说话的[语音听写](./voice-dictation)。需要 Claude.ai 账户 |

## MCP 提示

MCP 服务器可以暴露显示为命令的提示。它们使用 `/mcp__<server>__` 格式，从已连接的服务器动态发现。详见 [MCP 提示](./mcp#use-mcp-prompts-as-commands)。

## 另请参阅

* [技能](./skills)：创建你自己的命令
* [交互模式](./interactive-mode)：键盘快捷键、Vim 模式和命令历史
* [CLI 参考](./cli-reference)：启动时 flag
