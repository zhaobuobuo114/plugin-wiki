#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static documentation site (docs/) from docs-src/.

Usage:  python tools/build_wiki.py
"""

from __future__ import annotations

import json
import posixpath
import re
import shutil
import sys
from html import escape
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs-src"
PAGES = SRC / "pages"
OUT = ROOT / "docs"

STATUS_TEXT = {"stable": "稳定", "beta": "测试", "wip": "开发中"}


def load_site() -> dict:
    with (SRC / "site.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def collect(site: dict):
    """Build a flat page list; plugin pages live under each plugin."""
    pages = []
    alias = {}
    for group in site["groups"]:
        for item in group["items"]:
            page = dict(item)
            page["group"] = group["title"]
            page["plugin"] = None
            pages.append(page)
            alias[item["title"]] = item["slug"]
            alias[Path(item["source"]).stem] = item["slug"]
            for name in item.get("alias", []):
                alias.setdefault(name, item["slug"])
    for plugin in site.get("plugins", []):
        for item in plugin["pages"]:
            page = dict(item)
            page["group"] = plugin["fullName"]
            page["plugin"] = plugin
            pages.append(page)
            for name in [item["title"], Path(item["source"]).stem] + item.get("alias", []):
                alias.setdefault(name, item["slug"])
    return pages, alias


LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")


def rewrite_links(text: str, slug: str, alias: dict) -> str:
    def repl(match: re.Match) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        clean = target[:-3] if target.endswith(".md") else target
        dest = alias.get(clean) or alias.get(target)
        if not dest:
            return match.group(0)
        rel = posixpath.relpath(dest, posixpath.dirname(slug) or ".")
        return f"[{label}]({rel})"

    return LINK_RE.sub(repl, text)


def plain_text(md_text: str) -> str:
    text = re.sub(r"```.*?```", " ", md_text, flags=re.S)
    text = re.sub(r"\[\[[^\]]+\]\]", " ", text)
    text = re.sub(r"[#>*`|\-]{1,}", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_toc(tokens, level: int = 0) -> str:
    if not tokens:
        return ""
    cls = "toc-list" if level == 0 else "toc-sub"
    parts = [f'<ul class="{cls}">']
    for tok in tokens:
        parts.append(f'<li><a href="#{escape(tok["id"])}">{escape(tok["name"])}</a>')
        if tok.get("children"):
            parts.append(build_toc(tok["children"], level + 1))
        parts.append("</li>")
    parts.append("</ul>")
    return "".join(parts)


def render_nav(site: dict, active_slug: str, root: str) -> str:
    out = []
    for group in site["groups"]:
        out.append('<div class="nav-group">')
        out.append(f'<div class="nav-title">{escape(group["title"])}</div>')
        out.append('<ul class="nav-items">')
        for item in group["items"]:
            cls = "nav-link is-active" if item["slug"] == active_slug else "nav-link"
            out.append(
                f'<li><a class="{cls}" href="{root}{item["slug"]}">{escape(item["title"])}</a></li>'
            )
        out.append("</ul></div>")
    return "\n".join(out)


def render_stats(site: dict) -> str:
    plugins = site.get("plugins") or []
    page_count = sum(len(p["pages"]) for p in plugins) + sum(
        len(g["items"]) for g in site["groups"]
    )
    latest = max((p.get("updated", "") for p in plugins), default="")
    stats = [
        (str(len(plugins)), "个插件"),
        (str(page_count), "篇文档"),
        (latest or "—", "最近更新"),
    ]
    cells = "".join(
        f'<div class="stat"><b>{escape(v)}</b><span>{escape(k)}</span></div>'
        for v, k in stats
    )
    return f'<div class="stat-row">{cells}</div>'


def render_plugin_blocks(site: dict, root: str, limit: int | None = None) -> str:
    plugins = list(site.get("plugins") or [])
    if limit:
        plugins = plugins[:limit]
    blocks = []
    for p in plugins:
        status = p.get("status", "stable")
        tags = "".join(
            f'<span class="pc-tag">{escape(t)}</span>' for t in p.get("tags", [])
        )
        docs = "".join(
            f'<a class="pb-doc" href="{root}{escape(pg["slug"])}">{escape(pg["title"])}'
            '<span aria-hidden="true">→</span></a>'
            for pg in p["pages"]
        )
        haystack = " ".join(
            [p.get("name", ""), p.get("fullName", ""), p.get("summary", "")] + p.get("tags", [])
        )
        actions = (
            f'<a class="pc-btn" href="{root}{escape(p["pages"][0]["slug"])}">开始阅读</a>'
        )
        if p.get("repo"):
            actions += (
                f'<a class="pc-btn pc-btn-ghost" href="{escape(p["repo"])}" '
                'target="_blank" rel="noopener">源码</a>'
            )
        actions += (
            f'<a class="pc-btn pc-btn-ghost" href="{escape(p.get("download", ""))}" '
            'target="_blank" rel="noopener">下载</a>'
        )
        blocks.append(
            f'<article class="plugin-block" data-text="{escape(haystack.lower())}">'
            '<div class="pb-head"><div>'
            f'<h3 class="pb-title">{escape(p.get("name", ""))}'
            f'<span class="pb-ver">{escape(p.get("version", ""))}</span>'
            f'<span class="pc-status is-{escape(status)}">{escape(STATUS_TEXT.get(status, status))}</span>'
            "</h3>"
            f'<p class="pb-desc">{escape(p.get("summary", ""))}</p>'
            f'<div class="pc-tags"><span class="pc-tag pc-tag-mc">Minecraft {escape(p.get("mc", ""))}</span>{tags}</div>'
            f'</div><div class="pb-actions">{actions}</div></div>'
            f'<div class="pb-docs">{docs}</div>'
            "</article>"
        )
    if not blocks:
        return '<div class="plugin-empty">还没有上架的插件。</div>'
    return "".join(blocks)


def render_filter() -> str:
    return (
        '<div class="plugin-filter">'
        '<input id="pluginFilter" type="search" '
        'placeholder="搜插件名或标签，比如「签到」「经济」" autocomplete="off">'
        '<span class="filter-count" id="pluginCount"></span>'
        "</div>"
    )


def render_meta(site: dict, plugin_id: str) -> str:
    plugin = next((p for p in site.get("plugins", []) if p["id"] == plugin_id), None)
    if not plugin:
        return ""
    status = plugin.get("status", "stable")
    chips = (
        f'<span class="meta-chip"><b>版本</b>{escape(plugin.get("version", ""))}</span>'
        f'<span class="meta-chip"><b>适用</b>Minecraft {escape(plugin.get("mc", ""))}</span>'
        f'<span class="meta-chip"><b>状态</b>{escape(STATUS_TEXT.get(status, status))}</span>'
        f'<span class="meta-chip"><b>更新</b>{escape(plugin.get("updated", ""))}</span>'
    )
    if plugin.get("repo"):
        chips += (
            f'<a class="meta-chip meta-chip-link" href="{escape(plugin["repo"])}" '
            'target="_blank" rel="noopener">源码</a>'
        )
    chips += (
        f'<a class="meta-chip meta-chip-link" href="{escape(plugin.get("download", ""))}" '
        'target="_blank" rel="noopener">下载 jar</a>'
    )
    return f'<div class="meta-bar">{chips}</div>'


def render_tabs(plugin: dict | None, active_slug: str, root: str) -> str:
    if not plugin:
        return ""
    tabs = []
    for page in plugin["pages"]:
        cls = "ptab is-active" if page["slug"] == active_slug else "ptab"
        tabs.append(
            f'<a class="{cls}" href="{root}{page["slug"]}">'
            f'{escape(page.get("short", page["title"]))}</a>'
        )
    return f'<nav class="plugin-tabs">{"".join(tabs)}</nav>'


def render_crumb(page: dict, root: str) -> str:
    parts = [f'<a href="{root}index.html">首页</a>']
    plugin = page.get("plugin")
    if plugin:
        parts.append(f'<span class="sep">/</span><a href="{root}plugins.html">插件库</a>')
        parts.append(f'<span class="sep">/</span><span>{escape(plugin["fullName"])}</span>')
        parts.append(f'<span class="sep">/</span><span class="cur">{escape(page["title"])}</span>')
        return "".join(parts)
    if page["slug"] != "index.html":
        if page["group"] != "开始":
            parts.append(f'<span class="sep">/</span><span>{escape(page["group"])}</span>')
        parts.append(f'<span class="sep">/</span><span class="cur">{escape(page["title"])}</span>')
    return "".join(parts)


def apply_placeholders(text: str, site: dict, root: str) -> str:
    if "[[STATS]]" in text:
        text = text.replace("[[STATS]]", "\n\n" + render_stats(site) + "\n\n")
    if "[[PLUGINS_TOP]]" in text:
        text = text.replace(
            "[[PLUGINS_TOP]]", "\n\n" + render_plugin_blocks(site, root, 3) + "\n\n"
        )
    if "[[PLUGINS]]" in text:
        block = render_filter() + render_plugin_blocks(site, root)
        text = text.replace("[[PLUGINS]]", "\n\n" + block + "\n\n")
    for match in set(re.findall(r"\[\[META:([a-z0-9_-]+)\]\]", text)):
        text = text.replace(f"[[META:{match}]]", "\n\n" + render_meta(site, match) + "\n\n")
    return text


PAGE_TMPL = """<!DOCTYPE html>
<html lang="zh-CN" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {site_title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="{root}assets/icon.svg">
<link rel="apple-touch-icon" href="{root}assets/icon.svg">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<header class="topbar">
  <button class="menu-btn" id="menuBtn" aria-label="菜单">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  </button>
  <a class="brand" href="{root}index.html">
    <img class="brand-mark" src="{root}assets/icon.svg" width="28" height="28" alt="">
    <span class="brand-text">{site_title}</span>
  </a>
  <div class="topbar-right">
    <button class="search-btn" id="searchBtn" type="button">
      <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span>搜索文档</span>
      <kbd>/</kbd>
    </button>
    <a class="gh-link" href="{repo}" target="_blank" rel="noopener" aria-label="GitHub 仓库">
      <svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
    </a>
  </div>
</header>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <nav class="nav">{nav}</nav>
    <div class="sidebar-foot">
      <a class="btn-download" href="{root}custom.html">插件定制</a>
      <div class="sidebar-contact">QQ {qq}</div>
    </div>
  </aside>
  <main class="main">
    <div class="crumb">{crumb}</div>
    {tabs}
    <article class="markdown">{content}</article>
    <footer class="pagefoot">
      <div>承接所有版本 Minecraft 服务端插件定制 · 需求直说，工期和报价也直说</div>
      <div>QQ <a href="https://wpa.qq.com/msgrd?v=3&uin={qq}&site=qq&menu=yes" target="_blank" rel="noopener">{qq}</a> · 邮箱 <a href="mailto:{email}">{email}</a></div>
    </footer>
  </main>
  <aside class="toc" id="toc">
    <div class="toc-title">本页目录</div>
    {toc}
  </aside>
</div>
<div class="search-modal" id="searchModal" hidden>
  <div class="search-panel">
    <div class="search-head">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <input id="searchInput" type="search" placeholder="搜索文档标题、配置项、指令…" autocomplete="off">
      <button id="searchClose" type="button" aria-label="关闭">ESC</button>
    </div>
    <div class="search-results" id="searchResults"></div>
  </div>
</div>
<script src="{root}assets/app.js"></script>
</body>
</html>
"""


def main() -> int:
    site = load_site()
    pages, alias = collect(site)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(SRC / "assets", OUT / "assets")

    index = []

    for page in pages:
        src_file = PAGES / page["source"]
        if not src_file.exists():
            print(f"[missing] {src_file}")
            return 1
        raw = src_file.read_text(encoding="utf-8")
        raw = rewrite_links(raw, page["slug"], alias)

        slug = page["slug"]
        depth = len(posixpath.dirname(slug).split("/")) if posixpath.dirname(slug) else 0
        root = "../" * depth

        raw = apply_placeholders(raw, site, root)

        md = markdown.Markdown(
            extensions=[
                "fenced_code",
                "tables",
                "sane_lists",
                "attr_list",
                TocExtension(toc_depth="2-3", anchorlink=False),
            ]
        )
        body = md.convert(raw)
        body = re.sub(
            r'<a href="(https?://[^"]+)"',
            r'<a target="_blank" rel="noopener" href="\1"',
            body,
        )
        toc_html = build_toc(md.toc_tokens)

        page_title = page["title"]
        if page.get("plugin"):
            page_title = f'{page["plugin"]["name"]} · {page_title}'

        html_out = PAGE_TMPL.format(
            root=root,
            title=escape(page_title),
            site_title=escape(site["siteTitle"]),
            desc=escape(page.get("desc", site["description"])),
            repo=site["repo"],
            qq=site["qq"],
            email=site["email"],
            nav=render_nav(site, slug, root),
            crumb=render_crumb(page, root),
            tabs=render_tabs(page.get("plugin"), slug, root),
            content=body,
            toc=toc_html or '<div class="toc-empty">本页暂无小标题</div>',
        )

        target = OUT / slug
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html_out, encoding="utf-8")

        index.append(
            {
                "t": page["title"],
                "u": slug,
                "g": page["group"],
                "x": plain_text(raw)[:1200],
            }
        )
        print(f"[ok] {slug}")

    (OUT / "assets" / "search-index.json").write_text(
        json.dumps(index, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"[done] {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
