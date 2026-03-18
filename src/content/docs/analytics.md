---
title: "通过分析跟踪团队使用情况"
order: 46
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "在分析仪表板中查看 Claude Code 使用指标、跟踪采用情况并衡量工程速度。"
sourceUrl: "https://code.claude.com/docs/en/analytics.md"
sourceTitle: "Track team usage with analytics"
tags: []
---
# 通过分析跟踪团队使用情况

> 在分析仪表板中查看 Claude Code 使用指标、跟踪采用情况并衡量工程速度。

Claude Code 提供分析仪表板，帮助组织了解开发人员使用模式、跟踪贡献指标并衡量 Claude Code 如何影响工程速度。访问您的计划的仪表板：

|计划|仪表板网址 |包括 |了解更多 |
| -------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Claude 适用于团队/企业 | [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code) |使用量指标、贡献指标与 GitHub 集成、排行榜、数据导出 | [详情](#access-analytics-for-teams-and-enterprise) |
| API（Claude 控制台）| [platform.claude.com/claude-code](https://platform.claude.com/claude-code) |使用指标、支出跟踪、团队洞察 | [详情](#access-analytics-for-api-customers) |

## 访问团队和企业的分析

导航至 [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code)。管理员和所有者可以查看仪表板。

团队和企业仪表板包括：

* **使用指标**：接受的代码行数、建议接受率、每日活跃用户和会话
* **贡献指标**：在 Claude Code 协助下附带的 PR 和代码行，以及 [GitHub 集成](#enable-contribution-metrics)
* **排行榜**：按 Claude Code 使用情况排名的主要贡献者
* **数据导出**：下载 CSV 格式的贡献数据以用于自定义报告

### 启用贡献指标

**注意**

贡献指标处于公开测试阶段，可在适用于 Teams 的 Claude 和适用于企业计划的 Claude 上使用。这些指标仅涵盖 claude.ai 组织内的用户。不包括通过 Claude 控制台 API 或第三方集成的使用。

使用情况和采用数据适用于所有 Claude for Teams 和 Claude for Enterprise 帐户。贡献指标需要额外的设置才能连接您的 GitHub 组织。

您需要所有者角色来配置分析设置。 GitHub 管理员必须安装 GitHub 应用程序。

**警告**

贡献指标不适用于启用了[零数据保留](./zero-data-retention) 的组织。分析仪表板将仅显示使用指标。

### 安装 GitHub 应用程序

GitHub 管理员在您组织的 GitHub 帐户（位于 [github.com/apps/claude](https://github.com/apps/claude)）上安装 Claude GitHub 应用程序。

  
### 启用 Claude Code 分析

Claude 所有者导航到 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 并启用 Claude Code 分析功能。

  
### 启用 GitHub 分析

在同一页面上，启用“GitHub 分析”开关。

  
### 使用 GitHub 进行身份验证完成 GitHub 身份验证流程并选择要包含在分析中的 GitHub 组织。

数据通常会在启用后 24 小时内出现，并每日更新。如果没有显示数据，您可能会看到以下消息之一：

* **“需要 GitHub 应用程序”**：安装 GitHub 应用程序以查看贡献指标
* **“数据处理正在进行中”**：如果没有出现数据，请几天后回来检查并确认已安装 GitHub 应用程序

贡献指标支持 GitHub 云和 GitHub 企业服务器。

### 查看摘要指标

**注意**

这些指标故意保守，并且低估了 Claude Code 的实际影响。仅计算对 Claude Code 的参与具有高度信心的行和 PR。

仪表板在顶部显示这些摘要指标：

* **带有 CC 的 PR**：合并的拉取请求总数，其中至少包含一行用 Claude Code 编写的代码
* **带有 CC 的代码行**：在 Claude Code 协助下编写的所有合并 PR 的代码总行数。仅计算“有效行”：标准化后包含超过 3 个字符的行，不包括空行和仅包含括号或简单标点符号的行。
* **包含 Claude Code 的 PR (%)**：包含 Claude Code 辅助代码的所有合并 PR 的百分比
* **建议接受率**：用户接受 Claude Code 的代码编辑建议的百分比，包括 Edit、Write 和 NotebookEdit 工具使用情况
* **接受的代码行**：用户在会话中接受的由 Claude Code 编写的代码总行数。这排除了被拒绝的建议，并且不跟踪后续删除。

### 探索图表

仪表板包含多个图表，可直观地显示一段时间内的趋势。

#### 跟踪采用情况

采用率图表显示每日使用趋势：

* **用户**：每日活跃用户
* **会话**：每天活跃的 Claude Code 会话数

#### 衡量每个用户的 PR

此图表显示了一段时间内各个开发人员的活动：

* **每个用户的 PR**：每天合并的 PR 总数除以每日活跃用户数
* **用户**：每日活跃用户

使用它可以了解随着 Claude Code 采用率的增加，个人生产力如何变化。

#### 查看拉取请求细分

Pull 请求图表显示合并 PR 的每日细分：

* **带有 CC 的 PR**：包含 Claude Code 辅助代码的拉取请求
* **没有 CC 的 PR**：没有 Claude Code 辅助代码的拉取请求

切换到 **代码行** 视图可按代码行而不是 PR 计数查看相同的细分。

#### 查找杰出贡献者

排行榜显示按贡献量排名前 10 位的用户。之间切换：

* **拉取请求**：显示带有 Claude Code 的 PR 与每个用户的所有 PR
* **代码行**：显示带有 Claude Code 的行与每个用户的所有行

单击 **导出所有用户** 以 CSV 文件形式下载所有用户的完整贡献数据。导出内容包括所有用户，而不仅仅是显示的前 10 位用户。

### 公关归因启用贡献指标后，Claude Code 会分析合并的拉取请求，以确定哪些代码是在 Claude Code 协助下编写的。这是通过将 Claude Code 会话活动与每个 PR 中的代码进行匹配来完成的。

#### 标记标准

如果 PR 至少包含在 Claude Code 会话期间编写的一行代码，则它们会被标记为“with Claude Code”。系统使用保守匹配：只有对 Claude Code 的参与有较高置信度的代码才算作辅助。

#### 归因过程

合并拉取请求时：

1. 从 PR diff 中提取添加的行
2. 识别在某个时间窗口内编辑匹配文件的 Claude Code 会话
3. 使用多种策略将 PR 行与 Claude Code 输出进行匹配
4. AI辅助线数和总线数的指标计算

在比较之前，行会被标准化：空白被修剪，多个空格被折叠，引号被标准化，文本被转换为小写。

包含 Claude Code 辅助行的合并拉取请求在 GitHub 中标记为 `claude-code-assisted`。

#### 时间窗口

PR 合并日期之前 21 天到之后 2 天的会话将被考虑进行归因匹配。

#### 排除的文件

某些文件会自动从分析中排除，因为它们是自动生成的：

* 锁定文件：package-lock.json、yarn.lock、Cargo.lock 等
* 生成的代码：Protobuf 输出、构建工件、缩小文件
* 构建目录：dist/、build/、node\_modules/、target/
* 测试夹具：快照、磁带、模拟数据
* 超过 1,000 个字符的行，可能已缩小或生成

#### 归属说明

在解释归因数据时，请记住这些额外的详细信息：

* 代码被开发者大幅重写，差异超过20%，不归咎于Claude Code
* 不考虑 21 天窗口之外的会话
* 算法在进行归因时不考虑 PR 源或目标分支

### 充分利用分析

使用贡献指标来展示投资回报率、确定采用模式并找到可以帮助其他人入门的团队成员。

#### 监控采用情况

跟踪采用图表和用户计数以确定：

* 可以分享最佳实践的活跃用户
* 整个组织的总体采用趋势
* 使用量下降可能表明存在摩擦或问题

#### 衡量投资回报率

贡献指标有助于回答“这个工具值得投资吗？”使用您自己的代码库中的数据：

* 随着采用率的增加，跟踪每个用户 PR 随时间的变化
* 比较带 Claude Code 和不带 Claude Code 的 PR 和代码行
* 与 [DORA 指标](https://dora.dev/)、冲刺速度或其他工程 KPI 一起使用，以了解采用 Claude Code 带来的变化

#### 识别高级用户

排行榜可帮助您找到 Claude Code 采用率较高的团队成员，他们可以：

* 与团队分享提示技巧和工作流程
* 提供有关哪些方面运作良好的反馈
* 帮助新用户加入

#### 以编程方式访问数据

要通过 GitHub 查询此数据，请搜索标记为 `claude-code-assisted` 的 PR。

## API 客户的访问分析使用 Claude 控制台的 API 客户可以访问 [platform.claude.com/claude-code](https://platform.claude.com/claude-code) 上的分析。您需要具有UsageView 权限才能访问仪表板，该权限已授予开发人员、计费、管理员、所有者和主要所有者角色。

**注意**

API 客户当前无法使用 GitHub 集成的贡献指标。控制台仪表板仅显示使用情况和支出指标。

控制台仪表板显示：

* **接受的代码行**：用户在会话中接受的由 Claude Code 编写的代码总行数。这排除了被拒绝的建议，并且不跟踪后续删除。
* **建议接受率**：用户接受代码编辑工具使用的次数百分比，包括 Edit、Write 和 NotebookEdit 工具。
* **活动**：图表上显示的每日活跃用户和会话。
* **支出**：每日 API 成本（以美元为单位）以及用户数量。

### 查看团队见解

团队见解表显示每个用户的指标：

* **会员**：所有已通过 Claude Code 身份验证的用户。 API 密钥用户按密钥标识符显示，OAuth 用户按电子邮件地址显示。
* **本月支出**：当月每个用户的 API 总成本。
* **本月行数**：当月每个用户接受的代码行总数。

**注意**

控制台仪表板中的支出数字是出于分析目的的估计值。有关实际费用，请参阅您的账单页面。

## 相关资源

* [使用 OpenTelemetry 进行监控](./monitoring-usage)：将实时指标和事件导出到可观察性堆栈
* [有效管理成本](./costs)：设置支出限额并优化代币使用
* [权限](./permissions)：配置角色和权限
