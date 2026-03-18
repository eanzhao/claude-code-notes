#!/bin/bash
# Claude Code 状态栏脚本示例
# 保存到 ~/.claude/statusline.sh 并 chmod +x

# 从 stdin 读取 JSON 数据
input=$(cat)

# 提取字段
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "unknown"')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

# 格式化目录名（只取最后一部分）
DIR_NAME=$(basename "$DIR")

# 格式化成本
COST_FMT=$(printf '$%.2f' "$COST")

# 格式化时长
DURATION_SEC=$((DURATION_MS / 1000))
MINS=$((DURATION_SEC / 60))
SECS=$((DURATION_SEC % 60))

# 颜色定义
RESET='\033[0m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
CYAN='\033[36m'

# 根据上下文使用率选择颜色
if [ "$PCT" -ge 90 ]; then
    PCT_COLOR="$RED"
elif [ "$PCT" -ge 70 ]; then
    PCT_COLOR="$YELLOW"
else
    PCT_COLOR="$GREEN"
fi

# 构建进度条（10个字符）
BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
if [ "$FILLED" -gt 0 ]; then
    printf -v FILL "%${FILLED}s"
    BAR="${FILL// /█}"
fi
if [ "$EMPTY" -gt 0 ]; then
    printf -v PAD "%${EMPTY}s"
    BAR="${BAR}${PAD// /░}"
fi

# 获取 git 信息（如果在 git 仓库中）
GIT_INFO=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$BRANCH" ]; then
        # 检查是否有未提交的更改
        if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            GIT_INFO=" | 🌿 $BRANCH *"
        else
            GIT_INFO=" | 🌿 $BRANCH"
        fi
    fi
fi

# 输出状态行
echo -e "${CYAN}[$MODEL]${RESET} 📁 $DIR_NAME$GIT_INFO"
echo -e "${PCT_COLOR}${BAR}${RESET} ${PCT}% | 💰 ${COST_FMT} | ⏱️ ${MINS}m ${SECS}s"
