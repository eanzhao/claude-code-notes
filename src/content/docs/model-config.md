---
title: "型号配置"
order: 52
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "了解 Claude Code 模型配置，包括 `opusplan` 等模型别名"
sourceUrl: "https://code.claude.com/docs/en/model-config.md"
sourceTitle: "Model configuration"
tags: []
---
# 模型配置

> 了解 Claude Code 模型配置，包括 `opusplan` 等模型别名

## 可用型号

对于 Claude Code 中的 `model` 设置，您可以配置：

* **模型别名**
* **型号名称**
  * Anthropic API：完整 **[型号名称](https://platform.claude.com/docs/en/about-claude/models/overview)**
  * Bedrock：推理配置文件 ARN
  * Foundry：部署名称
  * Vertex：版本名称

### 模型别名

模型别名提供了一种方便的方法来选择模型设置，而无需
记住确切的版本号：

|型号别名 |行为 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`default`** |推荐的模型设置，取决于您的帐户类型 |
| **`sonnet`** |使用最新的 Sonnet 模型（当前为 Sonnet 4.6）进行日常编码任务 |
| **`opus`** |使用最新的Opus模型（目前为Opus 4.6）进行复杂的推理任务 |
| **`haiku`** |使用快速高效的俳句模型来完成简单的任务 |
| **`sonnet[1m]`** |使用 Sonnet 和 [100 万个令牌上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) 进行长时间会话 |
| **`opus[1m]`** |使用带有 [100 万代币上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) 的 Opus 进行长时间会话 |
| **`opusplan`** |特殊模式，在计划模式下使用 `opus`，然后切换到 `sonnet` 执行 |

别名始终指向最新版本。要固定到特定版本，请使用完整的型号名称（例如 `claude-opus-4-6`）或设置相应的环境变量，例如 `ANTHROPIC_DEFAULT_OPUS_MODEL`。

### 设置你的模型

您可以通过多种方式配置模型，按优先级顺序列出：

1. **会话期间** - 使用 `/model <alias|name>` 在会话中切换模型
2. **启动时** - 使用 `claude --model <alias|name>` 启动
3. **环境变量** - 设置`ANTHROPIC_MODEL=<alias|name>`
4. **设置** - 使用 `model` 在设置文件中永久配置
   场。

用法示例：

```bash
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

设置文件示例：

```json
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## 限制模型选择

企业管理员可以在[托管或策略设置](./settings#settings-files) 中使用 `availableModels` 来限制用户可以选择的型号。

设置 `availableModels` 后，用户无法通过 `/model`、`--model` 标志、配置工具或 `ANTHROPIC_MODEL` 环境变量切换到不在列表中的型号。

```json
{
  "availableModels": ["sonnet", "haiku"]
}
```

### 默认模型行为模型选择器中的默认选项不受 `availableModels` 的影响。它始终保持可用，并代表系统的运行时默认值[基于用户的订阅层](#default-model-setting)。

即使使用 `availableModels: []`，用户仍然可以使用 Claude Code 及其级别的默认型号。

### 控制用户运行的模型

要完全控制模型体验，请将 `availableModels` 与 `model` 设置一起使用：

* **availableModels**：限制用户可以切换到的模型
* **model**：设置显式模型覆盖，优先于默认值

此示例确保所有用户都运行 Sonnet 4.6，并且只能在 Sonnet 和 Haiku 之间进行选择：

```json
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### 合并行为

当 `availableModels` 设置为多个级别（例如用户设置和项目设置）时，阵列将被合并和重复数据删除。要强制执行严格的白名单，请在具有最高优先级的托管或策略设置中设置 `availableModels`。

## 特殊模型行为

### `default` 型号设置

`default` 的行为取决于您的账户类型：

* **Max 和 Team Premium**：默认为 Opus 4.6
* **专业版和团队标准版**：默认为 Sonnet 4.6
* **企业版**：Opus 4.6 可用，但不是默认版本

如果您达到 Opus 的使用阈值，Claude Code 可能会自动回退到 Sonnet。

### `opusplan` 型号设置

`opusplan` 模型别名提供了一种自动化混合方法：

* **在计划模式** - 使用 `opus` 进行复杂的推理和架构
  决定
* **在执行模式** - 自动切换到 `sonnet` 进行代码生成
  和实施

这为您提供了两全其美的优势：Opus 卓越的规划推理能力，
以及十四行诗的执行效率。

### 调整努力程度

[努力程度](https://platform.claude.com/docs/en/build-with-claude/effort)控制自适应推理，根据任务复杂性动态分配思维。较低的努力对于简单的任务来说更快、更便宜，而较高的努力可以为复杂的问题提供更深入的推理。

会话中存在三个级别：**低**、**中**和**高**。第四个级别，**max**，提供最深入的推理，对代币支出没有限制，因此响应速度较慢且成本比 `high` 更高。 `max` 仅在 Opus 4.6 上可用，并且适用于当前会话而不持续。 Opus 4.6 默认为 Max 和 Team 订阅者提供中等工作量。

**设置力度：**

* **`/effort`**：运行 `/effort low`、`/effort medium`、`/effort high` 或 `/effort max` 更改级别，或运行 `/effort auto` 重置为模型默认值
* **在 `/model`** 中：选择模型时使用左/右箭头键调整力度滑块
* **`--effort` 标志**：传递 `low`、`medium`、`high` 或 `max` 来设置启动 Claude Code 时单个会话的级别
* **环境变量**：将 `CLAUDE_CODE_EFFORT_LEVEL` 设置为 `low`、`medium`、`high`、`max` 或 `auto`
* **设置**：将设置文件中的 `effortLevel` 设置为 `"low"`、`"medium"` 或 `"high"`

环境变量优先，然后是您配置的级别，然后是模型默认值。Opus 4.6 和 Sonnet 4.6 支持 Effort。选择支持的模型后，工作量滑块会出现在 `/model` 中。当前的工作量级别还会显示在徽标和微调器旁边，例如“低工作量”，因此您无需打开 `/model` 即可确认哪个设置处于活动状态。

要禁用 Opus 4.6 和 Sonnet 4.6 上的自适应推理并恢复到之前的固定思维预算，请设置 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`。禁用时，这些模型使用由 `MAX_THINKING_TOKENS` 控制的固定预算。请参阅[环境变量](./env-vars)。

### 扩展上下文

Opus 4.6 和 Sonnet 4.6 支持 [100 万个令牌上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)，用于具有大型代码库的长时间会话。

可用性因型号和计划而异。在 Max、Team 和 Enterprise 计划中，Opus 会自动升级到 1M 上下文，无需额外配置。这适用于团队标准席位和团队高级席位。

|计划| Opus 4.6 具有 1M 上下文 |具有 1M 上下文的 Sonnet 4.6 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Max、团队和企业 |包含在订阅中 |需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
|专业|需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API 和按需付费 |完全访问 |完全访问 |

要完全禁用 1M 上下文，请设置 `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`。这将从模型选择器中删除 100 万个模型变体。请参阅[环境变量](./env-vars)。

1M 上下文窗口使用标准模型定价，超过 200K 的代币没有溢价。对于您的订阅中包含扩展上下文的计划，您的订阅仍涵盖使用情况。对于通过额外使用访问扩展上下文的计划，令牌按额外使用计费。

如果您的帐户支持 1M 上下文，该选项将显示在最新版本 Claude Code 的模型选择器 (`/model`) 中。如果您没有看到它，请尝试重新启动会话。

您还可以将 `[1m]` 后缀与型号别名或完整型号名称一起使用：

```bash
# Use the opus[1m] or sonnet[1m] alias
/model opus[1m]
/model sonnet[1m]

# Or append [1m] to a full model name
/model claude-opus-4-6[1m]
```

## 检查您当前的型号

您可以通过多种方式查看当前正在使用的型号：

1. 在[状态行](./statusline)中（如果已配置）
2. 在`/status`中，它还显示您的帐户信息。

## 环境变量

可以使用以下环境变量，必须是完整的**model
名称**（或 API 提供商的等效项），用于控制别名映射到的模型名称。|环境变量 |描述 |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` |用于 `opus` 的型号，或当 Plan Mode 处于活动状态时用于 `opusplan` 的型号。                      |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` |用于 `sonnet` 的型号，或者当 Plan Mode 未激活时用于 `opusplan` 的型号。                |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` |用于 `haiku` 的型号，或[后台功能](./costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL` |用于[子代理](./sub-agents) 的模型 |

注意：`ANTHROPIC_SMALL_FAST_MODEL` 已弃用，取而代之
`ANTHROPIC_DEFAULT_HAIKU_MODEL`。

### 第三方部署的引脚模型

通过 [Bedrock](./amazon-bedrock)、[Vertex AI](./google-vertex-ai) 或 [Foundry](./microsoft-foundry) 部署 Claude Code 时，请在向用户推出之前固定模型版本。

如果没有固定，Claude Code 使用解析为最新版本的模型别名（`sonnet`、`opus`、`haiku`）。当Anthropic发布新型号时，未启用新版本的帐户的用户将悄然崩溃。

**警告**

作为初始设置的一部分，将所有三个模型环境变量设置为特定版本 ID。跳过此步骤意味着 Claude Code 更新可能会破坏您的用户，而无需您采取任何操作。

将以下环境变量与您的提供商的特定于版本的模型 ID 结合使用：

|供应商|示例|
| :-------- | :---------------------------------------------------------------------- |
|基岩| `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
|顶点人工智能 | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'` |
|铸造 | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'` |

对 `ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 应用相同的图案。有关所有提供商的当前和旧模型 ID，请参阅[模型概述](https://platform.claude.com/docs/en/about-claude/models/overview)。要将用户升级到新的模型版本，请更新这些环境变量并重新部署。

要为固定模型启用 [扩展上下文](#extended-context)，请将 `[1m]` 附加到 `ANTHROPIC_DEFAULT_OPUS_MODEL` 或 `ANTHROPIC_DEFAULT_SONNET_MODEL` 中的模型 ID：

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

`[1m]` 后缀将 1M 上下文窗口应用于该别名的所有使用，包括 `opusplan`。 Claude Code 在将型号 ID 发送给您的提供商之前会去除后缀。仅当底层模型支持 1M 上下文（例如 Opus 4.6 或 Sonnet 4.6）时才附加 `[1m]`。

**注意**

使用第三方提供商时，`settings.availableModels` 许可名单仍然适用。过滤模型别名（`opus`、`sonnet`、`haiku`）的匹配项，而不是特定于提供商的模型 ID。

### 覆盖每个版本的模型 ID

上面的系列级别环境变量为每个系列别名配置一个模型 ID。如果您需要将同一系列中的多个版本映射到不同的提供商 ID，请改用 `modelOverrides` 设置。

`modelOverrides` 将各个 Anthropic 型号 ID 映射到 Claude Code 发送到提供商 API 的提供商特定字符串。当用户在 `/model` 选择器中选择映射模型时，Claude Code 将使用您配置的值而不是内置默认值。这使得企业管理员可以将每个模型版本路由到特定的 Bedrock 推理配置文件 ARN、Vertex AI 版本名称或 Foundry 部署名称，以进行治理、成本分配或区域路由。

在您的[设置文件](./settings#settings-files)中设置`modelOverrides`：

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

密钥必须是[型号概述](https://platform.claude.com/docs/en/about-claude/models/overview)中列出的 Anthropic 型号 ID。对于注明日期的型号 ID，请完全包含其中显示的日期后缀。未知的键将被忽略。

覆盖替换了支持 `/model` 选择器中每个条目的内置模型 ID。在 Bedrock 上，覆盖优先于 Claude Code 在启动时自动发现的任何推理配置文件。您直接通过 `ANTHROPIC_MODEL`、`--model` 或 `ANTHROPIC_DEFAULT_*_MODEL` 环境变量提供的值将按原样传递给提供程序，并且不会由 `modelOverrides` 进行转换。

`modelOverrides` 与 `availableModels` 一起使用。允许列表是根据 Anthropic 模型 ID（而不是覆盖值）进行评估的，因此即使 Opus 版本映射到 ARN，`availableModels` 中的 `"opus"` 之类的条目也会继续匹配。

### 提示缓存配置

Claude Code 自动使用[提示缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 来优化性能并降低成本。您可以全局或特定模型层禁用提示缓存：

|环境变量 |描述 |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING` |设置为 `1` 以禁用所有模型的提示缓存（优先于每个模型的设置）|
| `DISABLE_PROMPT_CACHING_HAIKU` |设置为 `1` 以仅对 Haiku 模型禁用提示缓存 |
| `DISABLE_PROMPT_CACHING_SONNET` |设置为 `1` 仅对 Sonnet 型号禁用提示缓存 |
| `DISABLE_PROMPT_CACHING_OPUS` |设置为 `1` 仅针对 Opus 型号禁用提示缓存 |

这些环境变量使您可以对提示缓存行为进行细粒度控制。全局 `DISABLE_PROMPT_CACHING` 设置优先于特定于型号的设置，允许您在需要时快速禁用所有缓存。每个模型的设置对于选择性控制很有用，例如在调试特定模型或与可能具有不同缓存实现的云提供商合作时。
