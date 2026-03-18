---
title: "将 Claude Code 与 Chrome（测试版）结合使用"
order: 16
section: "platforms"
sectionLabel: "平台与集成"
sectionOrder: 3
summary: "将 Claude Code 连接到 Chrome 浏览器以测试 Web 应用程序、使用控制台日志进行调试、自动填写表单以及从网页中提取数据。"
sourceUrl: "https://code.claude.com/docs/en/chrome.md"
sourceTitle: "Use Claude Code with Chrome (beta)"
tags: []
---
# 将 Claude Code 与 Chrome（测试版）结合使用

> 将 Claude Code 连接到 Chrome 浏览器以测试 Web 应用程序、使用控制台日志进行调试、自动填写表单以及从网页中提取数据。

Claude Code 与 Chrome 浏览器扩展中的 Claude 集成，为您提供来自 CLI 或 [VS Code 扩展](./vs-code#automate-browser-tasks-with-chrome) 的浏览器自动化功能。构建代码，然后在浏览器中进行测试和调试，而无需切换上下文。

Claude 为浏览器任务打开新选项卡并共享​​浏览器的登录状态，以便它可以访问您已登录的任何网站。浏览器操作在可见的 Chrome 窗口中实时运行。当 Claude 遇到登录页面或验证码时，它会暂停并要求您手动处理。

**注意**

Chrome 集成处于测试阶段，目前可与 Google Chrome 和 Microsoft Edge 配合使用。 Brave、Arc 或其他基于 Chromium 的浏览器尚不支持它。也不支持 WSL（Linux 的 Windows 子系统）。

## 能力

连接 Chrome 后，您可以在单个工作流程中将浏览器操作与编码任务链接起来：

* **实时调试**：直接读取控制台错误和 DOM 状态，然后修复导致它们的代码
* **设计验证**：从 Figma 模拟构建 UI，然后在浏览器中打开它以验证其匹配
* **Web 应用程序测试**：测试表单验证、检查视觉回归或验证用户流程
* **经过身份验证的网络应用程序**：与 Google Docs、Gmail、Notion 或您在没有 API 连接器的情况下登录的任何应用程序进行交互
* **数据提取**：从网页中提取结构化信息并保存在本地
* **任务自动化**：自动执行重复的浏览器任务，例如数据输入、表单填写或多站点工作流程
* **会话记录**：将浏览器交互记录为 GIF，以记录或分享发生的情况

## 先决条件

在将 Claude Code 与 Chrome 一起使用之前，您需要：

* [Google Chrome](https://www.google.com/chrome/) 或 [Microsoft Edge](https://www.microsoft.com/edge) 浏览器
* [Chrome 扩展中的 Claude](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 版本 1.0.36 或更高版本，适用于两种浏览器的 Chrome Web Store 中提供
* [Claude Code](./quickstart#step-1-install-claude-code) 版本 2.0.73 或更高版本
* 直接 Anthropic 计划（Pro、Max、Teams 或 Enterprise）

**注意**

Chrome 集成无法通过 Amazon Bedrock、Google Cloud Vertex AI 或 Microsoft Foundry 等第三方提供商提供。如果您仅通过第三方提供商访问 Claude，则需要单独的 claude.ai 帐户才能使用此功能。

## 在 CLI 中开始

### 与 Chrome 一起启动 Claude Code

使用 `--chrome` 标志启动 Claude Code：

```bash
claude --chrome
```

您还可以通过运行 `/chrome` 从现有会话中启用 Chrome。

  
### 要求 Claude 使用浏览器

此示例导航到一个页面，与其交互，并报告它找到的内容，所有这些都来自您的终端或编辑器：

```text
Go to code.claude.com/docs, click on the search box,
type "hooks", and tell me what results appear
```

随时运行 `/chrome` 以检查连接状态、管理权限或重新连接分机。

对于 VS Code，请参阅 [VS Code 中的浏览器自动化](./vs-code#automate-browser-tasks-with-chrome)。

### 默认启用 Chrome为了避免每个会话传递 `--chrome`，请运行 `/chrome` 并选择“默认启用”。

在 [VS Code 扩展](./vs-code#automate-browser-tasks-with-chrome) 中，只要安装 Chrome 扩展，Chrome 就可用。不需要额外的标志。

**注意**

在 CLI 中默认启用 Chrome 会增加上下文使用率，因为浏览器工具始终会加载。如果您发现上下文消耗增加，请禁用此设置并仅在需要时使用 `--chrome`。

### 管理站点权限

站点级权限继承自 Chrome 扩展。管理 Chrome 扩展设置中的权限，以控制 Claude 可以浏览、单击和输入的站点。

## 工作流程示例

这些示例展示了将浏览器操作与编码任务相结合的常见方法。运行 `/mcp` 并选择 `claude-in-chrome` 以查看可用浏览器工具的完整列表。

### 测试本地 Web 应用程序

开发 Web 应用程序时，请要求 Claude 验证您的更改是否正常工作：

```text
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude 导航到本地服务器，与表单交互，并报告其观察到的内容。

### 使用控制台日志进行调试

Claude 可以读取控制台输出以帮助诊断问题。告诉 Claude 要查找哪些模式，而不是询问所有控制台输出，因为日志可能很详细：

```text
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude 读取控制台消息并可以过滤特定模式或错误类型。

### 自动填写表格

加快重复数据输入任务的速度：

```text
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude 读取本地文件、导航 Web 界面并输入每条记录的数据。

### Google 文档中的草稿内容

使用 Claude 直接在文档中写入，无需设置 API：

```text
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude 打开文档，单击编辑器，然后键入内容。这适用于您登录的任何网络应用程序：Gmail、Notion、表格等。

### 从网页中提取数据

从网站中提取结构化信息：

```text
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude 导航到页面、读取内容并将数据编译为结构化格式。

### 运行多站点工作流程

跨多个网站协调任务：

```text
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude 跨选项卡工作以收集信息并完成工作流程。

### 录制演示 GIF

创建可共享的浏览器交互记录：

```text
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude 记录交互序列并将其保存为 GIF 文件。

## 故障排除

### 未检测到扩展

如果 Claude Code 显示“未检测到 Chrome 扩展”：

1. 验证 Chrome 扩展是否已在 `chrome://extensions` 中安装并启用
2. 通过运行 `claude --version` 验证 Claude Code 是最新的
3. 检查Chrome是否正在运行
4. 运行`/chrome`并选择“重新连接分机”以重新建立连接
5. 如果问题仍然存在，请重新启动 Claude Code 和 Chrome

首次启用 Chrome 集成时，Claude Code 会安装本机消息传递主机配置文件。 Chrome 在启动时读取此文件，因此如果第一次尝试时未检测到扩展名，请重新启动 Chrome 以获取新配置。

如果连接仍然失败，请验证主机配置文件是否存在：对于 Chrome：

* **macOS**：`~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**：`~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**：检查 Windows 注册表中的 `HKCU\Software\Google\Chrome\NativeMessagingHosts\`

对于边缘：

* **macOS**：`~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**：`~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**：检查 Windows 注册表中的 `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\`

### 浏览器没有响应

如果 Claude 的浏览器命令停止工作：

1. 检查模式对话框（警报、确认、提示）是否阻塞页面。 JavaScript 对话框会阻止浏览器事件并阻止 Claude 接收命令。手动关闭对话框，然后告诉 Claude 继续。
2. 要求Claude创建一个新选项卡并重试
3. 通过在 `chrome://extensions` 中禁用并重新启用 Chrome 扩展来重新启动它

### 长时间会话期间连接断开

Chrome 扩展的服务工作线程可能会在扩展会话期间处于空闲状态，从而中断连接。如果浏览器工具在一段时间不活动后停止工作，请运行 `/chrome` 并选择“重新连接扩展程序”。

### Windows 特定问题

在 Windows 上，您可能会遇到：

* **命名管道冲突 (EADDRINUSE)**：如果另一个进程正在使用相同的命名管道，请重新启动 Claude Code。关闭可能正在使用 Chrome 的任何其他 Claude Code 会话。
* **本机消息传递主机错误**：如果本机消息传递主机在启动时崩溃，请尝试重新安装 Claude Code 以重新生成主机配置。

### 常见错误消息

以下是最常遇到的错误以及解决方法：

|错误|原因 |修复 |
| ------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------- |
| “浏览器扩展未连接”|本机消息传递主机无法访问分机 |重新启动 Chrome 和 Claude Code，然后运行 ​​`/chrome` 重新连接 |
| “未检测到扩展”| Chrome 扩展未安装或被禁用 |在 `chrome://extensions` 中安装或启用扩展 |
| “没有可用的选项卡”| Claude 尝试在选项卡准备好之前采取行动 |要求 Claude 创建新选项卡并重试 |
| “接收端不存在” |推广服务人员闲置|运行 `/chrome` 并选择“重新连接扩展”|

## 另请参阅

* [在 VS Code 中使用 Claude Code](./vs-code#automate-browser-tasks-with-chrome)：VS Code 扩展中的浏览器自动化
* [CLI 参考](./cli-reference)：包括 `--chrome` 的命令行标志
* [常用工作流程](./common-workflows)：更多使用Claude Code的方式
* [数据和隐私](./data-usage)：Claude Code 如何处理您的数据
* [Chrome 中的 Claude 入门](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome)：Chrome 扩展的完整文档，包括快捷方式、计划和权限
