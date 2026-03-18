#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import textwrap
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".cache" / "claude-code-docs"
RAW_DIR = CACHE_DIR / "raw"
CONTENT_DIR = ROOT / "src" / "content" / "docs"
GENERATED_DIR = ROOT / "src" / "generated"
TRANSLATION_CACHE_PATH = CACHE_DIR / "translation-cache.json"
MANIFEST_PATH = GENERATED_DIR / "docs-manifest.json"

LLMS_URL = "https://code.claude.com/docs/llms.txt"
DOCS_MAP_URL = "https://code.claude.com/docs/en/claude_code_docs_map.md"
MCP_REGISTRY_URL = "https://api.anthropic.com/mcp-registry/v0/servers"

LEARNING_SLUG = "learning-roadmap"
SAMPLES_SLUG = "desktop-cli-samples"
DOCS_MAP_SLUG = "official-docs-map"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Claude Code Notes Sync Script)"
}

SECTION_META = {
    "Getting started": ("getting-started", "快速入门", 1),
    "Core concepts": ("core-concepts", "核心概念", 2),
    "Platforms and integrations": ("platforms", "平台与集成", 3),
    "Build with Claude Code": ("build", "构建与扩展", 4),
    "Deployment": ("deployment", "部署", 5),
    "Administration": ("administration", "管理", 6),
    "Configuration": ("configuration", "配置", 7),
    "Reference": ("reference", "参考", 8),
    "Resources": ("resources", "资源", 9),
}

GROUP_META = {
    "Platforms and integrations > Claude Code on desktop": "桌面端与图形界面",
    "Platforms and integrations > Code review & CI/CD": "代码评审与 CI/CD",
}

GLOSSARY = [
    "Claude Code",
    "Claude Desktop",
    "Claude",
    "Anthropic",
    "CLAUDE.md",
    "Remote Control",
    "Agent SDK",
    "Plan Mode",
    "Model Context Protocol",
    "MCP",
    "VS Code",
    "JetBrains",
    "GitHub Actions",
    "GitHub CLI",
    "GitHub",
    "GitLab",
    "Amazon Bedrock",
    "Google Vertex AI",
    "Microsoft Foundry",
    "Homebrew",
    "WinGet",
    "Chrome",
    "Docker",
    "tmux",
    "Node.js",
    "PowerShell",
    "Linux",
    "macOS",
    "Windows",
    "Slack",
    "Linear",
    "Notion",
    "Figma",
    "Gmail",
    "Sentry",
    "Statsig",
    "JIRA",
    "Discord",
    "OAuth",
    "JSON",
    "YAML",
]

POST_REPLACEMENTS = {
    "克劳德·科德": "Claude Code",
    "克劳德代码": "Claude Code",
    "GitHub 操作": "GitHub Actions",
    "自制": "Homebrew",
    "温盖特": "WinGet",
}


@dataclass
class DocEntry:
    slug: str
    order: int
    source_title: str
    source_summary: str
    source_url: str
    section: str
    section_label: str
    section_order: int
    group: str | None = None
    group_label: str | None = None
    headings: list[str] | None = None
    title_zh: str | None = None
    summary_zh: str | None = None


def ensure_directories() -> None:
    for directory in (CACHE_DIR, RAW_DIR, CONTENT_DIR, GENERATED_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def load_translation_cache() -> dict[str, str]:
    if not TRANSLATION_CACHE_PATH.exists():
        return {}
    return json.loads(TRANSLATION_CACHE_PATH.read_text())


def save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2) + "\n"
    )


def fetch_text(url: str, cache_name: str) -> str:
    cache_path = RAW_DIR / cache_name
    if cache_path.exists():
        return cache_path.read_text()

    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    cache_path.write_text(response.text)
    return response.text


def parse_llms(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"^- \[(?P<title>.*?)\]\((?P<url>https://code\.claude\.com/docs/en/(?P<slug>[^)]+?)\.md)\): (?P<summary>.+)$",
        re.M,
    )
    for match in pattern.finditer(text):
        slug = match.group("slug")
        entries[slug] = {
            "title": match.group("title").strip(),
            "summary": match.group("summary").strip(),
            "url": match.group("url").strip(),
        }
    return entries


def parse_docs_map(text: str, llms: dict[str, dict[str, str]]) -> list[DocEntry]:
    current_section: str | None = None
    current_group: str | None = None
    current_slug: str | None = None
    order = 0
    by_slug: dict[str, DocEntry] = {}

    for line in text.splitlines():
        if line.startswith("## ") and line not in {"## Documentation Index", "## Document Structure"}:
            current_section = line[3:].strip()
            current_group = None
            current_slug = None
            continue

        if line.startswith("### ") and not re.match(r"^### \[", line):
            current_group = line[4:].strip()
            current_slug = None
            continue

        page_match = re.match(
            r"^(?P<level>#{3,4}) \[(?P<title>.*?)\]\((?P<url>https://code\.claude\.com/docs/en/(?P<slug>[^)]+?)\.md)\)",
            line,
        )
        if page_match:
            slug = page_match.group("slug")
            level = len(page_match.group("level"))
            order += 1

            raw_section = current_section
            if level == 4 and current_group and " > " in current_group:
                raw_section = current_group.split(" > ", 1)[0]

            if raw_section not in SECTION_META:
                raise ValueError(f"Unknown section: {raw_section!r}")

            section, section_label, section_order = SECTION_META[raw_section]
            group_label = GROUP_META.get(current_group or "")

            llms_entry = llms[slug]
            by_slug[slug] = DocEntry(
                slug=slug,
                order=order,
                source_title=llms_entry["title"],
                source_summary=llms_entry["summary"],
                source_url=llms_entry["url"],
                section=section,
                section_label=section_label,
                section_order=section_order,
                group=current_group,
                group_label=group_label,
                headings=[],
            )
            current_slug = slug
            continue

        if current_slug and re.match(r"^\s*\* ", line):
            by_slug[current_slug].headings.append(line.rstrip())

    missing = sorted(set(llms) - set(by_slug))
    if missing:
        raise ValueError(f"Docs map is missing entries: {missing}")

    return sorted(by_slug.values(), key=lambda item: item.order)


def parse_attrs(raw_attrs: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for key, quoted, braced in re.findall(r'(\w+)=(?:"([^"]*)"|\{([^}]*)\})', raw_attrs):
        attrs[key] = quoted if quoted else braced
    return attrs


def tidy_body(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def rewrite_internal_target(url: str, known_slugs: set[str]) -> str:
    clean_url = url.replace("\\&", "&").strip()

    if clean_url == LLMS_URL or clean_url.endswith("/llms.txt"):
        return f"./{DOCS_MAP_SLUG}"
    if clean_url == DOCS_MAP_URL or clean_url.endswith("/claude_code_docs_map.md"):
        return f"./{DOCS_MAP_SLUG}"

    doc_match = re.match(
        r"^(?:https://code\.claude\.com/docs)?/en/(?P<slug>[^)#?]+?)(?:\.md)?(?P<anchor>#[^)]+)?$",
        clean_url,
    )
    if not doc_match:
        doc_match = re.match(
            r"^https://code\.claude\.com/docs/en/(?P<slug>[^)#?]+?)(?:\.md)?(?P<anchor>#[^)]+)?$",
            clean_url,
        )

    if doc_match:
        slug = doc_match.group("slug")
        anchor = doc_match.group("anchor") or ""
        if slug in known_slugs:
            return f"./{slug}{anchor}"
        return f"https://code.claude.com/docs/en/{slug}{anchor}"

    return clean_url


def rewrite_links(text: str, known_slugs: set[str]) -> str:
    def replace_markdown_link(match: re.Match[str]) -> str:
        label = match.group(1)
        target = rewrite_internal_target(match.group(2), known_slugs)
        return f"[{label}]({target})"

    def replace_html_link(match: re.Match[str]) -> str:
        tag_name = match.group(1)
        before = match.group(2)
        url = match.group(3)
        after = match.group(4)
        return f'<{tag_name}{before}"{rewrite_internal_target(url, known_slugs)}"{after}>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_markdown_link, text)
    text = re.sub(r'<(a|img)([^>]+?(?:href|src)=)"([^"]+)"([^>]*)>', replace_html_link, text)
    return text


def fetch_mcp_servers() -> list[dict[str, str]]:
    servers: list[dict[str, str]] = []
    cursor: str | None = None

    while True:
        response = requests.get(
            MCP_REGISTRY_URL,
            headers=HEADERS,
            params={
                "version": "latest",
                "visibility": "commercial",
                "limit": "100",
                **({"cursor": cursor} if cursor else {}),
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        servers.extend(payload["servers"])
        cursor = payload.get("metadata", {}).get("nextCursor")
        if not cursor:
            break

    return servers


def build_mcp_server_markdown() -> str:
    items: list[str] = []

    for item in fetch_mcp_servers():
        server = item["server"]
        registry_meta = item.get("_meta", {}).get("com.anthropic.api/mcp-registry", {})
        works_with = registry_meta.get("worksWith", [])
        if "claude-code" not in works_with:
            continue

        name = registry_meta.get("displayName") or server.get("title") or server.get("name")
        description = registry_meta.get("oneLiner") or server.get("description", "")
        documentation = registry_meta.get("documentation")
        remotes = server.get("remotes", [])
        http_remote = next((remote for remote in remotes if remote.get("type") == "streamable-http"), None)
        sse_remote = next((remote for remote in remotes if remote.get("type") == "sse"), None)
        preferred_remote = http_remote or sse_remote
        remote_url = preferred_remote.get("url") if preferred_remote else registry_meta.get("url")
        remote_type = preferred_remote.get("type") if preferred_remote else None

        command = None
        if remote_url and "{" not in remote_url:
            server_slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            if remote_type == "streamable-http":
                command = f"claude mcp add {server_slug} --transport http {remote_url}"
            elif remote_type == "sse":
                command = f"claude mcp add {server_slug} --transport sse {remote_url}"

        items.append(f"### {name}")
        if documentation:
            items.append(f"[官方文档]({documentation})")
        items.append("")
        if description:
            items.append(description)
            items.append("")
        if command:
            items.append(f"- Claude Code 接入命令：`{command}`")
        elif remote_url and "{" not in remote_url:
            items.append(f"- 远程地址：`{remote_url}`")
        else:
            setup_url = registry_meta.get("documentation")
            if setup_url:
                items.append(f"- 需要先完成服务端配置：[{setup_url}]({setup_url})")
        items.append("")

    intro = (
        "以下列表根据官方 MCP Registry 在构建时静态生成。"
        "由于这个目录是动态变化的，站内内容可能会晚于官方几小时到几天。"
    )
    return intro + "\n\n" + "\n".join(items).strip() + "\n"


def normalize_source(raw_text: str, slug: str, known_slugs: set[str]) -> str:
    text = raw_text.replace("\r\n", "\n")
    text = re.sub(r"^> ## Documentation Index\n>.*?\n\n", "", text, flags=re.S)
    text = re.sub(r"```([^\n`]*)\s+theme=\{null\}", r"```\1", text)

    if "export const MCPServersTable" in text:
        text = re.sub(
            r"^export const MCPServersTable = .*?^};\n+",
            "",
            text,
            flags=re.S | re.M,
        )

    text = rewrite_links(text, known_slugs)

    text = re.sub(r"<Tabs>\s*", "", text)
    text = re.sub(r"</Tabs>\s*", "", text)
    text = re.sub(r"<CodeGroup>\s*", "", text)
    text = re.sub(r"</CodeGroup>\s*", "", text)
    text = re.sub(r"<CardGroup[^>]*>\s*", "", text)
    text = re.sub(r"</CardGroup>\s*", "", text)
    text = re.sub(r"<AccordionGroup>\s*", "", text)
    text = re.sub(r"</AccordionGroup>\s*", "", text)
    text = re.sub(r"<Steps>\s*", "", text)
    text = re.sub(r"</Steps>\s*", "", text)
    text = re.sub(r"<Frame[^>]*>\s*", "", text)
    text = re.sub(r"</Frame>\s*", "", text)
    text = re.sub(r"<br\s*/?>", "\n", text)

    def replace_title_block(tag_name: str, heading_level: str) -> None:
        nonlocal text
        pattern = re.compile(fr"<{tag_name}([^>]*)>(.*?)</{tag_name}>", re.S)
        while True:
            changed = False

            def repl(match: re.Match[str]) -> str:
                nonlocal changed
                changed = True
                attrs = parse_attrs(match.group(1))
                title = attrs.get("title") or attrs.get("label") or tag_name
                body = tidy_body(match.group(2))
                if tag_name == "Update":
                    description = attrs.get("description")
                    if description:
                        title = f"{title}（{description}）"
                return f"\n{heading_level} {title}\n\n{body}\n"

            text = pattern.sub(repl, text)
            if not changed:
                break

    def replace_card_blocks() -> None:
        nonlocal text
        pattern = re.compile(r"<Card([^>]*)>(.*?)</Card>", re.S)
        while True:
            changed = False

            def repl(match: re.Match[str]) -> str:
                nonlocal changed
                changed = True
                attrs = parse_attrs(match.group(1))
                title = attrs.get("title", "Card")
                href = attrs.get("href")
                body = tidy_body(match.group(2))
                heading = f"[{title}]({href})" if href else title
                return f"\n### {heading}\n\n{body}\n"

            text = pattern.sub(repl, text)
            if not changed:
                break

    def replace_admonitions() -> None:
        nonlocal text
        mapping = {
            "Note": "注意",
            "Tip": "提示",
            "Info": "说明",
            "Warning": "警告",
            "Callout": "提示",
        }
        for tag_name, label in mapping.items():
            pattern = re.compile(fr"<{tag_name}([^>]*)>(.*?)</{tag_name}>", re.S)
            while True:
                changed = False

                def repl(match: re.Match[str]) -> str:
                    nonlocal changed
                    changed = True
                    attrs = parse_attrs(match.group(1))
                    title = attrs.get("title")
                    heading = f"{label}：{title}" if title else label
                    body = tidy_body(match.group(2))
                    return f"\n**{heading}**\n\n{body}\n"

                text = pattern.sub(repl, text)
                if not changed:
                    break

    replace_title_block("Tab", "###")
    replace_title_block("Accordion", "###")
    replace_title_block("Step", "###")
    replace_title_block("Update", "##")
    replace_card_blocks()
    replace_admonitions()

    text = text.replace('<MCPServersTable platform="claudeCode" />', build_mcp_server_markdown())
    text = text.replace("<MCPServersTable platform=\"claudeDesktop\" />", "")
    text = text.replace("<MCPServersTable platform=\"all\" />", build_mcp_server_markdown())
    text = text.replace("<MCPServersTable />", build_mcp_server_markdown())

    text = re.sub(r'<a href="([^"]+)">(.*?)</a>', r"[\2](\1)", text, flags=re.S)
    text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text, flags=re.S)
    text = re.sub(r"</?(div|span|p|table|thead|tbody|tr|td|th|summary|head|body|html)[^>]*>", "", text)
    text = re.sub(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>', r"![\2](\1)", text)
    text = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*src="([^"]+)"[^>]*/?>', r"![\1](\2)", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def split_text_for_translation(text: str, limit: int = 3200) -> list[str]:
    parts = re.split(r"(\n{2,})", text)
    chunks: list[str] = []
    current = ""

    def flush() -> None:
        nonlocal current
        if current:
            chunks.append(current)
            current = ""

    for part in parts:
        if len(part) > limit:
            flush()
            lines = re.split(r"(\n)", part)
            line_current = ""
            for line in lines:
                if len(line_current) + len(line) > limit and line_current:
                    chunks.append(line_current)
                    line_current = line
                else:
                    line_current += line
            if line_current:
                chunks.append(line_current)
            continue

        if len(current) + len(part) > limit and current:
            flush()
        current += part

    flush()
    return [chunk for chunk in chunks if chunk]


def protect_text(text: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def store(value: str) -> str:
        token = f"PHX{len(protected):05d}XHP"
        protected[token] = value
        return token

    text = re.sub(r"```.*?```", lambda match: store(match.group(0)), text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", lambda match: store(match.group(0)), text)
    text = re.sub(r"\]\(([^)]+)\)", lambda match: "](" + store(match.group(1)) + ")", text)
    text = re.sub(r"https?://[^\s)>]+", lambda match: store(match.group(0)), text)
    text = re.sub(r"<[^>]+>", lambda match: store(match.group(0)), text)

    for term in sorted(GLOSSARY, key=len, reverse=True):
        text = text.replace(term, store(term))

    return text, protected


def restore_text(text: str, protected: dict[str, str]) -> str:
    for token, value in sorted(protected.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(token, value)
    return text


def translate_chunk(chunk: str, cache: dict[str, str]) -> str:
    if not chunk.strip():
        return chunk

    cache_key = hashlib.sha1(chunk.encode("utf-8")).hexdigest()
    if cache_key in cache:
        return cache[cache_key]

    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = requests.get(
                "https://translate.googleapis.com/translate_a/single",
                headers=HEADERS,
                params={
                    "client": "gtx",
                    "sl": "en",
                    "tl": "zh-CN",
                    "dt": "t",
                    "q": chunk,
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            translated = "".join(
                part[0] for part in payload[0] if isinstance(part, list) and part and part[0]
            )
            cache[cache_key] = translated
            return translated
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(f"Failed to translate chunk after retries: {last_error}") from last_error


def translate_markdown(text: str, cache: dict[str, str]) -> str:
    protected_text, protected = protect_text(text)
    chunks = split_text_for_translation(protected_text)
    translated = "".join(translate_chunk(chunk, cache) for chunk in chunks)
    restored = restore_text(translated, protected)

    for source, target in POST_REPLACEMENTS.items():
        restored = restored.replace(source, target)

    restored = restored.replace("theme={null}", "")
    restored = restored.replace("** 提示**", "**提示**")
    restored = restored.replace("** 注意**", "**注意**")
    restored = restored.replace("** 说明**", "**说明**")
    restored = restored.replace("** 警告**", "**警告**")
    restored = re.sub(r"\[(https?://[^\]]+)\]\(PHX\d+XHP\)", r"[\1](\1)", restored)
    restored = re.sub(r"(?m)^(\d+)\.(\S)", r"\1. \2", restored)
    restored = re.sub(r"\n```(\w+)\s+\n", r"\n```\1\n", restored)
    restored = re.sub(r"\n{3,}", "\n\n", restored)

    cleaned_lines: list[str] = []
    for line in restored.splitlines():
        if line.startswith("```"):
            fence_suffix = line[3:].strip()
            if fence_suffix and re.match(r"^[^\w#+.-]", fence_suffix):
                cleaned_lines.append("```")
                cleaned_lines.append(fence_suffix)
                continue
        cleaned_lines.append(line)

    restored = "\n".join(cleaned_lines)
    return restored.strip() + "\n"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_doc(entry: DocEntry, markdown_body: str) -> None:
    frontmatter = [
        "---",
        f"title: {yaml_string(entry.title_zh or entry.source_title)}",
        f"order: {entry.order}",
        f"section: {yaml_string(entry.section)}",
        f"sectionLabel: {yaml_string(entry.section_label)}",
        f"sectionOrder: {entry.section_order}",
        f"summary: {yaml_string(entry.summary_zh or entry.source_summary)}",
        f"sourceUrl: {yaml_string(entry.source_url)}",
        f"sourceTitle: {yaml_string(entry.source_title)}",
    ]
    if entry.group:
        frontmatter.append(f"group: {yaml_string(entry.group)}")
    if entry.group_label:
        frontmatter.append(f"groupLabel: {yaml_string(entry.group_label)}")
    frontmatter.extend(["tags: []", "---", ""])

    target_path = CONTENT_DIR / f"{entry.slug}.md"
    target_path.write_text("\n".join(frontmatter) + markdown_body)


def build_docs_map_page(entries: Iterable[DocEntry]) -> str:
    lines = [
        "# Claude Code 官方文档地图",
        "",
        "这页根据官方的 `claude_code_docs_map.md` 自动整理，方便你按主题系统学习。",
        "如果你想快速开始，建议先看 [系统学习路线](./learning-roadmap) 和 [Desktop / CLI 高频样例](./desktop-cli-samples)。",
        "",
    ]

    grouped: dict[str, list[DocEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.section_label, []).append(entry)

    for section_label, section_docs in grouped.items():
        lines.append(f"## {section_label}")
        lines.append("")
        current_group = None
        for entry in section_docs:
            if entry.group_label and entry.group_label != current_group:
                current_group = entry.group_label
                lines.append(f"### {current_group}")
                lines.append("")

            lines.append(f"#### [{entry.title_zh or entry.source_title}](./{entry.slug})")
            lines.append("")
            if entry.summary_zh:
                lines.append(entry.summary_zh)
                lines.append("")
            for heading in entry.headings or []:
                lines.append(heading)
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_manifest(entries: list[DocEntry]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps([asdict(entry) for entry in entries], ensure_ascii=False, indent=2) + "\n"
    )


def main() -> None:
    ensure_directories()
    translation_cache = load_translation_cache()

    llms_text = fetch_text(LLMS_URL, "llms.txt")
    docs_map_text = fetch_text(DOCS_MAP_URL, "claude_code_docs_map.md")

    llms_entries = parse_llms(llms_text)
    doc_entries = parse_docs_map(docs_map_text, llms_entries)
    known_slugs = {entry.slug for entry in doc_entries} | {LEARNING_SLUG, SAMPLES_SLUG, DOCS_MAP_SLUG}

    for entry in doc_entries:
        source = fetch_text(entry.source_url, f"{entry.slug}.source.md")
        normalized = normalize_source(source, entry.slug, known_slugs)
        entry.title_zh = translate_markdown(entry.source_title, translation_cache).strip()
        entry.summary_zh = translate_markdown(entry.source_summary, translation_cache).strip()
        translated = translate_markdown(normalized, translation_cache)
        write_doc(entry, translated)
        save_translation_cache(translation_cache)
        print(f"Synced: {entry.slug}")

    docs_map_entry = DocEntry(
        slug=DOCS_MAP_SLUG,
        order=max(entry.order for entry in doc_entries) + 1,
        source_title="Claude Code docs map",
        source_summary="Official Claude Code documentation map with sections and headings.",
        source_url=DOCS_MAP_URL,
        section="resources",
        section_label="资源",
        section_order=9,
        title_zh="Claude Code 官方文档地图",
        summary_zh="按章节整理的官方文档目录与标题树，便于整体浏览。",
    )
    docs_map_body = translate_markdown(build_docs_map_page(doc_entries), translation_cache)
    write_doc(docs_map_entry, docs_map_body)

    all_entries = doc_entries + [docs_map_entry]
    write_manifest(all_entries)
    save_translation_cache(translation_cache)
    print(f"Generated {len(all_entries)} official pages.")


if __name__ == "__main__":
    main()
