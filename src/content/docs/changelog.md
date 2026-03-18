---
title: "变更日志"
order: 3
section: "getting-started"
sectionLabel: "快速入门"
sectionOrder: 1
summary: "Claude Code 的发行说明，包括按版本划分的新功能、改进和错误修复。"
sourceUrl: "https://code.claude.com/docs/en/changelog.md"
sourceTitle: "Changelog"
tags: []
---
# 变更日志

> Claude Code 的发行说明，包括按版本划分的新功能、改进和错误修复。

此页面是从 [GitHub 上的 CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) 生成的。

运行 `claude --version` 检查您安装的版本。

## v2.1.78（2026年3月17日）* 添加了 `StopFailure` 挂钩事件，该事件在回合由于 API 错误（速率限制、身份验证失败等）而结束时触发
* 为插件持久状态添加了 `${CLAUDE_PLUGIN_DATA}` 变量，该变量在插件更新后仍然存在； `/plugin uninstall` 删除前提示
* 添加了对插件传送代理的 `effort`、`maxTurns` 和 `disallowedTools` frontmatter 支持
* 当在 tmux 和 `set -g allow-passthrough on` 中运行时，终端通知（iTerm2/Kitty/Ghostty 弹出窗口、进度条）现在会到达外部终端
* 响应文本现在在生成时逐行流式传输
* 修复了 `git log HEAD` 在 Linux 上的沙盒 Bash 内因“模糊参数”而失败，以及存根文件污染工作目录中的 `git status`
* 修复了 `cc log` 和 `--resume` 在使用子代理的大型会话 (>5 MB) 上静默截断对话历史记录的问题
* 修复了当 API 错误触发停止钩子时的无限循环，该停止钩子将阻塞错误重新反馈给模型
* 修复了 `deny: ["mcp__servername"]` 权限规则在发送到模型之前不会删除 MCP 服务器工具，从而允许其查看并尝试阻止的工具
* 修复了 `sandbox.filesystem.allowWrite` 不适用于绝对路径的问题（之前需要 `//` 前缀）
* 修复了 `/sandbox` 依赖项选项卡，显示 macOS 上的 Linux 先决条件，而不是 macOS 特定信息
* **安全性：** 修复了设置 `sandbox.enabled: true` 但缺少依赖项时静默沙箱禁用的问题 - 现在显示可见的启动警告
* 修复了 `.git`、`.claude` 等受保护目录在 `bypassPermissions` 模式下无提示可写的问题
* 修复了正常模式滚动中的 ctrl+u 而不是 readlinekill-line（ctrl+u/ctrl+d 半页滚动仅移动到转录模式）
* 修复了语音模式修饰符组合按键通话键绑定（例如 ctrl+k）需要按住而不是立即激活
* 修复了语音模式在带有 WSLg (Windows 11) 的 WSL2 上不起作用的问题； WSL1/Win10 用户现在会收到明显的错误
* 修复了 `--worktree` 标志未从工作树目录加载技能和挂钩的问题
* 修复了 `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 和 `includeGitInstructions` 设置不抑制系统提示中的 git status 部分的问题
* 修复了从 Dock/Spotlight 启动 VS Code 时 Bash 工具找不到 Homebrew 和其他依赖于 PATH 的二进制文件的问题
* 修复了不宣传真彩色支持的 VS Code/光标/代码服务器终端中褪色的 Claude 橙色
* 添加了 `ANTHROPIC_CUSTOM_MODEL_OPTION` 环境变量，以向 `/model` 选择器添加自定义条目，并带有可选的 `_NAME` 和 `_DESCRIPTION` 后缀变量用于显示
* 修复了使用 Haiku 模型时 `ANTHROPIC_BETAS` 环境变量被默默忽略的问题
* 修复了在没有换行符的情况下连接排队提示的问题
* 改进了恢复大型会话时的内存使用情况和启动时间
* \[VSCode] 修复了在已通过身份验证的情况下打开侧边栏时登录屏幕短暂闪烁的问题
* \[VSCode] 修复了选择 Opus 时的“API 错误：达到速率限制” — 模型下拉列表不再向计划层级未知的订阅者提供 1M 上下文变体

## v2.1.77（2026年3月17日）* Claude Opus 4.6 的默认最大输出令牌限制增加到 64k 令牌，Opus 4.6 和 Sonnet 4.6 模型的上限增加到 128k 令牌
* 添加了 `allowRead` 沙箱文件系统设置以重新允许 `denyRead` 区域内的读取访问
* `/copy` 现在接受可选索引：`/copy N` 复制第 N 个最新的助理响应
* 修复了复合 bash 命令（例如 `cd src && npm test`）上的“始终允许”为完整字符串而不是每个子命令保存单个规则，从而导致死规则和重复的权限提示
* 修复了当斜杠命令覆盖重复打开和关闭时自动更新程序开始重叠二进制下载，累积数十 GB 内存的问题
* 修复了 `--resume` 由于内存提取写入和主记录之间的竞争而默默地截断最近的对话历史记录的问题
* 修复了 PreToolUse 挂钩返回 `"allow"` 绕过 `deny` 权限规则的问题，包括企业托管设置
* 修复了写入工具在覆盖 CRLF 文件或在 CRLF 目录中创建文件时以静默方式转换行结尾的问题
* 修复了长时间运行的会话中因压缩中幸存的进度消息而导致的内存增长
* 修复了当 API 回退到非流模式时无法跟踪成本和令牌使用情况的问题
* 修复了 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 未剥离 beta 工具架构字段，导致代理网关拒绝请求的问题
* 修复了当系统临时目录路径包含空格时 Bash 工具报告成功命令的错误
* 修复了粘贴后立即输入时粘贴丢失的问题
* 修复了 `/feedback` 文本输入中的 Ctrl+D 向前删除而不是按第二次退出会话的问题
* 修复了将 0 字节图像文件拖入提示时出现的 API 错误
* 修复了 Claude Desktop 会话错误地使用终端 CLI 配置的 API 密钥而不是 OAuth
* 修复了同一 monorepo 提交的不同子目录中的 `git-subdir` 插件在插件缓存中发生冲突的问题
* 修复了未在终端 UI 中呈现的有序列表编号
* 修复了一个竞争条件，其中陈旧工作树清理可能会删除刚刚从上次崩溃中恢复的代理工作树
* 修复了代理运行时打开 `/mcp` 或类似对话框时的输入死锁问题
* 修复了退格键和删除键在 vim NORMAL 模式下不起作用的问题
* 修复了打开或关闭 vim 模式时状态行不更新的问题
* 修复了在 VS Code、Cursor 和其他基于 xterm.js 的终端中 Cmd+click 上打开两次的超链接问题
* 修复了默认配置下 tmux 内的背景颜色渲染为终端默认的问题
* 修复了通过 SSH 选择 tmux 内的文本时 iTerm2 会话崩溃的问题
* 修复了 tmux 会话中剪贴板复制静默失败的问题；复制 toast 现在指示是否使用 `⌘V` 或 tmux `prefix+]` 进行粘贴
* 修复了 `←`/`→` 在导航列表时意外切换设置、权限和沙箱对话框中的选项卡的问题
* 修复了当 Claude Code 在 tmux 或屏幕内启动时 IDE 集成不会自动连接的问题
* 修复了 CJK 字符在右边缘被剪切时视觉上渗入相邻 UI 元素的问题
* 修正了领导者退出时队友面板不会关闭的问题* 修复了 iTerm2 自动模式无法检测本机拆分窗格队友的 iTerm2
* 通过在模块加载的同时读取钥匙串凭证，macOS 的启动速度更快（约 60 毫秒）
* 在 fork 繁重和非常大的会话上更快的 `--resume` — 加载速度提高 45%，峰值内存减少约 100-150MB
* 改进了 Esc 以中止正在进行的非流 API 请求
* 改进了 `claude plugin validate`，以检查技能、代理和命令前沿内容以及 `hooks/hooks.json`，捕获 YAML 解析错误和架构违规
* 现在，如果输出超过 5GB，后台 bash 任务就会被终止，从而防止失控进程填满磁盘
* 当您接受计划时，会话现在会根据计划内容自动命名
* 改进了无头模式插件安装，以便与 `CLAUDE_CODE_PLUGIN_SEED_DIR` 正确组合
* 当`apiKeyHelper`耗时超过10秒时显示通知，防止其阻塞主循环
* 代理工具不再接受 `resume` 参数 — 使用 `SendMessage({to: agentId})` 继续先前生成的代理
* `SendMessage` 现在会在后台自动恢复停止的代理，而不是返回错误
* 将 `/fork` 重命名为 `/branch`（`/fork` 仍可用作别名）
* \[VSCode] 改进了计划预览选项卡标题，以使用计划的标题而不是“Claude 的计划”
* \[VSCode] 当选项+单击未触发 macOS 上的本机选择时，页脚现在指向 `macOptionClickForcesSelection` 设置## v2.1.76（2026年3月14日）* 添加了 MCP 启发支持 - MCP 服务器现在可以通过交互式对话框（表单字段或浏览器 URL）请求结构化输入中间任务
* 添加了新的 `Elicitation` 和 `ElicitationResult` 挂钩，以在响应发送回之前拦截并覆盖响应
* 添加了 `-n` / `--name <name>` CLI 标志以设置启动时会话的显示名称
* 在大型 monorepos 中添加了 `claude --worktree` 的 `worktree.sparsePaths` 设置，以通过 git稀疏结帐仅签出您需要的目录
* 添加了 `PostCompact` 钩子，该钩子在压缩完成后触发
* 添加了 `/effort` 斜杠命令来设置模型工作量级别
* 添加了会话质量调查 - 企业管理员可以通过 `feedbackSurveyRate` 设置配置采样率
* 修复了延迟工具（通过 `ToolSearch` 加载）在对话压缩后丢失其输入模式，导致数组和数字参数因类型错误而被拒绝
* 修复了显示“未知技能”的斜杠命令
* 修复了计划被接受后要求重新批准的计划模式
* 修复了权限对话框或计划编辑器打开时语音模式吞咽按键的问题
* 修复了通过 npm 安装时 `/voice` 无法在 Windows 上运行的问题
* 修复了在 1M 上下文会话中使用 `model:` frontmatter 调用技能时出现的虚假“已达到上下文限制”
* 修复了使用非标准模型字符串时“此模型不支持自适应思维”的错误
* 修复了当带引号的参数包含 `#` 时 `Bash(cmd:*)` 权限规则不匹配的问题
* 修复了 Bash 权限对话框中的“不再询问”，显示管道和复合命令的完整原始命令
* 修复了自动压缩在连续失败后无限期重试的问题——断路器现在在 3 次尝试后停止
* 修复了 MCP 重新连接微调器在成功重新连接后仍然存在的问题
* 修复了在协调市场之前 LSP 管理器初始化时 LSP 插件不注册服务器的问题
* 修复了通过 SSH 在 tmux 中进行剪贴板复制的问题 - 现在尝试直接终端写入和 tmux 剪贴板集成
* 修复了 `/export` 在成功消息中仅显示文件名而不是完整文件路径的问题
* 修复了选择文本后文字记录不会自动滚动到新消息的问题
* 修复了 Escape 键无法退出登录方法选择屏幕的问题
* 修复了几个 Remote Control 问题：当服务器获得空闲环境时，会话会默默地终止，快速消息一次排队一个而不是批量，以及过时的工作项导致 JWT 刷新后重新传递
* 修复了扩展 WebSocket 断开连接后桥接会话无法恢复的问题
* 修复了输入软隐藏命令的确切名称时找不到斜杠命令的问题
* 通过直接读取 git refs 并在远程分支已在本地可用时跳过冗余 `git fetch`，改进了 `--worktree` 的启动性能
* 改进后台代理行为——杀死后台代理现在可以在对话上下文中保留其部分结果
* 改进的模型后备通知 - 现在始终可见，而不是隐藏在详细模式后面，并具有人性化的模型名称* 改进了深色终端主题上块引用的可读性 - 文本现在为斜体，带有左栏而不是暗色
* 改进了过时的工作树清理——并行运行中断后留下的工作树现在会自动清理
* 改进了 Remote Control 会话标题 - 现在源自您的第一个提示，而不是显示“交互式会话”
* 改进了 `/voice`，以在启用时显示您的听写语言，并在您的 `language` 设置不支持语音输入时发出警告
* 更新了 `--plugin-dir` 以仅接受一个路径来支持子命令 - 对多个目录使用重复的 `--plugin-dir`
* \[VSCode] 修复了包含逗号的 gitignore 模式，默默地从 @-mention 文件选择器中排除整个文件类型## v2.1.75（2026年3月13日）

* 默认为 Max、Team 和 Enterprise 计划添加 Opus 4.6 的 1M 上下文窗口（之前需要额外使用）
* 添加了 `/color` 命令，供所有用户为会话设置提示栏颜色
* 添加使用`/rename`时提示栏上显示会话名称
* 向内存文件添加了最后修改的时间戳，帮助 Claude 判断哪些内存是新鲜的，哪些是陈旧的
* 新增hook需要确认时权限提示中的hook来源显示（设置/插件/技能）
* 修复了在未切换 `/voice` 两次的情况下全新安装时语音模式无法正确激活的问题
* 修复了使用 `/model` 或 Option+P 切换型号后 Claude Code 标头不更新显示的型号名称的问题
* 修复了附件消息计算返回未定义值时会话崩溃的问题
* 修复了 Bash 工具在管道命令中损坏 `!`（例如，`jq 'select(.x != .y)'` 现在可以正常工作）
* 修复了 `/plugin`“已安装”选项卡中显示的托管禁用插件 — 由您的组织强制禁用的插件现在已隐藏
* 修复了思维和 `tool_use` 块的令牌估计过度计数，防止过早的上下文压缩
* 修复了损坏的市场配置路径处理
* 修复了 `/resume` 在恢复分叉或连续会话后丢失会话名称的问题
* 修复了访问“配置”选项卡后 Esc 未关闭 `/status` 对话框的问题
* 修复了接受或拒绝计划时的输入处理
* 修复了代理团队中的页脚提示，显示“↓ 展开”，而不是正确的“shift + ↓ 展开”
* 通过跳过不必要的子进程生成，提高了 macOS 非 MDM 计算机上的启动性能
* 默认情况下抑制异步挂钩完成消息（在 `--verbose` 或转录模式下可见）
* 重大更改：删除了 `C:\ProgramData\ClaudeCode\managed-settings.json` 处已弃用的 Windows 托管设置回退 — 使用 `C:\Program Files\ClaudeCode\managed-settings.json`

## v2.1.74（2026年3月12日）* 为 `/context` 命令添加了可操作的建议 - 通过特定的优化提示识别上下文繁重的工具、内存膨胀和容量警告
* 添加 `autoMemoryDirectory` 设置以配置自动内存存储的自定义目录
* 修复了生成器提前终止时未释放流式 API 响应缓冲区的内存泄漏，导致 Node.js/npm 代码路径上的 RSS 无限增长
* 修复了用户 `allow` 规则或技能 `allowed-tools` 绕过的托管策略 `ask` 规则
* 修复了在代理 frontmatter `model:` 字段和 `--agents` JSON 配置中默默忽略的完整模型 ID（例如 `claude-opus-4-5`）——代理现在接受与 `--model` 相同的模型值
* 修复了回调端口已在使用时 MCP OAuth 身份验证挂起的问题
* 修复了 MCP OAuth 刷新在刷新令牌过期后从不提示重新验证的问题，对于返回 HTTP 200 错误的 OAuth 服务器（例如 Slack）
* 修复了终端从未获得麦克风权限的用户在 macOS 本机二进制文件上语音模式无提示失败的问题 - 该二进制文件现在包含 `audio-input` 权利，因此 macOS 可以正确提示
* 修复了 `SessionEnd` 钩子在退出 1.5 秒后被杀死的问题，无论 `hook.timeout` 如何 - 现在可通过 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 进行配置
* 修复了 `/plugin install` 在 REPL 内针对具有本地源的市场插件失败的问题
* 修复了市场更新不同步 git 子模块的问题——子模块中的插件源在更新后不再中断
* 修复了带有参数的未知斜杠命令会默默地删除输入 - 现在将您的输入显示为警告
* 修复了希伯来语、阿拉伯语和其他 RTL 文本在 Windows 终端、conhost 和 VS Code 集成终端中无法正确呈现的问题
* 修复了由于文件 URI 格式错误而导致 LSP 服务器无法在 Windows 上运行的问题
* 更改了 `--plugin-dir`，因此本地开发副本现在会覆盖已安装的同名市场插件（除非该插件由托管设置强制启用）
* \[VSCode] 修复了删除按钮对无标题会话不起作用的问题
* \[VSCode] 通过终端感知加速改进了集成终端中的滚轮响应能力

## v2.1.73（2026年3月11日）* 添加了 `modelOverrides` 设置以将模型选择器条目映射到自定义提供商模型 ID（例如 Bedrock 推理配置文件 ARN）
* 添加了当 OAuth 登录或连接检查因 SSL 证书错误而失败时的可操作指南（公司代理、`NODE_EXTRA_CA_CERTS`）
* 修复了复杂 bash 命令的权限提示触发的冻结和 100% CPU 循环
* 修复了当许多技能文件同时更改时可能冻结 Claude Code 的死锁（例如，在具有大型 `.claude/skills/` 目录的存储库中的 `git pull` 期间）
* 修复了在同一项目目录中运行多个 Claude Code 会话时 Bash 工具输出丢失的问题
* 修复了 `model: opus`/`sonnet`/`haiku` 的子代理在 Bedrock、Vertex 和 Microsoft Foundry 上默默降级到旧型号版本的问题
* 修复了代理退出时子代理生成的后台 bash 进程未被清理的问题
* 修复了 `/resume` 在选择器中显示当前会话的问题
* 修复了自动安装扩展时 `/ide` 与 `onInstall is not defined` 一起崩溃的问题
* 修复了 `/loop` 在 Bedrock/Vertex/Foundry 上以及遥测禁用时不可用的问题
* 修复了通过 `--resume` 或 `--continue` 恢复会话时 SessionStart 挂钩触发两次的问题
* 修复了 JSON 输出挂钩在每回合将无操作系统提醒消息注入到模型上下文中的问题
* 修复了当慢速连接与新录音重叠时语音模式会话损坏的问题
* 修复了 Linux 沙箱在本机构建上无法启动并出现“ripgrep (rg) not found”的问题
* 修复了 Linux 本机模块无法在 Amazon Linux 2 和其他 glibc 2.26 系统上加载的问题
* 修复了通过 Remote Control 接收图像时的“media\_type: Field required”API 错误
* 修复了当桌面文件夹已存在时 `/heapdump` 在 Windows 上失败并出现 `EEXIST` 错误的问题
* 改进了中断 Claude 后的向上箭头 — 现在恢复中断的提示并一步倒回对话
* 提高启动时 IDE 检测速度
* 改进了 macOS 上的剪贴板图像粘贴性能
* 改进了 `/effort` 在 Claude 响应时工作，匹配 `/model` 行为
* 改进的语音模式可在快速一键通重按期间自动重试瞬时连接失败
* 改进了 Remote Control 生成模式选择提示，提供更好的上下文
* 将 Bedrock、Vertex 和 Microsoft Foundry 上的默认 Opus 模型更改为 Opus 4.6（原为 Opus 4.1）
* 已弃用 `/output-style` 命令 — 请改用 `/config`。现在，输出样式在会话开始时已修复，以实现更好的提示缓存
* VSCode：修复了代理后面或使用 Claude 4.5 型号的 Bedrock/Vertex 上的用户的 HTTP 400 错误

## v2.1.72（2026年3月10日）* 修复了只要设置了 `ENABLE_TOOL_SEARCH`，工具搜索即使使用 `ANTHROPIC_BASE_URL` 也会激活。
* 在 `/copy` 中添加了 `w` 密钥，以绕过剪贴板将焦点选择直接写入文件（通过 SSH 有用）
* 为 `/plan`（例如 `/plan fix the auth bug`）添加了可选描述参数，该参数进入计划模式并立即启动
* 添加了 `ExitWorktree` 工具以离开 `EnterWorktree` 会话
* 添加了 `CLAUDE_CODE_DISABLE_CRON` 环境变量以在会话中立即停止计划的 cron 作业
* 将 `lsof`、`pgrep`、`tput`、`ss`、`fd` 和 `fdfind` 添加到 bash 自动批准白名单中，减少常见只读操作的权限提示
* 恢复了代理工具上的 `model` 参数，用于每次调用模型覆盖
* 使用新符号 (○ ◐ ●) 和简短通知（而不是持久图标）将工作量级别简化为低/中/高（删除最大值）。使用 `/effort auto` 重置为默认值
* 改进了 `/config` - Escape 现在取消更改，Enter 保存并关闭，Space 切换设置
* 改进了向上箭头历史记录，以便在运行多个并发会话时首先显示当前会话的消息
* 改进了存储库名称和常见开发术语的语音输入转录准确性（正则表达式、OAuth、JSON）
* 通过切换到本机模块改进了 bash 命令解析 - 更快的初始化并且无内存泄漏
* 包大小减少了约 510 KB
* 更改了 CLAUDE.md HTML 注释 (`<!-- ... -->`)，使其在自动注入时对 Claude 隐藏。使用阅读工具阅读时评论仍然可见
* 修复后台任务或钩子响应缓慢时退出缓慢的问题
* 修复了代理任务进度停留在“正在初始化…”上的问题
* 当模型调用启用钩子的技能时，修复了技能钩子在每个事件中触发两次的问题
* 修复了几个语音模式问题：偶尔的输入延迟、释放一键通后错误的“未检测到语音”错误以及提交后重新填写提示的陈旧记录
* 修复了 `--continue` 无法从 `--compact` 之后的最近点恢复的问题
* 修复了 bash 安全解析边缘情况
* 添加了对不带 `.git` 后缀的市场 git URL 的支持（Azure DevOps、AWS CodeCommit）
* 改进了市场克隆失败消息，即使 git 不产生 stderr 也能显示诊断信息
* 修复了几个插件问题：Windows 安装失败，OneDrive 文件夹中出现 `EEXIST` 错误，当项目范围安装存在时，市场阻止用户范围安装，`CLAUDE_CODE_PLUGIN_CACHE_DIR` 创建文字 `~` 目录，以及 `plugin.json` 仅市场字段无法加载
* 修复了反馈调查在长时间会话中出现过于频繁的问题
* 修复了 `--effort` CLI 标志在启动时被无关设置写入重置的问题
* 修复了后台 Ctrl+B 查询在 `/clear` 之后丢失其记录或损坏新对话的问题
* 修复了 `/clear` 杀死后台代理/bash 任务的问题 — 现在仅清除前台任务
* 修复了工作树隔离问题：任务工具恢复不恢复 cwd，后台任务通知丢失 `worktreePath` 和 `worktreeBranch`
* 修复了 `/model` 在 Claude 工作时运行时不显示结果的问题* 修复了选择菜单选项的数字键，而不是在计划模式权限提示的文本输入中键入
* 修复沙箱权限问题：某些文件写入操作在没有提示的情况下被错误地允许，并且输出重定向到白名单目录（如 `/tmp/claude/`），不必要地提示
* 提高了长时间会话中的 CPU 利用率
* 修复了 SDK `query()` 调用中提示缓存失效的问题，将输入令牌成本降低高达 12 倍
* 修复了取消查询后 Escape 键变得无响应的问题
* 修复后台代理或任务运行时双Ctrl+C不退出的问题
* 修复团队代理继承领导者模型的问题
* 修复了“始终允许”保存权限规则不再匹配的问题
* 修复了几个挂钩问题：`transcript_path` 指向恢复/分叉会话的错误目录、在每次设置写入时从 settings.json 中默默删除代理 `prompt`、PostToolUse 阻止原因显示两次、异步挂钩未通过 bash `read -r` 接收标准输入，以及显示验证失败示例的验证错误消息
* 修复了读取包含 U+2028/U+2029 字符的返回文件时桌面/SDK 中的会话崩溃问题
* 修复了即使设置了 `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` 时终端标题也会在退出时被清除的问题
* 修复了多个权限规则匹配问题：通配符规则不匹配带有heredocs、嵌入换行符或无参数的命令； `sandbox.excludedCommands` 因 env var 前缀而失败； “始终允许”建议嵌套 CLI 工具使用过于宽泛的前缀；并拒绝不适用于所有命令形式的规则
* 修复了 Bash 数据 URL 输出中过大和截断的图像
* 修复了恢复包含 Bedrock API 错误的会话时发生的崩溃
* 修复了编辑、Bash 和 Grep 工具输入上间歇性的“预期布尔值，收到字符串”验证错误
* 修复了从第一条消息包含换行符的对话中分叉时的多行会话标题
* 修复了排队消息不显示附加图像以及按 ↑ 编辑排队消息时图像丢失的问题
* 修复了并行工具调用，其中失败的 Read/WebFetch/Glob 将取消其同级工具 - 现在只有 Bash 错误级联
* VSCode：修复了集成终端中的滚动速度与本机终端不匹配的问题
* VSCode：修复了 Shift+Enter 提交输入的问题，而不是为使用旧键绑定的用户插入换行符
* VSCode：在输入边框上添加了努力程度指示器
* VSCode：添加了 `vscode://anthropic.claude-code/open` URI 处理程序，以编程方式打开新的 Claude Code 选项卡，并带有可选的 `prompt` 和 `session` 查询参数## v2.1.71（2026年3月7日）* 添加了 `/loop` 命令以定期运行提示或斜线命令（例如 `/loop 5m check the deploy`）
* 添加了 cron 调度工具，用于在会话中重复提示
* 添加了 `voice:pushToTalk` 键绑定，使语音激活键可在 `keybindings.json` 中重新绑定（默认值：空格）——像 `meta+k` 这样的修饰符+字母组合具有零打字干扰
* 添加了 `fmt`、`comm`、`cmp`、`numfmt`、`expr`、`test`、`printf`、`getconf`、`seq`、`tsort` 和`pr` 加入 bash 自动批准白名单
* 修复了长时间运行会话中的标准输入冻结问题，其中击键停止处理，但进程保持活动状态
* 修复了启用语音模式的用户因 CoreAudio 初始化在系统唤醒后阻塞主线程而导致 5-8 秒启动冻结的问题
* 修复了当许多 claude.ai 代理连接器同时刷新过期的 OAuth 令牌时启动 UI 冻结的问题
* 修复了共享同一计划文件的分叉对话 (`/fork`)，这会导致一个分叉中的计划编辑覆盖另一个分叉中的计划编辑
* 修复了读取工具在图像处理失败时将超大图像放入上下文中的问题，从而在长时间的图像密集会话中中断后续回合
* 修复了包含heredoc提交消息的复合bash命令的误报权限提示
* 修复了运行多个 Claude Code 实例时插件安装丢失的问题
* 修复了 claude.ai 连接器在 OAuth 令牌刷新后无法重新连接的问题
* 修复了 claude.ai MCP 连接器启动通知出现在每个组织配置的连接器上的问题，而不是仅出现在之前连接的连接器上
* 修复了后台代理完成通知缺少输出文件路径，导致父代理在上下文压缩后难以恢复代理结果的问题
* 修复了当命令以非零状态退出时 Bash 工具错误消息中的重复输出
* 修复了 Chrome 扩展自动检测在没有本地 Chrome 的计算机上运行后永久卡在“未安装”状态的问题
* 修复了当市场固定到分支/标签引用时 `/plugin marketplace update` 因合并冲突而失败的问题
* 修复了 `/plugin marketplace add owner/repo@ref` 错误地解析 `@` — 以前只有 `#` 用作引用分隔符，导致 `strictKnownMarketplaces` 出现不可诊断的错误
* 修复了添加带或不带尾部斜杠的同一目录时 `/permissions` 工作区选项卡中的重复条目
* 修复了配置团队代理时 `--print` 永远挂起的问题 — 退出循环不再等待长期存在的 `in_process_teammate` 任务
* 修复了“❯工具已加载”的问题。每次 `ToolSearch` 调用后出现在 REPL 中
* 修复了模型使用 mingw 样式路径时在 Windows 上出现 `cd <cwd> && git ...` 的提示
* 通过将本机图像处理器加载推迟到首次使用来改进启动时间
* 改进了桥接会话重新连接，可在笔记本电脑从睡眠状态唤醒后几秒钟内完成，而不是等待 10 分钟
* 改进了 `/plugin uninstall` 以禁用 `.claude/settings.local.json` 中的项目范围插件，而不是修改 `.claude/settings.json`，因此更改不会影响队友* 改进的插件提供的 MCP 服务器重复数据删除 — 现在会跳过重复手动配置的服务器（相同命令/URL）的服务器，从而防止重复的连接和工具集。抑制显示在 `/plugin` 菜单中。
* 更新了 `/debug` 以在会话中切换调试日志记录，因为默认情况下不再写入调试日志
* 删除了未经身份验证的组织注册的 claude.ai 连接器的启动通知噪音## v2.1.70（2026年3月6日）* 修复了将 `ANTHROPIC_BASE_URL` 与第三方网关结合使用时的 API 400 错误 - 工具搜索现在可以正确检测代理端点并禁用 `tool_reference` 块
* 修复了使用自定义 Bedrock 推理配置文件或其他与标准 Claude 命名模式不匹配的模型标识符时的 `API Error: 400 This model does not support the effort parameter`
* 修复了 `ToolSearch` 之后立即出现的空模型响应 — 服务器在提示尾部渲染带有系统提示样式标签的工具模式，这可能会使模型感到困惑而提前停止
* 修复了当带有 `instructions` 的 MCP 服务器在第一回合后连接时提示缓存崩溃的问题
* 修复了通过慢速 SSH 连接输入时 Enter 插入换行符而不是提交的问题
* 使用 PowerShell `Set-Clipboard` 修复了剪贴板损坏 Windows/WSL 上的非 ASCII 文本（CJK、表情符号）的问题
* 修复了从 VS Code 集成终端运行时在 Windows 上启动时打开的额外 VS Code 窗口
* 修复了 Windows 本机二进制文件上语音模式失败的问题，并显示“本机音频模块无法加载”
* 修复了在设置中设置 `voiceEnabled: true` 时一键通无法在会话开始时激活的问题
* 修复了包含 `#NNN` 引用的 Markdown 链接错误地指向当前存储库而不是链接的 URL
* 修复了当项目的 `.claude/settings.json` 固定了旧版 Opus 模型字符串时重复的“模型已更新到 Opus 4.6”通知
* 修复了 `/plugin` 中显示安装不正确的插件
* 修正了插件在安装市场后自动刷新时显示“在市场中找不到”错误的问题
* 修复了 `/security-review` 命令在较旧的 git 版本上因 `unknown option merge-base` 而失败的问题
* 修复了 `/color` 命令无法重置回默认颜色的问题 - `/color default`、`/color gray`、`/color reset` 和 `/color none` 现在恢复默认颜色
* 修复了 `AskUserQuestion` 预览对话框中的性能回归，该对话框会在笔记输入中的每次击键时重新运行 Markdown 渲染
* 修复了早期启动期间读取的功能标志从不刷新其磁盘缓存，导致过时的值在会话中持续存在的问题
* 修复了在 Claude Code 远程环境中应用除 `acceptEdits` 或 `plan` 之外的 `permissions.defaultMode` 设置值 — 它们现在被忽略
* 修复了每个 `--resume` 上重新注入的技能列表（每份简历保存 600 个代币）
* 修复了传送标记在 VS Code 传送会话中不渲染的问题
* 改进了麦克风捕获静音时的错误消息，以区分“未检测到语音”
* 改进了压缩以保留摘要请求中的图像，允许快速重用缓存以实现更快、更便宜的压缩
* 改进了 `/rename` 在 Claude 处理时工作，而不是静默排队
* 回合中提示输入重新渲染减少了 74%
* 对于没有自定义 CA 证书的用户，启动内存减少了约 426KB
* 将 Remote Control `/poll` 速率降低至连接时每 10 分钟一次（为 1–2 秒），将服务器负载削减约 300 倍。重新连接不受影响——传输丢失会立即唤醒快速轮询。
* \[VSCode] 在 VS Code 活动栏中添加了 Spark 图标，列出了所有 Claude Code 会话，会话以完整编辑器的身份打开* \[VSCode] 为 VS Code 中的计划添加了完整的 Markdown 文档视图，支持添加评论以提供反馈
* \[VSCode] 添加了本机 MCP 服务器管理对话框 - 在聊天面板中使用 `/mcp` 来启用/禁用服务器、重新连接和管理 OAuth 身份验证，而无需切换到终端## v2.1.65（2026年3月5日）* 添加了 `/claude-api` 技能，用于使用 Claude API 和 Anthropic SDK 构建应用程序
* 在空 bash 提示符 (`!`) 上添加 Ctrl+U 以退出 bash 模式，匹配 `escape` 和 `backspace`
* 添加了数字键盘支持，用于在 Claude 的面试问题中选择选项（之前只有 QWERTY 上方的数字行有效）
* 向 `/remote-control` 和 `claude remote-control`（`/remote-control My Project` 或 `--name "My Project"`）添加了可选名称参数，以设置在 claude.ai/code 中可见的自定义会话标题
* 添加了对 10 种新语言（总共 20 种）的语音 STT 支持 - 俄语、波兰语、土耳其语、荷兰语、乌克兰语、希腊语、捷克语、丹麦语、瑞典语、挪威语
* 在徽标和微调器中添加了工作量级别显示（例如“低工作量”），以便更轻松地查看哪个工作量设置处于活动状态
* 添加使用 `claude --agent` 时终端标题中显示的代理名称
* 添加了 `sandbox.enableWeakerNetworkIsolation` 设置（仅限 macOS），以允许 `gh`、`gcloud` 和 `terraform` 等 Go 程序在使用自定义 MITM 代理与 `httpProxyPort` 时验证 TLS 证书
* 添加了 `includeGitInstructions` 设置（和 `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 环境变量），以从 Claude 的系统提示符中删除内置提交和 PR 工作流程说明
* 添加了 `/reload-plugins` 命令来激活挂起的插件更改而无需重新启动
* 添加了一次性启动提示，建议在 macOS 和 Windows 上使用 Claude Code 桌面（最多 3 次展示，可忽略）
* 添加了 `${CLAUDE_SKILL_DIR}` 变量，以便技能在 SKILL.md 内容中引用自己的目录
* 添加了 `InstructionsLoaded` 挂钩事件，该事件在 CLAUDE.md 或 `.claude/rules/*.md` 文件加载到上下文中时触发
* 添加了 `agent_id`（对于子代理）和 `agent_type`（对于子代理和 `--agent`）来挂钩事件
* 在 `--worktree` 会话中运行时，向状态行挂钩命令添加了 `worktree` 字段，其中包含名称、路径、分支和原始存储库目录
* 在托管设置中添加了 `pluginTrustMessage`，以将特定于组织的上下文附加到安装前显示的插件信任警告中
* 为团队计划 OAuth 用户（而不仅仅是企业用户）添加了策略限制获取（例如远程控制限制）
* 将 `pathPattern` 添加到 `strictKnownMarketplaces`，用于正则表达式匹配文件/目录市场源以及 `hostPattern` 限制
* 添加了插件源类型 `git-subdir` 以指向 git 存储库中的子目录
* 为 MCP 服务器添加了 `oauth.authServerMetadataUrl` 配置选项，以在标准发现失败时指定自定义 OAuth 元数据发现 URL
* 修复了嵌套技能发现可能从 gitignored 目录（如 `node_modules`）加载技能的安全问题
* 修复了信任对话框在首次运行时以静默方式启用所有 `.mcp.json` 服务器的问题。您现在将按预期看到每台服务器的批准对话框
* 修复了 `claude remote-control` 在使用“错误选项：--sdk-url”安装 npm 时立即崩溃的问题 (anthropics/claude-code#28334)
* 修复了 `--model claude-opus-4-0` 和 `--model claude-opus-4-1` 解析为已弃用的 Opus 版本而不是当前版本的问题
* 修复了使用多个 OAuth MCP 服务器时 macOS 钥匙串损坏的问题。大型 OAuth 元数据 blob 可能会溢出 `security -i` 标准输入缓冲区，默默地留下过时的凭据并导致重复的 `/login` 提示。* 修复了当配置文件端点在令牌刷新期间短暂失败时 `.credentials.json` 丢失 `subscriptionType`（显示“Claude API”而不是“Claude Pro”/“Claude Max”）的问题 (anthropics/claude-code#30185)
* 修复了在 Linux 上执行沙盒 Bash 命令后，幽灵点文件（`.bashrc`、`HEAD` 等）在工作目录中显示为未跟踪文件的问题
* 修复了 Shift+Enter 打印 `[27;2;13~` 而不是通过 SSH 在 Ghostty 中插入换行符的问题
* 修复了 Claude 工作时提交消息时存储 (Ctrl+S) 被清除的问题
* 修复了 ctrl+o（脚本切换）在进行大量文件编辑的长时间会话中冻结数秒的问题
* 修复了计划模式反馈输入不支持多行文本输入的问题（反斜杠+Enter 和 Shift+Enter 现在插入换行符）
* 修复了光标未向下移动到输入框顶部的空白行的问题
* 修复了当转录文件包含时间戳缺失或格式错误的条目时 `/stats` 崩溃的问题
* 修复了长时间会话中发生流式传输错误后的短暂挂起（记录被完全重写以删除一行；现在已就地截断）
* 修复`--setting-sources user`不阻止动态发现的项目技能
* 修复了从嵌套在其主存储库内的工作树运行时重复的 CLAUDE.md、斜线命令、代理和规则（例如 `claude -w`）
* 修复了插件 Stop/SessionEnd/etc 挂钩在任何 `/plugin` 操作后不会触发的问题
* 修复了当两个插件使用相同的 `${CLAUDE_PLUGIN_ROOT}/...` 命令模板时插件挂钩被默默删除的问题
* 修复了长时间运行的 SDK/CCR 会话中的内存泄漏问题，其中对话消息被不必要地保留
* 修复了恢复在工具批次中中断的会话时分叉代理（自动压缩、汇总）中的 API 400 错误
* 修复了恢复以孤立工具结果开始的对话时出现的“在工具\_结果块中发现意外的工具\_use\_id”错误
* 修复了队友通过代理工具的 `name` 参数意外生成嵌套队友的问题
* 修复了 `CLAUDE_CODE_MAX_OUTPUT_TOKENS` 在会话压缩期间被忽略的问题
* 修复了 `/compact` 摘要渲染为 SDK 使用者中的用户气泡的问题（Claude Code 远程 Web UI、VSCode 扩展）
* 修复了语音激活失败后语音空格键卡住的问题（模块加载竞赛、冷GrowthBook）
* 修复了 Windows 上的工作树文件副本
* 修复了 Windows 上的全局 `.claude` 文件夹检测
* 修复了符号链接绕过问题，其中通过符号链接父目录写入新文件可能会在 `acceptEdits` 模式下转义工作目录
* 修复了在托管设置中启用 `allowManagedDomainsOnly` 时提示用户批准非允许域的沙箱 — 不允许的域现在会自动阻止，不会绕过
* 修复了交互式工具（例如 `AskUserQuestion`）在技能的允许工具中列出时被静默自动允许，绕过权限提示并以空答案运行
* 修复了在工作树中提交大型未跟踪二进制文件时出现的多 GB 内存峰值
* 修正了当输入框有草稿文本时 Escape 不会中断正在运行的转弯。使用向上箭头将排队的消息拉回进行编辑，或使用 Ctrl+U 清除输入行。* 修复了在 Remote Control 会话中运行本地斜杠命令（`/voice`、`/cost`）时 Android 应用程序崩溃的问题
* 修复了长期会话中旧消息数组版本在 React Compiler `memoCache` 中累积的内存泄漏问题
* 修复了 REPL 渲染范围在长时间会话中累积的内存泄漏（超过 1000 回合约 35MB）
* 修复了进程中队友的内存保留问题，其中父级的完整对话历史记录被固定在队友的生命周期中，从而防止 `/clear` 或自动压缩后的 GC
* 修复了交互模式下的内存泄漏问题，其中挂钩事件在长时间会话期间可能会无限累积
* 修复了当 `--mcp-config` 指向损坏的文件时挂起的问题
* 修复安装过多技能/插件时启动缓慢的问题
* 修复了 `cd <outside-dir> && <cmd>` 权限提示以显示链接命令，而不是仅显示“是，允许从 `<dir>`/ 读取”
* 修复了条件 `.claude/rules/*.md` 文件（带有 `paths:` frontmatter）和嵌套 CLAUDE.md 文件未在打印模式下加载 (`claude -p`)
* 修复了 `/clear` 未完全清除所有会话缓存的问题，减少了长时间会话中的内存保留
* 修复了回滚边界处的动画元素导致的终端闪烁问题
* 修复了将 MCP 服务器与 OAuth 一起使用时 macOS 上的 UI 帧丢失问题（从 2.1.x 回归）
* 修复了同步调试日志刷新导致打字期间偶尔出现的帧停顿问题
* 修复 `TeammateIdle` 和 `TaskCompleted` 挂钩，以支持 `{"continue": false, "stopReason": "..."}` 停止队友，匹配 `Stop` 挂钩行为
* 修复了 `WorktreeCreate` 和 `WorktreeRemove` 插件挂钩被默默忽略的问题
* 修复了带有冒号的技能描述（例如，“触发器包括：X、Y、Z”）无法从 SKILL.md frontmatter 加载的问题
* 修复了没有 `description:` frontmatter 字段的项目技能未出现在 Claude 的可用技能列表中的问题
* 修复了 `/context` 显示服务器中所有 MCP 工具相同的令牌计数的问题
* 修复了模型在 Git Bash 中使用 CMD 样式 `2>nul` 重定向时在 Windows 上创建文字 `nul` 文件的问题
* 修复了扩展子代理记录视图 (Ctrl+O) 中每个工具调用下方出现的额外空白行
* 修复了当 `/config` 搜索框聚焦但为空时，选项卡/箭头键不会循环设置选项卡的问题
* 修复了服务密钥 OAuth 会话（CCR 容器）从配置文件范围端点向 `[ERROR]` 日志发送 403 垃圾邮件
* 修复了“Remote Control active”状态指示器颜色不一致的问题
* 修正了语音波形光标在听写中间输入时覆盖第一个后缀字母的问题
* 修正了语音输入在热身期间显示所有 5 个空格而不是上限为 \~2 （与“保持按住...”提示对齐）
* 通过将 50 毫秒动画循环与周围外壳隔离来提高旋转器性能，减少转弯期间的渲染和 CPU 开销
* 使用 React Compiler 改进了本机二进制文件中的 UI 渲染性能
* 通过消除启动路径上的 git 子进程来改进 `--worktree` 启动
* 通过消除托管设置解析时的冗余设置文件重新加载来改进 macOS 启动
* 通过跳过不必要的钥匙串查找，改进了 Claude.ai 企业/团队用户的 macOS 启动* 通过使用本地连接管道化 claude.ai 配置获取并使用并发池而不是顺序批处理，改进了 MCP `-p` 启动
* 通过消除导致重新渲染卡顿的难以察觉的预热脉冲动画来改进语音启动
* 改进了 MCP 二进制内容处理：返回 PDF、Office 文档或音频的工具现在将解码后的字节以正确的文件扩展名保存到磁盘，而不是将原始 base64 转储到对话上下文中。 WebFetch 还保存二进制响应及其摘要。
* 通过在消息更新过程中稳定 `onSubmit`，改善了长会话中的内存使用情况
* 改进了 LSP 工具渲染和内存上下文构建，不再读取整个文件
* 改进了会话上传和内存同步，以避免在大小/二进制检查之前将大文件读入内存
* 通过避免读取文件内容进行存在检查来提高文件操作性能（6 个站点）
* 改进了文档，以阐明 `--append-system-prompt-file` 和 `--system-prompt-file` 在交互模式下工作（文档之前仅提到打印模式）
* 通过推迟 Yoga WASM 预加载，将基线内存减少约 16MB
* 使用 Stream-json 输出减少 SDK 和 CCR 会话的内存占用
* 恢复大型会话时减少内存使用（包括压缩历史记录）
* 通过更简洁的子代理最终报告减少多代理任务上的令牌使用
* 将 Pro/Max/Team Premium 上的 Sonnet 4.5 用户更改为自动迁移到 Sonnet 4.6
* 更改了 `/resume` 选择器以显示最近的提示而不是第一个提示。这也解决了一些显示为 `(session)` 的标题。
* 更改了 claude.ai MCP 连接器故障以显示通知，而不是从工具列表中默默消失
* 更改了示例命令建议以确定性方式生成，而不是调用 Haiku
* 更改了压缩后的恢复，以便在继续之前不再生成前导码重述
* \[SDK] 更改了任务创建，不再需要 `activeForm` 字段 - 旋转器回退到任务主题
* \[VSCode] 添加压缩显示作为可折叠的“压缩聊天”卡，其中包含摘要
* \[VSCode] 权限模式选择器现在尊重有效 Claude Code 设置（包括托管/策略设置）中的 `permissions.disableBypassPermissionsMode` — 当设置为 `disable` 时，旁路权限模式对选择器隐藏
* \[VSCode] 修复了聊天面板中 RTL 文本（阿拉伯语、希伯来语、波斯语）渲染反转的问题（v2.1.63 中的回归）## v2.1.64（2026年3月4日）

* Opus 4.6 现在默认为 Max 和 Team 订阅者提供中等工作量。中等强度适用于大多数任务——这是速度和彻底性之间的最佳平衡点。您可以随时使用 `/model` 更改此设置
* 重新引入“ultrathink”关键词，为下一回合提供高度努力
* 在第一方 API 上从 Claude Code 中删除了 Opus 4 和 4.1 — 固定这些型号的用户将自动转移到 Opus 4.6

## 2.1.66（2026年3月4日）

* 减少虚假错误记录

## 2.1.63（2026年2月28日）

* 添加了 `/simplify` 和 `/batch` 捆绑斜杠命令
* 修复了本地斜杠命令输出（例如 /cost）在 UI 中显示为用户发送的消息而不是系统消息
* 项目配置和自动内存现在可以在同一存储库的 git 工作树之间共享
* 添加了 `ENABLE_CLAUDEAI_MCP_SERVERS=false` 环境变量以选择退出 claude.ai MCP 服务器可用
* 改进了 `/model` 命令以在斜杠命令菜单中显示当前活动模型
* 添加了 HTTP 挂钩，它可以将 JSON POST JSON 到 URL 并接收 JSON，而不是运行 shell 命令
* 修复了桥接轮询循环中的侦听器泄漏
* 修复了 MCP OAuth 流清理中的侦听器泄漏
* 在 MCP OAuth 身份验证期间添加了手动 URL 粘贴回退。如果自动本地主机重定向不起作用，您可以粘贴回调 URL 以完成身份验证。
* 修复了导航钩子配置菜单时的内存泄漏
* 修复了自动批准期间交互式权限处理程序中侦听器泄漏的问题
* 修复了忽略 glob 忽略模式的文件计数缓存
* 修复了 bash 命令前缀缓存中的内存泄漏
* 修复了服务器重新连接时的 MCP 工具/资源缓存泄漏问题
* 修复了 IDE 主机 IP 检测缓存错误地跨端口共享结果的问题
* 修复了传输重新连接时的 WebSocket 侦听器泄漏
* 修复了 git root 检测缓存中的内存泄漏，该泄漏可能导致长时间运行的会话无限增长
* 修复了 JSON 解析缓存中的内存泄漏问题，该缓存在长时间会话中无限增长
* VSCode：修复了远程会话未出现在对话历史记录中的问题
* 修复了 REPL 桥中的竞争条件，其中新消息可能会在初始连接刷新期间与历史消息交错到达服务器，从而导致消息排序问题。
* 修复了内存泄漏，即使在对话压缩之后，长时间运行的队友仍保留 AppState 中的所有消息
* 修复了内存泄漏，其中 MCP 服务器获取缓存在断开连接时未清除，导致频繁重新连接的服务器内存使用量增加
* 通过在上下文压缩期间剥离繁重的进度消息有效负载，改进了与子代理的长会话中的内存使用情况
* 向 `/copy` 选择器添加了“始终复制完整响应”选项。选择后，未来的 `/copy` 命令将跳过代码块选择器并直接复制完整响应。
* VSCode：添加会话重命名和删除会话列表操作
* 修复了 `/clear` 未重置缓存技能的问题，这可能导致过时的技能内容在新对话中持续存在

## 2.1.62（2026年2月27日）

* 修复提示建议缓存回归，降低缓存命中率## 2.1.61（2026年2月26日）

* 修复了 Windows 上并发写入损坏配置文件的问题

## 2.1.59（2026年2月26日）

* Claude 自动将有用的上下文保存到自动内存中。使用/内存进行管理
* 添加了 `/copy` 命令，以便在存在代码块时显示交互式选择器，从而允许选择单个代码块或完整响应。
* 改进了复合 bash 命令（例如 `cd /tmp && git fetch && git push`）的“始终允许”前缀建议，以计算更智能的每个子命令前缀，而不是将整个命令视为一个命令
* 改进了短任务列表的排序
* 通过释放已完成的子代理任务状态，改进了多代理会话中的内存使用情况
* 修复了同时运行多个 Claude Code 实例时 MCP OAuth 令牌刷新竞争状况
* 修复了删除工作目录时 shell 命令不显示明确错误消息的问题
* 修复了配置文件损坏，当多个 Claude Code 实例同时运行时可能会擦除身份验证

## 2.1.58（2026年2月25日）

* 将 Remote Control 扩展到更多用户

## 2.1.56（2026年2月25日）

* VS Code：修复了“未找到命令‘claude-vscode.editor.openLast’”崩溃的另一个原因

## v2.1.55（2026年2月25日）

* 修复了 BashTool 在 Windows 上失败并出现 EINVAL 错误的问题

## 2.1.53（2026年2月25日）

* 修复了用户输入在提交后、消息渲染之前会短暂消失的 UI 闪烁问题
* 修复了批量代理终止（ctrl+f）以发送单个聚合通知而不是每个代理一个，并正确清除命令队列
* 通过并行拆卸网络调用，修复了使用 Remote Control 时有时会留下陈旧会话的正常关闭问题
* 修复了 `--worktree` 有时在首次启动时被忽略的问题
* 修复了 Windows 上的恐慌（“打开损坏的值”）
* 修复了在 Windows 上生成许多进程时可能发生的崩溃
* 修复了 Linux x64 和 Windows x64 上 WebAssembly 解释器崩溃的问题
* 修复了Windows ARM64上有时2分钟后发生的崩溃

## 2.1.52（2026年2月24日）

* VS Code：修复了 Windows 上的扩展崩溃问题（“未找到命令 'claude-vscode.editor.openLast'”）

## 2.1.51（2026年2月24日）* 添加了用于外部构建的 `claude remote-control` 子命令，为所有用户提供本地环境服务。
* 将插件市场默认 git 超时从 30 秒更新为 120 秒，并添加 `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` 进行配置。
* 添加了对自定义 npm 注册表和从 npm 源安装插件时固定特定版本的支持
* 当 shell 快照可用时，BashTool 现在默认跳过登录 shell（`-l` 标志），从而提高命令执行性能。以前这需要设置 `CLAUDE_BASH_NO_LOGIN=true`。
* 修复了以下安全问题：在交互模式下，`statusLine` 和 `fileSuggestion` 挂钩命令可以在没有工作区信任接受的情况下执行。
* 大于 50K 字符的工具结果现在保存到磁盘（之前为 100K）。这减少了上下文窗口的使用并提高了对话的寿命。
* 修复了重复的 `control_response` 消息（例如来自 WebSocket 重新连接）可能通过将重复的助理消息推送到对话中而导致 API 400 错误的错误。
* 为 SDK 调用者添加了 `CLAUDE_CODE_ACCOUNT_UUID`、`CLAUDE_CODE_USER_EMAIL` 和 `CLAUDE_CODE_ORGANIZATION_UUID` 环境变量，以同步提供帐户信息，消除了早期遥测事件缺乏帐户元数据的竞争情况。
* 修复了当插件的 SKILL.md 描述是 YAML 数组或其他非字符串类型时斜杠命令自动完成崩溃的问题
* `/model` 选择器现在显示人类可读的标签（例如“Sonnet 4.5”），而不是固定模型版本的原始模型 ID，并在有新版本可用时显示升级提示。
* 现在可以通过 macOS plist 或 Windows 注册表设置托管设置。了解更多信息 [https://code.claude.com/docs/en/settings#settings-files](https://code.claude.com/docs/en/settings#settings-files)

## 2.1.50（2026年2月20日）* 添加了对 LSP 服务器的 `startupTimeout` 配置的支持
* 添加了 `WorktreeCreate` 和 `WorktreeRemove` 挂钩事件，以便在代理工作树隔离创建或删除工作树时启用自定义 VCS 设置和拆卸。
* 修复了当工作目录涉及符号链接时恢复的会话可能不可见的错误，因为会话存储路径在启动过程中的不同时间被解析。还通过在正常关闭序列中的挂钩和分析之前刷新会话数据，修复了 SSH 断开连接时的会话数据丢失问题。
* Linux：修复了本机模块无法在 glibc 早于 2.30 的系统上加载的问题（例如 RHEL 8）
*修复了代理团队中的内存泄漏，其中已完成的队友任务从未从会话状态中进行垃圾收集
* 修复了 `CLAUDE_CODE_SIMPLE` 以完全精简技能、会话内存、自定义代理和 CLAUDE.md 令牌计数
* 修复了 `/mcp reconnect` 在给定不存在的服务器名称时冻结 CLI 的问题
* 修复了内存泄漏，已完成的任务状态对象从未从 AppState 中删除
* 在代理定义中添加了对 `isolation: worktree` 的支持，允许代理以声明方式在隔离的 git 工作树中运行。
* `CLAUDE_CODE_SIMPLE` 模式现在还禁用 MCP 工具、附件、挂钩和 CLAUDE.md 文件加载，以获得完全最低限度的体验。
* 修复了启用工具搜索并且提示作为启动参数传入时未发现 MCP 工具的错误
* 通过压缩后清除内部缓存来改善长时间会话期间的内存使用情况
* 添加了 `claude agents` CLI 命令来列出所有已配置的代理
* 通过在处理大型工具结果后清除它们，改善了长时间会话期间的内存使用情况
* 修复了 LSP 诊断数据在交付后从未清理的内存泄漏，导致长会话中内存无限增长
* 修复了已完成的任务输出未从内存中释放的内存泄漏，减少了具有许多任务的长会话中的内存使用量
* 通过推迟 Yoga WASM 和 UI 组件导入，改进了无头模式（`-p` 标志）的启动性能
* 修复提示建议缓存回归，降低缓存命中率
* 通过限制文件历史快照修复了长会话中无限制的内存增长
* 添加 `CLAUDE_CODE_DISABLE_1M_CONTEXT` 环境变量以禁用 1M 上下文窗口支持
* Opus 4.6（快速模式）现在包含完整的 1M 上下文窗口
* VSCode：在 VS Code 会话中添加了 `/extra-usage` 命令支持
* 修复了任务输出在清理后保留最近行的内存泄漏问题
* 修复了 CircularBuffer 中的内存泄漏，其中已清除的项目保留在后备数组中
* 修复了 shell 命令执行中的内存泄漏，其中 ChildProcess 和 AbortController 引用在清理后被保留

## v2.1.49（2026年2月19日）* 改进了 MCP OAuth 身份验证，具有逐步身份验证支持和发现缓存，减少服务器连接期间的冗余网络请求
* 添加了 `--worktree` (`-w`) 标志以在隔离的 git 工作树中启动 Claude
* 子代理支持 `isolation: "worktree"` 在临时 git 工作树中工作
* 添加了 Ctrl+F 键绑定来杀死后台代理（按两次确认）
* 代理定义支持 `background: true` 始终作为后台任务运行
* 插件可以为默认配置提供 `settings.json`
* 修复了文件未找到错误，以在模型删除存储库文件夹时建议更正的路径
* 修复了当后台代理正在运行且主线程空闲时，Ctrl+C 和 ESC 会被默默忽略的问题。现在在 3 秒内按两次会杀死所有后台代理。
* 修复了提示建议缓存回归，降低了缓存命中率。
* 修复了 `plugin enable` 和 `plugin disable`，以便在未指定 `--scope` 时自动检测正确的范围，而不是始终默认为用户范围
* 简单模式（`CLAUDE_CODE_SIMPLE`）现在除了 Bash 工具之外还包括文件编辑工具，允许在简单模式下直接编辑文件。
* 现在，当安全检查触发询问响应时，会填充权限建议，使 SDK 使用者能够显示权限选项
* 具有 1M 上下文的 Sonnet 4.5 将从 Max 计划中删除，取而代之的是我们的前沿 Sonnet 4.6 模型，该模型现在具有 1M 上下文。请切换到/model。
* 修复了通过 `/config` 切换时详细模式不更新思维块显示的问题 — 备忘录比较器现在可以正确检测详细更改
* 通过定期重置树托管解析器，修复了长时间会话期间 WASM 内存无限增长的问题
* 修复了由过时的瑜伽布局参考引起的潜在渲染问题
* 通过在启动期间跳过不必要的 API 调用，提高了非交互模式 (`-p`) 的性能
* 通过缓存 HTTP 和 SSE MCP 服务器的身份验证失败来提高性能，避免重复尝试连接到需要身份验证的服务器
* 修复了由 Yoga WASM 线性内存永不收缩导致的长时间运行会话期间内存无限增长的问题
* SDK 模型信息现在包括 `supportsEffort`、`supportedEffortLevels` 和 `supportsAdaptiveThinking` 字段，以便消费者可以发现模型功能。
* 添加了 `ConfigChange` 挂钩事件，该事件在会话期间配置文件更改时触发，从而启用企业安全审核和可选的设置更改阻止。
* 通过缓存 MCP 身份验证失败来避免冗余连接尝试，从而提高启动性能
* 通过减少分析令牌计数的 HTTP 调用来提高启动性能
* 通过将 MCP 工具令牌计数批处理到单个 API 调用中，提高了启动性能
* 修复了 `disableAllHooks` 设置以尊重托管设置层次结构 - 非托管设置无法再禁用策略设置的托管挂钩 (#26637)
* 修复了 `--resume` 会话选择器，显示以 `/clear` 等命令开头的会话的原始 XML 标签。现在正确地转入会话 ID 后备。* 改进了路径安全和工作目录块的权限提示，以显示限制的原因，而不是没有上下文的裸提示## 2026 年 2 月 18 日（2026 年 2 月 18 日）* 修复了 FileWriteTool 行计数，以保留有意的尾随空白行，而不是使用 `trimEnd()` 删除它们。
* 修复了显示代码中由 `os.EOL` (`\r\n`) 引起的 Windows 终端渲染错误 — 行计数现在显示正确的值，而不是在 Windows 上始终显示 1。
* 改进了 VS Code 计划预览：随着 Claude 迭代自动更新，仅在计划可供审核时启用评论，并在拒绝时保持预览打开，以便 Claude 可以修改。
* 修复了以下错误：由于 `\r\n` 行结尾，Markdown 输出中的粗体和彩色文本可能会在 Windows 上转换为错误字符。
* 通过在发送到压缩 API 之前剥离文档块和图像来修复会话包含许多 PDF 文档时压缩失败的问题 (anthropics/claude-code#26188)
* 通过在使用后释放 API 流缓冲区、代理上下文和技能状态，改进了长时间运行会话中的内存使用情况
* 通过推迟 SessionStart 挂钩执行来提高启动性能，将交互时间缩短约 500 毫秒。
* 修复了使用 MSYS2 或 Cygwin shell 时 Windows 上的 bash 工具输出被默默丢弃的问题。
* 改进了 `@` 文件提及的性能 - 通过在启动时预热索引并使用基于会话的缓存和后台刷新，文件建议现在显示得更快。
* 通过在任务完成后修剪代理任务消息历史记录来提高内存使用率
* 通过消除更新过程中的 O(n²) 消息累积，改进了长时间代理会话期间的内存使用情况
* 修复了 bash 权限分类器，以验证返回的匹配描述是否与实际输入规则相对应，防止幻觉描述错误地授予权限
* 修复了用户定义的代理仅在报告零 inode 的 NFS/FUSE 文件系统上加载一个文件的问题 (anthropics/claude-code#26044)
* 修复了当通过裸名称而不是完全限定的插件名称引用时插件代理技能静默加载失败的问题 (anthropics/claude-code#25834)
* 为了清晰起见，折叠工具结果中的搜索模式现在显示在引号中
* Windows：修复了 CWD 跟踪临时文件永远不会被清理，导致它们无限期累积的问题 (anthropics/claude-code#17600)
* 使用 `ctrl+f` 杀死所有后台代理，而不是双击 ESC。现在，当您按 ESC 取消主线程时，后台代理会继续运行，从而使您可以更好地控制代理生命周期。
* 修复了在具有并发代理的会话中发生的 API 400 错误（“思维块无法修改”），该错误是由交错的流内容块阻止正确的消息合并引起的。
* 简化了队友导航，仅使用 Shift+Down（带换行），而不是同时使用 Shift+Up 和 Shift+Down。
* 修复了单个文件写入/编辑错误会中止所有其他并行文件写入/编辑操作的问题。即使同级文件失败，独立文件突变现在也会完成。
* 在 Stop 和 SubagentStop 挂钩输入中添加了 `last_assistant_message` 字段，提供最终的助手响应文本，以便挂钩可以访问它而无需解析脚本文件。* 修复了通过 `/rename` 设置的自定义会话标题在恢复对话后丢失的问题 (anthropics/claude-code#23610)
* 修复了通过从头开始截断的折叠阅读/搜索提示文本在狭窄终端上溢出的问题。
* 修复了带有反斜杠换行连续行的 bash 命令（例如，使用 `\` 跨多行分割的长命令）会产生虚假的空参数，可能会破坏命令执行的问题。
* 修复了安装许多用户技能时，内置斜杠命令（`/help`、`/model`、`/compact` 等）从自动完成下拉列表中隐藏的问题（anthropics/claude-code#22020）
* 修复了延迟加载后 MCP 服务器未出现在 MCP 管理对话框中的问题
* 修复了 `/clear` 命令后状态栏中持续显示的会话名称 (anthropics/claude-code#26082)
* 修复了当 SKILL.md frontmatter 中技能的 `name` 或 `description` 为裸数字（例如 `name: 3000`）时发生的崩溃 — 该值现在已正确强制为字符串（anthropics/claude-code#25837）
* 修复了当第一条消息超过 16KB 或使用数组格式内容时 /resume 静默删除会话 (anthropics/claude-code#25721)
* 为可配置的多行输入添加了 `chat:newline` 键绑定操作 (anthropics/claude-code#26075)
* 将 `added_dirs` 添加到状态行 JSON `workspace` 部分，将通过 `/add-dir` 添加的目录暴露给外部脚本 (anthropics/claude-code#26096)
* 修复了 `claude doctor` 将 mise 和 asdf 管理的安装错误分类为本机安装 (anthropics/claude-code#26033)
* 修复了 zsh heredoc 在沙盒命令中因“只读文件系统”错误而失败的问题 (anthropics/claude-code#25990)
* 修复了代理进度指示器，显示夸大的工具使用计数（anthropics/claude-code#26023）
* 修复了图像粘贴在 WSL2 系统上不起作用的问题，其中 Windows 将图像复制为 BMP 格式 (anthropics/claude-code#25935)
* 修复了后台代理结果返回原始转录数据而不是代理的最终答案（anthropics/claude-code#26012）
* 修复了 Warp 终端在原生支持时错误提示 Shift+Enter 设置的问题 (anthropics/claude-code#25957)
* 修复了导致 TUI 中时间戳和布局元素未对齐的 CJK 宽字符 (anthropics/claude-code#26084)
* 修复了 `.claude/agents/*.md` 中的自定义代理 `model` 字段在生成团队队友时被忽略的问题 (anthropics/claude-code#26064)
* 修复了上下文压缩后计划模式丢失，导致模型从计划模式切换到实施模式的问题 (anthropics/claude-code#26061)
* 修复了 settings.json 中的 `alwaysThinkingEnabled: true` 未在 Bedrock 和 Vertex 提供程序上启用思考模式的问题 (anthropics/claude-code#26074)
* 修复了在无头/SDK 模式下未发出 `tool_decision` OTel 遥测事件的问题 (anthropics/claude-code#26059)
* 修复了上下文压缩后会话名称丢失的问题 - 重命名的会话现在通过压缩保留其自定义标题 (anthropics/claude-code#26121)
* 将简历选择器中的初始会话计数从 10 增加到 50，以加快会话发现速度 (anthropics/claude-code#26123)
* Windows：修复了驱动器号大小写不同时的工作树会话匹配（anthropics/claude-code#26123）* 修复了 `/resume <session-id>` 无法找到第一条消息超过 16KB 的会话的问题 (anthropics/claude-code#25920)
* 修复了多行 bash 命令上的“始终允许”创建损坏设置的无效权限模式 (anthropics/claude-code#25909)
* 修复了当 SKILL.md frontmatter 中技能的 `argument-hint` 使用 YAML 序列语法（例如 `[topic: foo | bar]`）时的 React 崩溃（错误 #31）——该值现在已正确强制为字符串（anthropics/claude-code#25826）
* 修复了在使用 Web 搜索的会话上使用 `/fork` 时发生的崩溃 — 现在可以妥善处理来自转录本反序列化的搜索结果中的空条目 (anthropics/claude-code#25811)
* 通过添加 --no-optional-locks 标志修复了在 macOS 上触发 FSEvents 文件观察器循环的只读 git 命令 (anthropics/claude-code#25750)
* 修复了从 git 工作树运行时未发现的自定义代理和技能 - 现在包含主存储库中的项目级 `.claude/agents/` 和 `.claude/skills/` (anthropics/claude-code#25816)
* 修复了诸如 `claude doctor` 和 `claude plugin validate` 之类的非交互式子命令被阻止在嵌套 Claude 会话中的问题 (anthropics/claude-code#25803)
* Windows：修复了当路径之间的驱动器号大小写不同时，相同的 CLAUDE.md 文件被加载两次的问题 (anthropics/claude-code#25756)
* 修复了 markdown 中的内联代码跨度被错误地解析为 bash 命令的问题 (anthropics/claude-code#25792)
* 修复了队友旋转器不尊重设置中的自定义 spinnerVerbs (anthropics/claude-code#25748)
* 修复了命令删除其自己的工作目录后 shell 命令永久失败的问题 (anthropics/claude-code#26136)
* 修复了使用 Git Bash 而不是 cmd.exe 时挂钩（PreToolUse、PostToolUse）无法在 Windows 上静默执行的问题 (anthropics/claude-code#25981)
* 修复了 LSP `findReferences` 和其他基于位置的操作从 gitignored 文件返回结果（例如 `node_modules/`、`venv/`）（anthropics/claude-code#26051）
* 将配置备份文件从主目录根移动到 `~/.claude/backups/` 以减少主目录混乱（anthropics/claude-code#26130）
*修复了具有大的第一个提示（>16KB）的会话从/resume列表中消失的问题（anthropics/claude-code#26140）
* 修复了带有双下划线前缀（例如 `__git_ps1`）的 shell 函数未在 shell 会话中保留的问题（anthropics/claude-code#25824）
* 修复了在收到任何代币之前显示“0 代币”计数器的微调器 (anthropics/claude-code#26105)
* VSCode：修复了 AskUserQuestion 对话框打开时对话消息显示为灰色的问题 (anthropics/claude-code#26078)
* 修复了由于从工作树特定的 gitdir 而不是主存储库配置读取远程 URL 解析而导致 git 工作树中后台任务失败的问题 (anthropics/claude-code#26065)
* 修复了右 Alt 键在 Windows/Git Bash 终端的输入字段中留下可见的 `[25~` 转义序列残留的问题 (anthropics/claude-code#25943)
* `/rename` 命令现在默认更新终端选项卡标题 (anthropics/claude-code#25789)* 修复了编辑工具在编辑时将 Unicode 弯引号 (\u201c\u201d \u2018\u2019) 替换为直引号（anthropics/claude-code#26141）
* 修复了当链接文本跨多个终端行换行时，OSC 8 超链接只能在第一行单击。## v2.1.48（2026年2月18日）

* 修复了 macOS 上终端断开连接后孤立的 CC 进程
* 添加了对在 Claude Code 中使用 claude.ai MCP 连接器的支持

## v2.1.47（2026年2月17日）

* 添加了对 Claude Sonnet 4.6 的支持
* 添加了对从 `--add-dir` 目录读取 `enabledPlugins` 和 `extraKnownMarketplaces` 的支持
* 添加了 `spinnerTipsOverride` 设置以自定义旋转提示 - 使用一系列自定义提示字符串配置 `tips`，并可选择将 `excludeDefault: true` 设置为仅显示自定义提示而不是内置提示
* 在 SDK 中添加了 `SDKRateLimitInfo` 和 `SDKRateLimitEvent` 类型，使消费者能够接收速率限制状态更新，包括利用率、重置时间和超额信息
* 通过将 API 提供程序环境变量传播到 tmux 生成的进程，修复了 Agent Teams 队友在 Bedrock、Vertex 和 Foundry 上失败的问题 (anthropics/claude-code#23561)
* 修复了使用正确的每用户临时目录在 macOS 上写入临时文件时沙箱“不允许操作”错误 (anthropics/claude-code#21654)
* 修复了任务工具（后台代理）在完成时因 `ReferenceError` 崩溃的问题 (anthropics/claude-code#22087)
* 修复了当图像粘贴到输入中时，在 Enter 上不接受自动完成建议的问题
* 修复了压缩后子代理调用的技能错误地出现在主会话上下文中的问题
* 修复了每次启动时累积过多的 `.claude.json.backup` 文件
* 修复了插件提供的命令、代理和挂钩在安装后不立即可用而无需重新启动的问题
* 通过删除统计缓存的会话历史记录的急切加载来提高启动性能
* 改进了产生大量输出的 shell 命令的内存使用情况 - RSS 不再随命令输出大小无限增长
* 改进了折叠的读取/搜索组，以显示活动时在摘要行下方正在处理的当前文件或搜索模式
* \[VSCode] 改进了权限目标选择（项目/用户/会话）以跨会话保留

## v2.1.44（2026年2月16日）

* 修复了深层嵌套目录路径的 ENAMETOOLONG 错误
* 修复了身份验证刷新错误

## v2.1.43（2026年2月16日）

* 通过添加 3 分钟超时修复了 AWS 身份验证刷新无限期挂起的问题
* 修复了 `.claude/agents/` 目录中非代理降价文件的虚假警告
* 修复了在 Vertex/Bedrock 上无条件发送的结构化输出 beta 标头

## v2.1.42（2026年2月13日）

* 通过推迟 Zod 架构构建来提高启动性能
* 通过将日期移出系统提示来提高提示缓存命中率
* 为符合条件的用户添加了一次性 Opus 4.6 努力标注
* 修复 /resume 将中断消息显示为会话标题
* 修复了建议/compact的图像尺寸限制错误

## v2.1.41（2026年2月13日）* 添加了防止在另一个 Claude Code 会话中启动 Claude Code 的保护
* 修复了代理团队对 Bedrock、Vertex 和 Foundry 客户使用错误型号标识符的问题
* 修复了 MCP 工具在流式传输期间返回图像内容时的崩溃问题
* 修复/恢复会话预览显示原始 XML 标签而不是可读的命令名称
* 改进了为 Bedrock/Vertex/Foundry 用户提供的模型错误消息以及后备建议
* 修复了插件浏览显示已安装插件的误导性“空格切换”提示的问题
* 修复了钩子阻塞错误（退出代码 2），不向用户显示 stderr
* 向 OTel 事件和跟踪范围添加了 `speed` 属性，以实现快速模式可见性
* 添加了 `claude auth login`、`claude auth status` 和 `claude auth logout` CLI 子命令
* 添加了 Windows ARM64 (win32-arm64) 本机二进制支持
* 改进了 `/rename`，在不带参数调用时从对话上下文自动生成会话名称
* 改进了提示页脚的窄终端布局
* 修复了带有锚片段的@提及时文件解析失败的问题（例如 `@README.md#installation`）
* 修复了 FileReadTool 阻塞 FIFO、`/dev/stdin` 和大文件进程的问题
* 修复了流媒体 Agent SDK 模式下无法发送后台任务通知的问题
* 修复了分类器规则输入中每次击键时光标跳到末尾的问题
* 修复了原始 URL 被删除的 Markdown 链接显示文本
* 修复了向用户显示的自动压缩失败错误通知
* 修复了子代理经过时间显示中包含的权限等待时间
* 修复了计划模式下主动滴答声触发的问题
* 修复了磁盘上设置更改时清除过时权限规则的问题
* 修复了 UI 中显示 stderr 内容的钩子阻塞错误

## v2.1.39（2026年2月10日）

* 改进终端渲染性能
* 修复了被吞掉而不是显示的致命错误
* 修复了会话关闭后进程挂起的问题
* 修复了终端屏幕边界处的字符丢失问题
* 修复了详细记录视图中的空白行

## v2.1.38（2026年2月10日）

* 修复了 2.1.37 中引入的 VS Code 终端滚动到顶部回归问题
* 修复了 Tab 键排队斜杠命令而不是自动完成的问题
* 修复了使用环境变量包装器的命令的 bash 权限匹配
* 修复了不使用流媒体时工具使用之间的文本消失的问题
* 修复了在 VS Code 扩展中恢复时的重复会话
* 改进了heredoc分隔符解析以防止命令走私
* 在沙盒模式下阻止对 `.claude/skills` 目录的写入

## v2.1.37（2026年2月7日）

* 修复了启用 /extra-usage 后 /fast 无法立即可用的问题

## v2.1.36（2026年2月7日）

* Opus 4.6 现已提供快速模式。了解更多信息 [https://code.claude.com/docs/en/fast-mode](https://code.claude.com/docs/en/fast-mode)

## v2.1.34（2026年2月6日）

* 修复了代理团队设置在渲染之间更改时发生的崩溃
* 修复了启用 `autoAllowBashIfSandboxed` 时从沙箱中排除的命令（通过 `sandbox.excludedCommands` 或 `dangerouslyDisableSandbox`）可能绕过 Bash 询问权限规则的错误

## v2.1.33（2026年2月6日）* 修复了 tmux 中的代理队友会话以发送和接收消息
* 修复了有关当前计划中不可用的代理团队的警告
* 为多代理工作流程添加了 `TeammateIdle` 和 `TaskCompleted` 挂钩事件
* 添加了对通过代理“工具”frontmatter 中的 `Task(agent_type)` 语法限制可以生成哪些子代理的支持
* 为代理添加了 `memory` frontmatter 现场支持，支持 `user`、`project` 或 `local` 示波器的持久内存
* 在技能描述和 `/skills` 菜单中添加插件名称，以提高可发现性
* 修复了模型处于扩展思考时提交新消息会中断思考阶段的问题
* 修复了中止中止时可能发生的 API 错误，其中空白文本与思考块相结合将绕过规范化并产生无效请求
* 修复了 API 代理兼容性问题，其中流端点上的 404 错误不再触发非流回退
* 修复了通过 `settings.json` 环境变量配置的代理设置未应用于 Node.js 版本上的 WebFetch 和其他 HTTP 请求的问题
* 修复了 `/resume` 会话选择器显示原始 XML 标记而不是使用斜线命令启动的会话的干净标题
* 改进了 API 连接失败的错误消息 - 现在显示特定原因（例如 ECONNREFUSED、SSL 错误），而不是通用的“连接错误”
* 无效托管设置带来的错误现已浮出水面
* VSCode：添加了对远程会话的支持，允许 OAuth 用户从 claude.ai 浏览和恢复会话
* VSCode：在会话选择器中添加了 git 分支和消息计数，并支持按分支名称搜索
* VSCode：修复了初始会话加载和会话切换时滚动到底部的滚动不足问题

## 2.1.32（2026年2月5日）

* Claude Opus 4.6 现已上市！
* 添加了用于多代理协作的研究预览代理团队功能（令牌密集型功能，需要设置 CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS=1）
* Claude 现在在工作时自动记录和调用记忆
* 在消息选择器中添加了“从此处总结”，允许部分对话总结。
* 现在会自动加载附加目录 (`--add-dir`) 中 `.claude/skills/` 中定义的技能。
* 修复了从子目录运行时 `@` 文件补全显示不正确的相对路径的问题
* 更新了 --resume 以重新使用默认情况下在先前对话中指定的 --agent 值。
* 修复：当heredocs包含JavaScript模板文字（例如`${index + 1}`）时，Bash工具不再抛出“错误替换”错误，该错误之前会中断工具执行
* 技能角色预算现在随上下文窗口（上下文的 2%）缩放，因此具有较大上下文窗口的用户可以看到更多技能描述而不会被截断
* 修复了泰语/老挝语间隔元音 (สระ า, ำ) 在输入字段中无法正确呈现的问题
* VSCode：修复了在输入字段中按 Enter 键并带有前面的文本时错误执行斜杠命令的问题
* VSCode：加载过去的对话列表时添加了微调器

## 2.1.31（2026年2月4日）* 添加了退出时的会话恢复提示，显示稍后如何继续对话
* 在复选框选择中添加了对从日语 IME 输入全角 (zenkaku) 空格的支持
* 修复了 PDF 太大错误，永久锁定会话，要求用户开始新对话
* 修复了启用沙盒模式时 bash 命令错误地报告失败并出现“只读文件系统”错误的问题
* 修复了当 `~/.claude.json` 中的项目配置缺少默认字段时导致会话在进入计划模式后无法使用的崩溃问题
* 修复了 `temperatureOverride` 在流 API 路径中被默默忽略的问题，导致所有流请求都使用默认温度 (1)，无论配置的覆盖如何
* 修复了 LSP 关闭/退出与拒绝空参数的严格语言服务器的兼容性
* 改进的系统提示可以更清晰地引导模型使用专用工具（Read、Edit、Glob、Grep）而不是 bash 等效工具（`cat`、`sed`、`grep`、`find`），减少不必要的 bash 命令使用
* 改进了 PDF 和请求大小错误消息以显示实际限制（100 页，20MB）
* 减少了流媒体期间旋转器出现和消失时终端中的布局抖动
* 从第三方提供商（Bedrock、Vertex、Foundry）用户的模型选择器中删除了误导性的 Anthropic API 定价

## 2.1.30（2026年2月3日）* 在 PDF 读取工具中添加了 `pages` 参数，允许读取特定页面范围（例如 `pages: "1-5"`）。当提及 `@` 时，大型 PDF（>10 页）现在会返回轻量级参考，而不是内联到上下文中。
* 为不支持动态客户端注册的 MCP 服务器（例如 Slack）添加了预配置的 OAuth 客户端凭据。将 `--client-id` 和 `--client-secret` 与 `claude mcp add` 一起使用。
* 为 Claude 添加了 `/debug`，以帮助排除当前会话的故障
* 添加了对只读模式下其他 `git log` 和 `git show` 标志的支持（例如 `--topo-order`、`--cherry-pick`、`--format`、`--raw`）
* 在任务工具结果中添加了令牌计数、工具使用和持续时间指标
* 在配置中添加了简化运动模式
* 修复了 API 对话历史记录中出现的虚拟“（无内容）”文本块，减少了令牌浪费和潜在的模型混乱
* 修复了当工具描述或输入模式更改时提示缓存未正确失效的问题，仅当工具名称更改时
* 修复了当对话包含思维障碍时运行 `/login` 后可能出现的 400 错误
* 修复了使用包含 `parentUuid` 周期的损坏转录文件恢复会话时的挂起问题
* 修复了当额外使用不可用时，显示最多 20 倍用户的错误“/升级”建议的速率限制消息
* 修复了主动打字时权限对话框窃取焦点的问题
* 修复了子代理无法访问 SDK 提供的 MCP 工具的问题，因为它们未同步到共享应用程序状态
* 修复了具有 `.bashrc` 文件的 Windows 用户无法运行 bash 命令的回归
* 通过用轻量级的基于统计的加载和渐进式丰富替换会话索引，改进了 `--resume` 的内存使用情况（对于具有多个会话的用户，减少了 68%）
* 改进了 `TaskStop` 工具，以在结果行中显示已停止的命令/任务描述，而不是通用的“任务已停止”消息
* 将 `/model` 更改为立即执行而不是排队
* \[VSCode] 为问题对话框中的“其他”文本输入添加了多行输入支持（使用 Shift+Enter 换行）
* \[VSCode] 修复了开始新对话时会话列表中出现的重复会话

## 2.1.29（2026年1月31日）

* 修复了恢复具有 `saved_hook_context` 的会话时的启动性能问题

## 2.1.27（2026年1月30日）

* 添加工具调用失败和拒绝调试日志
* 修复了网关用户的上下文管理验证错误，确保 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 避免该错误
* 添加了 `--from-pr` 标志以恢复链接到特定 GitHub PR 编号或 URL 的会话
* 通过 `gh pr create` 创建时，会话现在会自动链接到 PR
* 修复了 /context 命令不显示彩色输出的问题
* 修复了显示 PR 状态时状态栏重复后台任务指示器的问题
* Windows：修复了使用 `.bashrc` 文件的用户执行 bash 命令失败的问题
* Windows：修复了生成子进程时控制台窗口闪烁的问题
* VSCode：修复了 OAuth 令牌过期导致扩展会话后出现 401 错误的问题

## 2.1.25（2026年1月29日）* 修复了 Bedrock 和 Vertex 上网关用户的 beta 标头验证错误，确保 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 避免该错误

## 2.1.23（2026年1月29日）

* 添加了可自定义的微调动词设置 (`spinnerVerbs`)
* 修复了企业代理背后或使用客户端证书的用户的 mTLS 和代理连接
* 修复了每用户临时目录隔离，以防止共享系统上的权限冲突
* 修复了启用提示缓存范围时可能导致 400 错误的竞争条件
* 修复了当无头流会话结束时挂起的异步挂钩不会被取消的问题
* 修复了接受建议时制表符补全不更新输入字段的问题
* 修复了 ripgrep 搜索超时默默返回空结果而不是报告错误的问题
* 通过优化屏幕数据布局提高终端渲染性能
* 更改了 Bash 命令以显示超时持续时间以及经过的时间
* 更改了合并的拉取请求，以在提示页脚中显示紫色状态指示器
* \[IDE] 修复了在无头模式下为 Bedrock 用户显示不正确区域字符串的模型选项

## 2.1.22（2026年1月28日）

* 修复了非交互 (-p) 模式的结构化输出

## 2.1.21（2026年1月28日）

* 在选项选择提示中添加了对从日语 IME 输入全角 (zenkaku) 数字的支持
* 修复了 shell 完成缓存文件在退出时被截断的问题
* 修复了恢复工具执行期间中断的会话时的 API 错误
* 修复了在具有大输出令牌限制的模型上过早触发自动压缩的问题
* 修复了删除后可能会重复使用的任务 ID
* 修复了文件搜索在 Windows 上的 VS Code 扩展中不起作用的问题
* 改进了阅读/搜索进度指示器，在进行时显示“正在阅读...”，在完成时显示“已读”
* 改进了 Claude，使其更喜欢文件操作工具（读取、编辑、写入）而不是 bash 等效工具（cat、sed、awk）
* \[VSCode] 添加了自动 Python 虚拟环境激活，确保 `python` 和 `pip` 命令使用正确的解释器（可通过 `claudeCode.usePythonEnvironment` 设置进行配置）
* \[VSCode] 修复了背景颜色不正确的消息操作按钮

## 2.1.20（2026年1月27日）* 添加了 vim 正常模式下光标无法进一步移动时的方向键历史导航
* 在帮助菜单中添加了外部编辑器快捷方式 (Ctrl+G)，以提高可发现性
* 在提示页脚中添加了 PR 审核状态指示器，以带有可点击链接的彩色点显示当前分支的 PR 状态（已批准、请求更改、待处理或草稿）
* 添加了对从通过 `--add-dir` 标志指定的其他目录加载 `CLAUDE.md` 文件的支持（需要设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`）
* 增加了通过 `TaskUpdate` 工具删除任务的功能
* 修复了会话压缩问题，该问题可能导致恢复加载完整历史记录而不是压缩摘要
* 修复了代理有时会忽略在积极执行任务时发送的用户消息
* 修复了宽字符（表情符号、CJK）渲染伪影，其中当替换为较窄字符时尾随列未被清除
* 修复了 MCP 工具响应包含特殊 Unicode 字符时的 JSON 解析错误
* 修复了多行和换行文本输入中的向上/向下箭头键，以优先考虑光标移动而不是历史导航
* 修复了按向上箭头导航命令历史记录时草稿提示丢失的问题
* 修复了在输入中输入斜杠命令时幻影文本闪烁的问题
* 修复了市场源删除未正确删除设置的问题
* 修复了某些命令（例如 `/context`）中的重复输出
* 修复了任务列表有时显示在主对话视图之外的问题
* 修复了 Python 文档字符串等多行结构中发生的差异的语法突出显示
* 修复了取消工具使用时的崩溃问题
* 改进了 `/sandbox` 命令 UI，以在缺少依赖项时通过安装说明显示依赖项状态
* 改进了思维状态文本，带有微妙的闪光动画
* 改进的任务列表可根据终端高度动态调整可见项目
* 改进了分叉对话提示，以显示如何恢复原始会话
* 更改了折叠的阅读/搜索组，以在进行时显示现在时（“阅读”、“搜索”），并在完成时显示过去时（“阅读”、“搜索”）
* 更改了 `ToolSearch` 结果，使其显示为简短通知，而不是内嵌在对话中
* 更改了 `/commit-push-pr` 技能，以便在通过 MCP 工具配置时自动将 PR URL 发布到 Slack 频道
* 更改了 `/copy` 命令以供所有用户使用
* 更改了后台代理以在启动前提示工具权限
* 更改了 `Bash(*)` 等权限规则，使其被接受并视为与 `Bash` 等效
* 将配置备份更改为带时间戳和轮换（保留 5 个最新的）以防止数据丢失

## v2.1.19（2026年1月23日）* 添加环境变量 `CLAUDE_CODE_ENABLE_TASKS`，设置为 `false` 以暂时保留旧系统
* 添加了简写 `$0`、`$1` 等，用于访问自定义命令中的各个参数
* 修复了不支持 AVX 指令的处理器上的崩溃问题
* 通过从 `process.exit()` 捕获 EIO 错误并使用 SIGKILL 作为后备，修复了终端关闭时悬空的 Claude Code 进程
* 修复了 `/rename` 和 `/tag` 从不同目录（例如 git worktrees）恢复时不更新正确会话的问题
* 修复了从不同目录运行时按自定义标题恢复会话不起作用的问题
* 修复了使用提示存储 (Ctrl+S) 和恢复时粘贴的文本内容丢失的问题
* 修复了没有明确模型设置的代理列表显示“Sonnet（默认）”而不是“继承（默认）”的问题
* 修复了后台挂钩命令未提前返回的问题，可能导致会话等待有意后台的进程
* 修复文件写入预览省略空行的问题
* 无需额外权限即可更改技能或无需批准即可允许挂钩
* 将索引参数语法从 `$ARGUMENTS.0` 更改为 `$ARGUMENTS[0]`（括号语法）
* \[SDK] 当启用 `replayUserMessages` 时，添加了 `queued_command` 附件消息作为 `SDKUserMessageReplay` 事件的重播
* \[VSCode] 为所有用户启用会话分叉和倒带功能

## v2.1.18（2026年1月23日）

* 添加了可自定义的键盘快捷键。根据上下文配置键绑定、创建和弦序列并个性化您的工作流程。运行 `/keybindings` 即可开始。了解更多信息 [https://code.claude.com/docs/en/keybindings](https://code.claude.com/docs/en/keybindings)

## v2.1.17（2026年1月22日）

* 修复了不支持 AVX 指令的处理器上的崩溃问题

## v2.1.16（2026年1月22日）

* 添加了新的任务管理系统，包括依赖性跟踪等新功能
* \[VSCode] 添加原生插件管理支持
* \[VSCode] 增加了 OAuth 用户从“会话”对话框浏览和恢复远程 Claude 会话的功能
* 修复了在子代理使用量较大的情况下恢复会话时内存不足崩溃的问题
* 修复运行 `/compact` 后“上下文剩余”警告未隐藏的问题
* 修复了简历屏幕上的会话标题不尊重用户语言设置的问题
* \[IDE] 修复了 Windows 上的竞争条件，其中 Claude Code 侧边栏视图容器不会出现在启动时

## v2.1.15（2026年1月21日）

* 添加了 npm 安装的弃用通知 - 运行 `claude install` 或参阅 [https://docs.anthropic.com/en/docs/claude-code/getting-started](https://docs.anthropic.com/en/docs/claude-code/getting-started) 了解更多选项
* 使用 React Compiler 改进 UI 渲染性能
* 修复了运行 `/compact` 后“上下文剩余直至自动压缩”警告不消失的问题
* 修复了 MCP stdio 服务器超时未杀死子进程的问题，这可能会导致 UI 冻结

## v2.1.14（2026年1月20日）* 在 bash 模式下添加了基于历史记录的自动完成功能 (`!`) - 输入部分命令并按 Tab 键从 bash 命令历史记录中完成
* 添加了对已安装插件列表的搜索 - 键入按名称或描述进行过滤
* 添加了对将插件固定到特定 git commit SHA 的支持，允许市场条目安装确切的版本
* 修复了上下文窗口阻止限制计算过于激进的回归，阻止用户使用上下文的 65%，而不是预期的 98%
* 修复了运行并行子代理时可能导致崩溃的内存问题
* 修复了长时间运行的会话中的内存泄漏问题，其中 shell 命令完成后流资源没有被清理
* 修复了 `@` 符号在 bash 模式下错误触发文件自动完成建议的问题
* 修复了 `@` 提及菜单文件夹单击行为以导航到目录而不是选择它们
* 修复了当描述很长时 `/feedback` 命令生成无效的 GitHub 问题 URL
* 修复了 `/context` 命令，以在详细模式下显示与状态行相同的令牌计数和百分比
* 修复了 `/config`、`/context`、`/model` 和 `/todos` 命令叠加层可能意外关闭的问题
* 修复了输入类似命令时斜杠命令自动完成选择错误命令的问题（例如 `/context` 与 `/compact`）
* 修复了仅配置一个市场时插件市场中返回导航不一致的问题
* 修复了 iTerm2 进度条在退出时无法正确清除的问题，从而防止指示器和铃声出现挥之不去的情况
* 改进了退格键，将粘贴的文本作为单个标记而不是一次删除一个字符
* \[VSCode] 添加 `/usage` 命令来显示当前计划使用情况

## 2.1.12（2026年1月17日）

* 修复消息渲染错误

## 2.1.11（2026年1月17日）

* 修复了 HTTP/SSE 传输的过多 MCP 连接请求

## 2.1.10（2026年1月17日）

* 添加了新的 `Setup` 挂钩事件，可通过 `--init`、`--init-only` 或 `--maintenance` CLI 标志触发，以进行存储库设置和维护操作
* 添加键盘快捷键“c”，用于在登录期间浏览器未自动打开时复制 OAuth URL
* 修复了运行包含带有 JavaScript 模板文本（如 `${index + 1}`）的 heredocs 的 bash 命令时的崩溃问题
* 改进了启动以捕获 REPL 完全准备好之前键入的击键
* 改进了文件建议，在接受时显示为可移动附件，而不是插入文本
* \[VSCode] 在插件列表中添加了安装计数显示
* \[VSCode] 安装插件时添加信任警告

## 2.1.9（2026年1月16日）* 添加了 `auto:N` 语法，用于配置 MCP 工具搜索自动启用阈值，其中 N 是上下文窗口百分比 (0-100)
* 添加了 `plansDirectory` 设置以自定义计划文件的存储位置
* 在 AskUserQuestion“其他”输入字段中添加了外部编辑器支持 (Ctrl+G)
* 为从网络会话创建的提交和 PR 添加了会话 URL 属性
* 添加了对 `PreToolUse` 挂钩的支持，以将 `additionalContext` 返回到模型
* 为访问当前会话 ID 的技能添加了 `${CLAUDE_SESSION_ID}` 字符串替换
* 修复了并行工具调用的长会话因有关孤立工具\_结果块的 API 错误而失败的问题
* 修复了缓存连接承诺永远无法解决时 MCP 服务器重新连接挂起的问题
* 修复了 Ctrl+Z 暂停在使用 Kitty 键盘协议的终端（Ghostty、iTerm2、kitty、WezTerm）中不起作用的问题

## 2.1.7（2026年1月14日）

* 添加了 `showTurnDuration` 设置以隐藏回合持续时间消息（例如，“煮了 1m 6s”）
* 增加了在接受权限提示时提供反馈的能力
* 在任务通知中添加了座席最终响应的内联显示，无需阅读完整的记录文件即可更轻松地查看结果
* 修复了通配符权限规则可能匹配包含 shell 操作符的复合命令的安全漏洞
* 修复了当云同步工具、防病毒扫描程序或 Git 触摸文件时间戳而不更改内容时 Windows 上的错误“文件已修改”错误
* 修复了同级工具在流执行期间失败时的孤立工具\_结果错误
*修复了使用完整上下文窗口而不是有效上下文窗口（为最大输出令牌保留空间）计算的上下文窗口阻塞限制
* 修复了运行 `/model` 或 `/theme` 等本地斜杠命令时微调器短暂闪烁的问题
* 使用固定宽度盲文字符修复了终端标题动画抖动问题
* 修复了 git 子模块的插件在安装时未完全初始化的问题
* 修复了当临时目录路径包含 `t` 或 `n` 等被误解为转义序列的字符时，bash 命令在 Windows 上失败的问题
* 通过减少终端渲染中的内存分配开销来提高打字响应能力
* 默认为所有用户启用 MCP 工具搜索自动模式。当 MCP 工具描述超过上下文窗口的 10% 时，它们会自动延迟并通过 MCPSearch 工具发现，而不是预先加载。这可以减少配置了许多 MCP 工具的用户的上下文使用情况。用户可以通过在设置中将 `MCPSearch` 添加到 `disallowedTools` 来禁用此功能。
* 将 OAuth 和 API 控制台 URL 从 console.anthropic.com 更改为 platform.claude.com
* \[VSCode] 修复了传递包装器路径而不是 Claude 二进制路径的 `claudeProcessWrapper` 设置

## 2.1.6（2026年1月13日）* 为 `/config` 命令添加搜索功能，以快速过滤设置
* 向 `/doctor` 添加了更新部分，显示自动更新通道和可用的 npm 版本（稳定/最新）
* 向 `/stats` 命令添加了日期范围过滤 - 按 `r` 在过去 7 天、过去 30 天和所有时间之间循环
* 添加了在处理子目录中的文件时自动发现嵌套 `.claude/skills` 目录中的技能
* 在状态行输入中添加了 `context_window.used_percentage` 和 `context_window.remaining_percentage` 字段，以便于上下文窗口显示
* 添加了 Ctrl+G 期间编辑器失败时的错误显示
* 通过 shell 行延续修复了权限绕过，可能允许执行被阻止的命令
* 修复了当文件观察者触摸文件而不更改内容时出现的错误“文件已被意外修改”的错误
* 修复了多行响应中文本样式（粗体、颜色）逐渐错位的问题
* 修复了在描述字段中输入“n”时反馈面板意外关闭的问题
* 修复了每周重置后低使用率时出现的速率限制警告（现在需要 70% 使用率）
* 修复了恢复上一个会话时速率限制选项菜单错误地自动打开的问题
* 修复了小键盘按键输出转义序列而不是 Kitty 键盘协议终端中的字符的问题
* 修复了 Option+Return 不在 Kitty 键盘协议终端中插入换行符的问题
* 修复了主目录中累积的损坏的配置备份文件（现在每个配置文件仅创建一个备份）
* 修复了 `mcp list` 和 `mcp get` 命令留下孤立的 MCP 服务器进程的问题
* 修复了 ink2 模式下节点通过 `display:none` 隐藏时的视觉伪影
* 改进了外部 CLAUDE.md 导入批准对话框，以显示正在导入哪些文件以及从何处导入
* 改进了 `/tasks` 对话框，以便在只有一个后台任务运行时直接进入任务详细信息
* 改进了@自动完成，带有不同建议类型和单行格式的图标
* 更新了“帮助改进 Claude”设置获取以刷新 OAuth 并在由于 OAuth 令牌过时而失败时重试
* 当多个后台任务同时完成时，将任务通知显示更改为最多 3 行并带有溢出摘要
* 在启动时将终端标题更改为“Claude Code”，以便更好地识别窗口
* 删除了@提及 MCP 服务器来启用/禁用的功能 - 使用 `/mcp enable <name>` 代替
* \[VSCode] 修复了手动压缩后使用指示器不更新的问题

## 2.1.5（2026年1月12日）

* 添加了 `CLAUDE_CODE_TMPDIR` 环境变量以覆盖用于内部临时文件的临时目录，对于具有自定义临时目录要求的环境非常有用

## 2.1.4（2026年1月11日）

* 添加了 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量以禁用所有后台任务功能，包括自动后台和 Ctrl+B 快捷键
* 修复了“帮助改进 Claude”设置获取以刷新 OAuth 并在由于 OAuth 令牌过时而失败时重试的问题

## 2.1.3（2026年1月9日）* 合并斜线命令和技能，简化思维模型而不改变行为
* 添加了发布通道（`stable` 或 `latest`）切换至 `/config`
* 添加了对无法访问的权限规则的检测和警告，并在 `/doctor` 中以及保存规则后发出警告，其中包括每个规则的来源和可操作的修复指南
* 修复了在 `/clear` 命令中持续存在的计划文件，现在确保在清除对话后使用新的计划文件
* 通过对 inode 值使用 64 位精度，修复了具有大 inode（例如 ExFAT）的文件系统上的错误技能重复检测
* 修复了状态栏中的后台任务计数与任务对话框中显示的项目之间的不匹配问题
* 修复了子代理在对话压缩期间使用错误模型的问题
* 修复了子代理中使用不正确模型的网络搜索问题
* 修复了从主目录运行时接受信任对话框而不在会话期间启用需要信任的功能（如挂钩）的问题
* 通过防止不受控制的写入破坏光标状态来提高终端渲染稳定性
* 通过将长描述截断为 2 行，提高了斜杠命令建议的可读性
* 将工具挂钩执行超时从 60 秒更改为 10 分钟
* \[VSCode] 为权限请求添加了可点击的目标选择器，允许您选择保存设置的位置（此项目、所有项目、与团队共享或仅会话）

## 2.1.2（2026年1月9日）* 为拖到终端的图像添加源路径元数据，帮助 Claude 了解图像的来源
* 在支持 OSC 8 的终端（如 iTerm）中的工具输出中添加了可点击的文件路径超链接
* 添加了对 Windows 软件包管理器 (winget) 安装的支持，并具有自动检测和更新说明
* 在计划模式下添加 Shift+Tab 键盘快捷键以快速选择“自动接受编辑”选项
* 添加了 `FORCE_AUTOUPDATE_PLUGINS` 环境变量，即使主自动更新程序被禁用，也允许插件自动更新
* 将 `agent_type` 添加到 SessionStart 挂钩输入，如果指定了 `--agent`，则填充
* 修复了 bash 命令处理中的命令注入漏洞，其中格式错误的输入可能会执行任意命令
* 修复了树守护者解析树未被释放的内存泄漏，导致 WASM 内存在长时间会话中无限增长
* 修复了在 CLAUDE.md 文件中使用 `@include` 指令时二进制文件（图像、PDF 等）意外包含在内存中的问题
* 修复了错误地声称另一个安装正在进行中的更新
* 修复了监视目录中存在套接字文件时的崩溃（EOPNOTSUPP 错误的深度防御）
* 修复了使用 `/tasks` 命令时远程会话 URL 和传送被破坏的问题
* 通过清理用户特定的服务器配置，修复了在分析事件中暴露的 MCP 工具名称
* 改进了 macOS 上的选项作为元提示，以显示 iTerm2、Kitty 和 WezTerm 等本机 CSIu 终端的终端特定指令
* 改进了通过 SSH 粘贴图像时的错误消息，建议使用 `scp` 而不是无用的剪贴板快捷方式提示
* 改进了权限解释器，不将常规开发工作流程（git fetch/rebase、npm install、测试、PR）标记为中等风险
* 将大型 bash 命令输出更改为保存到磁盘而不是截断，从而允许 Claude 读取完整内容
* 将大型工具输出更改为持久保存到磁盘而不是截断，通过文件引用提供完整的输出访问
* 更改了 `/plugins` 安装选项卡，以将插件和 MCP 与基于范围的分组统一起来
* 已弃用 Windows 托管设置路径 `C:\ProgramData\ClaudeCode\managed-settings.json` - 管理员应迁移到 `C:\Program Files\ClaudeCode\managed-settings.json`
* \[SDK] 将最小 zod 对等依赖项更改为 ^4.0.0
* \[VSCode] 修复了手动压缩后使用显示不更新的问题

## 2.1.0（2026年1月7日）* 添加了自动技能热重载 - 在 `~/.claude/skills` 或 `.claude/skills` 中创建或修改的技能现在无需重新启动会话即可立即可用
* 添加了对在技能 frontmatter 中使用 `context: fork` 在分叉子代理上下文中运行技能和斜线命令的支持
* 增加了对技能中`agent`字段的支持，以指定执行的代理类型
* 添加 `language` 设置以配置 Claude 的响应语言（例如语言：“日语”）
* 将 Shift+Enter 更改为在 iTerm2、WezTerm、Ghostty 和 Kitty 中开箱即用，无需修改终端配置
* 在 `settings.json` 中添加了 `respectGitignore` 支持，用于按项目控制 @-mention 文件选择器行为
* 添加了 `IS_DEMO` 环境变量以在 UI 中隐藏电子邮件和组织，对于流式传输或录制会话非常有用
* 修复了敏感数据（OAuth 令牌、API 密钥、密码）可能在调试日志中暴露的安全问题
* 修复了使用 `-c` 或 `--resume` 恢复会话时无法正确发现文件和技能的问题
* 修复了使用向上箭头或 Ctrl+R 搜索重播历史提示时粘贴的内容丢失的问题
* 修复了带有排队提示的 Esc 键，仅将它们移动到输入而不取消正在运行的任务
* 减少复杂 bash 命令的权限提示
* 修复了命令搜索，优先考虑命令名称中的精确匹配和前缀匹配，而不是描述中的模糊匹配
* 修复了 PreToolUse 挂钩，以在返回 `ask` 权限决策时允许 `updatedInput`，使挂钩能够充当中间件，同时仍然请求用户同意
* 修复了基于文件的市场源的插件路径解析
* 修复了未配置 LSP 服务器时错误启用 LSP 工具的问题
* 修复了名称中带有点的存储库的后台任务因“未找到 git 存储库”错误而失败的问题
* 修复了 Chrome 中的 Claude 对 WSL 环境的支持
* 修复了可执行文件创建失败时 Windows 本机安装程序静默失败的问题
* 改进了 CLI 帮助输出，以按字母顺序显示选项和子命令，以便于导航
* 在规则中的任何位置使用 `*` 添加了 Bash 工具权限的通配符模式匹配（例如 `Bash(npm *)`、`Bash(* install)`、`Bash(git * main)`）
* 为 bash 命令和代理添加了统一的 Ctrl+B 后台 - 按 Ctrl+B 现在可以同时后台所有正在运行的前台任务
* 增加了对 MCP `list_changed` 通知的支持，允许 MCP 服务器动态更新其可用工具、提示和资源，而无需重新连接
* 为 claude.ai 订阅者添加了 `/teleport` 和 `/remote-env` 斜杠命令，允许他们恢复和配置远程会话
* 添加了对使用 settings.json 权限中的 `Task(AgentName)` 语法或 `--disallowedTools` CLI 标志禁用特定代理的支持
* 为代理 frontmatter 添加了钩子支持，允许代理定义作用于代理生命周期的 PreToolUse、PostToolUse 和 Stop 钩子
* 添加了对技能和斜线命令 frontmatter 的钩子支持* 添加了新的 Vim 动作：`;` 和 `,` 用于重复 f/F/t/T 动作，`y` 操作符用于使用 `yy`/`Y` 进行猛拉，`p`/`P` 用于粘贴、文本对象（`iw`、 `aw`、`iW`、`aW`、`i"`、`a"`、`i'`、`a'`、`i(`、`a(`、`i[`、 `a[`、`i{`、`a{`)、`>>` 和 `<<` 用于缩进/缩进，以及 `J` 用于连接线
* 添加了 `/plan` 命令快捷方式以直接从提示符启用计划模式
* 当 `/` 出现在输入中的任何位置（而不仅仅是开头）时，添加了斜杠命令自动完成支持
* 在交互模式下添加了 `--tools` 标志支持，以限制 Claude 在交互会话期间可以使用哪些内置工具
* 添加了 `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` 环境变量以覆盖默认文件读取令牌限制
* 添加了对 `once: true` 挂钩配置的支持
* 在 frontmatter `allowed-tools` 字段中添加了对 YAML 样式列表的支持，以实现更清晰的技能声明
* 添加了对插件提示和代理挂钩类型的支持（以前仅支持命令挂钩）
* 在 iTerm2 中添加了对图像粘贴的 Cmd+V 支持（映射到 Ctrl+V）
* 添加了左/右箭头键导航，用于循环浏览对话框中的选项卡
* 新增Ctrl+O转录模式下实时思维块显示
* 在后台 bash 任务详细信息对话框中添加了完整输出的文件路径
* 在上下文可视化中添加了技能作为单独的类别
* 修复了当服务器报告令牌过期但本地过期检查不同意时不触发 OAuth 令牌刷新的问题
* 通过在实际存储条目时从 409 冲突中恢复来修复短暂服务器错误后会话持久性卡住的问题
* 修复了并发工具执行期间孤立工具结果导致的会话恢复失败
* 修复了在并发令牌刷新尝试期间可以从钥匙串缓存中读取过时的 OAuth 令牌的竞争情况
* 修复了 AWS Bedrock 子代理不继承 EU/APAC 跨区域推理模型配置，导致 IAM 权限范围仅限于特定区域时导致 403 错误的问题
* 修复了当后台任务通过文件路径引用截断为 30K 字符来产生大量输出时 API 上下文溢出的问题
* 通过跳过特殊文件类型的符号链接解析，修复了读取 FIFO 文件时的挂起问题
* 修正了 Ghostty、iTerm2、Kitty 和 WezTerm 中退出时终端键盘模式不会重置的问题
* 修复了 Alt+B 和 Alt+F（单词导航）在 iTerm2、Ghostty、Kitty 和 WezTerm 中不起作用的问题
* 修复了 `${CLAUDE_PLUGIN_ROOT}` 未在插件 `allowed-tools` frontmatter 中替换的问题，这导致工具错误地需要批准
* 修复了由写入工具使用硬编码 0o600 权限而不是遵循系统 umask 创建的文件
* 修复了 `$()` 命令替换因解析错误而失败的命令
* 修复了带有反斜杠延续的多行 bash 命令被错误地分割和标记为权限的问题
* 修复了 bash 命令前缀提取，以正确识别全局选项后的子命令（例如，`git -C /path log` 现在可以正确匹配 `Bash(git log:*)` 规则）* 修复了作为 CLI 参数传递的斜杠命令（例如 `claude /context`）无法正确执行的问题
* 修复了在 Tab 完成斜杠命令后按 Enter 键选择其他命令而不是提交已完成的命令的问题
* 修复了输入带有参数的命令时斜杠命令参数提示闪烁和显示不一致的问题
* 修复了 Claude 在直接运行斜杠命令时有时会冗余调用技能工具的问题
* 修复了 `/context` 中的技能标记估计，以准确反映仅 frontmatter 的加载
* 修复了子代理有时默认不继承父代理的模型的问题
* 修复了使用 `--model haiku` 的 Bedrock/Vertex 用户显示错误选择的模型选择器
* 修复了权限请求选项标签中出现重复的 Bash 命令的问题
* 修复了后台任务完成时的嘈杂输出 - 现在显示干净的完成消息而不是原始输出
* 修复了后台任务完成通知，以主动显示项目符号点
* 修正了分叉斜线命令在取消时显示“AbortError”而不是“Interrupted”消息
* 修复了关闭权限对话框后光标消失的问题
* 修复了 `/hooks` 菜单在滚动到不同选项时选择错误的钩子类型的问题
* 修复了按 Esc 取消时排队提示中的图像显示为“\[object Object]”
* 修复了在后台任务中排队消息时图像被默默丢弃的问题
* 修复了粘贴大图像失败并出现“图像太大”错误的问题
* 修复了包含 CJK 字符（日语、中文、韩语）的多行提示中的额外空白行
* 修复了当用户提示文本换行至多行时 Ultrathink 关键字突出显示应用于错误字符的问题
* 修复了当思维块出现在中途时，折叠的“正在阅读 X 文件…”指示器错误地切换到过去时态的问题
* 修复了 Bash 读取命令（如 `ls` 和 `cat`）未计入折叠的读取/搜索组中，导致组错误地显示“读取 0 个文件”的问题
* 修复了旋转器令牌计数器，以便在执行期间正确累积来自子代理的令牌
* 修复了 git diff 解析中的内存泄漏，其中切片字符串保留了较大的父字符串
* 修复了 LSP 工具在启动期间可能返回“无服务器可用”的竞争条件
* 修复了网络请求超时时反馈提交无限期挂起的问题
* 修复了按向上箭头时退出插件发现和日志选择器视图中的搜索模式
* 修复了当钩子没有输出时显示尾随冒号的钩子成功消息
* 多项优化，提升启动性能
* 改进了使用本机安装程序或 Bun 时的终端渲染性能，特别是对于带有表情符号、ANSI 代码和 Unicode 字符的文本
* 提高了读取具有多个单元的 Jupyter 笔记本时的性能
* 提高了 `cat refactor.md | claude` 等管道输入的可靠性
* 提高了 AskQuestion 工具的可靠性
* 改进了 sed 就地编辑命令，以通过差异预览呈现为文件编辑
* 改进了 Claude，当由于输出令牌限制而导致响应被切断时，自动继续，而不是显示错误消息
* 提高压实可靠性*改进的子代理（任务工具）在权限被拒绝后继续工作，允许他们尝试替代方法
* 改进了在执行时显示进度的技能，以及在发生时显示工具使用情况
* 改进了 `/skills/` 目录的技能，默认在斜杠命令菜单中可见（在 frontmatter 中使用 `user-invocable: false` 选择退出）
* 改进了技能建议，优先考虑最近和经常使用的技能
* 改进了等待第一个响应令牌时的旋转器反馈
* 改进了微调器中的令牌计数显示，以包含来自后台代理的令牌
* 改进了异步代理的增量输出，为主线程提供更多控制和可见性
* 改进了权限提示用户体验，将选项卡提示移至页脚，使用上下文占位符更清晰的是/否输入标签
* 改进了 Chrome 通知中的 Claude，缩短了帮助文本并持续显示直至关闭
* 通过 TIFF 格式支持改进了 macOS 屏幕截图粘贴的可靠性
* 改进`/stats`输出
* 更新了 Atlassian MCP 集成以使用更可靠的默认配置（可流传输的 HTTP）
* 将“中断”消息颜色从红色更改为灰色，以减少令人惊慌的外观
* 删除了进入计划模式时的权限提示 - 用户现在无需批准即可进入计划模式
* 从图像参考链接中删除了下划线样式
* \[SDK] 将最小 zod 对等依赖项更改为 ^4.0.0
* \[VSCode] 将当前选择的模型名称添加到上下文菜单中
* \[VSCode] 在自动接受权限按钮上添加了描述性标签（例如，“是的，允许此项目使用 npm”而不是“是的，不要再询问”）
* \[VSCode] 修复了在 Markdown 内容中不渲染的段落分隔符
* \[VSCode] 修复了扩展中的滚动无意中滚动父 iframe 的问题
* \[Windows] 修复了渲染不当的问题## 2.0.76（2026年1月7日）

* 修复了在 Chrome 集成中使用 Claude 时 macOS 代码签名警告的问题

## 2.0.75（2026年1月7日）

* 小错误修复

## 2.0.74（2025年12月19日）

* 添加了 LSP（语言服务器协议）工具，用于代码智能功能，例如转到定义、查找引用和悬停文档
* 添加了对 Kitty、Alacritty、Zed 和 Warp 终端的 `/terminal-setup` 支持
* 在 `/theme` 中添加了 ctrl+t 快捷键来打开/关闭语法高亮显示
* 向主题选择器添加语法突出显示信息
* 添加了当 Alt 快捷键因终端配置而失败时针对 macOS 用户的指导
* 修复了技能 `allowed-tools` 未应用于该技能调用的工具的问题
* 修复了 Opus 4.5 提示在用户已经使用 Opus 时错误显示的问题
* 修复了语法高亮未正确初始化时可能发生的崩溃
* 修复了 `/plugins discover` 中的视觉错误，该错误在搜索框聚焦时显示列表选择指示器
* 修复了 macOS 键盘快捷键以显示“opt”而不是“alt”
* 改进了 `/context` 命令可视化，按来源、斜杠命令和排序的令牌计数对技能和代理进行分组
* \[Windows] 修复了渲染不当的问题
* \[VSCode] 年终促销信息添加礼品标签象形图

## 2.0.73（2025年12月19日）

* 添加了可点击的 `[Image #N]` 链接，可在默认查看器中打开附加图像
*添加了alt-y yank-pop以在ctrl-y yank后循环浏览杀戮环历史记录
* 在插件发现屏幕中添加了搜索过滤（键入按名称、描述或市场进行过滤）
* 添加了在使用 `--session-id` 与 `--resume` 或 `--continue` 和 `--fork-session` 组合分叉会话时对自定义会话 ID 的支持
* 修复了缓慢的输入历史循环和竞争条件，可能会在消息提交后覆盖文本
* 改进`/theme`命令直接打开主题选择器
* 改进的主题选择器 UI
* 使用统一的 SearchBox 组件改进了跨恢复会话、权限和插件屏幕的搜索用户体验
* \[VSCode] 添加了显示待处理权限（蓝色）和未读完成（橙色）的选项卡图标徽章

## 2.0.72（2025年12月17日）

* 在 Chrome（测试版）功能中添加了 Claude，该功能与 Chrome 扩展 ([https://claude.ai/chrome](https://claude.ai/chrome)) 一起使用，让您直接从 Claude Code 控制浏览器
* 减少终端闪烁
* 在移动应用程序提示中添加了可扫描的二维码，以便快速下载应用程序
* 恢复对话时添加加载指示器以获得更好的反馈
* 修复了 `/context` 命令在非交互模式下不遵守自定义系统提示的问题
* 修复了使用 Ctrl+Y 粘贴时连续 Ctrl+K 行的顺序
* 改进@提及文件建议速度（在 git 存储库中快 3 倍）
* 改进了包含 `.ignore` 或 `.rgignore` 文件的存储库中的文件建议性能
* 改进设置验证错误，使其更加突出
* 将思维切换从 Tab 更改为 Alt+T，以避免意外触发

## 2.0.71（2025年12月16日）* 添加了 /config 开关以启用/禁用提示建议
* 添加 `/settings` 作为 `/config` 命令的别名
* 修复了当光标位于路径中间时错误触发的@文件引用建议
* 修复了使用 `--dangerously-skip-permissions` 时无法加载 `.mcp.json` 中的 MCP 服务器的问题
* 修复了错误拒绝包含 shell glob 模式的有效 bash 命令的权限规则（例如 `ls *.txt`、`for f in *.png`）
* Bedrock：环境变量 `ANTHROPIC_BEDROCK_BASE_URL` 现在受到令牌计数和推理配置文件列表的尊重
* 用于本机构建的新语法突出显示引擎

## 2.0.70（2025年12月15日）

* 添加回车键立即接受并提交提示建议（选项卡仍接受编辑）
* 为 MCP 工具权限添加通配符语法 `mcp__server__*`，以允许或拒绝来自服务器的所有工具
* 为插件市场添加了自动更新切换，允许每个市场控制自动更新
* 添加 `current_usage` 字段到状态行输入，实现准确的上下文窗口百分比计算
* 修复了用户键入时处理排队命令时输入被清除的问题
* 修复了按 Tab 时替换键入输入的提示建议
* 修复了调整终端大小时差异视图不更新的问题
* 大型对话的内存使用量提高了 3 倍
* 提高了复制到剪贴板 (Ctrl+S) 的统计屏幕截图的分辨率，以获得更清晰的图像
* 删除了用于快速记忆输入的 # 快捷方式（告诉 Claude 编辑您的 CLAUDE.md）
* 修复 /config 中思维模式切换未正确持续的问题
* 改进文件创建权限对话框的 UI

## 2.0.69（2025年12月13日）

* 小错误修复

## 2.0.68（2025年12月12日）

* 通过将合成窗口正确定位在光标处，修复了 IME（输入法编辑器）对中文、日文和韩文等语言的支持
* 修复了模型可以看到不允许的 MCP 工具的错误
* 修复了子代理工作时转向消息可能丢失的问题
* 修复了选项+箭头单词导航，将整个 CJK（中文、日语、韩语）文本序列视为单个单词，而不是按单词边界导航
* 改进了计划模式退出用户体验：在计划为空或缺少计划退出时显示简化的是/否对话框，而不是抛出错误
* 添加对企业管理设置的支持。请联系您的 Anthropic 客户团队以启用此功能。

## 2.0.67（2025年12月12日）* Opus 4.5 现在默认启用思考模式
* 思维模式配置已移至/config
* 为 `/permissions` 命令添加了搜索功能，使用 `/` 键盘快捷键按工具名称过滤规则
* 显示 `/doctor` 中禁用自动更新程序的原因
* 修复了当另一个实例已使用最新版本时运行 `claude update` 时出现的错误“另一个进程当前正在更新 Claude”错误
* 修复了 `.mcp.json` 中的 MCP 服务器在非交互模式下运行时陷入挂起状态的问题（`-p` 标志或管道输入）
* 修复 `/permissions` 中删除权限规则后滚动位置重置的问题
* 修复了单词删除 (opt+delete) 和单词导航 (opt+arrow) 无法正确处理非拉丁文本（例如西里尔文、希腊语、阿拉伯语、希伯来语、泰语和中文）的问题
* 修复了 `claude install --force` 无法绕过过时的锁定文件的问题
* 修复了 CLAUDE.md 中连续的 @\~/ 文件引用由于 Markdown 删除线干扰而被错误解析的问题
* Windows：修复了插件 MCP 服务器由于日志目录路径中的冒号而失败的问题

## 2.0.65（2025年12月11日）

* 添加了使用 alt+p（linux、windows）、option+p（macos）编写提示时切换模型的功能。
* 添加上下文窗口信息到状态行输入
* 为自定义 `@` 文件搜索命令添加了 `fileSuggestion` 设置
* 添加了 `CLAUDE_CODE_SHELL` 环境变量来覆盖自动 shell 检测（当登录 shell 与实际工作 shell 不同时有用）
* 修复了使用 Escape 中止查询时提示未保存到历史记录中的问题
* 修复了读取工具图像处理，以从字节而不是文件扩展名识别格式

## 2.0.64（2025年12月10日）

* 即时自动压实
* 代理和bash命令可以异步运行并发送消息来唤醒主代理
* /stats 现在为用户提供有趣的 CC 统计数据，例如最喜爱的模型、使用情况图表、使用情况记录
* 添加了命名会话支持：使用 `/rename` 命名会话，在 REPL 中使用 `/resume <name>` 或从终端使用 `claude --resume <name>` 来恢复会话
* 添加了对 .claude/rules/\` 的支持。  有关详细信息，请参阅 [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)。
* 添加图像大小调整时的图像尺寸元数据，实现大图像的精确坐标映射
* 修复了使用本机安装程序时自动加载 .env
* 修复了使用 `--continue` 或 `--resume` 标志时忽略 `--system-prompt` 的问题
* 改进了 `/resume` 屏幕，带有分组分叉会话以及用于预览 (P) 和重命名 (R) 的键盘快捷键
* VSCode：在代码块和 bash 工具输入上添加了“复制到剪贴板”按钮
* VSCode：通过仿真回退到 x64 二进制，修复了扩展在 Windows ARM64 上不起作用的问题
* Bedrock：提高 token 计数效率
* Bedrock：添加对 `aws login` AWS 管理控制台凭证的支持
* 取消了 AgentOutputTool 和 BashOutputTool，转而采用新的统一 TaskOutputTool

## 2.0.62（2025年12月9日）* 选择题添加“（推荐）”标记，推荐选项移至列表顶部
* 添加了 `attribution` 设置以自定义提交和 PR 署名（弃用 `includeCoAuthoredBy`）
* 修复了当 \~/.claude 符号链接到项目目录时出现的重复斜杠命令
* 修复了当多个命令共享相同名称时斜杠命令选择不起作用的问题
* 修复了符号链接技能目录中的技能文件可能变成循环符号链接的问题
* 修复了由于锁定文件错误地过时而导致运行版本被删除的问题
* 修复了拒绝文件更改时 IDE diff 选项卡未关闭的问题

## 2.0.61（2025年12月7日）

* 由于响应问题，恢复了对多个终端客户端的 VSCode 支持。

## 2.0.60（2025年12月6日）

* 添加了后台代理支持。当您工作时，代理会在后台运行
* 添加了 --disable-slash-commands CLI 标志以禁用所有斜杠命令
* 在“Co-Authored-By”提交消息中添加了模型名称
*启用“/mcp启用\[服务器名称]”或“/mcp禁用\[服务器名称]”以快速切换所有服务器
* 更新了 Fetch 以跳过预先批准网站的摘要
* VSCode：添加了对多个终端客户端同时连接到 IDE 服务器的支持

## 2.0.59（2025年12月4日）

* 添加了 --agent CLI 标志来覆盖当前会话的代理设置
* 添加 `agent` 设置以使用特定代理的系统提示、工具限制和模型配置主线程
* VS Code：修复了从错误位置读取的 .claude.json 配置文件

## 2.0.58（2025年12月3日）

* 专业用户现在可以通过订阅访问 Opus 4.5！
* 修复了计时器持续时间显示“11m 60s”而不是“12m 0s”的问题
* Windows：托管设置现在更喜欢 `C:\Program Files\ClaudeCode`（如果存在）。未来版本将删除对 `C:\ProgramData\ClaudeCode` 的支持。

## 2.0.57（2025年12月3日）

* 添加拒绝计划时的反馈输入，允许用户告诉 Claude 要更改什么
* VSCode：添加流消息支持，实时响应显示

## 2.0.56（2025年12月2日）

* 添加了启用/禁用终端进度条的设置（OSC 9;4）
* VSCode 扩展：添加了对 VS Code 辅助侧边栏（VS Code 1.97+）的支持，允许 Claude Code 显示在右侧侧边栏，同时将文件资源管理器保留在左侧。需要在配置中将侧边栏设置为首选位置。

## 2.0.55（2025年11月26日）

* 修复了默认强制启用代理 DNS 解析的问题。现在通过 `CLAUDE_CODE_PROXY_RESOLVES_HOSTS=true` 环境变量选择加入
* 修复了在内存位置选择器中按住箭头键时键盘导航变得无响应的问题
* 改进了 AskUserQuestion 工具，可自动提交最后一个问题的单选问题，消除了简单问题流程的额外审查屏幕
* 改进了 `@` 文件建议的模糊匹配，结果更快、更准确

## 2.0.54（2025年11月26日）

* 挂钩：启用 PermissionRequest 挂钩来处理“始终允许”建议并应用权限更新
* 修复 iTerm 通知过多的问题

## 2.0.52（2025年11月24日）* 修复了使用命令行参数启动 Claude 时的重复消息显示
* 修复了 `/usage` 命令进度条，随着使用量的增加而填满（而不是显示剩余百分比）
* 修复了图像粘贴在运行 Wayland 的 Linux 系统上不起作用的问题（现在当 xclip 不可用时回退到 wl-paste）
* 允许在 bash 命令中使用 `$!`

## 2.0.51（2025年11月24日）

* 添加了 Opus 4.5！[官方公告](https://www.anthropic.com/news/claude-opus-4-5)
* 推出桌面版 Claude Code：[https://claude.com/download](https://claude.com/download)
* 为了让您有空间尝试我们的新模型，我们更新了 Claude Code 用户的使用限制。请参阅 Claude Opus 4.5 博客了解完整详细信息
* 专业用户现在可以购买额外的使用费来访问 Claude Code 中的 Opus 4.5
* Plan Mode 现在可以制定更精确的计划并更彻底地执行
* 使用限制通知现在更容易理解
* 将 `/usage` 切换回“已使用百分比”
* 修正了思维错误的处理
* 修复了性能回归问题

## 2.0.50（2025年11月21日）

* 修复了阻止调用输入模式中具有嵌套引用的 MCP 工具的错误
* 消除了升级期间吵闹但无害的错误
* 改进了ultrathink文本显示
* 提高了 5 小时会话限制警告消息的清晰度

## 2.0.49（2025年11月21日）

* 添加了 readline-style ctrl-y 用于粘贴已删除的文本
* 提高了使用限制警告消息的清晰度
* 修复了子代理权限的处理

## 2.0.47（2025年11月19日）

* 改进了 `claude --teleport` 的错误消息和验证
* 改进了 `/usage` 中的错误处理
*修复了历史条目在退出时未记录的竞争条件
* 修复了 `settings.json` 未应用 Vertex AI 配置的问题

## 2.0.46（2025年11月19日）

* 修复了当无法从元数据中检测到格式时报告的图像文件媒体类型不正确的问题

## 2.0.45（2025年11月18日）

* 添加了对 Microsoft Foundry 的支持！请参阅 [https://code.claude.com/docs/en/azure-ai-foundry](https://code.claude.com/docs/en/azure-ai-foundry)
* 添加了 `PermissionRequest` 挂钩，以使用自定义逻辑自动批准或拒绝工具权限请求
* 通过使用 `&` 发起消息，将后台任务发送到网络上的 Claude Code

## 2.0.43（2025年11月18日）

* 为自定义代理添加了 `permissionMode` 字段
* 为 `PreToolUseHookInput` 和 `PostToolUseHookInput` 类型添加了 `tool_use_id` 字段
* 添加了技能 frontmatter 字段来声明为子代理自动加载的技能
* 添加`SubagentStart`挂钩事件
* 修复了@提及文件时未加载嵌套 `CLAUDE.md` 文件的问题
* 修复了 UI 中某些消息的重复渲染
* 修复了一些视觉闪烁问题
* 修复了当单元格 ID 与模式 `cell-N` 匹配时 NotebookEdit 工具将单元格插入到错误位置的问题

## 2.0.42（2025年11月15日）

* 向 `SubagentStop` 挂钩添加了 `agent_id` 和 `agent_transcript_path` 字段。

## 2.0.41（2025年11月14日）* 为基于提示的停止钩子添加了 `model` 参数，允许用户指定用于钩子评估的自定义模型
* 修复了用户设置中的斜线命令被加载两次的问题，这可能会导致渲染问题
* 修复了命令描述中用户设置与项目设置的错误标签
* 修复了插件命令在执行过程中挂钩超时时崩溃的问题
* 已修复：使用 `--model haiku` 时，Bedrock 用户不再在 /model 选择器中看到重复的 Opus 条目
* 修复了信任对话框和入门中损坏的安全文档链接
* 修复了按 ESC 关闭 diff 模式也会中断模型的问题
* ctrl-r 历史搜索登陆斜杠命令不再取消搜索
* SDK：支持自定义hook超时时间
* 允许更安全的git命令在未经批准的情况下运行
* 插件：添加了对共享和安装输出样式的支持
* 从网络传送会话将自动设置上游分支

## 2.0.37（2025年11月11日）

* 修复了如何计算通知的空闲度
* 挂钩：为通知挂钩事件添加了匹配器值
* 输出样式：在 frontmatter 中添加 `keep-coding-instructions` 选项

## 2.0.36（2025年11月7日）

* 修复：DISABLE\_AUTOUPDATER 环境变量现在可以正确禁用包管理器更新通知
* 修复了排队消息被错误地执行为 bash 命令的问题
* 修复了在处理排队消息时键入时丢失的输入

## 2.0.35（2025年11月6日）

* 改进搜索命令时的模糊搜索结果
* 改进了 VS Code 扩展，以尊重整个 UI 中的 `chat.fontSize` 和 `chat.fontFamily` 设置，并立即应用字体更改，无需重新加载
* 添加了 `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` 环境变量，可在指定的空闲时间后自动退出 SDK 模式，对于自动化工作流程和脚本非常有用
* 将 `ignorePatterns` 从项目配置迁移到拒绝 localSettings 中的权限。
* 修复了菜单导航卡在具有空字符串或其他虚假值的项目上的问题（例如，在 `/hooks` 菜单中）

## 2.0.34（2025年11月5日）

* VSCode 扩展：添加了为新对话配置初始权限模式的设置
* 使用基于 Rust 的原生模糊查找器改进了文件路径建议性能
* 修复了导致带有 OAuth（例如 Slack）的 MCP 服务器在连接期间挂起的无限令牌刷新循环
* 修复了读取或写入大文件（尤其是 base64 编码的图像）时的内存崩溃问题

## 2.0.33（2025年11月4日）

* 本机二进制安装现在启动速度更快。
* 通过正确解析符号链接修复了 `claude doctor` 错误地检测 Homebrew 与 npm-global 安装的问题
* 修复了具有不兼容输出模式的 `claude mcp serve` 暴露工具

## 2.0.32（2025年11月4日）

* 根据社区反馈取消弃用输出样式
* 添加了 `companyAnnouncements` 设置以在启动时显示公告
* 修复了 PostToolUse 挂钩执行期间挂钩进度消息未正确更新的问题

## 2.0.31（2025年10月31日）* Windows：本机安装使用shift+tab作为模式切换的快捷方式，而不是alt+m
* Vertex：在支持的型号上添加对 Web 搜索的支持
* VSCode：添加respectGitIgnore配置以在文件搜索中包含.gitignored文件（默认为true）
* 修复了与“工具名称必须唯一”错误相关的子代理和 MCP 服务器的错误
* 修复了导致 `/compact` 与 `prompt_too_long` 一起失败的问题，使其尊重现有的紧凑边界
* 修复插件卸载不删除插件的问题

## 2.0.30（2025年10月30日）

* 添加了在钥匙串锁定的 macOS 上遇到 API 密钥错误时运行 `security unlock-keychain` 的有用提示
* 添加了 `allowUnsandboxedCommands` 沙箱设置，以在策略级别禁用危险的DisableSandbox逃生舱口
* 将 `disallowedTools` 字段添加到自定义代理定义中，以实现显式工具阻止
* 添加了基于提示的停止钩子
* VSCode：添加了respectGitIgnore配置以在文件搜索中包含.gitignored文件（默认为true）
* 在本机构建上启用 SSE MCP 服务器
* 不推荐使用的输出样式。查看 `/output-style` 中的选项并使用 --system-prompt-file、--system-prompt、--append-system-prompt、CLAUDE.md 或插件
* 删除了对自定义 ripgrep 配置的支持，解决了搜索不返回结果且配置发现失败的问题
* 修复了探索代理在代码库探索期间创建不需要的 .md 调查文件的问题
* 修复了`/context`有时会失败并出现“max\_tokens必须大于thinking.budget\_tokens”错误消息的错误
* 修复了 `--mcp-config` 标志以正确覆盖基于文件的 MCP 配置
* 修复了将会话权限保存到本地设置的错误
* 修复了子代理无法使用 MCP 工具的问题
* 修复了使用 --dangerously-skip-permissions 标志时不执行的挂钩和插件
* 修复了使用箭头键导航输入提示建议时的延迟
* VSCode：恢复输入页脚中的选择指示器，显示当前文件或代码选择状态

## 2.0.28（2025年10月27日）

* 计划模式：引入新的计划子代理
* 子代理：克劳德现在可以选择恢复子代理
* 子代理：claude可以动态选择其子代理使用的模型
* SDK：添加了 --max-budget-usd 标志
* 自定义斜杠命令、子代理和输出样式的发现不再遵循 .gitignore
* 阻止 `/terminal-setup` 在 VS Code 中向 `Shift + Enter` 添加反斜杠
* 使用片段语法添加对基于 git 的插件和市场的分支和标签支持（例如 `owner/repo#branch`）
* 修复了从主目录启动时首次启动时出现 macOS 权限提示的错误
* 各种其他错误修复

## 2.0.27（2025年10月24日）

* 新的权限提示 UI
* 添加了当前分支过滤和搜索到会话恢复屏幕，以便于导航
* 修复目录@-提及导致“未找到助手消息”错误
* VSCode 扩展：添加配置设置以在文件搜索中包含 .gitignored 文件
* VSCode 扩展：修复了不相关的“预热”对话的错误，并且配置/设置偶尔会重置为默认值

## 2.0.25（2025年10月21日）* 删除了旧版 SDK 入口点。请迁移到 @anthropic-ai/claude-agent-sdk 以获取未来的 SDK 更新：[https://platform.claude.com/docs/en/agent-sdk/migration-guide](https://platform.claude.com/docs/en/agent-sdk/migration-guide)

## 2.0.24（2025年10月20日）

* 修复了指定 --setting-sources 'project' 时未加载项目级技能的错误
* Claude Code Web：支持Web -> CLI teleport
* 沙箱：在 Linux 和 Mac 上为 BashTool 发布沙箱模式
* Bedrock：需要身份验证时显示 awsAuthRefresh 输出

## 2.0.22（2025年10月17日）

* 修复了滚动斜杠命令时内容布局发生变化的问题
* IDE：添加开关以启用/禁用思维。
* 修复并行工具调用导致重复权限提示的错误
* 添加对企业管理的 MCP 允许列表和拒绝列表的支持

## 2.0.21（2025年10月18日）

* 支持工具响应中的 MCP `structuredContent` 字段
* 新增互动提问工具
* Claude 现在会在计划模式下更频繁地询问您问题
* 添加 Haiku 4.5 作为 Pro 用户的模型选项
* 修复了排队命令无法访问先前消息输出的问题

## 2.0.20（2025年10月16日）

* 添加了对 Claude 技能的支持

## 2.0.19（2025年10月15日）

* 自动将长时间运行的 bash 命令置于后台而不是终止它们。使用 BASH\_DEFAULT\_TIMEOUT\_MS 进行自定义
* 修正了打印模式下不必要地调用 Haiku 的错误

## 2.0.17（2025年10月15日）

* 在模型选择器中添加了 Haiku 4.5！
* Haiku 4.5 在计划模式下自动使用 Sonnet，并在执行时使用 Haiku（即默认的 SonnetPlan）
* 3P（Bedrock 和 Vertex）尚未自动升级。可通过设置`ANTHROPIC_DEFAULT_HAIKU_MODEL`进行手动升级
* 引入 Explore 子代理。由 Haiku 提供支持，它将有效地搜索您的代码库以保存上下文！
* OTEL: 支持HTTP\_PROXY 和 HTTPS\_PROXY
* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 现在禁用发行说明获取

## 2.0.15（2025年10月14日）

*修复了恢复之前创建的文件在写入之前需要再次读取的错误
* 修复了 `-p` 模式下@提到的文件在写入之前需要再次读取的错误

## 2.0.14（2025年10月10日）

* 修复@提及 MCP 服务器以打开/关闭它们
* 使用内联环境变量改进 bash 的权限检查
* 修复超思考+思考切换
* 减少不必要的登录
* 文档--系统提示
* 对渲染的多项改进
* 插件 UI 优化

## 2.0.13（2025年10月9日）

* 修复了 `/plugin` 无法在本机构建上运行的问题

## 2.0.12（2025年10月9日）

* **插件系统发布**：使用来自市场的自定义命令、代理、挂钩和 MCP 服务器扩展 Claude Code
* 用于插件管理的 `/plugin install`、`/plugin enable/disable`、`/plugin marketplace` 命令
* 通过 `extraKnownMarketplaces` 进行存储库级插件配置，以实现团队协作
* `/plugin validate` 命令用于验证插件结构和配置
* 插件公告博客文章位于 [https://www.anthropic.com/news/claude-code-plugins](https://www.anthropic.com/news/claude-code-plugins)
* 插件文档可在 [https://code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) 获取
* 通过 `/doctor` 命令进行全面的错误消息和诊断
* 避免 `/model` 选择器闪烁
* `/help` 的改进
* 避免在 `/resume` 摘要中提及钩子
* 对 `/config` 中“详细”设置的更改现在在各个会话中持续存在## 2.0.11（2025年10月8日）

* 系统提示符大小减少了 1.4k 个令牌
* IDE：修复了键盘快捷键和焦点问题，以实现更顺畅的交互
* 修复了 Opus 回退速率限制错误显示不正确的问题
* 修复 /add-dir 命令选择错误的默认选项卡

## 2.0.10（2025年10月8日）

* 重写终端渲染器以实现流畅的 UI
* 通过@提及或在 /mcp 中启用/禁用 MCP 服务器
* 为 bash 模式下的 shell 命令添加制表符补全
* PreToolUse 挂钩现在可以修改工具输入
* 按 Ctrl-G 在系统配置的文本编辑器中编辑提示
* 修复了命令中环境变量的 bash 权限检查

## 2.0.9（2025年10月6日）

* 修复 bash 后台停止工作的回归

## 2.0.8（2025年10月4日）

* 将 Bedrock 默认 Sonnet 模型更新为 `global.anthropic.claude-sonnet-4-5-20250929-v1:0`
* IDE：添加对聊天中文件和文件夹的拖放支持
* /context：修复思维块的计数
* 改进在深色终端上使用浅色主题的用户的消息渲染
* 删除已弃用的 .claude.json allowedTools、ignorePatterns、env 和 todoFeatureEnabled 配置选项（而是在 settings.json 中配置这些选项）

## 2.0.5（2025年10月4日）

* IDE：修复 IME 使用 Enter 和 Tab 意外提交消息的问题
* IDE：在登录屏幕中添加“在终端中打开”链接
* 修复未处理的 OAuth 过期 401 API 错误
* SDK：添加了SDKUserMessageReplay.isReplay以防止重复消息

## 2.0.1（2025年9月30日）

* 跳过 Sonnet 4.5 对 Bedrock 和 Vertex 默认模型设置的更改
* 各种错误修复和演示改进

## 2.0.0（2025年9月29日）

* 新的原生 VS Code 扩展
* 整个应用程序焕然一新
* /倒带对话以撤消代码更改
* /usage 命令查看计划限制
* 用于切换思维的选项卡（跨会话粘性）
* Ctrl-R 搜索历史记录
* 未发货的克劳德配置命令
* 挂钩：发现减少了 PostToolUse 'tool\_use' id，没有 'tool\_result' 块错误
* SDK：Claude Code SDK 现为 Claude Agent SDK
* 使用 `--agents` 标志动态添加子代理

## 1.0.126（2025年9月26日）

* 为 Bedrock 和 Vertex 启用 /context 命令
* 添加对基于 HTTP 的 OpenTelemetry 导出器的 mTLS 支持

## 1.0.124（2025年9月25日）

* 将 `CLAUDE_BASH_NO_LOGIN` 环境变量设置为 1 或 true 以跳过 BashTool 的登录 shell
* 修复 Bedrock 和 Vertex 环境变量，将所有字符串评估为真实值
* 权限被拒绝时不再通知 Claude 允许使用的工具列表
* 修复了 Bash 工具权限检查中的安全漏洞
* 改进了 VSCode 对大文件的扩展性能

## 1.0.123（2025年9月23日）* Bash 权限规则现在支持匹配时的输出重定向（例如，`Bash(python:*)` 匹配 `python script.py > output.txt`）
* 修正了否定短语（如“不认为”）触发的思维模式
* 修复了令牌流期间渲染性能下降的问题
* 添加了 SlashCommand 工具，使 Claude 能够调用斜杠命令。详见[官方说明](https://code.claude.com/docs/en/slash-commands#SlashCommand-tool)。
* 增强 BashTool 环境快照日志记录
* 修复了在无头模式下恢复对话有时会导致不必要的思考的错误
* 迁移 --debug 日志记录到文件，以实现轻松的尾随和过滤

## 1.0.120（2025年9月19日）

* 修复打字过程中的输入滞后问题，尤其是在出现较大的提示时尤其明显
* 改进了 VSCode 扩展命令注册表和会话对话框用户体验
* 增强会话对话响应能力和视觉反馈
* 通过删除工作树支持检查修复了 IDE 兼容性问题
* 修复了使用前缀匹配可以绕过 Bash 工具权限检查的安全漏洞

## 1.0.119（2025年9月19日）

* 修复 Windows 进入交互模式时进程视觉冻结的问题
* 通过 headersHelper 配置支持 MCP 服务器的动态标头
* 修复思维模式在无头会话中不起作用的问题
* 修复斜杠命令现在可以正确更新允许的工具而不是替换它们

## 1.0.117（2025年9月19日）

* 添加 Ctrl-R 历史搜索来回忆以前的命令，如 bash/zsh
* 修复打字时的输入延迟问题，尤其是在 Windows 上
* 将sed命令添加到acceptEdits模式下自动允许的命令中
* 修复 Windows PATH 比较，使驱动器号不区分大小写
* 添加权限管理提示到 /add-dir 输出

## 1.0.115（2025年9月16日）

* 改进思维模式显示，增强视觉效果
* 输入 /t 暂时禁用提示中的思考模式
* 改进 glob 和 grep 工具的路径验证
* 显示后工具挂钩的压缩输出，以减少视觉混乱
* 修复加载状态完成时的视觉反馈
* 改进权限请求对话框的 UI 一致性

## 1.0.113（2025年9月13日）

* 交互模式下弃用管道输入
* 将用于切换转录的 Ctrl+R 键绑定移至 Ctrl+O

## 1.0.112（2025年9月12日）

* 转录模式（Ctrl+R）：添加了用于生成每条辅助消息的模型
* 解决了部分 Claude Max 用户被错误识别为 Claude Pro 用户的问题
* 挂钩：添加了对 SessionEnd 挂钩的 systemMessage 支持
* 添加了 `spinnerTipsEnabled` 设置以禁用旋转器提示
* IDE：各种改进和错误修复

## 1.0.111（2025年9月10日）

* /model 现在验证提供的模型名称
* 修复了由于 shell 语法解析错误导致的 Bash 工具崩溃问题

## 1.0.110（2025年9月10日）

* /terminal-setup 命令现在支持 WezTerm
* MCP：OAuth 令牌现在会在过期前主动刷新
* 修复了后台 Bash 进程的可靠性问题

## 1.0.109（2025年9月9日）

* SDK：通过 `--include-partial-messages` CLI 标志添加了部分消息流支持

## 1.0.106（2025年9月5日）

* Windows：修复了路径权限匹配以一致使用 POSIX 格式（例如 `Read(//c/Users/...)`）

## 1.0.97（2025年8月29日）* 设置：/doctor 现在验证权限规则语法并提出更正建议

## 1.0.94（2025年8月27日）

* Vertex：为支持的模型添加对全局端点的支持
* /memory 命令现在允许直接编辑所有导入的内存文件
* SDK：添加自定义工具作为回调
* 添加了 /todos 命令来列出当前待办事项

## 1.0.93（2025年8月26日）

* Windows：添加 alt + v 快捷键用于从剪贴板粘贴图像
* 支持 NO\_PROXY 环境变量来绕过指定主机名和 IP 的代理

## 1.0.90（2025年8月25日）

* 设置文件更改立即生效 - 无需重新启动

## 1.0.88（2025年8月22日）

* 修复了导致“当前不支持 OAuth 身份验证”的问题
* 状态行输入现在包括 `exceeds_200k_tokens`
* 修复了 /cost 中不正确的使用情况跟踪。
* 引入了 `ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_OPUS_MODEL` 用于控制模型别名 opusplan、opus 和 sonnet。
* Bedrock：将默认 Sonnet 模型更新为 Sonnet 4

## 1.0.86（2025年8月22日）

* 添加了 /context 以帮助用户自助调试上下文问题
* SDK：为所有 SDK 消息添加了 UUID 支持
* SDK：添加 `--replay-user-messages` 以将用户消息重播回标准输出

## 1.0.85（2025年8月19日）

* 状态行输入现在包括会话成本信息
* 钩子：引入了 SessionEnd 钩子

## 1.0.84（2025年8月18日）

* 修复网络不稳定时 tool\_use/tool\_result id 不匹配的错误
* 修复 Claude 在完成任务时有时会忽略实时转向的问题
* @-mention：将 \~/.claude/\* 文件添加到建议中，以便于代理、输出样式和斜杠命令编辑
* 默认使用内置的ripgrep；要选择退出此行为，请设置 USE\_BUILTIN\_RIPGREP=0

## 1.0.83（2025年8月18日）

* @-mention: 支持路径中带空格的文件
* 新的闪光旋转器

## 1.0.82（2025年8月16日）

* SDK：添加请求取消支持
* SDK：新的additionalDirectories选项用于搜索自定义路径，改进了斜杠命令处理
* 设置：验证可防止 .claude/settings.json 文件中的无效字段
* MCP：提高工具名称一致性
* Bash：修复 Claude 尝试自动读取大文件时崩溃的问题

## 1.0.81（2025年8月14日）

* 发布输出样式，包括新的内置教育输出样式“解释”和“学习”。文件：[https://code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles)
* 代理：修复代理文件无法解析时加载自定义代理的问题

## 1.0.80（2025年8月14日）

* UI 改进：修复自定义子代理颜色的文本对比度和微调器渲染问题

## 1.0.77（2025年8月14日）

* Bash 工具：修复heredoc和多行字符串转义，改进stderr重定向处理
* SDK：添加会话支持和权限拒绝跟踪
* 修复对话摘要中的令牌限制错误
* Opus Plan Mode：`/model` 中的新设置仅在计划模式下运行 Opus，否则运行 Sonnet

## 1.0.73（2025年8月11日）* MCP：`--mcp-config file1.json file2.json` 支持多个配置文件
* MCP：按 Esc 键取消 OAuth 身份验证流程
* Bash：改进了命令验证并减少了错误的安全警告
* UI：增强的旋转动画和状态行视觉层次结构
* Linux：添加了对 Alpine 和基于 musl 的发行版的支持（需要单独安装 ripgrep）

## 1.0.72（2025年8月11日）

* 询问权限：Claude Code 始终要求确认使用具有/权限的特定工具

## 1.0.71（2025年8月7日）

* 后台命令：(Ctrl-b) 在后台运行任何 Bash 命令，以便 Claude 可以继续工作（非常适合开发服务器、跟踪日志等）
* 可定制的状态行：使用 /statusline 将终端提示添加到 Claude Code

## 1.0.70（2025年8月7日）

* 性能：优化消息渲染，以在大上下文中获得更好的性能
* Windows：修复了本机文件搜索、ripgrep 和子代理功能
* 添加了对斜杠命令参数中@提及的支持

## 1.0.69（2025年8月5日）

* Opus升级至4.1版本

## 1.0.68（2025年8月4日）

* 修复某些命令使用的不正确的型号名称，例如 `/pr-comments`
* Windows：改进允许/拒绝工具和项目信任的权限检查。这可能会在 `.claude.json` 中创建一个新的项目条目 - 如果需要，可以手动合并历史字段。
* Windows：改进子进程生成，以消除运行 pnpm 等命令时的“没有此类文件或目录”
* 增强 /doctor 命令，带有 CLAUDE.md 和 MCP 工具上下文，用于自助调试
* SDK：新增canUseTool工具确认回调支持
* 添加`disableAllHooks`设置
* 改进了大型存储库中的文件建议性能

## 1.0.65（2025年7月31日）

* IDE：修复了连接稳定性问题和诊断错误处理
* Windows：修复了没有 .bashrc 文件的用户的 shell 环境设置

## 1.0.64（2025年7月30日）

* 代理：添加了模型定制支持 - 您现在可以指定代理应使用哪个模型
* 代理：修复了对递归代理工具的意外访问
* 挂钩：添加了 systemMessage 字段来挂钩 JSON 输出以显示警告和上下文
* SDK：修复了多轮对话中的用户输入跟踪
* 在文件搜索和@提及建议中添加了隐藏文件

## 1.0.63（2025年7月29日）

* Windows：修复了文件搜索、@agent 提及和自定义斜杠命令功能

## 1.0.62（2025年7月28日）

* 为自定义代理添加了@-mention 支持和预先输入。 @`<your-custom-agent>` 调用它
* 挂钩：添加了 SessionStart 挂钩，用于新会话初始化
* /add-dir 命令现在支持目录路径的预先输入
* 提高网络连接检查的可靠性

## 1.0.61（2025年7月25日）* 转录模式 (Ctrl+R)：将 Esc 更改为退出转录模式而不是中断
* 设置：添加了 `--settings` 标志以从 JSON 文件加载设置
* 设置：修复了作为符号链接的设置文件路径的分辨率
* OTEL：修复了身份验证更改后错误组织的报告
* 斜线命令：修复了 Bash 允许工具的权限检查
* IDE：添加了对使用 ⌘+V 在 VSCode MacOS 中粘贴图像的支持
* IDE：添加 `CLAUDE_CODE_AUTO_CONNECT_IDE=false` 用于禁用 IDE 自动连接
* 添加了 `CLAUDE_CODE_SHELL_PREFIX`，用于包装 Claude 和由 Claude Code 运行的用户提供的 shell 命令

## 1.0.60（2025年7月24日）

* 您现在可以为专门任务创建自定义子代理！运行 /agents 开始

## 1.0.59（2025年7月23日）

* SDK：添加了带有canUseTool回调的工具确认支持
* SDK：允许为生成的进程指定环境
* Hooks：将 PermissionDecision 暴露给 hooks（包括“ask”）
* 挂钩：UserPromptSubmit 现在支持高级 JSON 输出中的additionalContext
* 修复了一些指定 Opus 的 Max 用户仍会看到回退到 Sonnet 的问题

## 1.0.58（2025年7月23日）

* 添加了对阅读 PDF 的支持
* MCP：改进了“claude mcp list”中的服务器健康状态显示
* 挂钩：为挂钩命令添加了 CLAUDE\_PROJECT\_DIR 环境变量

## 1.0.57（2025年7月23日）

* 添加了对在斜杠命令中指定模型的支持
* 改进了权限消息以帮助 Claude 了解允许的工具
* 修复：从终端包装中的 bash 输出中删除尾随换行符

## 1.0.56（2025年7月23日）

* Windows：在支持终端VT模式的Node.js版本上启用shift+tab进行模式切换
* 修复了 WSL IDE 检测
* 修复了导致 awsRefreshHelper 对 .aws 目录的更改无法被拾取的问题

## 1.0.55（2025年7月23日）

* 澄清了 Opus 4 和 Sonnet 4 型号的知识截止点
* Windows：修复了 Ctrl+Z 崩溃问题
* SDK：添加了捕获错误日志记录的功能
* 添加 --system-prompt-file 选项以覆盖打印模式下的系统提示

## 1.0.54（2025年7月19日）

* 挂钩：添加了 UserPromptSubmit 挂钩和当前工作目录来挂钩输入
* 自定义斜线命令：向 frontmatter 添加参数提示
* Windows：OAuth 使用端口 45454 并正确构建浏览器 URL
* Windows：模式切换现在使用 alt + m，并且计划模式可以正确渲染
* Shell：切换到内存中的shell快照来修复与文件相关的错误

## 1.0.53（2025年7月18日）

* 将 @-mention 文件截断从 100 行更新为 2000 行
* 添加 AWS 令牌刷新的帮助程序脚本设置：awsAuthRefresh（适用于 aws sso 登录等前台操作）和 awsCredentialExport（适用于具有类似 STS 响应的后台操作）。

## 1.0.52（2025年7月18日）

* 添加了对 MCP 服务器指令的支持

## 1.0.51（2025年7月11日）* 添加了对本机 Windows 的支持（Windows 需要 Git）
* 通过环境变量 AWS\_BEARER\_TOKEN\_BEDROCK 添加了对 Bedrock API 密钥的支持
* 设置：/doctor 现在可以帮助您识别和修复无效的设置文件
* `--append-system-prompt` 现在可以在交互模式下使用，而不仅仅是 --print/-p。
* 自动压缩警告阈值从 60% 增加到 80%
* 修复了处理带有 shell 快照空间的用户目录的问题
* OTEL 资源现在包括 os.type、os.version、host.arch 和 wsl.version（如果在 Linux 的 Windows 子系统上运行）
* 自定义斜线命令：修复子目录中的用户级命令
* 计划模式：修复了子任务中拒绝的计划将被丢弃的问题

## 1.0.48（2025年7月10日）

* 修复了 v1.0.45 中应用程序有时会在启动时冻结的错误
* 根据最后 5 行命令输出向 Bash 工具添加进度消息
* 添加了对 MCP 服务器配置的扩展变量支持
* 将 shell 快照从 /tmp 移至 \~/.claude，以获得更可靠的 Bash 工具调用
* 改进了 Claude Code 在 WSL 中运行时的 IDE 扩展路径处理
* 挂钩：添加了 PreCompact 挂钩
* Vim 模式：添加了 c、f/F、t/T

## 1.0.45（2025年7月10日）

* 重新设计的搜索 (Grep) 工具，具有新的工具输入参数和功能
* 禁用笔记本文件的 IDE 差异，修复“1000 毫秒后超时等待”错误
* 通过强制原子写入修复了配置文件损坏问题
* 将提示输入撤消更新为 Ctrl+\_ 以避免破坏现有的 Ctrl+U 行为，匹配 zsh 的撤消快捷方式
* Stop Hooks：修复了 /clear 后的转录路径，并修复了循环以工具调用结束时的触发
* 自定义斜杠命令：根据子目录恢复命令名称中的命名空间。例如，.claude/commands/frontend/component.md 现在是 /frontend:component，而不是 /component。

## 1.0.44（2025年7月7日）

* 新的 /export 命令可让您快速导出对话以进行共享
* MCP：现在支持资源\_link工具结果
* MCP：工具注释和工具标题现在显示在 /mcp 视图中
* 更改了 Ctrl+Z 以暂停 Claude Code。通过运行 `fg` 恢复。提示输入撤消现在是 Ctrl+U。

## 1.0.43（2025年7月3日）

* 修复了主题选择器保存过多的错误
* Hooks：添加EPIPE系统错误处理

## 1.0.42（2025年7月3日）

* 为 `/add-dir` 命令添加了波形符 (`~`) 扩展支持

## 1.0.41（2025年7月3日）

* 挂钩：将 Stop 挂钩触发拆分为 Stop 和 SubagentStop
* Hooks：为每个命令启用可选的超时配置
* 挂钩：添加“hook\_event\_name”来挂钩输入
* 修复了 MCP 工具在工具列表中显示两次的错误
* `tool_decision` 事件中 Bash 工具的新工具参数 JSON

## 1.0.40（2025年7月3日）

* 修复了如果设置了 `NODE_EXTRA_CA_CERTS` 则导致 API 连接错误且出现 UNABLE\_TO\_GET\_ISSUER\_CERT\_LOCALLY 的错误

## 1.0.39（2025年7月3日）

* OpenTelemetry 日志记录中的新活动时间指标

## 1.0.38（2025年6月30日）

* 释放钩子。特别感谢社区在 [https://github.com/anthropics/claude-code/issues/712](https://github.com/anthropics/claude-code/issues/712) 中的投入。文件：[https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

## 1.0.37（2025年6月30日）

* 删除通过 ANTHROPIC\_AUTH\_TOKEN 或 apiKeyHelper 设置 `Proxy-Authorization` 标头的功能## 1.0.36（2025年6月30日）

* 网络搜索现在将今天的日期纳入上下文
* 修复了 stdio MCP 服务器在退出时未正确终止的错误

## 1.0.35（2025年6月25日）

* 添加了对 MCP OAuth 授权服务器发现的支持

## 1.0.34（2025年6月24日）

* 修复了导致出现 MaxListenersExceededWarning 消息的内存泄漏

## 1.0.33（2025年6月24日）

* 通过会话 ID 支持改进了日志记录功能
* 添加提示输入撤消功能（Ctrl+Z 和 vim 'u' 命令）
* 计划模式的改进

## 1.0.32（2025年6月24日）

* 更新了 litellm 的环回配置
* 添加了forceLoginMethod设置以绕过登录选择屏幕

## 1.0.31（2025年6月24日）

* 修复了当文件包含无效 JSON 时 \~/.claude.json 会被重置的错误

## 1.0.30（2025年6月24日）

* 自定义斜线命令：运行 bash 输出、@-提及文件、使用思考关键字进行思考
* 改进了文件路径自动完成和文件名匹配
* 在 Ctrl-r 模式下添加了时间戳并修复了 Ctrl-c 处理
* 增强了 jq 正则表达式对带有管道和选择的复杂过滤器的支持

## 1.0.29（2025年6月24日）

* 改进了光标导航和渲染中的 CJK 字符支持

## 1.0.28（2025年6月24日）

* 斜线命令：修复历史导航期间选择器的显示
* 上传前调整图片大小以防止 API 大小限制错误
* 添加了 XDG\_CONFIG\_HOME 对配置目录的支持
* 内存使用性能优化
* OpenTelemetry 日志记录中的新属性（terminal.type、语言）

## 1.0.27（2025年6月18日）

* 现在支持可流式 HTTP MCP 服务器
* 远程 MCP 服务器（SSE 和 HTTP）现在支持 OAuth
* MCP资源现在可以被@提及
* /resume 斜杠命令用于在 Claude Code 内切换对话

## 1.0.25（2025年6月16日）

* 斜线命令：将“项目”和“用户”前缀移至描述中
* 斜线命令：提高命令发现的可靠性
* 改进了对 Ghostty 的支持
* 提高网络搜索的可靠性

## 1.0.24（2025年6月16日）

* 改进/mcp输出
* 修复了设置数组被覆盖而不是合并的错误

## 1.0.23（2025年6月16日）

* 发布 TypeScript SDK：导入@anthropic-ai/claude-code 开始使用
* 发布Python SDK：pip install claude-code-sdk即可开始使用

## 1.0.22（2025年6月12日）

* SDK：将 `total_cost` 重命名为 `total_cost_usd`

## 1.0.21（2025年6月12日）

* 改进了基于制表符缩进的文件编辑
* 修复工具\_use 没有匹配工具\_结果的错误
* 修复了退出 Claude Code 后 stdio MCP 服务器进程会持续存在的错误

## 1.0.18（2025年6月9日）* 添加了 --add-dir CLI 参数来指定其他工作目录
* 添加了流输入支持，无需 -p 标志
* 改进启动性能和会话存储性能
* 添加了 CLAUDE\_BASH\_MAINTAIN\_PROJECT\_WORKING\_DIR 环境变量以冻结 bash 命令的工作目录
* 添加了详细的 MCP 服务器工具显示 (/mcp)
* MCP 身份验证和权限改进
* 添加了断开连接时 MCP SSE 连接的自动重新连接
* 修复了出现对话框时粘贴内容丢失的问题

## 1.0.17（2025年6月9日）

* 我们现在以 -p 模式从子任务发出消息（查找parent\_tool\_use\_id 属性）
* 修复了快速多次调用 VS Code diff 工具时的崩溃问题
* MCP 服务器列表 UI 改进
* 更新 Claude Code 进程标题以显示“claude”而不是“node”

## 1.0.11（2025年6月4日）

* Claude Code 现在也可以与 Claude Pro 订阅一起使用
* 添加/升级以更平滑地切换到 Claude Max 计划
* 改进了 API 密钥和 Bedrock/Vertex/外部身份验证令牌身份验证的 UI
* 改进了 shell 配置错误处理
* 改进了压缩过程中的待办事项列表处理

## 1.0.10（2025年6月4日）

* 添加了 Markdown 表格支持
* 改进的流媒体性能

## 1.0.8（2025年6月2日）

* 修复了使用 CLOUD\_ML\_REGION 时 Vertex AI 区域回退的问题
* 将默认酒店间隔从 1 秒增加到 5 秒
* 修复了未考虑 MCP\_TIMEOUT 和 MCP\_TOOL\_TIMEOUT 的边缘情况
* 修复了搜索工具不必要地请求权限的回归问题
* 增加了对非英语语言触发思维的支持
* 改进了压缩 UI

## 1.0.7（2025年6月2日）

* 重命名为 /allowed-tools -> /permissions
* 从 .claude.json -> settings.json 迁移 allowedTools 和ignorePatterns
* 弃用 claude 配置命令，改为编辑 settings.json
* 修复了 --dangerously-skip-permissions 有时在 --print 模式下不起作用的错误
* 改进了 /install-github-app 的错误处理
* 错误修复、UI 优化和工具可靠性改进

## 1.0.6（2025年6月2日）

* 提高了制表符缩进文件的编辑可靠性
* 处处尊重 CLAUDE\_CONFIG\_DIR
* 减少不必要的工具权限提示
* 添加了对 @file typeahead 中符号链接的支持
* 错误修复、UI 优化和工具可靠性改进

## 1.0.4（2025年5月28日）

* 修复了 MCP 工具错误无法正确解析的错误

## 1.0.1（2025年5月22日）

* 添加了 `DISABLE_INTERLEAVED_THINKING`，让用户可以选择退出交错思维。
* 改进了模型参考以显示特定于提供商的名称（Sonnet 3.7 用于 Bedrock，Sonnet 4 用于 Console）
* 更新了文档链接和 OAuth 流程描述

## 1.0.0（2025年5月22日）

* Claude Code 现已全面上市
* 推出 Sonnet 4 和 Opus 4 型号

## 0.2.125（2025年5月21日）

* 重大更改：传递给 `ANTHROPIC_MODEL` 或 `ANTHROPIC_SMALL_FAST_MODEL` 的 Bedrock ARN 不应再包含转义斜杠（指定 `/` 而不是 `%2F`）
* 删除 `DEBUG=true` 以支持 `ANTHROPIC_LOG=debug`，以记录所有请求

## 0.2.117（2025年5月17日）* 重大更改：--print JSON 输出现在返回嵌套消息对象，以实现向前兼容性，因为我们引入了新的元数据字段
* 引入了settings.cleanupPeriodDays
* 引入了 CLAUDE\_CODE\_API\_KEY\_HELPER\_TTL\_MS 环境变量
* 引入--调试模式

## 0.2.108（2025年5月13日）

* 现在，您可以在 Claude 实时操纵 Claude 的同时向 Claude 发送消息
* 引入了 BASH\_DEFAULT\_TIMEOUT\_MS 和 BASH\_MAX\_TIMEOUT\_MS 环境变量
* 修复了思考在 -p 模式下不起作用的错误
*修复了/成本报告中的回归
* 已弃用 MCP 向导界面，转而使用其他 MCP 命令
* 许多其他错误修复和改进

## 0.2.107（2025年5月9日）

* CLAUDE.md 文件现在可以导入其他文件。将 @path/to/file.md 添加到 ./CLAUDE.md 以在启动时加载其他文件

## 0.2.106（2025年5月9日）

* MCP SSE 服务器配置现在可以指定自定义标头
* 修复了 MCP 权限提示并不总是正确显示的错误

## 0.2.105（2025年5月8日）

* Claude现在可以在网络上搜索
* 将系统和帐户状态移至/status
* 添加了 Vim 的文字移动键绑定
* 改进了启动、待办事项工具和文件编辑的延迟

## 0.2.102（2025年5月5日）

* 提高思维触发的可靠性
* 改进了图像和文件夹@mention 的可靠性
* 您现在可以将多个大块粘贴到一个提示中

## 0.2.100（2025年5月2日）

* 修复了由于堆栈溢出错误导致的崩溃
* 使数据库存储成为可选；缺少数据库支持会禁用 --continue 和 --resume

## 0.2.98（2025年5月1日）

* 修复了自动压缩运行两次的问题

## 0.2.96（2025年5月1日）

* Claude Code 现在也可以与 Claude Max 订阅一起使用 ([https://claude.ai/upgrade](https://claude.ai/upgrade))

## 0.2.93（2025年4月30日）

* 使用“claude --continue”和“claude --resume”从中断处继续对话
* Claude 现在可以访问待办事项列表，帮助其保持在正轨上并更有条理

## 0.2.82（2025年4月25日）

* 添加了对 --disallowedTools 的支持
* 重命名工具以保持一致性：LSTool -> LS、View -> Read 等。

## 0.2.75（2025年4月21日）

* 当 Claude 工作时，按 Enter 键可对其他消息进行排队
* 将图像文件直接拖入或复制/粘贴到提示中
* @-提及文件以直接将它们添加到上下文中
* 使用 `claude --mcp-config ` 运行一次性 MCP 服务器
* 改进了文件名自动完成的性能

## 0.2.74（2025年4月18日）

* 添加了对刷新动态生成的 API 密钥（通过 apiKeyHelper）的支持，TTL 为 5 分钟
* 任务工具现在可以执行写入并运行 bash 命令

## 0.2.72（2025年4月18日）

* 更新了微调器以指示已加载的令牌和工具使用情况

## 0.2.70（2025年4月17日）

* 像curl这样的网络命令现在可供Claude使用
* Claude 现在可以并行运行多个 Web 查询
* 按一次 ESC 立即中断处于自动接受模式的 Claude

## 0.2.69（2025年4月17日）

* 修复了 UI 故障并改进了 Select 组件行为
* 增强终端输出显示，具有更好的文本截断逻辑

## 0.2.67（2025年4月17日）

* 共享项目权限规则可以保存在.claude/settings.json中

## 0.2.66（2025年4月17日）* 打印模式 (-p) 现在支持通过 --output-format=stream-json 进行流式输出
* 修复了粘贴可能意外触发内存或 bash 模式的问题

## 0.2.63（2025年4月17日）

* 修复MCP工具加载两次导致工具调用错误的问题

## 0.2.61（2025年4月2日）

* 使用 vim 风格的键 (j/k) 或 bash/emacs 快捷键 (Ctrl+n/p) 导航菜单，以实现更快的交互
* 增强图像检测以实现更可靠的剪贴板粘贴功能
* 修复了 ESC 键可能导致对话历史选择器崩溃的问题

## 0.2.59（2025年4月2日）

* 将图像直接复制+粘贴到提示中
* 改进了 bash 和 fetch 工具的进度指示器
* 非交互模式的错误修复 (-p)

## 0.2.54（2025年4月2日）

* 以“#”开头的消息可以快速添加到内存中
* 按 ctrl+r 查看长工具结果的完整输出
* 添加了对 MCP SSE 传输的支持

## 0.2.53（2025年4月2日）

* 新的网络获取工具可让 Claude 查看您粘贴的 URL
* 修复了 JPEG 检测的错误

## 0.2.50（2025年4月2日）

* 新的 MCP“项目”范围现在允许您将 MCP 服务器添加到 .mcp.json 文件并将它们提交到您的存储库

## 0.2.49（2025年4月2日）

* 以前的 MCP 服务器范围已重命名：以前的“项目”范围现在是“本地”，“全局”范围现在是“用户”

## 0.2.47（2025年4月2日）

* 按 Tab 键自动补全文件和文件夹名称
* 按 Shift + Tab 切换自动接受文件编辑
* 自动对话压缩无限对话长度（使用 /config 切换）

## 0.2.44（2025年4月2日）

* 让Claude用思维模式制定计划：只需说“思考”或“更努力地思考”甚至“超思考”

## 0.2.41（2025年4月2日）

* MCP 服务器启动超时现在可以通过 MCP\_TIMEOUT 环境变量进行配置
* MCP 服务器启动不再阻止应用程序启动

## 0.2.37（2025年4月2日）

* 新的 /release-notes 命令可让您随时查看发行说明
* `claude config add/remove` 命令现在接受以逗号或空格分隔的多个值

## 0.2.36（2025年4月2日）

* 使用 `claude mcp add-from-claude-desktop` 从 Claude Desktop 导入 MCP 服务器
* 将 MCP 服务器添加为 JSON 字符串和 `claude mcp add-json <n> <json>`

## 0.2.34（2025年4月2日）

* 用于文本输入的 Vim 绑定 - 使用 /vim 或 /config 启用

## 0.2.32（2025年4月2日）

* 交互式 MCP 设置向导：运行“claude mcp add”通过分步界面添加 MCP 服务器
* 修复一些 PersistentShell 问题

## 0.2.31（2025年4月2日）

* 自定义斜杠命令：.claude/commands/ 目录中的 Markdown 文件现在显示为自定义斜杠命令，可将提示插入对话中
* MCP 调试模式：使用 --mcp-debug 标志运行以获取有关 MCP 服务器错误的更多信息

## 0.2.30（2025年4月2日）

* 新增 ANSI 颜色主题，更好的终端兼容性
* 修复了斜杠命令参数未正确发送的问题
*（仅限 Mac）API 密钥现在存储在 macOS 钥匙串中

## 0.2.26（2025年4月2日）

* 用于管理工具权限的新 /approved-tools 命令
* 字级差异显示，提高代码可读性
* 斜杠命令的模糊匹配## 0.2.21（2025年4月2日）

* /命令的模糊匹配
