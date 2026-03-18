---
title: "Claude Code 系统学习路线"
order: 0
section: "getting-started"
sectionLabel: "快速入门"
sectionOrder: 1
group: "curated"
groupLabel: "学习辅助"
summary: "先学什么、后学什么，以及 Desktop app 和 CLI 用户最值得优先吃透的能力。"
tags: []
---

# Claude Code 系统学习路线

这页不是官方原文，而是给你这种主要通过 Claude Desktop app 和 `claude` CLI 使用 Claude Code 的人准备的一条学习主线。官方文档很全，但页数多、话题散。如果一开始就从头平推，通常会记住很多名词，却很难建立手感。

我的建议很直接：先把“Claude Code 到底怎么工作”吃透，再去学权限、记忆、常用工作流，最后才是 MCP、hooks、skills、plugins 这些扩展能力。顺序对了，学习成本会低很多。

## 第一阶段：先把基本手感练出来

1. 看 [概览](./overview)。
2. 看 [快速开始](./quickstart)。
3. 接着看 [Claude Code 的工作原理](./how-claude-code-works)。
4. 再看 [常见工作流](./common-workflows)。

这一轮的目标只有一个：知道 Claude Code 平时会怎么读代码、什么时候会改文件、什么时候会跑命令、你应该怎样打断它、怎样把任务说清楚。

如果你平时主要用桌面端，这时顺手读掉 [Desktop 快速开始](./desktop-quickstart) 和 [Claude Code Desktop](./desktop)。如果你主要在终端里用，就把 [CLI 参考](./cli-reference) 和 [交互模式](./interactive-mode) 提前看一遍。

## 第二阶段：把“可控性”学明白

这一阶段最重要，尤其是你开始让 Claude 帮你真实改项目之后。

建议顺序：

1. [权限配置](./permissions)
2. [设置](./settings)
3. [记忆机制](./memory)
4. [最佳实践](./best-practices)
5. [Checkpointing](./checkpointing)

你会发现 Claude Code 好不好用，很多时候不取决于模型本身，而取决于三件事：

- 你给了多少明确上下文
- 你允许它做到什么程度
- 你有没有给它“自证正确”的办法，比如测试、lint、预览、diff、CI

这几页看完以后，你对 `CLAUDE.md`、自动记忆、权限模式、上下文压缩、会话恢复这些核心概念就基本不会再混。

## 第三阶段：针对你最常用的两个入口深挖

### 如果你更常用 Claude Desktop app

优先读这些：

1. [Claude Code Desktop](./desktop)
2. [远程控制](./remote-control)
3. [Claude Code on the web](./claude-code-on-the-web)
4. [Chrome 集成](./chrome)
5. [计划模式、并行会话、工作树相关内容](./common-workflows)

Desktop 最值钱的地方，不只是“有图形界面”，而是它把几个高价值能力串起来了：

- diff review
- app preview
- 并行 session
- worktree 隔离
- 远程长任务
- 定时任务

这些能力配合起来，特别适合改前端、跟 CI、修线上小问题，或者同时跑几条线索。

### 如果你更常用 CLI

优先读这些：

1. [CLI 参考](./cli-reference)
2. [内置命令](./commands)
3. [交互模式](./interactive-mode)
4. [工具参考](./tools-reference)
5. [沙箱机制](./sandboxing)
6. [终端优化](./terminal-config)

CLI 的关键不是记住所有 flag，而是把下面这些套路练熟：

- `claude` 开交互式会话
- `claude -p` 做一次性查询或接到脚本里
- `claude -c` / `claude -r` 接着之前的上下文干
- 用 `--permission-mode`、`--allowedTools`、`--tools` 控制风险
- 用 worktree 跑并行任务

终端里一旦这些习惯成型，Claude Code 会很像一个能持续协作的工程搭子，而不是“会聊天的命令行工具”。

## 第四阶段：开始扩展 Claude Code

这一块别太早学。等前面几阶段熟了，再读会轻松很多。

建议顺序：

1. [扩展能力总览](./features-overview)
2. [Skills](./skills)
3. [Subagents](./sub-agents)
4. [Hooks 指南](./hooks-guide)
5. [MCP](./mcp)
6. [Plugins](./plugins)

这一部分最容易掉进一个坑：看到什么都想接，结果项目里塞满规则、hooks、MCP、plugins，最后谁也不敢动。我的经验是先少量接入，先解决具体问题，再考虑体系化。

比如：

- 想让 Claude 总按你的项目约定做事，先写好 `CLAUDE.md`
- 想让它改完自动格式化或自动提醒，先上 hooks
- 想接外部系统，再看 MCP
- 想封装成可分发能力，再看 plugins

## 第五阶段：进入自动化和团队协作

如果你后面想把 Claude Code 用到团队里，这一段再补：

1. [GitHub Actions](./github-actions)
2. [GitLab CI/CD](./gitlab-ci-cd)
3. [Code Review](./code-review)
4. [分析与监控](./analytics)
5. [成本管理](./costs)
6. [安全与合规](./security)

这是“个人提效”走向“团队流程”的分界线。前面的重点是你和 Claude 怎么配合，这里的重点变成团队规则、成本、权限边界、审计和自动化。

## 一条更贴近实战的学习顺序

如果你只想先学最有用的那 12 页，我会推荐这条顺序：

1. [概览](./overview)
2. [快速开始](./quickstart)
3. [Claude Code 的工作原理](./how-claude-code-works)
4. [常见工作流](./common-workflows)
5. [最佳实践](./best-practices)
6. [权限配置](./permissions)
7. [记忆机制](./memory)
8. [Claude Code Desktop](./desktop)
9. [CLI 参考](./cli-reference)
10. [设置](./settings)
11. [扩展能力总览](./features-overview)
12. [MCP](./mcp)

这套顺序的好处是，前半段先把“怎么把活干对”学会，后半段再学“怎么把系统接大”。

## 配合这套路线一起看的页面

- [Desktop / CLI 高频样例](./desktop-cli-samples)
- [Claude Code 官方文档地图](./official-docs-map)
- [故障排查](./troubleshooting)
- [更新日志](./changelog)

`troubleshooting` 值得收藏，`changelog` 则适合隔段时间回来看一眼。Claude Code 更新挺快，很多能力不是“有没有”，而是“最近两个月刚变得更好用”。
