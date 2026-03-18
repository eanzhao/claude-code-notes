#!/bin/bash
# Git 预提交钩子示例
# 保存到 .git/hooks/pre-commit 并 chmod +x

# 这个钩子会在每次提交前运行，确保代码质量

echo "🔍 运行 Claude Code 预提交检查..."

# 检查是否有 Claude Code 配置文件
if [ -f ".claude/settings.json" ]; then
    echo "✓ 找到 Claude Code 配置"
else
    echo "⚠ 警告: 未找到 .claude/settings.json"
fi

# 运行 lint（如果存在）
if [ -f "package.json" ]; then
    if npm run lint --silent 2>/dev/null; then
        echo "✓ Lint 检查通过"
    else
        echo "✗ Lint 检查失败，请修复错误后再提交"
        exit 1
    fi
fi

# 运行测试（如果存在）
if [ -f "package.json" ]; then
    if npm test --silent 2>/dev/null; then
        echo "✓ 测试通过"
    else
        echo "✗ 测试失败，请修复错误后再提交"
        exit 1
    fi
fi

# 检查敏感信息
echo "🔍 检查敏感信息..."

# 检查 .env 文件是否被意外提交
if git diff --cached --name-only | grep -qE '\.env($|\.)'; then
    echo "✗ 错误: 尝试提交 .env 文件，这是不安全的！"
    echo "   请从暂存区移除: git reset HEAD .env"
    exit 1
fi

# 检查 AWS 密钥
if git diff --cached -U0 | grep -iE '(AKIA[0-9A-Z]{16}|aws_secret_access_key)' > /dev/null; then
    echo "✗ 错误: 检测到可能的 AWS 密钥！"
    exit 1
fi

# 检查私钥
if git diff --cached -U0 | grep -E 'BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY' > /dev/null; then
    echo "✗ 错误: 检测到私钥！"
    exit 1
fi

echo "✓ 预提交检查完成"
exit 0
