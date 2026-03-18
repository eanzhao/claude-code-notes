---
title: "工具参考"
order: 60
section: "reference"
sectionLabel: "参考"
sectionOrder: 8
summary: "Claude Code 可以使用的工具的完整参考，包括权限要求。"
sourceUrl: "https://code.claude.com/docs/en/tools-reference.md"
sourceTitle: "Tools reference"
tags: []
---
# 工具参考

> Claude Code 可用工具的完整参考，包括权限要求。

Claude Code 可以使用一组工具来理解和修改你的代码库。下面的工具名称是你在[权限规则](./permissions#tool-specific-permission-rules)、[子代理工具列表](./sub-agents)和 [hook 匹配器](./hooks)中使用的确切字符串。

| 工具 | 说明 | 需要权限 |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `Agent` | 生成一个拥有独立上下文窗口的[子代理](./sub-agents)来处理任务 | 否 |
| `AskUserQuestion` | 提出多选题来收集需求或澄清歧义 | 否 |
| `Bash` | 在你的环境中执行 shell 命令。详见 [Bash 工具行为](#bash-工具行为) | 是 |
| `CronCreate` | 在当前会话中安排重复或一次性提示（Claude 退出后失效）。详见[计划任务](./scheduled-tasks) | 否 |
| `CronDelete` | 按 ID 取消计划任务 | 否 |
| `CronList` | 列出会话中的所有计划任务 | 否 |
| `Edit` | 对指定文件进行精确编辑 | 是 |
| `EnterPlanMode` | 在写代码之前切换到计划模式来设计方案 | 否 |
| `EnterWorktree` | 创建隔离的 [git worktree](./common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 并切换进去 | 否 |
| `ExitPlanMode` | 提交计划供审批并退出计划模式 | 是 |
| `ExitWorktree` | 退出 worktree 会话并返回原目录 | 否 |
| `Glob` | 按模式匹配查找文件 | 否 |
| `Grep` | 搜索文件内容中的模式 | 否 |
| `ListMcpResourcesTool` | 列出已连接 [MCP 服务器](./mcp)暴露的资源 | 否 |
| `LSP` | 通过语言服务器进行代码智能。文件编辑后自动报告类型错误和警告。还支持导航操作：跳转到定义、查找引用、获取类型信息、列出符号、查找实现、跟踪调用层次。需要[代码智能插件](./discover-plugins#code-intelligence)及其语言服务器二进制文件 | 否 |
| `NotebookEdit` | 修改 Jupyter notebook 单元格 | 是 |
| `Read` | 读取文件内容 | 否 |
| `ReadMcpResourceTool` | 通过 URI 读取特定 MCP 资源 | 否 |
| `Skill` | 在主对话中执行[技能](./skills#control-who-invokes-a-skill) | 是 |
| `TaskCreate` | 在任务列表中创建新任务 | 否 |
| `TaskGet` | 获取特定任务的完整详情 | 否 |
| `TaskList` | 列出所有任务及其当前状态 | 否 |
| `TaskOutput` | 获取后台任务的输出 | 否 |
| `TaskStop` | 按 ID 终止正在运行的后台任务 | 否 |
| `TaskUpdate` | 更新任务状态、依赖、详情或删除任务 | 否 |
| `TodoWrite` | 管理会话任务清单。可用于非交互模式和 [Agent SDK](./headless)；交互式会话使用 TaskCreate、TaskGet、TaskList 和 TaskUpdate | 否 |
| `ToolSearch` | 启用[工具搜索](./mcp#scale-with-mcp-tool-search)时搜索并加载延迟工具 | 否 |
| `WebFetch` | 从指定 URL 获取内容 | 是 |
| `WebSearch` | 执行网络搜索 | 是 |
| `Write` | 创建或覆盖文件 | 是 |

可以通过 `/permissions` 或在[权限设置](./settings#available-settings)中配置权限规则。另请参阅[工具专属权限规则](./permissions#tool-specific-permission-rules)。

## Bash 工具行为

Bash 工具在独立进程中运行每条命令，有以下持久性行为：

* 工作目录在命令间保持不变。设置 `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` 可在每条命令后重置回项目目录。
* 环境变量不会跨命令持久化。一条命令中的 `export` 在下一条命令中不可用。

启动 Claude Code 前请先激活你的 virtualenv 或 conda 环境。要让环境变量在 Bash 命令中持续生效，可在启动 Claude Code 前将 [`CLAUDE_ENV_FILE`](./env-vars) 设为一个 shell 脚本，或使用 [SessionStart hook](./hooks#persist-environment-variables) 动态填充它。

## 另请参阅

* [权限](./permissions)：权限系统、规则语法和工具专属模式
* [子代理](./sub-agents)：配置子代理的工具访问权限
* [Hooks](./hooks-guide)：在工具执行前后运行自定义命令
