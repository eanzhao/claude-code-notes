---
title: "有效管理成本"
order: 45
section: "administration"
sectionLabel: "管理"
sectionOrder: 6
summary: "通过上下文管理、模型选择、扩展思维设置和预处理挂钩，跟踪代币使用情况、设置团队支出限制并降低 Claude Code 成本。"
sourceUrl: "https://code.claude.com/docs/en/costs.md"
sourceTitle: "Manage costs effectively"
tags: []
---
# 有效管理成本

> 通过上下文管理、模型选择、扩展思维设置和预处理 hook，跟踪 token 用量、设置团队支出限额并降低 Claude Code 成本。

Claude Code 每次交互都会消耗 token。成本取决于代码库大小、查询复杂度和会话长度。每个开发者每天的平均成本约为 6 美元，90% 的用户日成本低于 12 美元。

对于团队使用，Claude Code 按 API token 消耗计费。使用 Sonnet 4.6 的 Claude Code 平均每位开发者每月成本在 100-200 美元之间，但实际差异很大，取决于运行的实例数量和是否在自动化场景中使用。

本页介绍如何[跟踪成本](#track-your-costs)、[管理团队成本](#managing-costs-for-teams)和[减少 token 用量](#reduce-token-usage)。

## 跟踪成本

### 使用 `/cost` 命令

**注意**

`/cost` 命令显示 API token 用量，面向 API 用户。Claude Max 和 Pro 订阅者的用量包含在订阅中，`/cost` 数据与计费无关。订阅者可以用 `/stats` 查看使用情况。

`/cost` 命令提供当前会话的 token 用量详情：

```text
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## 管理团队成本

使用 Claude API 时，你可以为 Claude Code 工作区[设置支出限额](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits)。管理员可以在 Console 中[查看成本和使用报告](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking)。

**注意**

首次用 Claude Console 账户认证 Claude Code 时，系统会自动创建一个名为"Claude Code"的工作区。该工作区为组织内所有 Claude Code 使用提供集中的成本跟踪和管理。你无法为此工作区创建 API 密钥；它专门用于 Claude Code 认证和使用。

在 Bedrock、Vertex 和 Foundry 上，Claude Code 不会从你的云端发送指标。为了获取成本指标，一些大型企业使用 [LiteLLM](./llm-gateway#litellm-configuration) 这个开源工具来[按密钥跟踪支出](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend)。该项目与 Anthropic 无关，也未经安全审计。

### 速率限制建议

为团队设置 Claude Code 时，根据组织规模参考以下每用户每分钟 token 数 (TPM) 和每分钟请求数 (RPM) 建议：

| 团队规模 | 每用户 TPM | 每用户 RPM |
| ------------- | ------------ | ------------ |
| 1-5 人 | 20 万-30 万 | 5-7 |
| 5-20 人 | 10 万-15 万 | 2.5-3.5 |
| 20-50 人 | 50k-75k | 1.25-1.75 |
| 50-100 人 | 25k-35k | 0.62-0.87 |
| 100-500 人 | 15k-20k | 0.37-0.47 |
| 500+ 人 | 10k-15k | 0.25-0.35 |

例如，200 个用户可以按每用户 20k TPM 申请，总计 400 万 TPM（200 * 20,000 = 400 万）。团队越大，每用户 TPM 越低，因为大组织中同时使用 Claude Code 的人比例更小。这些速率限制在组织级别生效，而非针对个人——当其他人不活跃时，个人可以临时超出计算份额。

**注意**

如果预期会有高并发场景（如大型团队现场培训），可能需要为每用户分配更高的 TPM。

### Agent Teams 的 token 成本

[Agent Teams](./agent-teams) 会生成多个 Claude Code 实例，每个实例有独立的上下文窗口。Token 用量随活跃队友数量和各自运行时长而变化。

控制 Agent Teams 成本的建议：

* 队友使用 Sonnet。它在协调任务上能力够用，且成本更低。
* 保持团队规模精简。每个队友都运行独立的上下文窗口，token 用量大致与团队规模成正比。
* 保持生成 prompt 简洁聚焦。队友会自动加载 CLAUDE.md、MCP 服务器和技能，但生成 prompt 中的内容从一开始就会加入上下文。
* 工作完成后及时清理团队。活跃的队友即使空闲也会持续消耗 token。
* Agent Teams 默认关闭。在 [settings.json](./settings) 或环境变量中设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用。详见[启用 Agent Teams](./agent-teams#enable-agent-teams)。

## 减少 token 用量

Token 成本随上下文大小增长：Claude 处理的上下文越多，消耗的 token 越多。Claude Code 通过 prompt 缓存（降低系统提示等重复内容的成本）和自动压缩（接近上下文上限时总结对话历史）来自动优化成本。

以下策略帮助你缩小上下文、降低每条消息的成本。

### 主动管理上下文

用 `/cost` 查看当前 token 用量，或[配置状态栏](./statusline#context-window-usage)持续显示。

* **切换任务时清理上下文**：切换到不相关的工作时，用 `/clear` 重新开始。过时的上下文会让后续每条消息都浪费 token。清理前用 `/rename` 命名会话，之后可以用 `/resume` 回到该会话。
* **自定义压缩指令**：`/compact Focus on code samples and API usage` 告诉 Claude 压缩时优先保留哪些内容。

你也可以在 CLAUDE.md 中自定义压缩行为：

```markdown
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### 选择合适的模型

Sonnet 能胜任大多数编码任务，成本远低于 Opus。Opus 留给复杂的架构决策或多步推理。用 `/model` 在会话中切换模型，或在 `/config` 中设置默认值。对于简单的子 Agent 任务，在[子 Agent 配置](./sub-agents#choose-a-model)中指定 `model: haiku`。

### 减少 MCP 服务器开销

每个 MCP 服务器都会向上下文添加工具定义，即使空闲时也是如此。运行 `/context` 查看占用情况。

* **优先使用 CLI 工具**：`gh`、`aws`、`gcloud` 和 `sentry-cli` 等工具比 MCP 服务器更省上下文，因为它们不添加持久的工具定义。Claude 可以直接运行 CLI 命令，零开销。
* **禁用不用的服务器**：运行 `/mcp` 查看已配置的服务器，禁用不活跃的。
* **工具搜索自动启用**：当 MCP 工具描述超过上下文窗口的 10% 时，Claude Code 会自动延迟加载，通过[工具搜索](./mcp#scale-with-mcp-tool-search)按需加载。可以用 `ENABLE_TOOL_SEARCH=auto:<N>` 设置更低的阈值（如 `auto:5` 表示超过 5% 即触发）。

### 为类型化语言安装代码智能插件

[代码智能插件](./discover-plugins#code-intelligence)为 Claude 提供精确的符号导航，替代基于文本的搜索，减少探索陌生代码时不必要的文件读取。一次"跳转到定义"就能取代 grep 加读取多个候选文件。安装的语言服务器还会在编辑后自动报告类型错误，Claude 无需运行编译器就能发现问题。

### 用 hook 和技能分担处理

自定义 [hook](./hooks) 可以在 Claude 接触数据前先做预处理。与其让 Claude 读取 10,000 行日志去找错误，不如用 hook 先 grep 出 `ERROR` 行只返回匹配结果，把上下文从数万 token 降到几百。

[技能](./skills)可以给 Claude 提供领域知识，省去探索过程。例如，"代码库概览"技能可以描述项目架构、关键目录和命名规范。调用该技能时 Claude 立刻获得上下文，不用花 token 读多个文件来理解结构。

例如，这个 PreToolUse hook 可以过滤测试输出，只展示失败项：

### settings.json

把以下内容添加到 [settings.json](./settings#settings-files)，在每个 Bash 命令前运行 hook：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/filter-test-output.sh"
          }
        ]
      }
    ]
  }
}
```


### filter-test-output.sh

这个脚本检查命令是否是测试运行器，如果是就修改为只显示失败：

```bash
#!/bin/bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

# If running tests, filter to show only failures
if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
  filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
else
  echo "{}"
fi
```

### 把指令从 CLAUDE.md 移到技能中

[CLAUDE.md](./memory) 文件在会话开始时就会加载到上下文中。如果里面包含特定工作流的详细说明（如 PR 审查、数据库迁移），即使你在做不相关的工作，这些 token 也在消耗。[技能](./skills)是按需加载的，把专项指令转移到技能中可以缩小基础上下文。建议把 CLAUDE.md 控制在 500 行以内，只保留必要内容。

### 调整扩展思维

扩展思维默认开启，能显著提升复杂规划和推理任务的表现。思维 token 按输出 token 计费，默认预算可达每个请求数万 token。对于不需要深度推理的简单任务，可以用 `/effort` 或 `/model` 降低[工作量级别](./model-config#adjust-effort-level)、在 `/config` 中禁用思维，或用 `MAX_THINKING_TOKENS=8000` 降低预算来节省成本。

### 把高消耗操作委托给子 Agent

运行测试、获取文档或处理日志文件可能消耗大量上下文。把这些委托给[子 Agent](./sub-agents#isolate-high-volume-operations)，详细输出留在子 Agent 的上下文中，只有摘要返回到主对话。

### 管理 Agent Teams 成本

Agent Teams 在计划模式下运行时，token 用量约为标准会话的 7 倍，因为每个队友都维护独立的上下文窗口、作为独立的 Claude 实例运行。保持团队任务小而独立，以限制每个成员的 token 消耗。详见 [Agent Teams](./agent-teams)。

### 写具体的 prompt

模糊的请求如"改进这个代码库"会触发大范围扫描。具体的请求如"给 auth.ts 中的 login 函数添加输入验证"让 Claude 能以最少的文件读取高效完成工作。

### 高效完成复杂任务

对于较长或较复杂的工作，以下习惯有助于避免浪费 token 走弯路：

* **复杂任务用计划模式**：执行前按 Shift+Tab 进入[计划模式](./common-workflows#use-plan-mode-for-safe-code-analysis)。Claude 先探索代码库、提出方案供你审批，避免初始方向错误时的高成本返工。
* **尽早纠偏**：如果 Claude 方向不对，按 Escape 立即停止。用 `/rewind` 或双击 Escape 将对话和代码回退到之前的检查点。
* **给出验证目标**：附上测试用例、粘贴截图或在 prompt 中定义期望输出。Claude 能自我验证时，会在你需要修复前就发现问题。
* **增量测试**：写一个文件，测试，再继续。这样问题早发现，修复成本低。

## 后台 token 消耗

Claude Code 即使空闲时也会为某些后台功能消耗少量 token：

* **对话摘要**：后台任务，为 `claude --resume` 功能总结之前的对话
* **命令处理**：某些命令（如 `/cost`）可能生成状态检查请求

这些后台进程消耗的 token 很少（通常每会话低于 $0.04）。

## 了解 Claude Code 行为变化

Claude Code 会定期更新，可能改变功能行为，包括成本报告。运行 `claude --version` 检查当前版本。具体的计费问题请通过[Console 账户](https://platform.claude.com/login)联系 Anthropic 支持。团队部署建议先从小型试点组开始，建立使用模式后再大范围推广。
