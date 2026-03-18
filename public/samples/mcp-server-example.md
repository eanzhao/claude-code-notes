# MCP Server 配置示例

Model Context Protocol (MCP) 允许 Claude Code 连接外部工具和服务。

## 配置文件位置

- 用户级：`~/.claude.json` 中的 `mcpServers`
- 项目级：`.mcp.json`

## 示例配置

### 1. 基础 MCP 配置 (mcp.json)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/projects"]
    },
    "postgres": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

### 2. 开发工具 MCP 配置

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data.db"]
    },
    "redis": {
      "command": "uvx",
      "args": ["mcp-server-redis", "--host", "localhost", "--port", "6379"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

### 3. 云服务 MCP 配置

```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-aws"],
      "env": {
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
        "AWS_REGION": "us-east-1"
      }
    },
    "gcp": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gcp"]
    }
  }
}
```

### 4. 开发工作流 MCP 配置

```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": {
        "SENTRY_AUTH_TOKEN": "${SENTRY_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    },
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    }
  }
}
```

### 5. 浏览器自动化 MCP 配置

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-playwright"]
    }
  }
}
```

## 环境变量处理

使用 `${VAR_NAME}` 语法引用环境变量：

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

然后在你的 shell 中设置：

```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
```

## 常用 MCP 服务器列表

| 名称 | 包名 | 功能 |
|------|------|------|
| GitHub | `@modelcontextprotocol/server-github` | 仓库管理、PR、Issues |
| Git | `@modelcontextprotocol/server-git` | Git 操作 |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | 数据库查询 |
| SQLite | `mcp-server-sqlite` | SQLite 数据库 |
| Filesystem | `@modelcontextprotocol/server-filesystem` | 文件操作 |
| Fetch | `mcp-server-fetch` | HTTP 请求 |
| Brave Search | `@modelcontextprotocol/server-brave-search` | 网络搜索 |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | 浏览器自动化 |
| Sentry | `@modelcontextprotocol/server-sentry` | 错误监控 |
| Slack | `@modelcontextprotocol/server-slack` | 消息发送 |
| Notion | `@modelcontextprotocol/server-notion` | 文档管理 |
| Linear | `@modelcontextprotocol/server-linear` | 项目管理 |

## 命令参考

```bash
# 添加 MCP 服务器
claude mcp add <name> <command>

# 示例：添加 GitHub MCP
claude mcp add github npx -y @modelcontextprotocol/server-github

# 查看已配置的 MCP 服务器
/mcp

# 在 Claude Code 中查看 MCP 状态
```
