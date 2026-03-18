---
title: "企业网络配置"
order: 35
section: "deployment"
sectionLabel: "部署"
sectionOrder: 5
summary: "使用代理服务器、自定义证书颁发机构 (CA) 和相互传输层安全 (mTLS) 身份验证为企业环境配置 Claude Code。"
sourceUrl: "https://code.claude.com/docs/en/network-config.md"
sourceTitle: "Enterprise network configuration"
tags: []
---
# 企业网络配置

> 使用代理服务器、自定义证书颁发机构 (CA) 和相互传输层安全 (mTLS) 身份验证为企业环境配置 Claude Code。

Claude Code通过环境变量支持各种企业网络和安全配置。这包括通过企业代理服务器路由流量、信任自定义证书颁发机构 (CA) 以及使用相互传输层安全 (mTLS) 证书进行身份验证以增强安全性。

**注意**

本页显示的所有环境变量也可以在 [`settings.json`](./settings) 中配置。

## 代理配置

### 环境变量

Claude Code 尊重标准代理环境变量：

```bash
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Bypass proxy for specific requests - space-separated format
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Bypass proxy for specific requests - comma-separated format
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Bypass proxy for all requests
export NO_PROXY="*"
```

**注意**

Claude Code 不支持 SOCKS 代理。

### 基本身份验证

如果您的代理需要基本身份验证，请在代理 URL 中包含凭据：

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

**警告**

避免在脚本中对密码进行硬编码。请改用环境变量或安全凭证存储。

**提示**

对于需要高级身份验证（NTLM、Kerberos 等）的代理，请考虑使用支持您的身份验证方法的 LLM 网关服务。

## 自定义 CA 证书

如果您的企业环境使用自定义 CA 进行 HTTPS 连接（无论是通过代理还是直接 API 访问），请将 Claude Code 配置为信任它们：

```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 身份验证

对于需要客户端证书身份验证的企业环境：

```bash
# Client certificate for authentication
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Client private key
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase for encrypted private key
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## 网络访问要求

Claude Code 需要访问以下 URL：

* `api.anthropic.com`：Claude API 端点
* `claude.ai`：claude.ai 帐户的身份验证
* `platform.claude.com`：Anthropic 控制台帐户的身份验证

确保这些 URL 在您的代理配置和防火墙规则中列入白名单。在容器化或受限网络环境中使用 Claude Code 时，这一点尤其重要。

本机安装程序和更新检查还需要以下 URL。如果您通过 npm 安装 Claude Code 或管理您自己的二进制发行版，最终用户可能不需要访问权限：

* `downloads.claude.ai`：托管安装脚本、版本指针、清单和可执行文件的 CDN
* `storage.googleapis.com`：旧版下载存储桶，正在弃用

[网络上的 Claude Code](./claude-code-on-the-web) 和 [代码审查](./code-review) 从 Anthropic 管理的基础设施连接到您的存储库。如果您的 GitHub 企业云组织限制通过 IP 地址进行访问，请启用 [已安装的 GitHub 应用程序的 IP 允许列表继承](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)。 Claude GitHub 应用程序注册其 IP 范围，因此启用此设置无需手动配置即可进行访问。要[手动将范围添加到允许列表](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)，或配置其他防火墙，请参阅 [Anthropic API IP 地址](https://platform.claude.com/docs/en/api/ip-addresses)。

## 其他资源

* [Claude Code 设置](./settings)
* [环境变量参考](./env-vars)
* [故障排除指南](./troubleshooting)
