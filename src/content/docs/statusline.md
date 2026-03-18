---
title: "自定义您的状态行"
order: 55
section: "configuration"
sectionLabel: "配置"
sectionOrder: 7
summary: "配置自定义状态栏以监控 Claude Code 中的上下文窗口使用情况、成本和 git 状态"
sourceUrl: "https://code.claude.com/docs/en/statusline.md"
sourceTitle: "Customize your status line"
tags: []
---
# 自定义你的状态行

> 配置自定义状态栏以监控 Claude Code 中的上下文窗口使用情况、成本和 git 状态

状态行是 Claude Code 底部的可自定义栏，可运行您配置的任何 shell 脚本。它在 stdin 上接收 JSON 会话数据并显示您的脚本打印的任何内容，为您提供上下文使用情况、成本、git 状态或您想要跟踪的任何其他内容的持久、一目了然的视图。

当您执行以下操作时，状态行非常有用：

* 希望在工作时监控上下文窗口的使用情况
* 需要跟踪会话成本
* 跨多个会话工作并需要区分它们
* 希望 git 分支和状态始终可见

下面是一个[多行状态行](#display-multiple-lines) 的示例，它在第一行显示 git 信息，在第二行显示颜色编码的上下文栏。

![多行状态行，第一行显示模型名称、目录、git 分支，第二行显示上下文使用进度条，显示成本和持续时间](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87)
本页将逐步介绍[设置基本状态行](#set-up-a-status-line)，解释[数据如何从 Claude Code 流向](#how-status-lines-work) 到您的脚本，列出[您可以显示的所有字段](#available-data)，并为 git 状态、成本跟踪和进度条等常见模式提供[即用示例](#examples)。

## 设置状态行

使用 [`/statusline` 命令](#use-the-statusline-command) 让 Claude Code 为您生成脚本，或[手动创建脚本](#manually-configure-a-status-line) 并将其添加到您的设置中。

### 使用 /statusline 命令

`/statusline` 命令接受描述您想要显示的内容的自然语言指令。 Claude Code 在 `~/.claude/` 中生成脚本文件并自动更新您的设置：

```text
/statusline show model name and context percentage with a progress bar
```

### 手动配置状态行

将 `statusLine` 字段添加到您的用户设置（`~/.claude/settings.json`，其中 `~` 是您的主目录）或 [项目设置](./settings#settings-files)。将 `type` 设置为 `"command"`，并将 `command` 指向脚本路径或内联 shell 命令。有关创建脚本的完整演练，请参阅[逐步构建状态行](#build-a-status-line-step-by-step)。

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

`command` 字段在 shell 中运行，因此您还可以使用内联命令而不是脚本文件。此示例使用 `jq` 解析 JSON 输入并显示模型名称和上下文百分比：

```json
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

可选的 `padding` 字段向状态行内容添加额外的水平间距（以字符为单位）。默认为 `0`。此填充是界面内置间距的补充，因此它控制相对缩进，而不是距终端边缘的绝对距离。

### 禁用状态行

运行 `/statusline` 并要求它删除或清除您的状态行（例如 `/statusline delete`、`/statusline clear`、`/statusline remove it`）。您还可以从 settings.json 中手动删除 `statusLine` 字段。

## 一步步构建状态行

本演练通过手动创建显示当前模型、工作目录和上下文窗口使用百分比的状态行来展示幕后发生的情况。

**注意**

运行 [`/statusline`](#use-the-statusline-command) 并描述您想要的内容，会自动为您配置所有这些。这些示例使用适用于 macOS 和 Linux 的 Bash 脚本。在 Windows 上，请参阅 [Windows 配置](#windows-configuration) 了解 PowerShell 和 Git Bash 示例。

![显示模型名称、目录和上下文百分比的状态行](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=696445e59ca0059213250651ad23db6b)

### 创建一个读取 JSON 并打印输出的脚本

Claude Code 通过标准输入将 JSON 数据发送到您的脚本。此脚本使用 [`jq`](https://jqlang.github.io/jq/)（您可能需要安装的命令行 JSON 解析器）来提取模型名称、目录和上下文百分比，然后打印格式化行。

将其保存到 `~/.claude/statusline.sh`（其中 `~` 是您的主目录，例如 macOS 上的 `/Users/username` 或 Linux 上的 `/home/username`）：

```bash
#!/bin/bash
# Read JSON data that Claude Code sends to stdin
input=$(cat)

# Extract fields using jq
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
# The "// 0" provides a fallback if the field is null
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Output the status line - ${DIR##*/} extracts just the folder name
echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
```

  
### 使其可执行

将脚本标记为可执行文件，以便您的 shell 可以运行它：

```bash
chmod +x ~/.claude/statusline.sh
```

  
### 添加到设置

告诉 Claude Code 将脚本作为状态行运行。将此配置添加到 `~/.claude/settings.json`，这会将 `type` 设置为 `"command"`（意思是“运行此 shell 命令”）并将 `command` 指向您的脚本：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

您的状态行显示在界面底部。设置会自动重新加载，但直到您下次与 PH​​X00207XHP 交互时才会显示更改。

## 状态行如何工作

Claude Code 运行您的脚本并通过标准输入将 [JSON 会话数据](#available-data) 传输到它。您的脚本读取 JSON，提取它需要的内容，并将文本打印到标准输出。 Claude Code 显示脚本打印的任何内容。

**什么时候更新**

当权限模式更改或 vim 模式切换时，您的脚本会在每条新的助理消息之后运行。更新在 300 毫秒时进行去抖，这意味着快速更改会一起批处理，一旦事情解决，您的脚本就会运行。如果在脚本仍在运行时触发新的更新，则正在进行的执行将被取消。如果您编辑脚本，则在您下次与 PH​​X00207XHP 交互触发更新之前，更改不会显示。

**您的脚本可以输出什么**

* **多行**：每个 `echo` 或 `print` 语句显示为单独的行。请参阅[多行示例](#display-multiple-lines)。
* **颜色**：使用 [ANSI 转义码](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)，例如 `\033[32m` 表示绿色（终端必须支持它们）。请参阅 [git 状态示例](#git-status-with-colors)。
* **链接**：使用 [OSC 8 转义序列](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC) 使文本可单击（Cmd+单击 macOS，Ctrl+单击 Windows/Linux）。需要支持 iTerm2、Kitty 或 WezTerm 等超链接的终端。请参阅[可点击链接示例](#clickable-links)。

**注意**

状态行在本地运行，不消耗 API 令牌。它在某些 UI 交互期间暂时隐藏，包括自动完成建议、帮助菜单和权限提示。

## 可用数据

Claude Code 通过 stdin 将以下 JSON 字段发送到您的脚本：|领域 |描述 |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `model.id`、`model.display_name` |当前型号标识符和显示名称 |
| `cwd`、`workspace.current_dir` |当前工作目录。两个字段包含相同的值；优先选择 `workspace.current_dir`，以与 `workspace.project_dir` 保持一致。                                            |
| `workspace.project_dir` | Claude Code 启动的目录，如果工作目录在会话期间发生更改，该目录可能与 `cwd` 不同 |
| `cost.total_cost_usd` |总会话费用（美元）|
| `cost.total_duration_ms` |自会话开始以来的总挂钟时间（以毫秒为单位）|
| `cost.total_api_duration_ms` |等待 API 响应所花费的总时间（以毫秒为单位）|
| `cost.total_lines_added`、`cost.total_lines_removed` |代码行已更改 |
| `context_window.total_input_tokens`、`context_window.total_output_tokens` |整个会话中的累积令牌计数 |
| `context_window.context_window_size` |最大上下文窗口大小（以标记为单位）。默认情况下为 200000，对于具有扩展上下文的模型为 1000000。                                                                                       |
| `context_window.used_percentage` |预先计算的上下文窗口使用百分比 || `context_window.remaining_percentage` |预先计算的上下文窗口剩余百分比 |
| `context_window.current_usage` |上次 API 调用的令牌计数，如 [上下文窗口字段](#context-window-fields) | 中所述
| `exceeds_200k_tokens` |最近 API 响应的总令牌计数（输入、缓存和输出令牌组合）是否超过 200k。无论实际上下文窗口大小如何，这都是一个固定阈值。 |
| `session_id` |唯一会话标识符 |
| `transcript_path` |对话记录文件的路径 |
| `version` | Claude Code版本|
| `output_style.name` |当前输出样式的名称 |
| `vim.mode` |启用 [vim 模式](./interactive-mode#vim-editor-mode) 时的当前 vim 模式（`NORMAL` 或 `INSERT`）|
| `agent.name` |使用 `--agent` 标志或配置的代理设置运行时的代理名称 |
| `worktree.name` |活动工作树的名称。仅在 `--worktree` 会话期间出现 |
| `worktree.path` |工作树目录的绝对路径 |
| `worktree.branch` |工作树的 Git 分支名称（例如 `"worktree-my-feature"`）。缺少基于钩子的工作树 || `worktree.original_cwd` |进入工作树之前目录 Claude 所在的位置 |
| `worktree.original_branch` | Git 分支在进入工作树之前签出。缺少基于钩子的工作树 |### 完整 JSON 架构

您的状态行命令通过 stdin 接收此 JSON 结构：

```json
{
  "cwd": "/current/working/directory",
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.jsonl",
  "model": {
    "id": "claude-opus-4-6",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  },
  "context_window": {
    "total_input_tokens": 15234,
    "total_output_tokens": 4521,
    "context_window_size": 200000,
    "used_percentage": 8,
    "remaining_percentage": 92,
    "current_usage": {
      "input_tokens": 8500,
      "output_tokens": 1200,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  },
  "exceeds_200k_tokens": false,
  "vim": {
    "mode": "NORMAL"
  },
  "agent": {
    "name": "security-reviewer"
  },
  "worktree": {
    "name": "my-feature",
    "path": "/path/to/.claude/worktrees/my-feature",
    "branch": "worktree-my-feature",
    "original_cwd": "/path/to/project",
    "original_branch": "main"
  }
}
```

**可能不存在的字段**（JSON 中不存在）：

* `vim`：仅在启用 vim 模式时出现
* `agent`：仅在使用 `--agent` 标志或配置的代理设置运行时出现
* `worktree`：仅在 `--worktree` 会话期间出现。如果存在，对于基于钩子的工作树，`branch` 和 `original_branch` 也可能不存在

**可能是 `null` 的字段**：

* `context_window.current_usage`：会话中第一次 API 调用之前的 `null`
* `context_window.used_percentage`、`context_window.remaining_percentage`：可能是会话早期的 `null`

使用条件访问处理缺失字段，并使用脚本中的后备默认值处理空值。

### 上下文窗口字段

`context_window` 对象提供了两种跟踪上下文使用情况的方法：

* **累计总数**（`total_input_tokens`、`total_output_tokens`）：整个会话中所有代币的总和，可用于跟踪总消耗
* **当前使用情况** (`current_usage`)：最近一次 API 调用的令牌计数，使用它来获得准确的上下文百分比，因为它反映了实际的上下文状态

`current_usage` 对象包含：

* `input_tokens`：当前上下文中的输入标记
* `output_tokens`：生成的输出令牌
* `cache_creation_input_tokens`：令牌写入缓存
* `cache_read_input_tokens`：从缓存读取令牌

`used_percentage` 字段仅根据输入标记计算：`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`。它不包括 `output_tokens`。

如果您根据 `current_usage` 手动计算上下文百分比，请使用相同的仅输入公式来匹配 `used_percentage`。

在会话中第一次 API 调用之前，`current_usage` 对象是 `null`。

## 示例

这些示例显示了常见的状态行模式。使用任何示例：

1. 将脚本保存到 `~/.claude/statusline.sh`（或 `.py`/`.js`）等文件中
2. 使其可执行：`chmod +x ~/.claude/statusline.sh`
3. 将路径添加到您的[设置](#manually-configure-a-status-line)

Bash 示例使用 [`jq`](https://jqlang.github.io/jq/) 来解析 JSON。 Python 和 Node.js 具有内置的 JSON 解析。

### 上下文窗口的使用

使用可视进度条显示当前模型和上下文窗口的使用情况。每个脚本从标准输入读取 JSON，提取 `used_percentage` 字段，并构建一个 10 个字符的栏，其中填充块 (▓) 代表用法：

![显示模型名称的状态行和带百分比的进度条](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=15b58ab3602f036939145dde3165c6f7)
```bash Bash
  #!/bin/bash
  # Read all of stdin into a variable
  input=$(cat)

  # Extract fields with jq, "// 0" provides fallback for null
  MODEL=$(echo "$input" | jq -r '.model.display_name')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

  # Build progress bar: printf -v creates a run of spaces, then
  # ${var// /▓} replaces each space with a block character
  BAR_WIDTH=10
  FILLED=$((PCT * BAR_WIDTH / 100))
  EMPTY=$((BAR_WIDTH - FILLED))
  BAR=""
  [ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
  [ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

  echo "[$MODEL] $BAR $PCT%"
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys

  # json.load reads and parses stdin in one step
  data = json.load(sys.stdin)
  model = data['model']['display_name']
  # "or 0" handles null values
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)

  # String multiplication builds the bar
  filled = pct * 10 // 100
  bar = '▓' * filled + '░' * (10 - filled)

  print(f"[{model}] {bar} {pct}%")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  // Node.js reads stdin asynchronously with events
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      // Optional chaining (?.) safely handles null fields
      const pct = Math.floor(data.context_window?.used_percentage || 0);

      // String.repeat() builds the bar
      const filled = Math.floor(pct * 10 / 100);
      const bar = '▓'.repeat(filled) + '░'.repeat(10 - filled);

      console.log(`[${model}] ${bar} ${pct}%`);
  });
  ```
### Git 状态与颜色

显示带有颜色编码指示器的 git 分支，用于暂存和修改的文件。此脚本使用 [ANSI 转义码](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) 作为终端颜色：`\033[32m` 为绿色，`\033[33m` 为黄色，`\033[0m` 重置为默认值。

![显示模型、目录、git 分支以及暂存和修改文件的彩色指示器的状态行](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e656f34f90d1d9a1d0e220988914345f)
每个脚本都会检查当前目录是否是 git 存储库，对暂存和修改的文件进行计数，并显示颜色编码的指示器：

```bash Bash
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  GREEN='\033[32m'
  YELLOW='\033[33m'
  RESET='\033[0m'

  if git rev-parse --git-dir > /dev/null 2>&1; then
      BRANCH=$(git branch --show-current 2>/dev/null)
      STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
      MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

      GIT_STATUS=""
      [ "$STAGED" -gt 0 ] && GIT_STATUS="${GREEN}+${STAGED}${RESET}"
      [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

      echo -e "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH $GIT_STATUS"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  GREEN, YELLOW, RESET = '\033[32m', '\033[33m', '\033[0m'

  try:
      subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
      staged_output = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
      modified_output = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
      staged = len(staged_output.split('\n')) if staged_output else 0
      modified = len(modified_output.split('\n')) if modified_output else 0

      git_status = f"{GREEN}+{staged}{RESET}" if staged else ""
      git_status += f"{YELLOW}~{modified}{RESET}" if modified else ""

      print(f"[{model}] 📁 {directory} | 🌿 {branch} {git_status}")
  except:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RESET = '\x1b[0m';

      try {
          execSync('git rev-parse --git-dir', { stdio: 'ignore' });
          const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
          const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
          const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;

          let gitStatus = staged ? `${GREEN}+${staged}${RESET}` : '';
          gitStatus += modified ? `${YELLOW}~${modified}${RESET}` : '';

          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} ${gitStatus}`);
      } catch {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
### 成本和持续时间跟踪跟踪您的会话的 API 成本和经过的时间。 `cost.total_cost_usd` 字段累计当前会话中所有 API 调用的成本。 `cost.total_duration_ms` 字段测量自会话开始以来的总运行时间，而 `cost.total_api_duration_ms` 仅跟踪等待 API 响应所花费的时间。

每个脚本将成本格式化为货币并将毫秒转换为分钟和秒：

![显示模型名称、会话成本和持续时间的状态行](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e3444a51fe6f3440c134bd5f1f08ad29)
```bash Bash
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  COST_FMT=$(printf '$%.2f' "$COST")
  DURATION_SEC=$((DURATION_MS / 1000))
  MINS=$((DURATION_SEC / 60))
  SECS=$((DURATION_SEC % 60))

  echo "[$MODEL] 💰 $COST_FMT | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  duration_sec = duration_ms // 1000
  mins, secs = duration_sec // 60, duration_sec % 60

  print(f"[{model}] 💰 ${cost:.2f} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const cost = data.cost?.total_cost_usd || 0;
      const durationMs = data.cost?.total_duration_ms || 0;

      const durationSec = Math.floor(durationMs / 1000);
      const mins = Math.floor(durationSec / 60);
      const secs = durationSec % 60;

      console.log(`[${model}] 💰 $${cost.toFixed(2)} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
### 显示多行

您的脚本可以输出多行以创建更丰富的显示。每个 `echo` 语句都会在状态区域中生成一个单独的行。

![多行状态行，第一行显示模型名称、目录、git 分支，第二行显示上下文使用进度条，显示成本和持续时间](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87)
此示例结合了多种技术：基于阈值的颜色（绿色低于 70%、黄色 70-89%、红色 90%+）、进度条和 git 分支信息。每个 `print` 或 `echo` 语句都会创建一个单独的行：

```bash Bash
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'

  # Pick bar color based on context usage
  if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
  elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
  else BAR_COLOR="$GREEN"; fi

  FILLED=$((PCT / 10)); EMPTY=$((10 - FILLED))
  printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
  BAR="${FILL// /█}${PAD// /░}"

  MINS=$((DURATION_MS / 60000)); SECS=$(((DURATION_MS % 60000) / 1000))

  BRANCH=""
  git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"

  echo -e "${CYAN}[$MODEL]${RESET} 📁 ${DIR##*/}$BRANCH"
  COST_FMT=$(printf '$%.2f' "$COST")
  echo -e "${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  CYAN, GREEN, YELLOW, RED, RESET = '\033[36m', '\033[32m', '\033[33m', '\033[31m', '\033[0m'

  bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
  filled = pct // 10
  bar = '█' * filled + '░' * (10 - filled)

  mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

  try:
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True, stderr=subprocess.DEVNULL).strip()
      branch = f" | 🌿 {branch}" if branch else ""
  except:
      branch = ""

  print(f"{CYAN}[{model}]{RESET} 📁 {directory}{branch}")
  print(f"{bar_color}{bar}{RESET} {pct}% | {YELLOW}${cost:.2f}{RESET} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);
      const cost = data.cost?.total_cost_usd || 0;
      const pct = Math.floor(data.context_window?.used_percentage || 0);
      const durationMs = data.cost?.total_duration_ms || 0;

      const CYAN = '\x1b[36m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m', RESET = '\x1b[0m';

      const barColor = pct >= 90 ? RED : pct >= 70 ? YELLOW : GREEN;
      const filled = Math.floor(pct / 10);
      const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);

      const mins = Math.floor(durationMs / 60000);
      const secs = Math.floor((durationMs % 60000) / 1000);

      let branch = '';
      try {
          branch = execSync('git branch --show-current', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          branch = branch ? ` | 🌿 ${branch}` : '';
      } catch {}

      console.log(`${CYAN}[${model}]${RESET} 📁 ${dir}${branch}`);
      console.log(`${barColor}${bar}${RESET} ${pct}% | ${YELLOW}$${cost.toFixed(2)}${RESET} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
### 可点击的链接

此示例创建一个指向 GitHub 存储库的可单击链接。它读取 git 远程 URL，使用 `sed` 将 SSH 格式转换为 HTTPS，并将存储库名称包装在 OSC 8 转义码中。按住 Cmd (macOS) 或 Ctrl (Windows/Linux) 并单击以在浏览器中打开链接。

![状态行显示指向 GitHub 存储库的可点击链接](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=4bcc6e7deb7cf52f41ab85a219b52661)
每个脚本都会获取 git 远程 URL，将 SSH 格式转换为 HTTPS，并将存储库名称包装在 OSC 8 转义码中。 Bash 版本使用 `printf '%b'`，它在不同 shell 中比 `echo -e` 更可靠地解释反斜杠转义：

```bash Bash
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')

  # Convert git SSH URL to HTTPS
  REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

  if [ -n "$REMOTE" ]; then
      REPO_NAME=$(basename "$REMOTE")
      # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
      # printf %b interprets escape sequences reliably across shells
      printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
  else
      echo "[$MODEL]"
  fi
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys, subprocess, re, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']

  # Get git remote URL
  try:
      remote = subprocess.check_output(
          ['git', 'remote', 'get-url', 'origin'],
          stderr=subprocess.DEVNULL, text=True
      ).strip()
      # Convert SSH to HTTPS format
      remote = re.sub(r'^git@github\.com:', 'https://github.com/', remote)
      remote = re.sub(r'\.git$', '', remote)
      repo_name = os.path.basename(remote)
      # OSC 8 escape sequences
      link = f"\033]8;;{remote}\a{repo_name}\033]8;;\a"
      print(f"[{model}] 🔗 {link}")
  except:
      print(f"[{model}]")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;

      try {
          let remote = execSync('git remote get-url origin', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          // Convert SSH to HTTPS format
          remote = remote.replace(/^git@github\.com:/, 'https://github.com/').replace(/\.git$/, '');
          const repoName = path.basename(remote);
          // OSC 8 escape sequences
          const link = `\x1b]8;;${remote}\x07${repoName}\x1b]8;;\x07`;
          console.log(`[${model}] 🔗 ${link}`);
      } catch {
          console.log(`[${model}]`);
      }
  });
  ```
### 缓存昂贵的操作

您的状态行脚本在活动会话期间频繁运行。 `git status` 或 `git diff` 等命令可能会很慢，尤其是在大型存储库中。此示例将 git 信息缓存到临时文件中，并且每 5 秒才刷新一次。

为缓存文件使用稳定、固定的文件名，例如 `/tmp/statusline-git-cache`。每个状态行调用都作为一个新进程运行，因此基于进程的标识符（例如 `$$`、`os.getpid()` 或 `process.pid`）每次都会生成不同的值，并且永远不会重用缓存。

每个脚本在运行 git 命令之前都会检查缓存文件是否丢失或早于 5 秒：

```bash Bash
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  CACHE_FILE="/tmp/statusline-git-cache"
  CACHE_MAX_AGE=5  # seconds

  cache_is_stale() {
      [ ! -f "$CACHE_FILE" ] || \
      # stat -f %m is macOS, stat -c %Y is Linux
      [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
  }

  if cache_is_stale; then
      if git rev-parse --git-dir > /dev/null 2>&1; then
          BRANCH=$(git branch --show-current 2>/dev/null)
          STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
          MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
          echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
      else
          echo "||" > "$CACHE_FILE"
      fi
  fi

  IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

  if [ -n "$BRANCH" ]; then
      echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python
  #!/usr/bin/env python3
  import json, sys, subprocess, os, time

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  CACHE_FILE = "/tmp/statusline-git-cache"
  CACHE_MAX_AGE = 5  # seconds

  def cache_is_stale():
      if not os.path.exists(CACHE_FILE):
          return True
      return time.time() - os.path.getmtime(CACHE_FILE) > CACHE_MAX_AGE

  if cache_is_stale():
      try:
          subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
          branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
          staged = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
          modified = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
          staged_count = len(staged.split('\n')) if staged else 0
          modified_count = len(modified.split('\n')) if modified else 0
          with open(CACHE_FILE, 'w') as f:
              f.write(f"{branch}|{staged_count}|{modified_count}")
      except:
          with open(CACHE_FILE, 'w') as f:
              f.write("||")

  with open(CACHE_FILE) as f:
      branch, staged, modified = f.read().strip().split('|')

  if branch:
      print(f"[{model}] 📁 {directory} | 🌿 {branch} +{staged} ~{modified}")
  else:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const fs = require('fs');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const CACHE_FILE = '/tmp/statusline-git-cache';
      const CACHE_MAX_AGE = 5; // seconds

      const cacheIsStale = () => {
          if (!fs.existsSync(CACHE_FILE)) return true;
          return (Date.now() / 1000) - fs.statSync(CACHE_FILE).mtimeMs / 1000 > CACHE_MAX_AGE;
      };

      if (cacheIsStale()) {
          try {
              execSync('git rev-parse --git-dir', { stdio: 'ignore' });
              const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
              const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              fs.writeFileSync(CACHE_FILE, `${branch}|${staged}|${modified}`);
          } catch {
              fs.writeFileSync(CACHE_FILE, '||');
          }
      }

      const [branch, staged, modified] = fs.readFileSync(CACHE_FILE, 'utf8').trim().split('|');

      if (branch) {
          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} +${staged} ~${modified}`);
      } else {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
### Windows 配置

在 Windows 上，Claude Code 通过 Git Bash 运行状态行命令。您可以从该 shell 调用 PowerShell：

```json settings.json
  {
    "statusLine": {
      "type": "command",
      "command": "powershell -NoProfile -File C:/Users/username/.claude/statusline.ps1"
    }
  }
  ```

  ```powershell statusline.ps1
  $input_json = $input | Out-String | ConvertFrom-Json
  $cwd = $input_json.cwd
  $model = $input_json.model.display_name
  $used = $input_json.context_window.used_percentage
  $dirname = Split-Path $cwd -Leaf

  if ($used) {
      Write-Host "$dirname [$model] ctx: $used%"
  } else {
      Write-Host "$dirname [$model]"
  }
  ```
或者直接运行 Bash 脚本：

```json settings.json
  {
    "statusLine": {
      "type": "command",
      "command": "~/.claude/statusline.sh"
    }
  }
  ```

  ```bash statusline.sh
  #!/usr/bin/env bash
  input=$(cat)
  cwd=$(echo "$input" | grep -o '"cwd":"[^"]*"' | cut -d'"' -f4)
  model=$(echo "$input" | grep -o '"display_name":"[^"]*"' | cut -d'"' -f4)
  dirname="${cwd##*[/\\]}"
  echo "$dirname [$model]"
  ```
## 提示

* **使用模拟输入进行测试**：`echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":25}}' | ./statusline.sh`
* **保持输出短**：状态栏的宽度有限，因此长输出可能会被截断或换行尴尬
* **缓存缓慢操作**：您的脚本在活动会话期间频繁运行，因此 `git status` 等命令可能会导致延迟。请参阅[缓存示例](#cache-expensive-operations) 了解如何处理此问题。

[ccstatusline](https://github.com/sirmalloc/ccstatusline) 和 [starship-claude](https://github.com/martinemde/starship-claude) 等社区项目提供带有主题和附加功能的预构建配置。## 故障排除

**状态行未出现**

* 验证您的脚本可执行：`chmod +x ~/.claude/statusline.sh`
* 检查您的脚本输出到 stdout，而不是 stderr
* 手动运行脚本以验证它是否产生输出
* 如果您的设置中将 `disableAllHooks` 设置为 `true`，则状态行也会被禁用。删除此设置或将其设置为 `false` 以重新启用。
* 运行 `claude --debug` 以记录会话中第一个状态行调用的退出代码和 stderr
* 要求 Claude 读取您的设置文件并直接执行 `statusLine` 命令以显示错误

**状态行显示 `--` 或空值**

* 在第一个 API 响应完成之前，字段可能是 `null`
* 使用后备处理脚本中的空值，例如 jq 中的 `// 0`
* 如果在多条消息后值仍为空，请重新启动 Claude Code

**上下文百分比显示意外值**

* 使用 `used_percentage` 获得准确的上下文状态而不是累积总数
* `total_input_tokens` 和 `total_output_tokens` 在会话期间累积，可能会超出上下文窗口大小
* 由于计算时间不同，上下文百分比可能与 `/context` 输出有所不同

**OSC 8 链接不可点击**

* 验证您的终端支持 OSC 8 超链接（iTerm2、Kitty、WezTerm）
* Terminal.app不支持可点击的链接
* SSH 和 tmux 会话可能会根据配置删除 OSC 序列
* 如果转义序列显示为 `\e]8;;` 等文字文本，请使用 `printf '%b'` 而不是 `echo -e` 以获得更可靠的转义处理

**显示带有转义序列的故障**

* 复杂的转义序列（ANSI 颜色、OSC 8 链接）如果与其他 UI 更新重叠，有时会导致乱码输出
* 如果您看到损坏的文本，请尝试将脚本简化为纯文本输出
* 带有转义码的多行状态行比单行纯文本更容易出现渲染问题

**脚本错误或挂起**

* 以非零代码退出或不产生输出的脚本会导致状态行变为空白
* 缓慢的脚本会阻止状态行更新，直到完成为止。保持脚本快速以避免输出过时。
* 如果在缓慢的脚本运行时触发新的更新，则正在运行的脚本将被取消
* 在配置脚本之前使用模拟输入独立测试您的脚本

**通知共享状态行行**

* MCP 服务器错误、自动更新和令牌警告等系统通知显示在状态行同一行的右侧
* 启用详细模式会向该区域添加令牌计数器
* 在窄终端上，这些通知可能会截断您的状态行输出
