# AGENTS

## 项目简介

这是一个基于 Astro 搭建的中文文档站点，用来系统整理和翻译 Claude Code 官方文档。

项目目标有两层：

1. 完整收录 Claude Code 官方英文文档，并生成可浏览的中文站点。
2. 在官方文档之外，补充更适合中文用户上手的学习路线、常用样例和实践说明。

当前站点内容主要覆盖：

- Claude Code 官方文档中文翻译
- 官方文档地图整理页
- 面向 Desktop app 和 CLI 用户的学习路线
- 常见提示词和工作流样例

## 技术栈

- Astro
- Astro Content Collections
- TypeScript
- Python 脚本，用于抓取、清洗、翻译和生成文档页面

## 目录说明

- `src/content/docs/`
  - 站点正文内容。
  - 大部分官方文档页面由同步脚本生成。
  - `learning-roadmap.md` 和 `desktop-cli-samples.md` 这类页面是人工补充内容。

- `src/pages/docs/`
  - 纯静态 Astro 页面入口。
  - 每篇文档都有对应的 `<slug>.astro`。
  - 同时生成 `<slug>.md.astro` 作为旧式 `.md` URL 的重定向页。
  - 这些页面是脚本自动生成的，不建议手工维护。

- `src/components/`
  - 通用 Astro 组件。
  - `DocEntryPage.astro` 负责渲染单篇文档。
  - `RedirectPage.astro` 负责重定向页。

- `src/layouts/`
  - 站点和文档布局。

- `src/styles/`
  - 全局样式。

- `scripts/sync_claude_code_docs.py`
  - 核心同步脚本。
  - 负责抓取官方文档索引、下载页面、清洗特殊组件、翻译成中文、写入内容文件，并生成静态路由页面。

- `boot.sh`
  - 本地启动脚本。
  - 自动检查依赖并启动 Astro 开发服务器。

## 内容来源

官方文档主要来自：

- `https://code.claude.com/docs/en/`
- `https://code.claude.com/docs/en/claude_code_docs_map.md`
- `https://code.claude.com/docs/llms.txt`

MCP 文档中的部分服务器列表会在同步时通过官方 registry 接口静态展开。

## 开发与使用

安装依赖：

```bash
pnpm install
```

启动本地开发站点：

```bash
./boot.sh
```

或者：

```bash
pnpm dev
```

重新同步官方文档并生成页面：

```bash
pnpm sync:docs
```

构建静态站点：

```bash
pnpm build
```

## 编辑约定

- 可以直接手改：
  - `src/content/docs/learning-roadmap.md`
  - `src/content/docs/desktop-cli-samples.md`
  - 布局、组件、样式文件

- 尽量不要直接手改：
  - `src/content/docs/` 下由官方同步生成的页面
  - `src/pages/docs/` 下自动生成的文档入口页

如果要更新官方文档，优先修改同步脚本，再重新执行 `pnpm sync:docs`。

## 维护建议

- 如果只是想修正少量中文表述，可以考虑在同步脚本里增加后处理规则，而不是逐页手改。
- 如果要增加新的导览内容，建议放在 `src/content/docs/` 下的人工页面里，并保持与官方页分离。
- 如果页面结构要继续向参考项目靠拢，优先保持“内容在 `src/content/docs`，静态入口在 `src/pages/docs`”这条约定。
