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

The crawler runs these techniques together and merges the unique in-scope URLs, so a partial sitemap does not suppress richer sidebar/static HTML discovery. This handles path-specific sitemaps, broad site sitemaps, missing or incomplete sitemaps, and server-rendered documentation sites whose route trees are present in HTML. For Next/RSC pages with no normal body HTML, the crawler also attempts a best-effort text extraction from server-sent flight payloads.

By default, the crawler first uses direct browser-like HTTP requests for speed. If an HTML page fetch fails with browser-verification, WAF, timeout, or HTTP errors such as `431`, it automatically launches a temporary real Chromium process with Chrome DevTools Protocol (CDP), retries the page in the browser, and reuses that browser for the rest of the crawl. Use `--browser-cdp auto` to force browser rendering from the start, `--browser-executable` to point at a specific Chrome/Chromium binary, or `--no-browser-fallback` to disable automatic browser retry. If a site returns static shell HTML successfully but only populates links/content after client-side JavaScript, force `--browser-cdp auto`.

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
| `--scope-url` | entry URL | URL whose path defines crawl scope. Use when the seed URL is a deep page but the docs sidebar covers a broader section. |
| `--url-file` | none | Newline-delimited list of additional URLs to merge into discovery. Use when a site blocks discovery but you can export or otherwise obtain the URL tree. |
| `--url-file-only` | false | Crawl only URLs from `--url-file`, skipping sitemap and HTML discovery. Use for curated URL exports where rendered nav discovers adjacent pages you do not want. |
| `--header` | none | Extra request header in `Name: value` form. Can be repeated. |
| `--cookie` | none | Cookie header value to send with page and sitemap requests. Useful after obtaining a browser session that can access a protected docs site. |
| `--write-fetch-errors` | false | Write transparent error pages for URLs that are discovered but fail to fetch. |
| `--browser-cdp` | automatic fallback | Use Chrome DevTools Protocol to fetch rendered page HTML. Pass `auto` to launch a temporary Chromium from the start, or pass an existing websocket endpoint, browser URL/port, or profile directory containing `DevToolsActivePort`. Useful for JavaScript-rendered docs or WAF/browser-verification edge cases. |
| `--browser-executable` | auto-detect | Chrome/Chromium executable to use for automatic CDP launch. The crawler checks `CRAWL_BROWSER_EXECUTABLE`, common system Chrome/Chromium paths, and Playwright-installed Chromium. |
| `--no-browser-fallback` | false | Disable automatic Chromium/CDP retry when direct HTML fetches fail. |
| `--discover-limit` | 250 | Max HTML pages to fetch during SSR/static discovery |
| `--check` | false | Same as the `check` positional command; list pages only |

When a docs URL is a leaf page but the desired crawl should include the
surrounding guide tree, pass the leaf as the positional URL and the broader
root as `--scope-url`:

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py \
  https://developer.example.com/docs/guides/quick-start/getting-started \
  --scope-url https://developer.example.com/docs/guides/
```

When a site blocks crawler discovery with browser verification, WAF behavior,
or errors such as `HTTP 431`, the crawler should automatically retry failed
HTML fetches through a temporary Chromium/CDP browser. If the site returns an
empty app shell instead of an error, force browser rendering from the start:

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py \
  https://developer.example.com/docs/ \
  --browser-cdp auto
```

When a protected site still requires an authenticated browser session, use
`--url-file` for the exported URL tree and `--cookie`/`--header` for a browser
session that can fetch those pages. Without valid access headers, the crawler
can discover URLs from the file but cannot extract protected page content.
If cookies are tied to browser fingerprinting, use `--browser-cdp` with an
already-open Chrome/Chromium instance that can access the docs:

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py \
  https://developer.example.com/docs/ \
  --url-file urls.txt \
  --browser-cdp 9222
```

For browsers using a profile-specific `DevToolsActivePort` file, pass the
profile directory or the websocket endpoint printed in that file:

```bash
python3 ~/.agents/skills/crawl/scripts/crawl.py \
  https://developer.example.com/docs/page \
  --scope-url https://developer.example.com/docs/ \
  --url-file urls.txt \
  --url-file-only \
  --browser-cdp "/path/to/browser/profile"
```

The script prints `CRAWL_COMPLETE|<skill_dir>|<page_count>` on successful crawl. Parse this to get the skill directory path and page count.

The script prints `CRAWL_CHECK|<page_count>` in check mode. Report the listed pages to the user if they asked to inspect discovery.

If the script fails, report the error to the user and stop.

**Requirements:** `beautifulsoup4` (`pip install beautifulsoup4`), Python 3.8+. If a compatible `markitdown` package is installed, the crawler uses it for higher-fidelity HTML conversion; otherwise it falls back to a built-in BeautifulSoup-based converter.

Automatic CDP fallback requires a Chrome/Chromium executable. In Codex Desktop, the crawler can usually reuse the bundled Playwright Chromium. Outside Codex, install Chrome/Chromium, run `playwright install chromium`, set `CRAWL_BROWSER_EXECUTABLE`, or pass `--browser-executable /path/to/chrome`.

---

## Phase 2: Build the Skill (YOU do this)

The crawler already wrote a raw `SKILL.md` at `<skill_dir>/SKILL.md` with frontmatter and a flat page listing. Your job is to read the docs and rewrite it into a well-crafted skill.

### Step 1: Read and understand the documentation

1. Read `<skill_dir>/SKILL.md` to get the page listing
2. Read a representative sample of the doc files (index, getting-started, key API pages) — enough to understand what the documentation covers, its structure, and its key topics
3. For large doc sets (>30 pages), read at least 5-10 files spanning different sections

### Step 2: Rewrite SKILL.md

Rewrite `<skill_dir>/SKILL.md` with the lookup workflow before the table of contents:

```markdown
---
name: {skill_name}
description: "Documentation for {domain}. Use when the user asks about {skill_name}, references {domain}, or needs API docs, concepts, configuration, examples, migrations, troubleshooting, or guides from {base_url}. Trigger on mentions of '{skill_name}', '{domain}', or {key topics you identified}."
---

# {Skill Title} Documentation

> {page_count} pages from [{base_url}]({base_url})

This `SKILL.md` is an index, not the full documentation. The actual docs are the linked markdown files in this skill folder.

## Required Lookup

When this skill triggers for a documentation question:

1. Search this skill folder or choose the relevant entry from Contents.
2. Read at least one linked `.md` file before answering API, syntax, configuration, behavior, migration, or troubleshooting questions.
3. Read multiple files when the answer spans concepts, examples, reference pages, or framework integrations.
4. Treat the local markdown files as the source of truth. If the local docs do not cover the question, say that instead of filling gaps from memory.

## Overview

{2-4 sentences summarizing what this documentation covers, what the tool/library does, and its main use cases. Written from reading the actual docs, not generic.}

## Contents

{hierarchical TOC — indented entries matching directory structure}
{format each entry as: "- [Descriptive Title](relative/path.md)"}
{use indentation (2 spaces per level) to show nesting}
{group related pages under section headings when the structure is flat}

## Search Hints

- Use the Contents section when the topic maps cleanly to a page.
- Use text search inside this skill folder when the topic could appear in many pages, for example `rg -n "<api-or-topic>" .`.
- Prefer files with exact API names, component names, config keys, or error messages.
```

Key points:
- The **description** field in frontmatter is critical — it determines when the skill triggers. Include the skill name, domain, and the key topics/keywords you identified from reading the docs.
- The **Overview** should be specific to this documentation, not generic boilerplate.
- The **Contents** TOC should use descriptive titles derived from reading the actual page content (first `#` heading), not just filename-to-title-case.
- Organize the TOC hierarchically to match the doc structure.
- Put **Required Lookup** before the overview and Contents so it is seen before the agent scans the page list.
- Do not paste large chunks of docs into `SKILL.md`; keep it an index with strong retrieval instructions.

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
| Client-side JS-rendered SPA (no SSR/static links) | Retry with `--browser-cdp auto` so Chromium executes the app before extraction. If content is still empty, report that the crawler cannot extract the rendered docs. |

## Troubleshooting

- **"No URLs found for the given base path"** — The site is likely JS-rendered (no static HTML links), or the entry URL is wrong. Try a deeper docs URL where the sidebar is rendered server-side.
- **Sitemap had URLs but few were on the right base path** — The sitemap covers the full site. The crawler will still merge in HTML discovery, but a more specific URL (e.g. `https://x.com/docs/api/` instead of `https://x.com/`) can improve filtering.
- **HTML discovery found few URLs** — Either the entry page genuinely has no nav, or it returned a static app shell without triggering browser fallback. Retry with `--browser-cdp auto`.
- **Missing dependencies** — Run `pip install beautifulsoup4`; optionally install a compatible `markitdown` for richer conversion.
- **Automatic browser fallback unavailable** — Install Chrome/Chromium, run `playwright install chromium`, set `CRAWL_BROWSER_EXECUTABLE`, pass `--browser-executable`, or pass `--browser-cdp` for an already-running browser.
- **Empty pages during crawl** — Site may be JS-rendered or blocking requests. Retry with `--browser-cdp auto`; if that still fails, use an authenticated browser session with `--browser-cdp`.
- **Blocked by site** — The crawler uses direct browser-like requests first, then Chromium/CDP fallback for failed HTML fetches. For stricter sites, open the docs in a browser profile that has access and pass that profile or CDP endpoint with `--browser-cdp`.
