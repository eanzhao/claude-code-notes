# Claude Code 中文文档站

这是一个基于 Astro 搭建的静态文档站，用来系统整理和翻译 Claude Code 官方文档，并补充一些更适合中文用户快速上手的导览内容。

目前这个项目包含三类内容：

- Claude Code 官方文档的中文翻译
- 官方文档地图整理页
- 面向 Claude Desktop app 和 `claude` CLI 用户的学习路线与高频样例

## 预览与启动

推荐直接使用项目自带脚本：

```bash
./boot.sh
```

它会自动：

- 检查 `pnpm`
- 如果需要则安装依赖
- 启动 Astro 本地开发服务器
- 在 macOS 上自动打开浏览器

默认打开地址：

```text
http://127.0.0.1:4321/docs/learning-roadmap
```

你也可以手动启动：

```bash
pnpm install
pnpm dev
```

## 构建静态站点

```bash
pnpm build
```

构建产物会输出到：

```text
dist/
```

## 同步官方文档

项目提供了一个同步脚本，会抓取 Claude Code 官方文档索引、下载页面、做格式清洗、翻译成中文，并生成站点内容与静态页面入口。

运行方式：

```bash
pnpm sync:docs
```

核心脚本位置：

```text
scripts/sync_claude_code_docs.py
```

主要来源：

- `https://code.claude.com/docs/en/`
- `https://code.claude.com/docs/en/claude_code_docs_map.md`
- `https://code.claude.com/docs/llms.txt`

## 项目结构

```text
.
├── boot.sh
├── scripts/
│   └── sync_claude_code_docs.py
├── src/
│   ├── components/
│   ├── content/
│   │   └── docs/
│   ├── layouts/
│   ├── pages/
│   │   └── docs/
│   └── styles/
└── dist/
```

几个关键目录的作用：

- `src/content/docs/`
  - 文档正文内容
  - 大部分官方页面由同步脚本生成
  - `learning-roadmap.md` 和 `desktop-cli-samples.md` 是人工补充内容

- `src/pages/docs/`
  - 纯静态 Astro 页面入口
  - 每篇文档都有显式的 `<slug>.astro`
  - 同时生成 `<slug>.md.astro` 作为重定向页

- `scripts/`
  - 同步、抓取、翻译和页面生成逻辑

## 推荐阅读顺序

如果你是第一次进入这个项目，建议先看：

1. `docs/learning-roadmap`
2. `docs/desktop-cli-samples`
3. `docs/overview`
4. `docs/quickstart`
5. `docs/how-claude-code-works`

## 维护说明

- 手工适合修改的内容：
  - `src/content/docs/learning-roadmap.md`
  - `src/content/docs/desktop-cli-samples.md`
  - 布局、组件、样式

- 尽量不要直接手改的内容：
  - 官方同步生成的文档页
  - `src/pages/docs/` 下自动生成的静态入口页

如果你想改善翻译质量或格式，优先修改同步脚本，再重新执行：

```bash
pnpm sync:docs
```

## 备注

这个项目当前已经是纯静态站点结构，页面入口采用和参考项目类似的显式静态路由方式，而不是动态 `[slug]` 路由。
