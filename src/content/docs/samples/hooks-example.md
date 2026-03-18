# Hooks 示例

Claude Code Hooks 允许你在特定事件发生时自动执行脚本。

## 配置位置

在 `settings.json` 中配置 hooks：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/pre-bash.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command", 
            "command": "~/.claude/hooks/post-edit.sh"
          }
        ]
      }
    ]
  }
}
```

## 示例 Hooks

### 1. 阻止危险命令 (PreToolUse)

```bash
#!/bin/bash
# ~/.claude/hooks/block-dangerous.sh

# 从 stdin 读取 JSON 输入
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# 检查危险命令
if echo "$command" | grep -qE '(rm -rf /|rm -rf \*|>:/)'; then
  echo '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Dangerous command blocked by hook"
    }
  }'
  exit 0
fi

# 允许命令继续
echo '{}'
```

### 2. 编辑后自动格式化 (PostToolUse)

```bash
#!/bin/bash
# ~/.claude/hooks/auto-format.sh

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# 检查文件类型并相应格式化
case "$file_path" in
  *.js|*.ts|*.jsx|*.tsx)
    if command -v prettier &> /dev/null; then
      prettier --write "$file_path" 2>/dev/null
    fi
    ;;
  *.py)
    if command -v black &> /dev/null; then
      black "$file_path" 2>/dev/null
    fi
    ;;
  *.go)
    if command -v gofmt &> /dev/null; then
      gofmt -w "$file_path" 2>/dev/null
    fi
    ;;
esac

echo '{}'
```

### 3. 记录命令使用日志

```bash
#!/bin/bash
# ~/.claude/hooks/log-commands.sh

input=$(cat)
event_name=$(echo "$input" | jq -r '.hook_event_name')
tool_name=$(echo "$input" | jq -r '.tool_name')

# 记录到日志文件
log_file="$HOME/.claude/logs/tool-usage.log"
mkdir -p "$(dirname "$log_file")"

echo "$(date '+%Y-%m-%d %H:%M:%S') - $event_name: $tool_name" >> "$log_file"

echo '{}'
```

### 4. Session 开始时检查环境

```bash
#!/bin/bash
# ~/.claude/hooks/session-start.sh

# 检查必要的工具
missing_tools=()

for tool in node npm git; do
  if ! command -v $tool &> /dev/null; then
    missing_tools+=($tool)
  fi
done

if [ ${#missing_tools[@]} -ne 0 ]; then
  echo "Warning: Missing tools: ${missing_tools[*]}"
fi

# 检查 node_modules
if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
  echo "Note: package.json found but node_modules missing. Run 'npm install'?"
fi

echo '{}'
```

### 5. HTTP Webhook 示例

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "type": "http",
        "url": "https://hooks.example.com/claude/session-end",
        "headers": {
          "Authorization": "Bearer ${WEBHOOK_TOKEN}"
        }
      }
    ]
  }
}
```

### 6. 发送通知 (Prompt Hook)

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "prompt",
        "prompt": "Generate a brief summary (max 10 words) of what was accomplished in this response"
      }
    ]
  }
}
```

## 可用 Hook 事件

| 事件 | 触发时机 |
|------|----------|
| `SessionStart` | Session 开始时 |
| `SessionEnd` | Session 结束时 |
| `UserPromptSubmit` | 用户提交 prompt 时 |
| `PreToolUse` | 工具执行前（可阻止） |
| `PostToolUse` | 工具执行成功后 |
| `PostToolUseFailure` | 工具执行失败后 |
| `PermissionRequest` | 出现权限请求时 |
| `Stop` | Claude 完成响应时 |
| `SubagentStart` | Subagent 启动时 |
| `SubagentStop` | Subagent 完成时 |
| `PreCompact` | 上下文压缩前 |
| `PostCompact` | 上下文压缩后 |

## Hook 响应格式

### 允许操作
```json
{}
```

### 阻止操作
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Reason for blocking"
  }
}
```

### 修改输入
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "modified command"
    }
  }
}
```
