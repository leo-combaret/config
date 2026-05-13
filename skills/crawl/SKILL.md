---
name: crawl
description: "Crawl a documentation website and create a Claude Code skill with clean, hierarchical content. Triggers on 'crawl', 'scrape docs', 'turn this site into a skill', 'create skill from website', 'crawl documentation', or when the user gives a docs URL and wants it available as a skill."
argument-hint: ["url", "check https://docs.example.com/"]
---

# Crawl — Website-to-Skill Generator

Two-phase workflow: a Python script crawls pages and generates a raw SKILL.md (Phase 1), then you read the docs and rewrite it into a proper skill (Phase 2).

## Phase 1: Crawl

Run the crawler from the directory where the user wants the generated skill to live. It discovers URLs, fetches each page, strips site chrome, converts to markdown, writes `.md` files, and generates a raw `SKILL.md` with all page references under the caller's local `.agents/skills/<skill-name>/` directory.

**Discovery strategy**:
1. **Path sitemap** — for an entry like `https://zed.dev/docs/`, tries `https://zed.dev/docs/sitemap.xml`, `sitemap_index.xml`, and `sitemap-index.xml` (handles sitemap index files with nested children)
2. **Origin sitemap** — tries the same sitemap names at the site root, such as `https://zed.dev/sitemap.xml`, then filters to the requested docs base path
3. **SSR/static HTML discovery** — fetches the entry URL and extracts links from sidebar/nav containers (`nav`, `aside`, `[role="navigation"]`, `.sidebar`, `.docs-sidebar`, Docusaurus/Nextra/VitePress/MkDocs selectors), JSON/RSC script payloads, preload/meta tags, and finally all internal links on discovered docs pages.

The crawler runs these techniques together and merges the unique in-scope URLs, so a partial sitemap does not suppress richer sidebar/static HTML discovery. This handles path-specific sitemaps, broad site sitemaps, missing or incomplete sitemaps, and server-rendered documentation sites whose route trees are present in HTML. For Next/RSC pages with no normal body HTML, the crawler also attempts a best-effort text extraction from server-sent flight payloads. It does not execute client-side JavaScript; if a docs app only reveals links or content after JS runs, report that limitation.

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py <URL> [OPTIONS]
```

To only inspect what would be crawled, use `check` mode:

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py check <URL> [OPTIONS]
```

`check` mode prints the discovered page URLs and exits without creating files.

| Flag | Default | Description |
|------|---------|-------------|
| `--name` | from domain | Skill name (kebab-case) |
| `--limit` | all | Max pages to crawl |
| `--discover-limit` | 250 | Max HTML pages to fetch during SSR/static discovery |
| `--check` | false | Same as the `check` positional command; list pages only |

The script prints `CRAWL_COMPLETE|<skill_dir>|<page_count>` on successful crawl. Parse this to get the skill directory path and page count.

The script prints `CRAWL_CHECK|<page_count>` in check mode. Report the listed pages to the user if they asked to inspect discovery.

If the script fails, report the error to the user and stop.

**Requirements:** `beautifulsoup4` (`pip install beautifulsoup4`), Python 3.8+. If a compatible `markitdown` package is installed, the crawler uses it for higher-fidelity HTML conversion; otherwise it falls back to a built-in BeautifulSoup-based converter.

---

## Phase 2: Build the Skill (YOU do this)

The crawler already wrote a raw `SKILL.md` at `<skill_dir>/SKILL.md` with frontmatter and a flat page listing. Your job is to read the docs and rewrite it into a well-crafted skill.

### Step 1: Read and understand the documentation

1. Read `<skill_dir>/SKILL.md` to get the page listing
2. Read a representative sample of the doc files (index, getting-started, key API pages) — enough to understand what the documentation covers, its structure, and its key topics
3. For large doc sets (>30 pages), read at least 5-10 files spanning different sections

### Step 2: Rewrite SKILL.md

Rewrite `<skill_dir>/SKILL.md` with:

```markdown
---
name: {skill_name}
description: "Documentation for {domain}. Use when the user asks about {skill_name}, references {domain}, or needs API docs, concepts, or guides from {base_url}. Trigger on mentions of '{skill_name}', '{domain}', or {key topics you identified}."
---

# {Skill Title} Documentation

> {page_count} pages from [{base_url}]({base_url})

## Overview

{2-4 sentences summarizing what this documentation covers, what the tool/library does, and its main use cases. Written from reading the actual docs, not generic.}

## Contents

{hierarchical TOC — indented entries matching directory structure}
{format each entry as: "- [Descriptive Title](relative/path.md)"}
{use indentation (2 spaces per level) to show nesting}
{group related pages under section headings when the structure is flat}

## Lookup

1. Find the relevant section in Contents above
2. Read that file with the Read tool
3. If the answer spans sections, read multiple files
```

Key points:
- The **description** field in frontmatter is critical — it determines when the skill triggers. Include the skill name, domain, and the key topics/keywords you identified from reading the docs.
- The **Overview** should be specific to this documentation, not generic boilerplate.
- The **Contents** TOC should use descriptive titles derived from reading the actual page content (first `#` heading), not just filename-to-title-case.
- Organize the TOC hierarchically to match the doc structure.

### Step 3: Report

Tell the user:
- Skill created at `<skill_dir>/`
- N pages organized into M sections
- Show the Contents from the generated SKILL.md

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No in-scope sitemap URLs found | SSR/static HTML discovery can still provide pages. Script proceeds if any source finds links. |
| Path sitemap missing | Origin sitemap and SSR/static HTML discovery are still checked and filtered to the requested base path. |
| Sitemap is incomplete | Sitemap URLs are merged with SSR/static HTML URLs, so richer sidebar discovery can fill the gaps. |
| Sidebar selectors don't match | Script reads JSON/RSC route data and then falls back to same-origin `<a>` tags. |
| 0 URLs from all sources | Script exits with error. Suggest a different entry URL, broader base path, or JS-rendering support. |
| Single page | Write as `index.md`, minimal SKILL.md. |
| Client-side JS-rendered SPA (no SSR/static links) | Discovery and content extraction will be empty. Tell user the site requires JavaScript rendering. |

## Troubleshooting

- **"No URLs found for the given base path"** — The site is likely JS-rendered (no static HTML links), or the entry URL is wrong. Try a deeper docs URL where the sidebar is rendered server-side.
- **Sitemap had URLs but few were on the right base path** — The sitemap covers the full site. The crawler will still merge in HTML discovery, but a more specific URL (e.g. `https://x.com/docs/api/` instead of `https://x.com/`) can improve filtering.
- **HTML discovery found few URLs** — Either the entry page genuinely has no nav, or it's client-side rendered. Inspect the page source manually.
- **Missing dependencies** — Run `pip install beautifulsoup4`; optionally install a compatible `markitdown` for richer conversion.
- **Empty pages during crawl** — Site is JS-rendered or blocking requests. The crawler can't execute JavaScript.
- **Blocked by site** — The crawler uses a browser-like User-Agent but some sites check more aggressively.
