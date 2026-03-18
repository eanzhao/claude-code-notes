---
title: "输出样式"
order: 26
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "使 Claude Code 适应软件工程以外的用途"
sourceUrl: "https://code.claude.com/docs/en/output-styles.md"
sourceTitle: "Output styles"
tags: []
---
# 输出样式

> 使 Claude Code 适应软件工程以外的用途

输出样式允许您使用 Claude Code 作为任何类型的代理，同时保持
其核心功能，例如运行本地脚本、读/写文件以及
跟踪 TODO。

## 内置输出样式

Claude Code的**默认**输出风格是现有系统提示符，设计
帮助您高效完成软件工程任务。

还有两种额外的内置输出样式，专注于教您
代码库以及 Claude 的运行方式：

* **解释性**：在帮助您的同时提供教育“见解”
  完成软件工程任务。帮助您了解实施
  选择和代码库模式。

* **学习**：协作、边做边学的模式，Claude 不仅会
  在编码时分享“见解”，但也要求您做出小的、战略性的贡献
  自己编写一些代码。 Claude Code 将在您的
  代码供您实施。

## 输出样式如何工作

输出样式直接修改Claude Code的系统提示符。

* 所有输出样式均不包括高效输出的指令（例如
  回答简洁）。
* 自定义输出样式不包括编码指令（例如验证代码
  带测试），除非 `keep-coding-instructions` 为真。
* 所有输出样式都有自己的自定义指令添加到末尾
  系统提示。
* 所有输出样式都会触发Claude遵守输出样式的提醒
  谈话过程中的指示。

## 改变你的输出风格

运行 `/config` 并选择 **输出样式** 从菜单中选择样式。你的
选择保存到 `.claude/settings.local.json`
[本地项目级别](./settings)。

要设置不带菜单的样式，请直接在文件中编辑 `outputStyle` 字段
设置文件：

```json
{
  "outputStyle": "Explanatory"
}
```

因为输出样式是在会话启动时的系统提示符中设置的，
更改将在您下次开始新会话时生效。这样可以保持系统
在整个对话过程中提示保持稳定，因此提示缓存可以减少延迟
成本。

## 创建自定义输出样式

自定义输出样式是带有 frontmatter 和文本的 Markdown 文件
添加到系统提示符中：

```markdown
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

您可以在用户级别保存这些文件 (`~/.claude/output-styles`) 或
项目级别（`.claude/output-styles`）。

### 前题

输出样式文件支持 frontmatter 来指定元数据：

|前沿 |目的|默认|
| ：-------------------------- | :-------------------------------------------------------------------------- | :---------------------- |
| `name` |输出样式的名称，如果不是文件名 |继承自文件名 |
| `description` |输出样式的描述，显示在 `/config` 选择器中 |无 |
| `keep-coding-instructions` |是否保留Claude Code系统提示中与编码相关的部分。 |假 |

## 相关功能比较

### 输出样式 vs. CLAUDE.md vs. --append-system-prompt输出样式完全“关闭”Claude Code默认系统的部分
特定于软件工程的提示。 CLAUDE.md 和
`--append-system-prompt` 编辑 Claude Code 的默认系统提示符。 CLAUDE.md
将内容添加为用户消息*以下*Claude Code 的默认系统
提示。 `--append-system-prompt` 将内容附加到系统提示符中。

### 输出样式与[代理](./sub-agents)

输出样式直接影响主代理循环并且只影响系统
提示。调用代理来处理特定任务，并且可以包括其他任务
设置，例如要使用的模型、可用的工具以及一些上下文
关于何时使用该代理。

### 输出风格与[技能](./skills)

输出样式修改 Claude 的响应方式（格式、语气、结构），并且一旦选择就始终处于活动状态。技能是特定于任务的提示，您可以使用 `/skill-name` 调用或 Claude 在相关时自动加载。使用输出样式来实现一致的格式首选项；使用可重复使用的工作流程和任务的技能。
