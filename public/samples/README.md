# Claude Code 配置示例

这里提供了一系列 Claude Code 的配置示例，帮助你快速上手各种功能。

## 示例列表

### 基础配置

| 文件 | 说明 |
|------|------|
| [CLAUDE.md](./CLAUDE.md) | 项目级持久上下文配置示例 |
| [settings.json](./settings.json) | 完整的设置文件示例 |

### 扩展功能

| 文件 | 说明 |
|------|------|
| [skill-example.md](./skill-example.md) | Skill（技能）定义示例，包括代码审查、部署等 |
| [hooks-example.md](./hooks-example.md) | Hooks（钩子）配置示例，用于自动化工作流 |
| [subagent-example.md](./subagent-example.md) | Subagent（子代理）定义示例 |
| [mcp-server-example.md](./mcp-server-example.md) | MCP 服务器配置示例 |

### 工作流示例

| 文件 | 说明 |
|------|------|
| [github-actions-workflow.yml](./github-actions-workflow.yml) | GitHub Actions 集成示例 |
| [pre-commit-hook.sh](./pre-commit-hook.sh) | Git 预提交钩子示例 |

### 实用脚本

| 文件 | 说明 |
|------|------|
| [statusline.sh](./statusline.sh) | 自定义状态栏脚本示例 |
| [file-suggestion.sh](./file-suggestion.sh) | 文件建议脚本示例 |

## 快速开始

1. **复制 CLAUDE.md 到你的项目根目录**
   ```bash
   cp CLAUDE.md /path/to/your/project/
   ```

2. **复制 settings.json 到用户配置目录**
   ```bash
   mkdir -p ~/.claude
   cp settings.json ~/.claude/settings.json
   ```

3. **创建你的第一个 skill**
   ```bash
   mkdir -p ~/.claude/skills/my-skill
   cp skill-example.md ~/.claude/skills/my-skill/SKILL.md
   ```

4. **配置 MCP 服务器**
   ```bash
   cp mcp-server-example.json /path/to/your/project/.mcp.json
   ```

## 更多资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Agent Skills 标准](https://agentskills.io)
