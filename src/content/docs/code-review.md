---
title: "代码审查"
order: 11
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "设置自动 PR 审查，使用对完整代码库的多代理分析来捕获逻辑错误、安全漏洞和回归"
sourceUrl: "https://code.claude.com/docs/en/code-review.md"
sourceTitle: "Code Review"
group: "Platforms and integrations > Code review & CI/CD"
groupLabel: "代码评审与 CI/CD"
tags: []
---
# 代码审查

> 自动化 PR 审查：用多 agent 分析完整代码库，捕获逻辑错误、安全漏洞和回归问题

**注意**

代码审查处于研究预览阶段，面向 [Teams 和 Enterprise](https://claude.ai/admin-settings/claude-code) 订阅开放。不适用于启用了[零数据保留](./zero-data-retention)的组织。

代码审查会分析你的 GitHub pull request，在发现问题的代码行上以行内注释的形式发布结果。一组专门的 agent 在完整代码库的上下文中检查代码变更，查找逻辑错误、安全漏洞、边界情况和潜在回归。

发现的问题会按严重程度标记，不会批准或阻止你的 PR，现有的审查流程不受影响。你可以通过在仓库中添加 `CLAUDE.md` 或 `REVIEW.md` 文件来调整 Claude 关注的内容。

如果你想在自己的 CI 基础设施中（而非此托管服务）运行 Claude，请参阅 [GitHub Actions](./github-actions) 或 [GitLab CI/CD](./gitlab-ci-cd)。

本页涵盖：

* [审查机制](#how-reviews-work)
* [设置方法](#set-up-code-review)
* [自定义审查规则](#customize-reviews)（`CLAUDE.md` 和 `REVIEW.md`）
* [定价](#pricing)

## 审查机制

管理员为组织[启用代码审查](#set-up-code-review)后，审查会在 PR 打开、每次推送或手动请求时触发，具体取决于仓库的配置。在任何模式下，评论 `@claude review` 都可以[手动触发审查](#manually-trigger-reviews)。

审查运行时，多个 agent 在 Anthropic 基础设施上并行分析 diff 和周围代码。每个 agent 关注不同类别的问题，然后验证步骤会根据实际代码行为检查候选问题，过滤掉误报。结果去重后按严重程度排序，以行内注释的形式发布在发现问题的具体代码行上。如果没有发现问题，Claude 会在 PR 上发一条简短的确认评论。

审查的耗费随 PR 规模和复杂度而变化，平均在 20 分钟内完成。管理员可以通过[分析面板](#view-usage)监控审查活动和开支。

### 严重程度

每个发现都标有严重程度：

| 标记 | 严重程度 | 含义 |
| :-----| :---------- | :------------------------------------------------------------------ |
| 🔴 | Normal（正常） | 合并前应该修复的 bug |
| 🟡 | Nit（小问题） | 值得修但不阻塞合并的小问题 |
| 🟣 | Pre-existing（既有问题） | 代码库中已有的 bug，不是这个 PR 引入的 |

每个发现都包含可折叠的推理详情，展开后可以看到 Claude 标记问题的原因及其验证过程。

### 代码审查检查哪些内容

默认情况下，代码审查专注于正确性：会在生产环境中引发问题的 bug，而不是格式偏好或测试覆盖率。你可以通过[添加指导文件](#customize-reviews)来扩展检查范围。

## 设置代码审查

管理员为组织启用一次代码审查，并选择要包含的仓库。

### 打开 Claude Code 管理设置

前往 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)，找到"Code Review"部分。你需要 Claude 组织的管理员权限，以及在 GitHub 组织中安装 GitHub App 的权限。


### 开始设置

点击 **Set Up**，进入 GitHub App 安装流程。


### 安装 Claude GitHub App

按提示将 Claude GitHub App 安装到你的 GitHub 组织。该应用需要以下仓库权限：

* **Contents**：读写
* **Issues**：读写
* **Pull requests**：读写

代码审查使用 Contents 的读取权限和 Pull requests 的写入权限。更广泛的权限集也支持 [GitHub Actions](./github-actions)（如果你后续启用的话）。


### 选择仓库

选择要启用代码审查的仓库。如果看不到某个仓库，确认你在安装过程中已授权 Claude GitHub App 访问它。之后可以随时添加更多仓库。


### 设置审查触发条件

设置完成后，"Code Review"部分会以表格形式显示你的仓库。对于每个仓库，用 **Review behavior** 下拉菜单选择审查的触发时机：

* **PR 创建后一次**：PR 打开或标记为可审查时运行一次
* **每次推送后**：每次推送到 PR 分支时都运行，随着 PR 演进捕获新问题，修复已标记问题后自动关闭对应的评论线程
* **手动**：只有在 PR 上评论 `@claude review` 时才开始审查；之后对该 PR 的后续推送会自动触发审查

每次推送触发的审查次数最多，成本也最高。手动模式适合高流量仓库——你可以挑选特定 PR 进行审查，或等 PR 准备好后再开始。

仓库表还显示每个仓库基于近期活动的平均审查成本。用行操作菜单可以开启/关闭每个仓库的代码审查，或完全移除仓库。

要验证设置是否成功，打开一个测试 PR。如果选择了自动触发，几分钟内会出现名为 **Claude Code Review** 的 check run。如果选择了手动模式，在 PR 上评论 `@claude review` 启动首次审查。如果 check run 没有出现，确认仓库已在管理设置中列出，且 Claude GitHub App 有权访问它。

## 手动触发审查

在 pull request 上评论 `@claude review` 即可启动审查，同时将该 PR 纳入后续推送触发的审查范围。无论仓库配置了哪种触发条件都可以使用：在手动模式下用它挑选特定 PR 进行审查，在其他模式下用它立即重新审查。从那以后，该 PR 的每次推送都会触发审查。

触发审查的评论要求：

* 作为顶级 PR 评论发布，不是 diff 行上的行内评论
* `@claude review` 放在评论开头
* 你必须有仓库的 Owner、Member 或 Collaborator 权限
* PR 必须是公开的且不是草稿

如果该 PR 已有审查正在进行，新请求会排队等当前审查完成后再执行。你可以通过 PR 上的 check run 监控进度。

## 自定义审查规则

代码审查会读取仓库中的两个文件来指导它关注什么内容。两者都是在默认正确性检查之上的补充：

* **`CLAUDE.md`**：Claude Code 在所有任务中使用的共享项目说明，不限于审查。当指导规则同样适用于交互式 Claude Code session 时使用它。
* **`REVIEW.md`**：仅用于审查的规则，在代码审查期间专门读取。适合那些严格限定在审查中才需要标记或跳过的内容，放到 `CLAUDE.md` 里会显得杂乱的规则。

### CLAUDE.md

代码审查会读取仓库的 `CLAUDE.md` 文件，新引入的违规会作为 Nit 级别的发现报告。反过来也成立：如果你的 PR 改动导致 `CLAUDE.md` 中的描述过时，Claude 会标记文档也需要更新。

Claude 会读取目录层级中每一级的 `CLAUDE.md` 文件，子目录的 `CLAUDE.md` 中的规则只适用于该路径下的文件。更多信息参见[记忆文档](./memory)。

如果有些指导规则只想在审查时生效、不想应用于常规 Claude Code session，请使用 [`REVIEW.md`](#review-md)。

### REVIEW.md

在仓库根目录添加 `REVIEW.md` 文件来定义审查专用规则。可以用来编写：

* 公司或团队的代码风格指南："优先用 early return，避免嵌套条件"
* linter 没覆盖到的语言或框架约定
* Claude 应该始终标记的内容："所有新 API 路由必须有集成测试"
* Claude 应该跳过的内容："不要对 `/gen/` 下生成的代码评论格式问题"

示例 `REVIEW.md`：

```markdown
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude 会自动发现仓库根目录中的 `REVIEW.md`，无需额外配置。

## 查看用量

前往 [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) 查看全组织的代码审查活动。面板显示：

| 板块 | 内容 |
| :-------------------- | :---------------------------------------------------------------------------------------------------- |
| PR 审查数 | 所选时间范围内每日审查的 pull request 数量 |
| 每周费用 | 每周的代码审查花费 |
| 反馈 | 开发者修复问题后自动关闭的审查评论数 |
| 仓库明细 | 每个仓库已审查的 PR 数和已关闭的评论数 |

管理设置中的仓库表还显示每个仓库的平均单次审查成本。

## 定价

代码审查按 token 用量计费。平均每次审查费用为 15-25 美元，具体取决于 PR 大小、代码库复杂度和需要验证的问题数量。代码审查的用量通过[额外用量](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)单独计费，不计入你的订阅包含的用量。审查触发条件会影响总成本：

* **PR 创建后一次**：每个 PR 运行一次
* **每次推送后**：每次推送都运行，成本随推送次数成比例增长
* **手动**：在有人评论 `@claude review` 之前不会产生审查

在任何模式下，评论 `@claude review` 会[将该 PR 纳入推送触发的审查](#manually-trigger-reviews)，此后每次推送都会产生费用。

无论你的组织是否使用 AWS Bedrock 或 Google Vertex AI 来运行其他 Claude Code 功能，代码审查的费用都会出现在你的 Anthropic 账单上。要设置代码审查的月度支出上限，前往 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) 配置 Claude Code Review Service 的限额。

可通过[分析面板](#view-usage)中的每周费用图表或管理设置中的仓库平均成本列来监控支出。

## 相关资源

代码审查设计为与 Claude Code 的其他功能协同工作。如果你想在提交 PR 前在本地运行审查、需要自托管方案，或者想深入了解 `CLAUDE.md` 如何跨工具影响 Claude 的行为，这些页面值得看看：

* [插件](./discover-plugins)：浏览插件市场，其中有一个 `code-review` 插件可以在推送前本地运行按需审查
* [GitHub Actions](./github-actions)：在你自己的 GitHub Actions 工作流中运行 Claude，实现代码审查之外的自定义自动化
* [GitLab CI/CD](./gitlab-ci-cd)：面向 GitLab 流水线的自托管 Claude 集成
* [记忆](./memory)：`CLAUDE.md` 文件在 Claude Code 中的工作方式
* [分析](./analytics)：追踪代码审查之外的 Claude Code 使用情况
