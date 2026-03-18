---
title: "语音听写"
order: 54
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "使用一键通语音听写说出提示，而不是在 Claude Code CLI 中键入提示。"
sourceUrl: "https://code.claude.com/docs/en/voice-dictation.md"
sourceTitle: "Voice dictation"
tags: []
---
# 语音听写

> 使用一键通语音听写说出提示，而不是在 Claude Code CLI 中键入提示。

按住按键并说话来听写提示。您的语音会实时转录到提示输入中，因此您可以在同一条消息中混合语音和打字。使用 `/voice` 启用听写。默认一键通键为 `Space`； [重新绑定到修饰符组合](#rebind-the-push-to-talk-key) 在第一次按键时激活，而不是短暂按住后激活。

**注意**

语音听写需要 Claude Code v2.1.69 或更高版本。使用 `claude --version` 检查您的版本。

## 要求

语音听写使用流式语音转文本服务，该服务仅在您使用 Claude.ai 帐户进行身份验证时可用。当 Claude Code 配置为直接使用 Anthropic API 密钥、Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 时，该功能不可用。

语音听写还需要本地麦克风访问，因此它不适用于远程环境，例如 [网络上的 Claude Code](./claude-code-on-the-web) 或 SSH 会话。在 WSL 中，语音听写需要 WSLg 进行音频访问，该功能包含在 Windows 11 上的 WSL2 中。在 Windows 10 或 WSL1 上，请改为在本机 Windows 中运行 Claude Code。

音频录制使用 macOS、Linux 和 Windows 上的内置本机模块。在 Linux 上，如果本机模块无法加载，Claude Code 将回退到 ALSA utils 中的 `arecord` 或 SoX 中的 `rec`。如果两者都不可用，`/voice` 会打印包管理器的安装命令。

## 启用语音听写

运行 `/voice` 以打开语音听写。第一次启用它时，Claude Code 会运行麦克风检查。在 macOS 上，如果从未授予终端麦克风权限，则会触发系统麦克风权限提示。

```
/voice
Voice mode enabled. Hold Space to record. Dictation language: en (/config to change).
```

语音听写在整个会话中持续存在。再次运行 `/voice` 将其关闭，或直接在您的[用户设置文件](./settings)中设置：

```json
{
  "voiceEnabled": true
}
```

启用语音听写后，当提示为空时，输入页脚会显示 `hold Space to speak` 提示。如果您配置了[自定义状态行](./statusline)，则不会出现提示。

## 记录提示

按住 `Space` 开始录音。 Claude Code 通过观察终端上的快速按键重复事件来检测按住的按键，因此在录制开始之前会有短暂的预热。页脚在预热期间显示 `keep holding…`，然后在记录激活后切换到实时波形。

前几个按键重复字符在预热期间输入到输入中，并在录音激活时自动删除。单个 `Space` 敲击仍会键入空格，因为保持检测仅在快速重复时触发。

**提示**

要跳过预热，请[重新绑定到修改器组合](#rebind-the-push-to-talk-key)，例如 `meta+k`。修改器组合在第一次按键时开始记录。当您说话时，您的演讲会出现在提示中，在文字记录完成之前会变暗。释放 `Space` 以停止录制并完成文本。文字记录将插入到您的光标位置，并且光​​标停留在插入文本的末尾，因此您可以按任何顺序混合打字和听写。再次按住 `Space` 可附加另一个录音，或先移动光标以在提示中的其他位置插入语音：

```
> refactor the auth middleware to ▮
  # hold Space, speak "use the new token validation helper"
> refactor the auth middleware to use the new token validation helper▮
```

转录针对编码词汇进行了调整。可以正确识别 `regex`、`OAuth`、`JSON` 和 `localhost` 等常见开发术语，并自动添加您当前的项目名称和 git 分支名称作为识别提示。

## 更改听写语言

语音听写使用与控制 Claude 的响应语言相同的 [`language` 设置](./settings)。如果该设置为空，则听写默认为英语。

### 支持的听写语言

|语言 |代码|
| :--------- | :--- |
|捷克语 | `cs` |
|丹麦语 | `da` |
|荷兰语 | `nl` |
|英语 | `en` |
|法语 | `fr` |
|德语 | `de` |
|希腊语 | `el` |
|印地语 | `hi` |
|印度尼西亚语 | `id` |
|意大利语 | `it` |
|日语 | `ja` |
|韩语 | `ko` |
|挪威语 | `no` |
|波兰语 | `pl` |
|葡萄牙语 | `pt` |
|俄语 | `ru` |
|西班牙语 | `es` |
|瑞典语 | `sv` |
|土耳其语 | `tr` |
|乌克兰语 | `uk` |

在 `/config` 中或直接在设置中设置语言。您可以使用 [BCP 47 语言代码](https://en.wikipedia.org/wiki/IETF_language_tag) 或语言名称：

```json
{
  "language": "japanese"
}
```

如果您的 `language` 设置不在受支持的列表中，`/voice` 会在启用时向您发出警告，并退回到英语进行听写。 Claude 的文本响应不受此回退的影响。

## 重新绑定一键通键

一键通密钥绑定到 `Chat` 上下文中的 `voice:pushToTalk`，默认为 `Space`。在 [`~/.claude/keybindings.json`](./keybindings) 中重新绑定它：

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "meta+k": "voice:pushToTalk",
        "space": null
      }
    }
  ]
}
```

设置 `"space": null` 将删除默认绑定。如果您希望两个键都处于活动状态，请忽略它。

由于保持检测依赖于按键重复，因此请避免绑定像 `v` 这样的裸字母键，因为它会在预热期间输入提示。使用 `Space`，或使用 `meta+k` 等修饰符组合在第一次按键时开始录制，无需预热。有关完整的键绑定语法，请参阅[自定义键盘快捷键](./keybindings)。

## 故障排除

语音听写无法激活或录制时的常见问题：* **`Voice mode requires a Claude.ai account`**：您已通过 API 密钥或第三方提供商进行身份验证。运行 `/login` 以使用 Claude.ai 帐户登录。
* **`Microphone access is denied`**：在系统设置中授予您的终端麦克风权限。在 macOS 上，转至系统设置 → 隐私和安全 → 麦克风。在 Windows 上，转至设置 → 隐私 → 麦克风。然后再次运行 `/voice`。
* **Linux 上的 `No audio recording tool found`**：本机音频模块无法加载并且未安装回退。使用错误消息中显示的命令安装 SoX，例如 `sudo apt-get install sox`。
* **按住 `Space` 时没有任何反应**：按住时观察提示输入。如果空格不断累积，语音听写就会关闭；运行 `/voice` 来启用它。如果只出现一两个空格，然后什么也没有出现，则语音听写已开启，但保持检测未触发。保持检测要求您的终端发送按键重复事件，因此如果在操作系统级别禁用按键重复，则它无法检测保持的按键。
* **转录出现乱码或语言错误**：听写默认为英语。如果您使用其他语言听写，请先将其设置为 `/config`。请参阅[更改听写语言](#change-the-dictation-language)。

## 另请参阅

* [自定义键盘快捷键](./keybindings)：重新绑定 `voice:pushToTalk` 和其他 CLI 键盘操作
* [配置设置](./settings)：`voiceEnabled`、`language` 和其他设置键的完整参考
* [交互模式](./interactive-mode)：键盘快捷键、输入模式和会话控制
* [内置命令](./commands)：参考 `/voice`、`/config` 和所有其他命令
