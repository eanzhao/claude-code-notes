---
title: "自定义键盘快捷键"
order: 56
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "使用键绑定配置文件自定义 Claude Code 中的键盘快捷键。"
sourceUrl: "https://code.claude.com/docs/en/keybindings.md"
sourceTitle: "Customize keyboard shortcuts"
tags: []
---
# 自定义键盘快捷键

> 使用键绑定配置文件自定义 Claude Code 中的键盘快捷键。

**注意**

可自定义的键盘快捷键需要 Claude Code v2.1.18 或更高版本。使用 `claude --version` 检查您的版本。

Claude Code 支持自定义键盘快捷键。运行 `/keybindings` 以创建或打开位于 `~/.claude/keybindings.json` 的配置文件。

## 配置文件

键绑定配置文件是一个带有 `bindings` 数组的对象。每个块指定一个上下文以及击键到操作的映射。

**注意**

系统会自动检测并应用对键绑定文件的更改，而无需重新启动 Claude Code。

|领域 |描述 |
| :--------- | :------------------------------------------------- |
| `$schema` |用于编辑器自动完成的可选 JSON 架构 URL |
| `$docs` |可选文档 URL |
| `bindings` |按上下文排列的绑定块数组 |

此示例绑定 `Ctrl+E` 以在聊天上下文中打开外部编辑器，并取消绑定 `Ctrl+U`：

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## 上下文

每个绑定块指定一个绑定应用的**上下文**：

|背景 |描述 |
| :---------------- | :------------------------------------------------------------ |
| `Global` |适用于应用程序中的任何地方 |
| `Chat` |主聊天输入区|
| `Autocomplete` |自动完成菜单已打开 |
| `Settings` |设置菜单（仅退出关闭）|
| `Confirmation` |许可和确认对话框 |
| `Tabs` |标签导航组件 |
| `Help` |帮助菜单可见 |
| `Transcript` |成绩单查看器 |
| `HistorySearch` |历史搜索模式 (Ctrl+R) |
| `Task` |后台任务正在运行 |
| `ThemePicker` |主题选择器对话框 |
| `Attachments` |图片/附件栏导航 |
| `Footer` |页脚指示器导航（任务、团队、差异）|
| `MessageSelector` |倒回并总结对话框消息选择 |
| `DiffDialog` |差异查看器导航 |
| `ModelPicker` |模型选择器工作量 |
| `Select` |通用选择/列表组件 |
| `Plugin` |插件对话框（浏览、发现、管理）|

## 可用的操作

操作遵循 `namespace:action` 格式，例如 `chat:submit` 用于发送消息或 `app:toggleTodos` 用于显示任务列表。每个上下文都有可用的特定操作。

### 应用程序操作

`Global` 上下文中可用的操作：|行动|默认 |描述 |
| :-------------------- | :------ | :-------------------------- |
| `app:interrupt` | Ctrl+C |取消当前操作 |
| `app:exit` | Ctrl+D |退出 Claude Code |
| `app:toggleTodos` | Ctrl+T |切换任务列表可见性 |
| `app:toggleTranscript` | Ctrl+O |切换详细记录 |

### 历史动作

用于导航命令历史记录的操作：

|行动|默认 |描述 |
| ：------------------ | :------ | :-------------------- |
| `history:search` | Ctrl+R |打开历史搜索 |
| `history:previous` |上 |上一个历史项目 |
| `history:next` |向下|下一个历史项目 |

### 聊天操作

`Chat` 上下文中可用的操作：

|行动|默认 |描述 |
| :-------------------- | :------------------------ | :------------------------ |
| `chat:cancel` |逃亡|取消当前输入 |
| `chat:cycleMode` | Shift+Tab\* |循环权限模式 |
| `chat:modelPicker` | Cmd+P / 元+P |打开模型选择器 |
| `chat:thinkingToggle` | Cmd+T / 元+T |切换扩展思维 |
| `chat:submit` |输入 |提交留言 |
| `chat:undo` | Ctrl+\_ |撤消上一个操作 |
| `chat:externalEditor` | Ctrl+G |在外部编辑器中打开 |
| `chat:stash` | Ctrl+S |隐藏当前提示 |
| `chat:imagePaste` | Ctrl+V（Windows 上为 Alt+V）|粘贴图像 |

\*在没有 VT 模式的 Windows 上（Node \<24.2.0/\<22.17.0，Bun \<1.2.23），默认为 Meta+M。

### 自动完成操作

`Autocomplete` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------------- | :------ | :------------------ |
| `autocomplete:accept` |选项卡|接受建议 |
| `autocomplete:dismiss` |逃亡|关闭菜单 |
| `autocomplete:previous` |上 |上一个建议 |
| `autocomplete:next` |向下|下一个建议 |

### 确认动作

`Confirmation` 上下文中可用的操作：

|行动|默认|描述 |
| :-------------------------- | :-------- | :---------------------------- |
| `confirm:yes` |是，输入 |确认行动 |
| `confirm:no` | N，逃脱|拒绝行动 |
| `confirm:previous` |上 |上一个选项 |
| `confirm:next` |向下|下一个选项 |
| `confirm:nextField` |选项卡|下一个字段 |
| `confirm:previousField` | （不受约束）|上一个字段 |
| `confirm:cycleMode` | Shift+Tab |循环权限模式 |
| `confirm:toggleExplanation` | Ctrl+E |切换权限说明 |

### 权限操作

`Confirmation` 上下文中可用于权限对话框的操作：

|行动|默认 |描述 |
| :------------------------ | :------ | :---------------------------- |
| `permission:toggleDebug` | Ctrl+D |切换权限调试信息 |### 记录动作

`Transcript` 上下文中可用的操作：

|行动|默认 |描述 |
| ：-------------------------- | :------------- | :---------------------- |
| `transcript:toggleShowAll` | Ctrl+E |切换显示所有内容 |
| `transcript:exit` | Ctrl+C，退出 |退出成绩单视图 |

### 历史搜索操作

`HistorySearch` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------------- | :---------- | :------------------------ |
| `historySearch:next` | Ctrl+R |下一场比赛 |
| `historySearch:accept` |逃脱，选项卡|接受选择 |
| `historySearch:cancel` | Ctrl+C |取消搜索 |
| `historySearch:execute` |输入 |执行选定的命令 |

### 任务动作

`Task` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------- | :------ | :---------------------- |
| `task:background` | Ctrl+B |后台当前任务 |

### 主题动作

`ThemePicker` 上下文中可用的操作：

|行动|默认 |描述 |
| :-------------------------------- | :------ | ：-------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T |切换语法高亮|

### 帮助操作

`Help` 上下文中可用的操作：

|行动|默认 |描述 |
| :------------- | :------ | :-------------- |
| `help:dismiss` |逃亡|关闭帮助菜单 |

### 选项卡操作

`Tabs` 上下文中可用的操作：

|行动|默认 |描述 |
| :-------------- | :-------------- | ：---------- |
| `tabs:next` |选项卡，右 |下一个选项卡 |
| `tabs:previous` | Shift+Tab，向左|上一个选项卡 |

### 附件操作

`Attachments` 上下文中可用的操作：

|行动|默认 |描述 |
| :-------------------- | :---------------- | ：-------------------------- |
| `attachments:next` |对|下一个附件 |
| `attachments:previous` |左|上一个附件 |
| `attachments:remove` |退格键、删除 |删除选定的附件 |
| `attachments:exit` |下来，逃脱|退出附件栏 |

### 页脚操作

`Footer` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------------- | :------ | :------------------------ |
| `footer:next` |对|下一个页脚项目 |
| `footer:previous` |左|上一个页脚项目 |
| `footer:openSelected` |输入 |打开选定的页脚项目 |
| `footer:clearSelection` |逃亡|清除页脚选择 |

### 消息选择器操作

`MessageSelector` 上下文中可用的操作：|行动|默认 |描述 |
| :------------------------ | :---------------------------------------- | :---------------- |
| `messageSelector:up` |向上、K、Ctrl+P |在列表中上移 |
| `messageSelector:down` |向下，J，Ctrl+N |在列表中下移 |
| `messageSelector:top` | Ctrl+向上、Shift+向上、Meta+向上、Shift+K |跳转至顶部 |
| `messageSelector:bottom` | Ctrl+向下、Shift+向下、元+向下、Shift+J |跳转至底部 |
| `messageSelector:select` |输入|选择留言 |

### 差异动作

`DiffDialog` 上下文中可用的操作：

|行动|默认|描述 |
| :-------------------- | ：------------------ | :-------------------- |
| `diff:dismiss` |逃亡|关闭差异查看器 |
| `diff:previousSource` |左|上一个 diff 源 |
| `diff:nextSource` |对|下一个差异源 |
| `diff:previousFile` |上 | diff 中的上一个文件 |
| `diff:nextFile` |向下| diff 中的下一个文件 |
| `diff:viewDetails` |输入 |查看差异详细信息 |
| `diff:back` | （具体情况）|返回差异查看器 |

### 模型选择器操作

`ModelPicker` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------------------- | :------ | :-------------------- |
| `modelPicker:decreaseEffort` |左|减少努力水平 |
| `modelPicker:increaseEffort` |对|增加努力水平|

### 选择操作

`Select` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------- | :-------------- | ：-------------- |
| `select:next` |向下，J，Ctrl+N |下一个选项 |
| `select:previous` |向上、K、Ctrl+P |上一个选项 |
| `select:accept` |输入 |接受选择 |
| `select:cancel` |逃亡|取消选择 |

### 插件操作

`Plugin` 上下文中可用的操作：

|行动|默认 |描述 |
| ：-------------- | :------ | :------------------------ |
| `plugin:toggle` |空间|切换插件选择 |
| `plugin:install` |我|安装选定的插件 |

### 设置操作

`Settings` 上下文中可用的操作：

|行动|默认 |描述 |
| :---------------- | :------ | :---------------------------------- |
| `settings:search` | / |进入搜索模式 |
| `settings:retry` |右 |重试加载使用数据（出错时）|

### 语音动作

启用 [语音听写](./voice-dictation) 时，`Chat` 上下文中可用的操作：

|行动|默认 |描述 |
| ：------------------ | :------ | :------------------------ |
| `voice:pushToTalk` |空间|按住可听写提示 |

## 按键语法

### 修饰符

使用带有 `+` 分隔符的修饰键：

* `ctrl` 或 `control` - 控制键
* `alt`、`opt` 或 `option` - Alt/Option 键
* `shift` - Shift 键
* `meta`、`cmd` 或 `command` - 元/命令键

例如：```text 
ctrl+k          Single key with modifier
shift+tab       Shift + Tab
meta+p          Command/Meta + P
ctrl+shift+c    Multiple modifiers
```

### 大写字母

独立的大写字母表示 Shift。例如，`K` 相当于 `shift+k`。这对于 vim 样式的绑定很有用，其中大写和小写键具有不同的含义。

带修饰符的大写字母（例如 `ctrl+K`）被视为风格，并不意味着 Shift — `ctrl+K` 与 `ctrl+k` 相同。

### 和弦

和弦是由空格分隔的击键序列：

```text
ctrl+k ctrl+s   Press Ctrl+K, release, then Ctrl+S
```

### 特殊键

* `escape` 或 `esc` - 退出键
* `enter` 或 `return` - 输入键
* `tab` - Tab 键
* `space` - 空格键
* `up`、`down`、`left`、`right` - 箭头键
* `backspace`、`delete` - 删除键

## 解除默认快捷键的绑定

将操作设置为 `null` 以取消绑定默认快捷方式：

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

## 保留的快捷键

这些快捷键不能被反弹：

|快捷方式|原因 |
| :----- | ：-------------------------- |
| Ctrl+C |硬编码中断/取消|
| Ctrl+D |硬编码退出 |

## 终端冲突

一些快捷方式可能与终端多路复用器冲突：

|快捷方式|冲突|
| :----- | :-------------------------------- |
| Ctrl+B | tmux 前缀（按两次发送）|
| Ctrl+A | GNU 屏幕前缀 |
| Ctrl+Z | Unix 进程挂起 (SIGTSTP) |

## Vim 模式交互

启用 vim 模式 (`/vim`) 时，按键绑定和 vim 模式独立运行：

* **Vim 模式** 处理文本输入级别的输入（光标移动、模式、动作）
* **按键绑定** 处理组件级别的操作（切换待办事项、提交等）
* vim模式下的Escape键切换INSERT到NORMAL模式；它不会触发 `chat:cancel`
* 大多数 Ctrl+快捷键通过 vim 模式传递到键绑定系统
* 在 vim NORMAL 模式下，`?` 显示帮助菜单（vim 行为）

## 验证

Claude Code 验证您的键绑定并显示以下警告：

* 解析错误（无效的 JSON 或结构）
* 无效的上下文名称
* 预留快捷键冲突
* 终端多路复用器冲突
* 同一上下文中的重复绑定

运行 `/doctor` 以查看任何键绑定警告。
