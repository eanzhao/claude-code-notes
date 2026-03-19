---
title: "Claude Code 学习路线"
order: 0
section: "getting-started"
sectionLabel: "快速入门"
sectionOrder: 1
group: "curated"
groupLabel: "学习辅助"
summary: "从入门到精通的学习顺序建议，避免踩坑，快速上手。"
tags: []
---

# 怎么学 Claude Code 最顺？

官方文档很全，但直接从头看到尾容易晕。这里给你一条更接地气的学习路线，帮你少走弯路。

## 先玩起来（第 1 阶段）

别急着看原理，先让 Claude Code 跑起来：

1. **[概览](./overview)** - 5 分钟了解它能干啥
2. **[快速开始](./quickstart)** - 跟着敲一遍，熟悉基本操作
3. **[它是怎么干活的](./how-claude-code-works)** - 理解 Claude 怎么读代码、改文件、跑命令
4. **[常见工作流](./common-workflows)** - 看别人怎么用它修 Bug、加功能

**这阶段的目标**：能流畅地跟 Claude 对话，知道怎么让它改代码、什么时候该喊停。

> 💡 如果你用桌面版，顺手看看 [Desktop 快速开始](./desktop-quickstart)；如果用终端，看看 [CLI 参考](./cli-reference)。

---

## 学会控制（第 2 阶段）

 Claude 能自动改文件、跑命令，但前提是你要管得住它。

按这个顺序看：

1. **[权限配置](./permissions)** - 设置哪些操作要问你、哪些可以直接干
2. **[记忆机制](./memory)** - 教 Claude 记住你的项目规范
3. **[最佳实践](./best-practices)** - 怎么写提示词效果最好
4. **[设置](./settings)** - 把常用的配置固化下来

**这阶段的核心**：让 Claude 按照你的规矩来，而不是它自己瞎折腾。

---

## 深挖你常用的工具（第 3 阶段）

### 用桌面版（Desktop）的看这里

重点看这几个：

1. **[Desktop 完整指南](./desktop)** - 图形界面所有功能
2. **[远程控制](./remote-control)** - 手机也能接着电脑上的会话继续
3. **[网页版](./claude-code-on-the-web)** - 不用装软件，浏览器直接开干
4. **[Chrome 插件](./chrome)** - 让 Claude 直接操作浏览器

**Desktop 的杀手锏**：
- 改代码前先看 diff，改得对不对一目了然
- 能预览网页效果（比如前端项目）
- 可以同时开多个会话，互不干扰
- 能跑定时任务，比如每小时检查一次部署状态

### 用命令行（CLI）的看这里

重点练这几个：

1. **[CLI 参考](./cli-reference)** - 所有命令参数
2. **[内置命令](./commands)** - `/` 开头的快捷指令
3. **[交互模式](./interactive-mode)** - 快捷键和技巧
4. **[沙箱](./sandboxing)** - 安全地跑命令

**CLI 的精髓**：
```bash
claude                    # 进入交互模式
claude -p "修复登录 Bug"   # 一次性任务
claude -c                 # 接着上次的会话继续
```

终端用熟了，Claude 就像你的编程搭档，而不是一个聊天机器人。

---

## 开始扩展（第 4 阶段）

等前面都顺手了，再考虑扩展。太早折腾这些容易过度设计。

推荐顺序：

1. **[扩展总览](./features-overview)** - 先搞清楚各功能能干嘛
2. **[Skills](./skills)** - 自定义命令，比如 `/code-review`
3. **[Subagents](./sub-agents)** - 让专门的小助手干特定任务
4. **[Hooks](./hooks-guide)** - 自动执行脚本（比如改完代码自动格式化）
5. **[MCP](./mcp)** - 接外部工具（数据库、Slack、GitHub 等）
6. **[Plugins](./plugins)** - 打包分享你的配置

**⚠️ 避坑建议**：
- 先写 `CLAUDE.md` 定义项目规范
- 需要自动化时再加 hooks
- 真的要接外部系统再上 MCP
- 别一上来就搞一堆配置，简单够用就好

---

## 团队协作（第 5 阶段）

想在整个团队推广时再看：

1. **[GitHub Actions](./github-actions)** - PR 自动审查、Issue 自动处理
2. **[Code Review](./code-review)** - 让 Claude 帮你审代码
3. **[成本管理](./costs)** - 控制团队开销
4. **[安全与合规](./security)** - 企业级安全

---

## 如果你只有时间看 12 页

按这个顺序：

1. [概览](./overview)
2. [快速开始](./quickstart)
3. [工作原理](./how-claude-code-works)
4. [常见工作流](./common-workflows)
5. [最佳实践](./best-practices)
6. [权限配置](./permissions)
7. [记忆机制](./memory)
8. [Desktop 指南](./desktop) 或 [CLI 参考](./cli-reference)
9. [设置](./settings)
10. [扩展总览](./features-overview)
11. [MCP](./mcp)
12. [故障排查](./troubleshooting)

---

## 一些实用小贴士

- **[Desktop/CLI 样例](./desktop-cli-samples)** - 直接抄作业
- **[官方文档地图](./official-docs-map)** - 找不到东西时来这查
- **[更新日志](./changelog)** - 隔几周回来看一眼，Claude Code 更新很快

有问题先问 Claude：`/help` 或者直接打字问。
