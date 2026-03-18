---
title: "通过 MCP 将 Claude Code 连接到工具"
order: 29
section: "build"
sectionLabel: "构建与扩展"
sectionOrder: 4
summary: "了解如何使用 Model Context Protocol 将 Claude Code 连接到您的工具。"
sourceUrl: "https://code.claude.com/docs/en/mcp.md"
sourceTitle: "Connect Claude Code to tools via MCP"
tags: []
---
# 通过 MCP 将 Claude Code 连接到工具

> 了解如何使用 Model Context Protocol 将 Claude Code 连接到您的工具。

Claude Code 可以通过 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)（一种用于 AI 工具集成的开源标准）连接到数百个外部工具和数据源。 MCP 服务器使 Claude Code 能够访问您的工具、数据库和 API。

## MCP 可以做什么

连接 MCP 服务器后，您可以要求 Claude Code：

* **实现问题跟踪器的功能**：“添加 JIRA 问题 ENG-4521 中描述的功能并在 GitHub 上创建 PR。”
* **分析监控数据**：“检查Sentry和Statsig以检查ENG-4521中描述的功能的使用情况。”
* **查询数据库**：“根据我们的 PostgreSQL 数据库，查找使用功能 ENG-4521 的 10 个随机用户的电子邮件。”
* **集成设计**：“根据 Slack 中发布的新 Figma 设计更新我们的标准电子邮件模板”
* **自动化工作流程**：“创建 Gmail 草稿，邀请这 10 位用户参加有关新功能的反馈会议。”

## 热门 MCP 服务器

以下是一些可以连接到 Claude Code 的常用 MCP 服务器：

**警告**

使用第三方 MCP 服务器的风险由您自行承担 - Anthropic 尚未验证
所有这些服务器的正确性或安全性。
确保您信任正在安装的 MCP 服务器。
使用可能获取不受信任的 MCP 服务器时要特别小心
内容，因为这些可能会让您面临即时注入风险。

以下列表根据官方 MCP 注册表在构建时静态生成。由于此目录是动态变化的，站内内容可能会晚于官方几小时到几天。

### Notion
[官方文档](https://developers.notion.com/docs/mcp)

连接您的 Notion 工作区以跨工具搜索、更新和支持工作流程

- Claude Code 接入命令：`claude mcp add notion --transport http https://mcp.notion.com/mcp`

### Canva
[官方文档](https://www.canva.dev/docs/connect/canva-mcp-server-setup/)

搜索、创建、自动填充和导出 Canva 设计

- Claude Code 接入命令：`claude mcp add canva --transport http https://mcp.canva.com/mcp`

### Figma
[官方文档](https://help.figma.com/hc/en-us/articles/32132100833559)

从 Figma 上下文生成图表和更好的代码

- Claude Code 接入命令：`claude mcp add figma --transport http https://mcp.figma.com/mcp`

### Slack
[官方文档](https://docs.slack.dev/ai/mcp-server)

发送消息、创建画布(Canvas)并获取 Slack 数据

- Claude Code 接入命令：`claude mcp add slack --transport http https://mcp.slack.com/mcp`

### Atlassian
[官方文档](https://community.atlassian.com/forums/Atlassian-Platform-articles/Using-the-Atlassian-Remote-MCP-Server-beta/ba-p/3005104)

从 Claude 访问 Jira 和 Confluence

- Claude Code 接入命令：`claude mcp add atlassian --transport http https://mcp.atlassian.com/v1/mcp`

### Linear
[官方文档](https://linear.app/docs/mcp)

在 Linear 中管理问题、项目和团队工作流程

- Claude Code 接入命令：`claude mcp add linear --transport http https://mcp.linear.app/mcp`

### monday.com
[官方文档](https://developer.monday.com/apps/docs/mondaycom-mcp-integration)

在 monday.com 中管理项目、看板和工作流程

- Claude Code 接入命令：`claude mcp add monday-com --transport http https://mcp.monday.com/mcp`

### Intercom
[官方文档](https://developers.intercom.com/docs/guides/mcp)

访问 Intercom 数据以获得更好的客户洞察

- Claude Code 接入命令：`claude mcp add intercom --transport http https://mcp.intercom.com/mcp`

### Box
[官方文档](https://developer.box.com/guides/box-mcp)

搜索、访问并深入了解您的 Box 内容

- Claude Code 接入命令：`claude mcp add box --transport http https://mcp.box.com`

### Gamma
[官方文档](https://gamma.app/docs/Gamma-MCP-Server-Documentation-m6p43kobgzy15zj?mode=doc)

使用 AI 创建演示文稿、文档、社交活动和网站

- Claude Code 接入命令：`claude mcp add gamma --transport http https://mcp.gamma.app/mcp`

### Vercel
[官方文档](https://vercel.com/docs/mcp/vercel-mcp)

分析、调试和管理项目和部署

- Claude Code 接入命令：`claude mcp add vercel --transport http https://mcp.vercel.com/`

### Granola
[官方文档](https://help.granola.ai/article/granola-mcp#set-up-guide)

用于会议的 AI 记事本

- Claude Code 接入命令：`claude mcp add granola --transport http https://mcp.granola.ai/mcp`

### Asana
[官方文档](https://developers.asana.com/docs/mcp-server)

连接到 Asana 以协调任务、项目和目标- Claude Code 接入命令：`claude mcp add asana --transport http https://mcp.asana.com/v2/mcp`

### Miro
[官方文档](https://developers.miro.com/docs/miro-mcp)

在 Miro 板上访问并创建新内容

- Claude Code 接入命令：`claude mcp add miro --transport http https://mcp.miro.com/`

### Sentry
[官方文档](https://docs.sentry.io/product/sentry-mcp/)

智能搜索、查询、调试错误

- Claude Code 接入命令：`claude mcp add sentry --transport http https://mcp.sentry.dev/mcp`

### PubMed
[官方文档](https://support.claude.com/en/)

从 PubMed 搜索生物医学文献

- Claude Code 接入命令：`claude mcp add pubmed --transport http https://pubmed.mcp.claude.com/mcp`

### n8n
[官方文档](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)

访问并运行您的 n8n 工作流程

- 需要先完成服务端配置：[https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)

### 苏帕巴斯
[官方文档](https://supabase.com/docs/guides/getting-started/mcp)

管理数据库、身份验证和存储

- Claude Code 接入命令：`claude mcp add supabase --transport http https://mcp.supabase.com/mcp`

### 点击
[官方文档](https://help.clickup.com/hc/en-us/articles/33335772678423-What-is-ClickUp-MCP)

团队和代理的项目管理和协作

- Claude Code 接入命令：`claude mcp add clickup --transport http https://mcp.clickup.com/mcp`

### 抱脸
[官方文档](https://huggingface.co/settings/mcp)

访问 Hugging Face Hub 和数千个 Gradio 应用程序

- Claude Code 接入命令：`claude mcp add hugging-face --transport http https://huggingface.co/mcp?login&gradio=none`

### 上下文7
[官方文档](https://context7.com/docs/overview)

LLM 和 AI 代码编辑器的最新文档

- Claude Code 接入命令：`claude mcp add context7 --transport http https://mcp.context7.com/mcp`

### 条纹
[官方文档](https://docs.stripe.com/mcp)

支付处理和金融基础设施工具

- Claude Code 接入命令：`claude mcp add stripe --transport http https://mcp.stripe.com`

### 微软学习
[官方文档](https://learn.microsoft.com/en-us/training/support/mcp)

搜索可信的 Microsoft 文档来支持您的开发

- Claude Code 接入命令：`claude mcp add microsoft-learn --transport http https://learn.microsoft.com/api/mcp`

### 粘土
[官方文档](https://www.notion.so/clayrun/Clay-Claude-MCP-Server-Documentation-2ef7e66eb01480c9820de48041591aeb?showMoveTo=true&saveParent=true)

寻找前景。研究账户。个性化外展

- Claude Code 接入命令：`claude mcp add clay --transport http https://api.clay.com/v3/mcp`

### NetSuite
[官方文档](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_7200233106.html)

将 Claude 连接到 NetSuite 数据以进行分析和见解

- 需要先完成服务端配置：[https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_7200233106.html](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_7200233106.html)

### 网络流
[官方文档](https://developers.webflow.com/mcp/v1.0.0/reference/overview)

管理 Webflow CMS、页面、资产和站点

- Claude Code 接入命令：`claude mcp add webflow --transport http https://mcp.webflow.com/mcp`

### 阿雷夫斯
[官方文档](https://docs.ahrefs.com/docs/mcp/reference/introduction)

SEO 和 AI 搜索分析

- Claude Code 接入命令：`claude mcp add ahrefs --transport http https://api.ahrefs.com/mcp/mcp`

### 临床试验
[官方文档](https://docs.mcp.deepsense.ai/guides/clinical_trials.html)

访问 ClinicalTrials.gov 数据

- Claude Code 接入命令：`claude mcp add clinical-trials --transport http https://mcp.deepsense.ai/clinical_trials/mcp`

### Cloudflare 开发者平台
[官方文档](https://www.support.cloudflare.com/)

利用计算、存储和人工智能构建应用程序

- Claude Code 接入命令：`claude mcp add cloudflare-developer-platform --transport http https://bindings.mcp.cloudflare.com/mcp`

### 学者门户
[官方文档](https://docs.scholargateway.ai)

通过学术研究和引用增强回应

- Claude Code 接入命令：`claude mcp add scholar-gateway --transport http https://connector.scholargateway.ai/mcp`

### 智能表
[官方文档](https://help.smartsheet.com/articles/2483663-use-smartsheet-connector-claude)

使用 Claude 分析和管理 Smartsheet 数据

- 需要先完成服务端配置：[https://help.smartsheet.com/articles/2483663-use-smartsheet-connector-claude](https://help.smartsheet.com/articles/2483663-use-smartsheet-connector-claude)

### 坡道
[官方文档](https://docs.ramp.com/developer-api/v1/guides/ramp-mcp-remote)

搜索、访问和分析您的 Ramp 财务数据

- Claude Code 接入命令：`claude mcp add ramp --transport http https://ramp-mcp-remote.ramp.com/mcp`

### 缩放信息
[官方文档](https://docs.zoominfo.com/docs/zi-api-mcp-overview/)

利用 GTM 智能丰富联系人和客户

- Claude Code 接入命令：`claude mcp add zoominfo --transport http https://mcp.zoominfo.com/mcp`

### 生物Rxiv
[官方文档](https://docs.mcp.deepsense.ai/guides/biorxiv.html)

访问 bioRxiv 和 medRxiv 预印本数据

- Claude Code 接入命令：`claude mcp add biorxiv --transport http https://mcp.deepsense.ai/biorxiv/mcp`

### WordPress.com
[官方文档](https://developer.wordpress.com/docs/mcp/)

安全的 AI 访问来管理您的 WordPress.com 网站

- Claude Code 接入命令：`claude mcp add wordpress-com --transport http https://public-api.wordpress.com/wpcom/v2/mcp/v1`

### 网络化
[官方文档](https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/)

在 Netlify 上创建、部署、管理和保护网站。

- Claude Code 接入命令：`claude mcp add netlify --transport http https://netlify-mcp.netlify.app/mcp`

### 雪花
[官方文档](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)

检索结构化和非结构化数据

- 需要先完成服务端配置：[https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)

### 制作
[官方文档](https://developers.make.com/mcp-server/)

运行 Make 场景并管理您的 Make 帐户

- Claude Code 接入命令：`claude mcp add make --transport http https://mcp.make.com`

### NPI 注册表
[官方文档](https://docs.mcp.deepsense.ai/guides/npi_registry.html)

访问美国国家提供商标识符 (NPI) 注册表

- Claude Code 接入命令：`claude mcp add npi-registry --transport http https://mcp.deepsense.ai/npi_registry/mcp`

### GoDaddy
[官方文档](https://developer.godaddy.com/mcp)

搜索域并检查可用性

- Claude Code 接入命令：`claude mcp add godaddy --transport http https://api.godaddy.com/v1/domains/mcp`

### 谷歌云 BigQuery
[官方文档](https://cloud.google.com/bigquery/docs/use-bigquery-mcp)BigQuery：为客服人员提供高级分析见解

- Claude Code 接入命令：`claude mcp add google-cloud-bigquery --transport http https://bigquery.googleapis.com/mcp`

### CMS 覆盖范围
[官方文档](https://docs.mcp.deepsense.ai/guides/cms_coverage.html)

访问 CMS 覆盖范围数据库

- Claude Code 接入命令：`claude mcp add cms-coverage --transport http https://mcp.deepsense.ai/cms_coverage/mcp`

### 收集
[官方文档](https://docs.glean.com/administration/platform/mcp/about)

将企业环境引入 Claude 和您的 AI 工具

- 需要先完成服务端配置：[https://docs.glean.com/administration/platform/mcp/about](https://docs.glean.com/administration/platform/mcp/about)

### 化学BL
[官方文档](https://docs.mcp.deepsense.ai/guides/chembl.html)

访问 ChEMBL 数据库

- Claude Code 接入命令：`claude mcp add chembl --transport http https://mcp.deepsense.ai/chembl/mcp`

### 十六进制
[官方文档](https://learn.hex.tech/docs/administration/mcp-server)

与 Hex 代理解答问题

- 需要先完成服务端配置：[https://learn.hex.tech/docs/administration/mcp-server](https://learn.hex.tech/docs/administration/mcp-server)

### ICD-10 代码
[官方文档](https://docs.mcp.deepsense.ai/guides/icd10_codes.html)

访问 ICD-10-CM 和 ICD-10-PCS 代码集

- Claude Code 接入命令：`claude mcp add icd-10-codes --transport http https://mcp.deepsense.ai/icd10_codes/mcp`

### 贝宝
[官方文档](https://mcp.paypal.com/)

接入PayPal支付平台

- Claude Code 接入命令：`claude mcp add paypal --transport http https://mcp.paypal.com/mcp`

### 开放目标
[官方文档](https://github.com/opentargets/open-targets-platform-mcp)

药物靶点发现和优先排序平台

- Claude Code 接入命令：`claude mcp add open-targets --transport http https://mcp.platform.opentargets.org/mcp`

### 数据块
[官方文档](https://docs.databricks.com/aws/en/generative-ai/mcp/connect-external-services)

具有 Unity Catalog 和 Mosaic AI 的托管 MCP 服务器

- 需要先完成服务端配置：[https://docs.databricks.com/aws/en/generative-ai/mcp/connect-external-services](https://docs.databricks.com/aws/en/generative-ai/mcp/connect-external-services)

### 氛围勘探
[官方文档](https://developers.explorium.ai/mcp-docs/agentsource-mcp)

查找公司和联系方式

- Claude Code 接入命令：`claude mcp add vibe-prospecting --transport http https://vibeprospecting.explorium.ai/mcp`

### AWS 市场
[官方文档](https://docs.aws.amazon.com/marketplace/latest/APIReference/marketplace-mcp-server.html)

发现、评估和购买云解决方案

- Claude Code 接入命令：`claude mcp add aws-marketplace --transport http https://marketplace-mcp.us-east-1.api.aws/mcp`

### 维克斯
[官方文档](https://dev.wix.com/docs/sdk/articles/use-the-wix-mcp/about-the-wix-mcp)

在 Wix 上管理和构建网站和应用程序

- Claude Code 接入命令：`claude mcp add wix --transport http https://mcp.wix.com/mcp`

### 彭多
[官方文档](https://support.pendo.io/hc/en-us/articles/41102236924955)

连接 Pendo 获取产品和用户见解

- 需要先完成服务端配置：[https://support.pendo.io/hc/en-us/articles/41102236924955](https://support.pendo.io/hc/en-us/articles/41102236924955)

### 克拉维约
[官方文档](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server)

使用实时 Klaviyo 数据进行报告、制定策略和创建

- Claude Code 接入命令：`claude mcp add klaviyo --transport http https://mcp.klaviyo.com/mcp?include-mcp-app=true`

### 邮差猪
[官方文档](https://posthog.com/docs/model-context-protocol)

查询、分析和管理您的 PostHog 见解

- Claude Code 接入命令：`claude mcp add posthog --transport http https://mcp.posthog.com/mcp`

### 类似网站
[官方文档](https://docs.similarweb.com/api-v5/mcp/mcp-setup)

实时网络、移动应用程序和市场数据。

- Claude Code 接入命令：`claude mcp add similarweb --transport http https://mcp.similarweb.com`

### Crypto.com
[官方文档](https://mcp.crypto.com/docs)

加密货币的实时价格、订单、图表等

- Claude Code 接入命令：`claude mcp add crypto-com --transport http https://mcp.crypto.com/market-data/mcp`

### 生物渲染
[官方文档](https://help.biorender.com/hc/en-gb/articles/30870978672157-How-to-use-the-BioRender-MCP-connector)

搜索并使用科学模板和图标

- Claude Code 接入命令：`claude mcp add biorender --transport http https://mcp.services.biorender.com/mcp`

### 阿蒂奥
[官方文档](https://docs.attio.com/mcp/overview)

从 Claude 搜索、管理和更新您的 Attio CRM

- Claude Code 接入命令：`claude mcp add attio --transport http https://mcp.attio.com/mcp`

### 大师
[官方文档](https://help.getguru.com/docs/connecting-gurus-mcp-server)

搜索您的公司知识并与之互动

- Claude Code 接入命令：`claude mcp add guru --transport http https://mcp.api.getguru.com/mcp`

### 特里瓦戈
[官方文档](https://mcp.trivago.com/docs)

以最优惠的价格找到您理想的酒店。

- Claude Code 接入命令：`claude mcp add trivago --transport http https://mcp.trivago.com/mcp`

### 温莎.ai
[官方文档](https://windsor.ai/introducing-windsor-mcp/#method-1-using-claude-desktop-3)

连接 325+ 营销、分析和 CRM 数据源

- Claude Code 接入命令：`claude mcp add windsor-ai --transport http https://mcp.windsor.ai`

### Synapse.org
[官方文档](https://github.com/susheel/synapse-mcp?tab=readme-ov-file#synapse-mcp-server)

Synapse 科学数据的搜索和元数据工具

- Claude Code 接入命令：`claude mcp add synapse-org --transport http https://mcp.synapse.org/mcp`

### 果酱
[官方文档](https://jam.dev/docs/debug-a-jam/mcp)

录制屏幕并自动收集问题上下文

- Claude Code 接入命令：`claude mcp add jam --transport http https://mcp.jam.dev/mcp`

### 共识
[官方文档](https://docs.consensus.app/docs/mcp)

探索科学研究

- Claude Code 接入命令：`claude mcp add consensus --transport http https://mcp.consensus.app/mcp`

### 横梁
[官方文档](https://help.crossbeam.com/en/articles/12601327-crossbeam-mcp-server-beta)

在 Claude 中探索合作伙伴数据和生态系统见解

- Claude Code 接入命令：`claude mcp add crossbeam --transport http https://mcp.crossbeam.com`

### 顺时针
[官方文档](https://support.getclockwise.com/article/238-connecting-to-clockwise-mcp)

先进的工作安排和时间管理。

- Claude Code 接入命令：`claude mcp add clockwise --transport http https://mcp.getclockwise.com/mcp`

### 回圈
[官方文档](https://circleback.ai/docs/mcp)

搜索并访问会议背景

- Claude Code 接入命令：`claude mcp add circleback --transport http https://app.circleback.ai/api/mcp`

### 最后一分钟.com
[官方文档](https://mcp.lastminute.com/docs)搜索、比较和预订全球航空公司和酒店供应商的航班、动态套餐（航班 + 酒店）和酒店。

- Claude Code 接入命令：`claude mcp add lastminute-com --transport http https://mcp.lastminute.com/mcp`

### 外展
[官方文档](https://support.outreach.io/hc/en-us/articles/46370115253403-Outreach-MCP-Server)

利用 Outreach AI 发挥团队的最佳绩效

- Claude Code 接入命令：`claude mcp add outreach --transport http https://api.outreach.io/mcp/`

### 混合面板
[官方文档](https://docs.mixpanel.com/docs/features/mcp)

分析、查询和管理您的 Mixpanel 数据

- Claude Code 接入命令：`claude mcp add mixpanel --transport http https://mcp.mixpanel.com/mcp`

### 比特利
[官方文档](https://dev.bitly.com/bitly-mcp/)

缩短链接、生成二维码并跟踪绩效

- Claude Code 接入命令：`claude mcp add bitly --transport http https://api-ssl.bitly.com/v4/mcp`

### CData 连接人工智能
[官方文档](https://cloud.cdata.com/docs/Claude-Client.html)

管理 350 个来源的 MCP 平台

- Claude Code 接入命令：`claude mcp add cdata-connect-ai --transport http https://mcp.cloud.cdata.com/mcp`

### MT 通讯社
[官方文档](https://console.blueskyapi.com/docs/EDGE/news/MT_NEWSWIRES_Global#mcp)

值得信赖的实时全球财经新闻提供商

- Claude Code 接入命令：`claude mcp add mt-newswires --transport http https://vast-mcp.blueskyapi.com/mcp`

### 广场
[官方文档](https://developer.squareup.com/docs/mcp)

搜索和管理交易、商家和支付数据

- Claude Code 接入命令：`claude mcp add square --transport sse https://mcp.squareup.com/sse`

### 埃及人
[官方文档](https://developers.egnyte.com/docs/Remote_MCP_Server)

安全访问和分析 Egnyte 内容

- Claude Code 接入命令：`claude mcp add egnyte --transport http https://mcp-server.egnyte.com/mcp`

### 塔架
[官方文档](https://support.usepylon.com/articles/2407390554-connecting-to-the-pylon-mcp-server?lang=en)

搜索和管理 Pylon 支持问题

- Claude Code 接入命令：`claude mcp add pylon --transport http https://mcp.usepylon.com/`

### 蜂窝
[官方文档](https://docs.honeycomb.io/troubleshoot/product-lifecycle/beta/mcp/)

查询和探索可观测性数据和 SLO

- Claude Code 接入命令：`claude mcp add honeycomb --transport http https://mcp.honeycomb.io/mcp`

### 水星
[官方文档](https://docs.mercury.com/docs/connecting-mercury-mcp)

在 Mercury 上搜索、分析和了解您的财务状况

- Claude Code 接入命令：`claude mcp add mercury --transport http https://mcp.mercury.com/mcp`

### 水星
[官方文档](https://docs.mercury.com/docs/connecting-mercury-mcp)

在 Mercury 上搜索、分析和了解您的财务状况

- Claude Code 接入命令：`claude mcp add mercury --transport http https://mcp.mercury.com/mcp`

### 蜂窝
[官方文档](https://docs.honeycomb.io/troubleshoot/product-lifecycle/beta/mcp/)

查询和探索可观测性数据和 SLO

- Claude Code 接入命令：`claude mcp add honeycomb --transport http https://mcp.honeycomb.io/mcp`

### Jotform
[官方文档](https://www.jotform.com/developers/mcp/)

在 Claude 内创建表单并分析提交内容

- Claude Code 接入命令：`claude mcp add jotform --transport http https://mcp.jotform.com/mcp-app`

### 扎皮尔
[官方文档](https://docs.zapier.com/mcp/home)

通过对话自动化数千个应用程序的工作流程

- Claude Code 接入命令：`claude mcp add zapier --transport http https://mcp.zapier.com/api/v1/connect`

### Coupler.io
[官方文档](https://help.coupler.io/article/592-coupler-local-mcp-server)

从数百个来源访问业务数据

- Claude Code 接入命令：`claude mcp add coupler-io --transport http https://mcp.coupler.io/mcp/`

### 全方位分析
[官方文档](https://docs.omni.co/ai/mcp)

通过 Omni 语义模型使用自然语言查询数据

- Claude Code 接入命令：`claude mcp add omni-analytics --transport http https://callbacks.omniapp.co/callback/mcp`

### 日间人工智能
[官方文档](https://day.ai/mcp)

通过 CRMx 了解有关您的潜在客户和客户的一切

- Claude Code 接入命令：`claude mcp add day-ai --transport http https://day.ai/api/mcp`

### 客户.io
[官方文档](https://docs.customer.io/ai/mcp-server/)

通过 Claude 探索客户数据并生成见解

- 需要先完成服务端配置：[https://docs.customer.io/ai/mcp-server/](https://docs.customer.io/ai/mcp-server/)

### 云端
[官方文档](https://cloudinary.com/documentation/cloudinary_llm_mcp#available_mcp_servers)

管理、转换和交付您的图像和视频

- Claude Code 接入命令：`claude mcp add cloudinary --transport sse https://asset-management.mcp.cloudinary.com/sse`

### 月球粉碎
[官方文档](https://lunarcrush.com/developers/api/ai)

将实时社交媒体数据添加到您的搜索中

- Claude Code 接入命令：`claude mcp add lunarcrush --transport http https://lunarcrush.ai/mcp`

### 坦诚
[官方文档](https://support.claude.com/en/articles/12923235-using-the-candid-connector-in-claude)

使用 Candid 的数据研究非营利组织和资助者

- Claude Code 接入命令：`claude mcp add candid --transport http https://mcp.candid.org/mcp`

### 沃卡托
[官方文档](https://docs.workato.com/en/mcp.html)

自动化工作流程并连接您的业务应用程序

- 需要先完成服务端配置：[https://docs.workato.com/en/mcp.html](https://docs.workato.com/en/mcp.html)

### 骰子
[官方文档](https://www.dice.com/about/mcp)

在 Dice 上查找活跃的技术职位

- Claude Code 接入命令：`claude mcp add dice --transport http https://mcp.dice.com/mcp`

### 颜料
[官方文档](https://kb.pigment.com/docs/mcp-server)

分析业务数据

- 需要先完成服务端配置：[https://kb.pigment.com/docs/mcp-server](https://kb.pigment.com/docs/mcp-server)

### 谐波
[官方文档](https://support.harmonic.ai/en/articles/12785899-harmonic-mcp-server-getting-started-guide)

发现、研究并丰富公司和个人

- Claude Code 接入命令：`claude mcp add harmonic --transport http https://mcp.api.harmonic.ai`

### 中页法律研究
[官方文档](https://midpage-docs.apidocumentation.com/documentation/integration/mcp-tools)

进行法律研究并创建工作产品

- Claude Code 接入命令：`claude mcp add midpage-legal-research --transport http https://app.midpage.ai/mcp`### 空中行动
[官方文档](https://docs.airops.com/mcp)

精心制作赢得人工智能搜索的内容

- Claude Code 接入命令：`claude mcp add airops --transport http https://app.airops.com/mcp`

### 鸭妈妈
[官方文档](https://motherduck.com/docs/sql-reference/mcp/)

从您的数据中获取答案

- Claude Code 接入命令：`claude mcp add motherduck --transport http https://api.motherduck.com/mcp`

### 魔法图案
[官方文档](https://www.magicpatterns.com/docs/documentation/features/mcp-server/overview)

讨论并迭代 Magic Patterns 设计

- Claude Code 接入命令：`claude mcp add magic-patterns --transport http https://mcp.magicpatterns.com/mcp`

### 计时码表
[官方文档](https://lp-help.chronograph.pe/article/735-chronograph-mcp)

直接在 Claude 中与您的计时码表数据交互

- Claude Code 接入命令：`claude mcp add chronograph --transport http https://ai.chronograph.pe/mcp`

### 活动活动
[官方文档](https://developers.activecampaign.com/page/mcp)

自主营销改变您的工作方式

- 需要先完成服务端配置：[https://developers.activecampaign.com/page/mcp](https://developers.activecampaign.com/page/mcp)

### MailerLite
[官方文档](https://developers.mailerlite.com/mcp/#how-mcp-works)

将 Claude 变成您的电子邮件营销助手

- Claude Code 接入命令：`claude mcp add mailerlite --transport http https://mcp.mailerlite.com/mcp`

### 欧金
[官方文档](https://docs.owkin.com/core-features-and-usage)

与专为生物学而构建的 AI 代理进行交互

- Claude Code 接入命令：`claude mcp add owkin --transport http https://mcp.k.owkin.com/mcp`

### 块侦察兵
[官方文档](https://github.com/blockscout/mcp-server)

访问和分析区块链数据

- Claude Code 接入命令：`claude mcp add blockscout --transport http https://mcp.blockscout.com/mcp`

### 理智
[官方文档](https://www.sanity.io/docs/ai/mcp-server)

在 Sanity 中创建、查询和管理结构化内容

- Claude Code 接入命令：`claude mcp add sanity --transport http https://mcp.sanity.io`

### 开发版本
[官方文档](https://support.devrev.ai/en-US/devrev/article/ART-21859-remote-mcp-server)

搜索并更新您公司的知识图谱

- Claude Code 接入命令：`claude mcp add devrev --transport http https://api.devrev.ai/mcp/v1`

### 光环
[官方文档](https://docs.getaura.ai/)

公司情报和劳动力分析

- Claude Code 接入命令：`claude mcp add aura --transport http https://mcp.auraintelligence.com/mcp`

### 医疗数据
[官方文档](https://learn.medidata.com/en-US/bundle/mcp-server-documentation/page/medidata_mcp_server_documentation.html)

临床试验软件和网站排名工具

- Claude Code 接入命令：`claude mcp add medidata --transport http https://mcp.imedidata.com/mcp`

### 甜瓜
[官方文档](https://tech.kakaoent.com/ai/using-melon-mcp-server-en/)

浏览音乐排行榜和您的个性化音乐精选

- Claude Code 接入命令：`claude mcp add melon --transport http https://mcp.melon.com/mcp/`

### PlayMCP
[官方文档](https://www.notion.so/2189b97b4888803dbbdcef264e7eff58)

连接并使用工具箱中的 PlayMCP 服务器

- Claude Code 接入命令：`claude mcp add playmcp --transport http https://playmcp.kakao.com/mcp`

###内存
[官方文档](https://docs.mem.ai/mcp/overview)

AI 笔记本可满足您的所有需求

- Claude Code 接入命令：`claude mcp add mem --transport http https://mcp.mem.ai/mcp`

### 克里斯普
[官方文档](https://help.krisp.ai/hc/en-us/articles/25416265429660-Krisp-MCP-Supported-tools)

通过文字记录和笔记添加会议背景

- Claude Code 接入命令：`claude mcp add krisp --transport http https://mcp.krisp.ai/mcp`

### 澄清一下
[官方文档](https://docs.clarify.ai/en/articles/13367278-clarify-mcp)

查询您的 CRM。创建记录。询问任何事情。

- Claude Code 接入命令：`claude mcp add clarify --transport http https://api.clarify.ai/mcp`

### 票务裁缝
[官方文档](https://help.tickettailor.com/en/articles/11892797-how-to-connect-ticket-tailor-to-your-favourite-ai-agent)

用于管理门票、订单等的活动平台

- Claude Code 接入命令：`claude mcp add ticket-tailor --transport http https://mcp.tickettailor.ai/mcp`

### 文员
[官方文档](https://clerk.com/docs/guides/ai/mcp/clerk-mcp-server)

添加身份验证、组织和计费

- Claude Code 接入命令：`claude mcp add clerk --transport http https://mcp.clerk.com/mcp`

### 端口IO
[官方文档](https://docs.port.io/ai-interfaces/port-mcp-server/overview-and-installation)

搜索您的上下文湖并安全地运行操作

- 需要先完成服务端配置：[https://docs.port.io/ai-interfaces/port-mcp-server/overview-and-installation](https://docs.port.io/ai-interfaces/port-mcp-server/overview-and-installation)

### 工艺
[官方文档](https://documents.craft.me/jWeCVJrSfxFRuA)

笔记和第二大脑

- Claude Code 接入命令：`claude mcp add craft --transport http https://mcp.craft.do/my/mcp`

### 塔维利
[官方文档](https://docs.tavily.com/documentation/mcp)

将您的 AI 代理连接到网络

- Claude Code 接入命令：`claude mcp add tavily --transport http https://mcp.tavily.com/mcp`

### 星球规模
[官方文档](https://planetscale.com/docs/connect/mcp)

对 Postgres 和 MySQL 数据库进行身份验证的访问

- Claude Code 接入命令：`claude mcp add planetscale --transport http https://mcp.pscale.dev/mcp/planetscale`

### 鲁明
[官方文档](https://github.com/luminpdf/lumin-mcp-server)

管理文档、发送签名请求以及将 Markdown 转换为 PDF

- Claude Code 接入命令：`claude mcp add lumin --transport http https://mcp.luminpdf.com/mcp`

### 温德姆酒店及度假村
[官方文档](https://www.wyndhamhotels.com/mcp-doc)

更快地找到最适合您的温德姆酒店

- Claude Code 接入命令：`claude mcp add wyndham-hotels-and-resorts --transport http https://mcp.wyndhamhotels.com/claude/mcp`

### 萌芽数据智能
[官方文档](https://support.sprouts.ai/en/articles/13384582-sprouts-mcp-server-documentation#h_541c149a52)

从查询到合格的潜在客户只需几秒钟。

- Claude Code 接入命令：`claude mcp add sprouts-data-intelligence --transport http https://sprouts-mcp-server.kartikay-dhar.workers.dev`

### 轻快
[官方文档](https://support.lilt.com/kb/LILT-mcp)

人工验证的高质量翻译

- Claude Code 接入命令：`claude mcp add lilt --transport http https://mcp.lilt.com/mcp`

### 元视图
[官方文档](https://support.metaview.ai/integrations/mcp-integration/mcp-overview.mdx)

人工智能招聘平台。

- Claude Code 接入命令：`claude mcp add metaview --transport http https://mcp.metaview.ai/mcp`### GraphOS MCP 工具
[官方文档](https://www.apollographql.com/docs/graphos/platform/graphos-mcp-tools)

搜索 Apollo 文档、规格和最佳实践

- Claude Code 接入命令：`claude mcp add graphos-mcp-tools --transport http https://mcp.apollographql.com`

### 当地猎鹰
[官方文档](https://github.com/local-falcon/mcp)

AI可见性和本地搜索智能平台

- Claude Code 接入命令：`claude mcp add local-falcon --transport http https://mcp.localfalcon.com`

### 卧推
[官方文档](https://help.benchling.com/hc/en-us/articles/40342713479437-Benchling-MCP)

连接到研发数据、源实验和笔记本

- 需要先完成服务端配置：[https://help.benchling.com/hc/en-us/articles/40342713479437-Benchling-MCP](https://help.benchling.com/hc/en-us/articles/40342713479437-Benchling-MCP)

### Airwallex 开发者
[官方文档](https://www.airwallex.com/docs/developer-tools/ai/developer-mcp)

使用 Claude 与 Airwallex 平台集成

- Claude Code 接入命令：`claude mcp add airwallex-developer --transport http https://mcp-demo.airwallex.com/developer`

### 清晰度人工智能
[官方文档](https://clarity-sfdr20-mcp.pro.clarity.ai/)

模拟拟议的 SFDR 2.0 下的基金分类

- Claude Code 接入命令：`claude mcp add clarity-ai --transport http https://clarity-sfdr20-mcp.pro.clarity.ai/mcp`

### 发烧事件发现
[官方文档](https://developer.feverup.com/)

探索世界各地的现场娱乐活动

- Claude Code 接入命令：`claude mcp add fever-event-discovery --transport http https://data-search.apigw.feverup.com/mcp`

### 维西尔
[官方文档](https://docs.visier.com/developer/agents/mcp/mcp-server.htm)

寻找人员、生产力和业务影响见解

- 需要先完成服务端配置：[https://docs.visier.com/developer/agents/mcp/mcp-server.htm](https://docs.visier.com/developer/agents/mcp/mcp-server.htm)

### 数据圣杯
[官方文档](https://docs.datagrail.io/docs/vera/vera-mcp/introduction-and-use)

安全、可用于生产的 AI 编排保护隐私

- 需要先完成服务端配置：[https://docs.datagrail.io/docs/vera/vera-mcp/introduction-and-use](https://docs.datagrail.io/docs/vera/vera-mcp/introduction-and-use)

### 星爆
[官方文档](https://docs.starburst.io/starburst-galaxy/ai-workflows/mcp-server.html)

从联合数据源安全地检索数据

- 需要先完成服务端配置：[https://docs.starburst.io/starburst-galaxy/ai-workflows/mcp-server.html](https://docs.starburst.io/starburst-galaxy/ai-workflows/mcp-server.html)

### 幅度
[官方文档](https://amplitude.com/docs/analytics/amplitude-mcp)

搜索、访问并获取有关 Amplitude 数据的见解

- 需要先完成服务端配置：[https://amplitude.com/docs/analytics/amplitude-mcp](https://amplitude.com/docs/analytics/amplitude-mcp)

### 空中桌
[官方文档](https://github.com/domdomegg/airtable-mcp-server)

读取和写入 Airtable 数据库

- 需要先完成服务端配置：[https://github.com/domdomegg/airtable-mcp-server](https://github.com/domdomegg/airtable-mcp-server)

**注意**

**需要特定集成？** [在 GitHub 上查找数百个 MCP 服务器](https://github.com/modelcontextprotocol/servers)，或使用 [MCP SDK](https://modelcontextprotocol.io/quickstart/server) 构建您自己的服务器。

## 安装 MCP 服务器

MCP 服务器可以根据您的需求以三种不同的方式进行配置：

### 选项 1：添加远程 HTTP 服务器

HTTP 服务器是连接到远程 MCP 服务器的推荐选项。这是基于云的服务最广泛支持的传输。

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 选项 2：添加远程 SSE 服务器

**警告**

SSE（服务器发送事件）传输已弃用。如果可用，请改用 HTTP 服务器。

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### 选项 3：添加本地 stdio 服务器

Stdio 服务器在您的计算机上作为本地进程运行。它们非常适合需要直接系统访问或自定义脚本的工具。

```bash
# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

**注意**

**重要：选项订购**

所有选项（`--transport`、`--env`、`--scope`、`--header`）必须位于服务器名称**之前**。然后，`--`（双破折号）将服务器名称与传递到 MCP 服务器的命令和参数分开。

例如：

* `claude mcp add --transport stdio myserver -- npx server` → 运行 `npx server`
* `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → 在环境中运行 `python server.py --port 8080` 和 `KEY=value`

这可以防止 Claude 的标志与服务器的标志之间发生冲突。

### 管理您的服务器

配置完成后，您可以使用以下命令管理 MCP 服务器：

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

### 动态工具更新

Claude Code 支持 MCP `list_changed` 通知，允许 MCP 服务器动态更新其可用工具、提示和资源，而无需您断开连接并重新连接。当 MCP 服务器发送 `list_changed` 通知时，Claude Code 会自动刷新该服务器的可用功能。

**提示**

温馨提示：* 使用 `--scope` 标志指定配置的存储位置：
  * `local`（默认）：仅在当前项目中可用（在旧版本中称为 `project`）
  * `project`：通过 `.mcp.json` 文件与项目中的每个人共享
  * `user`：适用于所有项目（在旧版本中称为 `global`）
* 使用 `--env` 标志设置环境变量（例如 `--env KEY=value`）
* 使用 MCP\_TIMEOUT 环境变量配置 MCP 服务器启动超时（例如 `MCP_TIMEOUT=10000 claude` 设置 10 秒超时）
* 当 MCP 工具输出超过 10,000 个令牌时，Claude Code 将显示警告。要增加此限制，请设置 `MAX_MCP_OUTPUT_TOKENS` 环境变量（例如 `MAX_MCP_OUTPUT_TOKENS=50000`）
* 使用 `/mcp` 向需要 OAuth 2.0 身份验证的远程服务器进行身份验证

**警告**

**Windows 用户**：在本机 Windows（不是 WSL）上，使用 `npx` 的本地 MCP 服务器需要 `cmd /c` 包装器以确保正确执行。

```bash
# This creates command="cmd" which Windows can execute
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

如果没有 `cmd /c` 包装器，您将遇到“连接已关闭”错误，因为 Windows 无法直接执行 `npx`。 （有关 `--` 参数的说明，请参阅上面的注释。）

### 插件提供的 MCP 服务器

[插件](./plugins) 可以捆绑 MCP 服务器，启用插件后自动提供工具和集成。插件 MCP 服务器的工作方式与用户配置的服务器相同。

**插件 MCP 服务器如何工作**：

* 插件在插件根目录的 `.mcp.json` 中定义 MCP 服务器或在 `plugin.json` 中内联
* 启用插件后，其 MCP 服务器自动启动
* 插件 MCP 工具与手动配置的 MCP 工具一起出现
* 插件服务器通过插件安装进行管理（不是 `/mcp` 命令）

**插件 MCP 配置示例**：

在插件根目录的 `.mcp.json` 中：

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

或内嵌在 `plugin.json` 中：

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**插件 MCP 功能**：

* **自动生命周期**：会话启动时，启用插件的服务器会自动连接。如果您在会话期间启用或禁用插件，请运行 `/reload-plugins` 以连接或断开其 MCP 服务器
* **环境变量**：使用 `${CLAUDE_PLUGIN_ROOT}` 作为捆绑插件文件，使用 `${CLAUDE_PLUGIN_DATA}` 作为在插件更新后仍然存在的[持久状态](./plugins-reference#persistent-data-directory)
* **用户环境访问**：访问与手动配置的服务器相同的环境变量
* **多种传输类型**：支持 stdio、SSE 和 HTTP 传输（传输支持可能因服务器而异）

**查看插件 MCP 服务器**：

```bash
# Within Claude Code, see all MCP servers including plugin ones
/mcp
```

插件服务器出现在列表中，并带有指示符显示它们来自插件。

**插件 MCP 服务器的优点**：

* **捆绑分发**：工具和服务器打包在一起
* **自动设置**：无需手动 MCP 配置
* **团队一致性**：安装插件后，每个人都获得相同的工具

有关将 MCP 服务器与插件捆绑在一起的详细信息，请参阅[插件组件参考](./plugins-reference#mcp-servers)。

## MCP 安装范围MCP 服务器可以在三个不同的范围级别进行配置，每个级别都用于管理服务器可访问性和共享的不同目的。了解这些范围有助于您确定根据您的特定需求配置服务器的最佳方法。

### 本地范围

本地范围的服务器代表默认配置级别，并存储在项目路径下的 `~/.claude.json` 中。这些服务器对您来说是私有的，并且只有在当前项目目录中工作时才能访问。此范围非常适合个人开发服务器、实验配置或包含不应共享的敏感凭据的服务器。

**注意**

MCP 服务器的术语“本地范围”与一般本地设置不同。 MCP 本地范围服务器存储在 `~/.claude.json`（您的主目录）中，而常规本地设置使用 `.claude/settings.local.json`（在项目目录中）。有关设置文件位置的详细信息，请参阅[设置](./settings#settings-files)。

```bash
# Add a local-scoped server (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Explicitly specify local scope
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### 项目范围

项目范围的服务器通过将配置存储在项目根目录的 `.mcp.json` 文件中来实现团队协作。该文件旨在签入版本控制，确保所有团队成员都可以访问相同的 MCP 工具和服务。添加项目范围的服务器时，Claude Code 会使用适当的配置结构自动创建或更新此文件。

```bash
# Add a project-scoped server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

生成的 `.mcp.json` 文件遵循标准化格式：

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

出于安全原因，Claude Code 在使用 `.mcp.json` 文件中的项目范围服务器之前会提示您进行批准。如果您需要重置这些批准选择，请使用 `claude mcp reset-project-choices` 命令。

### 用户范围

用户范围的服务器存储在 `~/.claude.json` 中，并提供跨项目可访问性，使它们在您计算机上的所有项目中可用，同时对您的用户帐户保持私有。此范围非常适合您在不同项目中经常使用的个人实用服务器、开发工具或服务。

```bash
# Add a user server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### 选择正确的范围

根据以下条件选择您的范围：

* **本地范围**：个人服务器、实验配置或特定于一个项目的敏感凭据
* **项目范围**：团队共享服务器、项目特定工具或协作所需的服务
* **用户范围**：跨多个项目、开发工具或常用服务所需的个人实用程序

**注意**

**MCP 服务器存储在哪里？**

* **用户和本地范围**：`~/.claude.json`（在 `mcpServers` 字段中或项目路径下）
* **项目范围**：项目根目录中的 `.mcp.json`（签入源代码管理）
* **托管**：系统目录中的 `managed-mcp.json`（请参阅[托管 MCP 配置](#managed-mcp-configuration)）

### 范围层次结构和优先级

MCP 服务器配置遵循明确的优先级层次结构。当多个作用域存在同名服务器时，系统会通过优先考虑本地作用域的服务器、其次是项目作用域的服务器、最后是用户作用域的服务器来解决冲突。这种设计确保个人配置可以在需要时覆盖共享配置。### `.mcp.json` 中的环境变量扩展

Claude Code 支持 `.mcp.json` 文件中的环境变量扩展，允许团队共享配置，同时保持机器特定路径和 API 密钥等敏感值的灵活性。

**支持的语法：**

* `${VAR}` - 扩展到环境变量 `VAR` 的值
* `${VAR:-default}` - 如果设置则扩展为 `VAR`，否则使用 `default`

**扩张地点：**
环境变量可以扩展为：

* `command` - 服务器可执行路径
* `args` - 命令行参数
* `env` - 传递到服务器的环境变量
* `url` - 适用于 HTTP 服务器类型
* `headers` - 用于 HTTP 服务器身份验证

**变量扩展示例：**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

如果未设置所需的环境变量且没有默认值，Claude Code 将无法解析配置。

## 实际例子

{/* ### 示例：使用 Playwright 自动化浏览器测试

  ```bash
  claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
  ```

  然后编写并运行浏览器测试：

  ```text
  Test if the login flow works with test@example.com
  ```
  ```text
  Take a screenshot of the checkout page on mobile
  ```
  ```text
  Verify that the search feature returns results
  ``` */}

### 示例：使用 Sentry 监视错误

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

使用您的 Sentry 帐户进行身份验证：

```text
/mcp
```

然后调试生产问题：

```text
What are the most common errors in the last 24 hours?
```

```text
Show me the stack trace for error ID abc123
```

```text
Which deployment introduced these new errors?
```

### 示例：连接到 GitHub 进行代码审查

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

如果需要，请为 GitHub 选择“身份验证”进行身份验证：

```text
/mcp
```

然后使用 GitHub：

```text
Review PR #456 and suggest improvements
```

```text
Create a new issue for the bug we just found
```

```text
Show me all open PRs assigned to me
```

### 示例：查询您的 PostgreSQL 数据库

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

然后自然地查询你的数据库：

```text
What's our total revenue this month?
```

```text
Show me the schema for the orders table
```

```text
Find customers who haven't made a purchase in 90 days
```

## 使用远程 MCP 服务器进行身份验证

许多基于云的 MCP 服务器需要身份验证。 Claude Code 支持 OAuth 2.0 以实现安全连接。

### 添加需要认证的服务器

例如：

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

  
### 在 Claude Code 中使用 /mcp 命令

在 Claude 代码中，使用以下命令：

```text
/mcp
```

然后按照浏览器中的步骤进行登录。

**提示**

温馨提示：

* 身份验证令牌安全存储并自动刷新
* 使用 `/mcp` 菜单中的“清除身份验证”来撤销访问权限
* 如果您的浏览器没有自动打开，请复制提供的 URL 并手动打开
* 如果身份验证后浏览器重定向失败并出现连接错误，请将浏览器地址栏中的完整回调 URL 粘贴到 Claude Code 中显示的 URL 提示中
* OAuth 身份验证适用于 HTTP 服务器

### 使用固定的OAuth回调端口

某些 MCP 服务器需要提前注册特定的重定向 URI。默认情况下，Claude Code 为 OAuth 回调选择一个随机可用端口。使用 `--callback-port` 修复端口，使其与 `http://localhost:PORT/callback` 形式的预注册重定向 URI 匹配。

您可以单独使用 `--callback-port`（通过动态客户端注册）或与 `--client-id` 一起使用（通过预配置的凭据）。

```bash
# Fixed callback port with dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### 使用预配置的 OAuth 凭据某些 MCP 服务器不支持自动 OAuth 设置。如果您看到类似“不兼容的身份验证服务器：不支持动态客户端注册”的错误，则服务器需要预先配置的凭据。首先通过服务器的开发人员门户注册 OAuth 应用程序，然后在添加服务器时提供凭据。

### 向服务器注册 OAuth 应用程序

通过服务器的开发人员门户创建应用程序，并记下您的客户端 ID 和客户端密钥。

许多服务器还需要重定向 URI。如果是这样，请选择一个端口并以 `http://localhost:PORT/callback` 格式注册重定向 URI。在下一步中使用与 `--callback-port` 相同的端口。

  
### 使用您的凭据添加服务器

    选择以下方法之一。用于 `--callback-port` 的端口可以是任何可用端口。它只需要与您在上一步中注册的重定向 URI 匹配即可。

### 克劳德·MCP 添加

使用 `--client-id` 传递应用程序的客户端 ID。 `--client-secret` 标志提示使用屏蔽输入的秘密：

```bash
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### 克劳德 mcp add-json

将 `oauth` 对象包含在 JSON 配置中，并将 `--client-secret` 作为单独的标志传递：

```bash
claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
  --client-secret
```

### claude mcp add-json （仅限回调端口）

在使用动态客户端注册时，使用不带客户端 ID 的 `--callback-port` 来修复端口：

```bash
claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
```

### CI / 环境变量

通过环境变量设置秘密以跳过交互式提示：

```bash
MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

  
### 在 Claude Code 中进行身份验证

在 Claude Code 中运行 `/mcp` 并按照浏览器登录流程进行操作。

**提示**

温馨提示：

* 客户端密钥安全地存储在您的系统钥匙串 (macOS) 或凭证文件中，而不是存储在您的配置中
* 如果服务器使用没有密钥的公共 OAuth 客户端，则仅使用 `--client-id`，而不使用 `--client-secret`
* `--callback-port` 可与或不与 `--client-id` 一起使用
* 这些标志仅适用于 HTTP 和 SSE 传输。它们对 stdio 服务器没有影响
* 使用 `claude mcp get <name>` 验证是否为服务器配置了 OAuth 凭据

### 覆盖 OAuth 元数据发现

如果您的 MCP 服务器在标准 OAuth 元数据端点 (`/.well-known/oauth-authorization-server`) 上返回错误，但公开工作的 OIDC 端点，您可以告诉 Claude Code 直接从您指定的 URL 获取 OAuth 元数据，绕过标准发现链。

在 `.mcp.json` 中服务器配置的 `oauth` 对象中设置 `authServerMetadataUrl`：

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL 必须使用 `https://`。此选项需要 Claude Code v2.1.64 或更高版本。

## 从 JSON 配置添加 MCP 服务器

如果您有 MCP 服务器的 JSON 配置，则可以直接添加：

### 从 JSON 添加 MCP 服务器

```bash
# Basic syntax
claude mcp add-json <name> '<json>'

# Example: Adding an HTTP server with JSON configuration
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

# Example: Adding an HTTP server with pre-configured OAuth credentials
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
```

  
### 验证服务器是否已添加

```bash
claude mcp get weather-api
```

**提示**

温馨提示：

* 确保 JSON 在您的 shell 中正确转义
* JSON 必须符合 MCP 服务器配置架构
* 您可以使用 `--scope user` 将服务器添加到您的用户配置中，而不是特定于项目的配置

## 从 Claude Desktop 导入 MCP 服务器

如果您已经在 Claude Desktop 中配置了 MCP 服务器，则可以导入它们：

### 从 Claude Desktop 导入服务器

```bash
# Basic syntax 
claude mcp add-from-claude-desktop 
```### 选择要导入的服务器

运行该命令后，您将看到一个交互式对话框，允许您选择要导入的服务器。

  
### 验证服务器是否已导入

```bash
claude mcp list 
```

**提示**

温馨提示：

* 此功能仅适用于 macOS 和 Windows Linux 子系统 (WSL)
* 它从这些平台上的标准位置读取 Claude Desktop 配置文件
* 使用 `--scope user` 标志将服务器添加到您的用户配置中
* 导入的服务器将具有与 Claude Desktop 中相同的名称
* 如果已存在同名服务器，它们将获得数字后缀（例如 `server_1`）

## 使用 Claude.ai 的 MCP 服务器

如果您已使用 [Claude.ai](https://claude.ai) 帐户登录 Claude Code，则您在 Claude.ai 中添加的 MCP 服务器将自动在 Claude Code 中可用：

### 在 Claude.ai 中配置 MCP 服务器

在 [claude.ai/settings/connectors](https://claude.ai/settings/connectors) 添加服务器。在团队和企业计划中，只有管理员可以添加服务器。

  
### 验证 MCP 服务器

在 Claude.ai 中完成任何必需的身份验证步骤。

  
### 查看和管理 Claude Code 中的服务器

在 Claude Code 中，使用命令：

```text
/mcp
```

Claude.ai 服务器出现在列表中，并带有指示符显示它们来自 Claude.ai。

要在 Claude Code 中禁用 claude.ai MCP 服务器，请将 `ENABLE_CLAUDEAI_MCP_SERVERS` 环境变量设置为 `false`：

```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## 使用 Claude Code 作为 MCP 服务器

您可以使用 Claude Code 本身作为其他应用程序可以连接到的 MCP 服务器：

```bash
# Start Claude as a stdio MCP server
claude mcp serve
```

您可以通过将此配置添加到 claude\_desktop\_config.json 在 Claude Desktop 中使用它：

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**警告**

**配置可执行文件路径**：`command` 字段必须引用 Claude Code 可执行文件。如果 `claude` 命令不在系统的 PATH 中，则需要指定可执行文件的完整路径。

要查找完整路径：

```bash
which claude
```

然后在配置中使用完整路径：

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "/full/path/to/claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

如果没有正确的可执行路径，您将遇到类似 `spawn claude ENOENT` 的错误。

**提示**

温馨提示：

* 服务器提供对 Claude 的查看、编辑、LS 等工具的访问。
* 在 Claude Desktop 中，尝试要求 Claude 读取目录中的文件、进行编辑等。
* 请注意，此 MCP 服务器仅向您的 MCP 客户端公开 Claude Code 的工具，因此您自己的客户端负责实现各个工具调用的用户确认。

## MCP 输出限制和警告

当 MCP 工具产生大量输出时，Claude Code 帮助管理令牌使用情况，以防止淹没您的对话上下文：

* **输出警告阈值**：当任何 MCP 工具输出超过 10,000 个令牌时，Claude Code 将显示警告
* **可配置限制**：您可以使用 `MAX_MCP_OUTPUT_TOKENS` 环境变量调整允许的最大 MCP 输出令牌
* **默认限制**：默认最大值为 25,000 个代币

要增加产生大输出的工具的限制：

```bash
# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

当使用 MCP 服务器时，这特别有用：* 查询大型数据集或数据库
* 生成详细的报告或文档
* 处理大量日志文件或调试信息

**警告**

如果您经常遇到特定 MCP 服务器的输出警告，请考虑增加限制或配置服务器以分页或过滤其响应。

## 响应 MCP 启发请求

MCP 服务器可以使用启发向您请求中间任务的结构化输入。当服务器需要它自己无法获取的信息时，Claude Code 会显示一个交互式对话框，并将您的响应传递回服务器。您无需进行任何配置：当服务器请求时，会自动出现诱导对话框。

服务器可以通过两种方式请求输入：

* **表单模式**：Claude Code 显示一个对话框，其中包含服务器定义的表单字段（例如，用户名和密码提示）。填写字段并提交。
* **URL 模式**：Claude Code 打开浏览器 URL 进行身份验证或批准。在浏览器中完成流程，然后在 CLI 中确认。

要自动响应诱导请求而不显示对话框，请使用 [`Elicitation` 挂钩](./hooks#elicitation)。

如果您正在构建使用诱导的 MCP 服务器，请参阅 [MCP 诱导规范](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) 以获取协议详细信息和架构示例。

## 使用 MCP 资源

MCP 服务器可以公开您可以使用@提及引用的资源，类似于引用文件的方式。

###参考MCP资源

### 列出可用资源

在提示中键入 `@` 可查看所有连接的 MCP 服务器的可用资源。资源与文件一起显示在自动完成菜单中。

  
### 引用特定资源

使用 `@server:protocol://resource/path` 格式引用资源：

```text
Can you analyze @github:issue://123 and suggest a fix?
```

```text
Please review the API documentation at @docs:file://api/authentication
```

  
### 多个资源引用

您可以在单个提示中引用多个资源：

```text
Compare @postgres:schema://users with @docs:file://database/user-model
```

**提示**

温馨提示：

* 引用时自动获取资源并作为附件包含在内
* 资源路径在@提及自动完成中可模糊搜索
* Claude Code 在服务器支持时自动提供列出和读取 MCP 资源的工具
* 资源可以包含 MCP 服务器提供的任何类型的内容（文本、JSON、结构化数据等）

## 使用 MCP 工具搜索进行扩展

当您配置了许多 MCP 服务器时，工具定义可能会占用上下文窗口的很大一部分。 MCP 工具搜索通过按需动态加载工具而不是预加载所有工具来解决此问题。

### 它是如何工作的

当 MCP 工具描述占用上下文窗口的 10% 以上时，Claude Code 会自动启用工具搜索。您可以[调整此阈值](#configure-tool-search) 或完全禁用工具搜索。触发时：

1. MCP 工具被推迟而不是预先加载到上下文中
2. Claude在需要时使用搜索工具发现相关的MCP工具
3. 仅将 Claude 实际需要的工具加载到上下文中
4. 从您的角度来看，MCP 工具继续像以前一样工作

### 对于 MCP 服务器作者如果您正在构建 MCP 服务器，则启用工具搜索后，服务器说明字段将变得更加有用。服务器说明可帮助 Claude 了解何时搜索您的工具，类似于[技能](./skills) 的工作方式。

添加清晰的描述性服务器指令来解释：

* 您的工具处理什么类别的任务
* Claude 何时应搜索您的工具
* 您的服务器提供的关键功能

### 配置工具搜索

默认情况下启用工具搜索：MCP 工具会延迟并按需发现。当 `ANTHROPIC_BASE_URL` 指向非第一方主机时，默认情况下会禁用工具搜索，因为大多数代理不会转发 `tool_reference` 块。如果您的代理这样做，请明确设置 `ENABLE_TOOL_SEARCH`。此功能需要支持 `tool_reference` 块的模型：Sonnet 4 及更高版本，或 Opus 4 及更高版本。 Haiku 模型不支持工具搜索。

使用 `ENABLE_TOOL_SEARCH` 环境变量控制工具搜索行为：

|价值|行为 |
| :--------- | :------------------------------------------------------------------------------------------------ |
| （未设置）|默认启用。 `ANTHROPIC_BASE_URL` 为非第一方主机时禁用 |
| `true` |始终启用，包括非第一方 `ANTHROPIC_BASE_URL` |
| `auto` |当 MCP 工具超过上下文的 10% 时激活 |
| `auto:<N>` |在自定义阈值处激活，其中 `<N>` 是百分比（例如，`auto:5` 表示 5%）|
| `false` |已禁用，所有 MCP 工具均已预先加载 |

```bash
# Use a custom 5% threshold
ENABLE_TOOL_SEARCH=auto:5 claude

# Disable tool search entirely
ENABLE_TOOL_SEARCH=false claude
```

或者在 [settings.json `env` 字段](./settings#available-settings) 中设置值。

您还可以专门使用 `disallowedTools` 设置禁用 MCPSearch 工具：

```json
{
  "permissions": {
    "deny": ["MCPSearch"]
  }
}
```

## 使用 MCP 提示符作为命令

MCP 服务器可以公开提示，这些提示可作为 Claude Code 中的命令使用。

###执行MCP提示

### 发现可用的提示

键入 `/` 可查看所有可用命令，包括来自 MCP 服务器的命令。 MCP 提示以 `/mcp__servername__promptname` 格式显示。

  
### 执行不带参数的提示

```text
/mcp__github__list_prs
```

  
### 执行带有参数的提示

许多提示接受参数。在命令后传递它们，以空格分隔：

```text
/mcp__github__pr_review 456
```

```text
/mcp__jira__create_issue "Bug in login flow" high
```

**提示**

温馨提示：

* MCP 提示是从连接的服务器动态发现的
* 根据提示定义的参数解析参数
* 提示结果直接注入到对话中
* 服务器和提示符名称已标准化（空格变为下划线）

## 托管 MCP 配置

对于需要集中控制 MCP 服务器的组织，Claude Code 支持两种配置选项：

1. **与`managed-mcp.json`独占控制**：部署一组固定的MCP服务器，用户无法修改或扩展
2. **基于策略的允许列表/拒绝列表**：允许用户添加自己的服务器，但限制允许的服务器

这些选项允许 IT 管理员：* **控制员工可以访问哪些 MCP 服务器**：在整个组织内部署一组标准化的经批准的 MCP 服务器
* **防止未经授权的 MCP 服务器**：限制用户添加未经批准的 MCP 服务器
* **完全禁用 MCP**：如果需要，完全删除 MCP 功能

### 选项 1：使用 Managed-mcp.json 进行独占控制

当您部署 `managed-mcp.json` 文件时，它会对所有 MCP 服务器进行**独占控制**。用户无法添加、修改或使用除此文件中定义的服务器之外的任何 MCP 服务器。对于想要完全控制的组织来说，这是最简单的方法。

系统管理员将配置文件部署到系统范围的目录中：

* macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux 和 WSL：`/etc/claude-code/managed-mcp.json`
* Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

**注意**

这些是需要管理员权限的系统范围路径（不是像 `~/Library/...` 这样的用户主目录）。它们旨在由 IT 管理员部署。

`managed-mcp.json` 文件使用与标准 `.mcp.json` 文件相同的格式：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### 选项 2：使用允许列表和拒绝列表进行基于策略的控制

管理员可以允许用户配置自己的 MCP 服务器，同时对允许的服务器实施限制，而不是采取独占控制。此方法使用 [托管设置文件](./settings#settings-files) 中的 `allowedMcpServers` 和 `deniedMcpServers`。

**注意**

**在选项之间进行选择**：当您想要部署一组固定的服务器而不需要用户自定义时，请使用选项 1 (`managed-mcp.json`)。当您希望允许用户在策略限制内添加自己的服务器时，请使用选项 2（允许列表/拒绝列表）。

#### 限制选项

允许列表或拒绝列表中的每个条目都可以通过三种方式限制服务器：

1. **按服务器名称** (`serverName`)：匹配服务器的配置名称
2. **按命令** (`serverCommand`)：匹配用于启动 stdio 服务器的确切命令和参数
3. **按 URL 模式** (`serverUrl`)：使用通配符支持匹配远程服务器 URL

**重要提示**：每个条目必须恰好具有 `serverName`、`serverCommand` 或 `serverUrl` 之一。

#### 配置示例

```json
{
  "allowedMcpServers": [
    // Allow by server name
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Allow by exact command (for stdio servers)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Allow by URL pattern (for remote servers)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Block by server name
    { "serverName": "dangerous-server" },

    // Block by exact command (for stdio servers)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Block by URL pattern (for remote servers)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### 基于命令的限制如何工作

**精确匹配**：

* 命令数组必须**完全**匹配 - 命令和所有参数都按正确的顺序
* 示例：`["npx", "-y", "server"]` 将与 `["npx", "server"]` 或 `["npx", "-y", "server", "--flag"]` 不匹配

**Stdio 服务器行为**：

* 当允许列表包含**任何** `serverCommand` 条目时，stdio 服务器**必须**匹配这些命令之一
* 当存在命令限制时，Stdio 服务器无法单独通过名称传递
* 这确保管理员可以强制执行哪些命令被允许运行

**非 stdio 服务器行为**：

* 当白名单中存在 `serverUrl` 条目时，远程服务器（HTTP、SSE、WebSocket）使用基于 URL 的匹配
* 如果不存在 URL 条目，远程服务器将回退到基于名称的匹配
* 命令限制不适用于远程服务器

#### 基于 URL 的限制如何工作

URL 模式支持使用 `*` 的通配符来匹配任何字符序列。这对于允许整个域或子域非常有用。

**通配符示例**：* `https://mcp.company.com/*` - 允许特定域上的所有路径
* `https://*.example.com/*` - 允许 example.com 的任何子域
* `http://localhost:*/*` - 允许本地主机上的任何端口

**远程服务器行为**：

* 当允许列表包含**任何** `serverUrl` 条目时，远程服务器**必须**匹配这些 URL 模式之一
* 当存在 URL 限制时，远程服务器无法仅通过名称传递
* 这确保管理员可以强制允许哪些远程端点

### 示例：仅限 URL 的白名单

```json
{
  "allowedMcpServers": [
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ]
}
```

**结果**：

* HTTP 服务器位于 `https://mcp.company.com/api`： ✅ 允许（匹配 URL 模式）
* HTTP 服务器位于 `https://api.internal.corp/mcp`： ✅ 允许（匹配通配符子域）
* HTTP 服务器位于 `https://external.com/mcp`：❌ 已阻止（与任何 URL 模式都不匹配）
* 具有任何命令的 Stdio 服务器： ❌ 已阻止（没有名称或命令条目匹配）

### 示例：仅限命令的白名单

```json
{
  "allowedMcpServers": [
    { "serverCommand": ["npx", "-y", "approved-package"] }
  ]
}
```

**结果**：

* 具有 `["npx", "-y", "approved-package"]` 的 Stdio 服务器： ✅ 允许（与命令匹配）
* 具有 `["node", "server.js"]` 的 Stdio 服务器：❌ 已阻止（与命令不匹配）
* 名为“my-api”的 HTTP 服务器：❌ 已阻止（没有可匹配的名称条目）

### 示例：混合名称和命令白名单

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": ["npx", "-y", "approved-package"] }
  ]
}
```

**结果**：

* 名为“local-tool”且带有 `["npx", "-y", "approved-package"]` 的 Stdio 服务器： ✅ 允许（与命令匹配）
* 名为“local-tool”且带有 `["node", "server.js"]` 的 Stdio 服务器：❌ 已阻止（命令条目存在但不匹配）
* 名为“github”且带有 `["node", "server.js"]` 的 Stdio 服务器：❌ 已阻止（当命令条目存在时，stdio 服务器必须匹配命令）
* 名为“github”的 HTTP 服务器： ✅ 允许（与名称匹配）
* 名为“other-api”的 HTTP 服务器：❌ 已阻止（名称不匹配）

### 示例：仅限名称白名单

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "internal-tool" }
  ]
}
```

**结果**：

* 名为“github”的 Stdio 服务器，带有任何命令： ✅ 允许（无命令限制）
* 名为“internal-tool”的 Stdio 服务器，可使用任何命令： ✅ 允许（无命令限制）
* 名为“github”的 HTTP 服务器： ✅ 允许（与名称匹配）
* 任何名为“其他”的服务器： ❌ 已阻止（名称不匹配）

#### 允许列表行为 (`allowedMcpServers`)

* `undefined`（默认）：无限制 - 用户可以配置任何 MCP 服务器
* 空阵列 `[]`：完全锁定 - 用户无法配置任何 MCP 服务器
* 条目列表：用户只能配置按名称、命令或 URL 模式匹配的服务器

#### 拒绝列表行为 (`deniedMcpServers`)

* `undefined`（默认）：没有服务器被阻止
* 空阵列 `[]`：没有服务器被阻止
* 条目列表：指定服务器在所有范围内被明确阻止

#### 重要提示

* **选项1和选项2可以组合**：如果`managed-mcp.json`存在，则具有独占控制权，用户无法添加服务器。允许列表/拒绝列表仍然适用于托管服务器本身。
* **拒绝列表具有绝对优先级**：如果服务器与拒绝列表条目（按名称、命令或 URL）匹配，即使它位于允许列表中，也会被阻止
* 基于名称、基于命令和基于 URL 的限制协同工作：如果服务器与 **名称条目、命令条目或 URL 模式匹配**则通过（除非被拒绝列表阻止）

**注意****使用 `managed-mcp.json` 时**：用户无法通过 `claude mcp add` 或配置文件添加 MCP 服务器。 `allowedMcpServers` 和 `deniedMcpServers` 设置仍适用于筛选实际加载的托管服务器。
