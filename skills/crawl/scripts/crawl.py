#!/usr/bin/env python3
"""
Crawl a documentation website into a local .agents/skills/<name> directory.

Flow:
  1. Try path-scoped sitemaps for the given docs URL
  2. Try origin-level sitemaps
  3. Discover links from SSR/static HTML sidebars/app payloads
  4. Merge all discovery results so partial sitemaps do not hide richer nav data
  5. Fetch each page, extract main content, convert to markdown via markitdown
  6. Write .md files in a directory tree + a raw SKILL.md with page references

Usage:
  python3 crawl.py <URL> [--name NAME] [--limit N]
  python3 crawl.py check <URL>

Examples:
  python3 crawl.py https://docs.polymarket.com/
  python3 crawl.py https://docs.polymarket.com/trading/ --name polymarket-trading
  python3 crawl.py check https://docs.example.com/

Requirements:
  pip install beautifulsoup4 markitdown
"""

import argparse
import html as html_lib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# ISO 639-1 two-letter language codes (common subset)
LOCALE_CODES = frozenset(
    {
        "aa",
        "ab",
        "af",
        "ak",
        "am",
        "an",
        "ar",
        "as",
        "av",
        "ay",
        "az",
        "ba",
        "be",
        "bg",
        "bh",
        "bi",
        "bm",
        "bn",
        "bo",
        "br",
        "bs",
        "ca",
        "ce",
        "ch",
        "cn",
        "co",
        "cr",
        "cs",
        "cu",
        "cv",
        "cy",
        "da",
        "de",
        "dv",
        "dz",
        "ee",
        "el",
        "en",
        "eo",
        "es",
        "et",
        "eu",
        "fa",
        "ff",
        "fi",
        "fj",
        "fo",
        "fr",
        "fy",
        "ga",
        "gd",
        "gl",
        "gn",
        "gu",
        "gv",
        "ha",
        "he",
        "hi",
        "ho",
        "hr",
        "ht",
        "hu",
        "hy",
        "hz",
        "ia",
        "id",
        "ie",
        "ig",
        "ii",
        "ik",
        "io",
        "is",
        "it",
        "iu",
        "ja",
        "jv",
        "ka",
        "kg",
        "ki",
        "kj",
        "kk",
        "kl",
        "km",
        "kn",
        "ko",
        "kr",
        "ks",
        "ku",
        "kv",
        "kw",
        "ky",
        "la",
        "lb",
        "lg",
        "li",
        "ln",
        "lo",
        "lt",
        "lu",
        "lv",
        "mg",
        "mh",
        "mi",
        "mk",
        "ml",
        "mn",
        "mr",
        "ms",
        "mt",
        "my",
        "na",
        "nb",
        "nd",
        "ne",
        "ng",
        "nl",
        "nn",
        "no",
        "nr",
        "nv",
        "ny",
        "oc",
        "oj",
        "om",
        "or",
        "os",
        "pa",
        "pi",
        "pl",
        "ps",
        "pt",
        "qu",
        "rm",
        "rn",
        "ro",
        "ru",
        "rw",
        "sa",
        "sc",
        "sd",
        "se",
        "sg",
        "si",
        "sk",
        "sl",
        "sm",
        "sn",
        "so",
        "sq",
        "sr",
        "ss",
        "st",
        "su",
        "sv",
        "sw",
        "ta",
        "te",
        "tg",
        "th",
        "ti",
        "tk",
        "tl",
        "tn",
        "to",
        "tr",
        "ts",
        "tt",
        "tw",
        "ty",
        "ug",
        "uk",
        "ur",
        "uz",
        "ve",
        "vi",
        "vo",
        "wa",
        "wo",
        "xh",
        "yi",
        "yo",
        "za",
        "zh",
        "zu",
    }
)

SITEMAP_FILENAMES = ("sitemap.xml", "sitemap_index.xml", "sitemap-index.xml")

BLOCKED_PAGE_EXTENSIONS = frozenset(
    {
        ".7z",
        ".avi",
        ".avif",
        ".css",
        ".csv",
        ".dmg",
        ".doc",
        ".docx",
        ".eot",
        ".gif",
        ".gz",
        ".ico",
        ".jpeg",
        ".jpg",
        ".js",
        ".json",
        ".map",
        ".mov",
        ".mp3",
        ".mp4",
        ".otf",
        ".pdf",
        ".png",
        ".rar",
        ".rss",
        ".svg",
        ".tar",
        ".tgz",
        ".ttf",
        ".txt",
        ".wasm",
        ".webm",
        ".webmanifest",
        ".webp",
        ".woff",
        ".woff2",
        ".xml",
        ".zip",
    }
)

# Shared MarkItDown instance, loaded lazily so `check` mode can run without it.
_converter = None


def make_soup(html):
    """Create a BeautifulSoup parser, reporting the dependency only when needed."""
    if BeautifulSoup is None:
        print("ERROR: beautifulsoup4 required. Run: pip install beautifulsoup4")
        sys.exit(1)
    return BeautifulSoup(html, "html.parser")


@dataclass
class DiscoveryReport:
    """Discovery results and counts for user-visible reporting."""

    urls: List[str]
    path_sitemap_urls: Set[str] = field(default_factory=set)
    origin_sitemap_urls: Set[str] = field(default_factory=set)
    html_urls: Set[str] = field(default_factory=set)
    path_sitemaps_found: List[str] = field(default_factory=list)
    origin_sitemaps_found: List[str] = field(default_factory=list)
    html_pages_fetched: int = 0
    html_error: Optional[str] = None


# --- Sitemap fetching ----------------------------------------


class RedirectHandler(urllib.request.HTTPRedirectHandler):
    """Follow modern redirects such as 308 Permanent Redirect."""

    def http_error_307(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, code, msg, headers)

    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, code, msg, headers)


_opener = urllib.request.build_opener(RedirectHandler)


def open_url(req, timeout=30, redirects=5):
    """Open a URL request with crawler redirect behavior."""
    try:
        return _opener.open(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        if e.code in {301, 302, 303, 307, 308} and redirects > 0:
            location = e.headers.get("Location")
            if location:
                redirected = urljoin(req.full_url, location)
                new_req = urllib.request.Request(
                    redirected,
                    headers=dict(req.header_items()),
                    method="GET",
                )
                return open_url(new_req, timeout=timeout, redirects=redirects - 1)
        raise


def fetch_sitemap_content(url):
    """Fetch a URL (sitemap XML) and return its content as string."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; CrawlSkill/1.0)",
            "Accept": "text/xml, application/xml, */*",
        },
    )
    with open_url(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_sitemap(xml_text):
    """Parse a sitemap XML and return list of <loc> URLs."""
    urls = []
    xml_text = re.sub(r'\s+xmlns\s*=\s*"[^"]*"', "", xml_text, count=1)
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return urls

    for sitemap in root.findall(".//sitemap"):
        loc = sitemap.find("loc")
        if loc is not None and loc.text:
            urls.append(("sitemap_index", loc.text.strip()))

    for url_elem in root.findall(".//url"):
        loc = url_elem.find("loc")
        if loc is not None and loc.text:
            urls.append(("url", loc.text.strip()))

    return urls


def unique_in_order(items):
    """Return items without duplicates while preserving first-seen order."""
    seen = set()
    result = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def sitemap_candidates(origin, base_path, scope):
    """Build sitemap URLs for the docs path or site origin."""
    origin = origin.rstrip("/")
    if scope == "path" and base_path != "/":
        prefix = origin + base_path.rstrip("/")
    else:
        prefix = origin
    return [prefix.rstrip("/") + "/" + name for name in SITEMAP_FILENAMES]


def fetch_sitemap_tree(sitemap_url, seen=None, depth=0):
    """Fetch a sitemap or sitemap index recursively and return page URLs."""
    if seen is None:
        seen = set()
    if sitemap_url in seen or depth > 8:
        return []
    seen.add(sitemap_url)

    try:
        xml_text = fetch_sitemap_content(sitemap_url)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return []

    entries = parse_sitemap(xml_text)
    if not entries:
        return []

    urls = []
    for entry_type, url in entries:
        if entry_type == "sitemap_index":
            urls.extend(fetch_sitemap_tree(url, seen, depth + 1))
        else:
            urls.append(url)
    return urls


def fetch_sitemap_urls(candidates):
    """Fetch sitemap candidates and return (page URLs, sitemap URLs that worked)."""
    all_urls = []
    found_sitemaps = []
    seen_sitemaps = set()

    for sitemap_url in candidates:
        urls = fetch_sitemap_tree(sitemap_url, seen_sitemaps)
        if not urls:
            continue
        found_sitemaps.append(sitemap_url)
        all_urls.extend(urls)

    return unique_in_order(all_urls), found_sitemaps


# Selectors for sidebar / navigation containers across common doc frameworks.
# Kept separate from STRIP_SELECTORS — those are what we *remove* when extracting
# article content; these are what we *read* to discover pages.
NAV_SELECTORS = [
    "nav",
    "aside",
    '[role="navigation"]',
    ".sidebar",
    ".nav-sidebar",
    ".docs-sidebar",
    ".left-sidebar",
    ".menu",
    ".main-menu",
    ".docs-menu",
    ".docs-nav",
    ".navigation",
    ".nav-tree",
    ".toc-sidebar",
    "#sidebar",
    "#nav",
    "#navigation",
    "#docs-sidebar",
    # Framework-specific
    ".theme-doc-sidebar-container",  # Docusaurus
    ".sidebar-content",
    ".nextra-sidebar",  # Nextra
    ".menu-list",  # GitBook / Bulma
    ".VPSidebar",  # VitePress
    ".md-nav",
    ".md-sidebar",  # MkDocs Material
]


def ensure_url(url):
    """Add https:// when the user passes a bare domain."""
    if re.match(r"^https?://", url, flags=re.IGNORECASE):
        return url
    return "https://" + url


def canonicalize_page_url(url):
    """Canonicalize a page URL for dedupe and local link rewriting."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return None

    path = parsed.path or "/"
    path = re.sub(r"/{2,}", "/", path)
    path = re.sub(r"/index\.html?$", "/", path, flags=re.IGNORECASE)
    path = re.sub(r"\.html?$", "", path, flags=re.IGNORECASE)
    path = path.rstrip("/")
    if not path:
        path = "/"

    if path == "/":
        return f"{parsed.scheme}://{parsed.netloc}"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def path_matches_base(path, base_path):
    """Return True when path is exactly base_path or below it."""
    base = "/" + base_path.strip("/")
    if base == "/":
        return True
    current = path.rstrip("/") or "/"
    return current == base or current.startswith(base + "/")


def is_probable_page_url(url):
    """Filter obvious non-page assets from sitemaps and page links."""
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    return suffix not in BLOCKED_PAGE_EXTENSIONS


def normalize_discovered_url(raw_url, page_url):
    """Resolve and canonicalize a discovered link against a source page."""
    raw_url = (
        raw_url.strip()
        .replace("\\/", "/")
        .replace("\\u002F", "/")
        .replace("\\u002f", "/")
    )
    if not raw_url:
        return None
    if "\\" in raw_url or re.search(r"\s", raw_url):
        return None
    if raw_url.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None

    resolved = urljoin(page_url, raw_url)
    resolved = resolved.split("#")[0].split("?")[0]
    return canonicalize_page_url(resolved)


def looks_like_url_candidate(value):
    """Return True for strings that are intentionally URL-like."""
    value = value.strip()
    return value.startswith(("http://", "https://", "/", "./", "../"))


def url_in_scope(url, origin, base_path):
    """Return True if URL is same-origin, under base_path, and page-like."""
    parsed = urlparse(url)
    origin_parsed = urlparse(origin)
    if parsed.netloc != origin_parsed.netloc:
        return False
    if not path_matches_base(parsed.path or "/", base_path):
        return False
    return is_probable_page_url(url)


def _normalize_link(href, page_url):
    """Resolve a link's href against the current page URL, return same-origin absolute URL or None.

    page_url is the URL of the page the link was found on — needed to resolve
    relative paths like 'ai/agent-panel.html' (common in mdbook, Sphinx, etc).

    Also strips '.html'/'.htm' suffixes so '/foo' and '/foo.html' (which servers
    like mdbook treat as the same resource) collapse to a single canonical URL.
    """
    normalized = normalize_discovered_url(href, page_url)
    if not normalized:
        return None

    if urlparse(normalized).netloc != urlparse(page_url).netloc:
        return None
    return normalized


def extract_nav_links(html, page_url):
    """Pull links from sidebar/navigation containers only.

    More targeted than scraping every <a> on the page — sidebars in doc sites
    typically mirror the full content hierarchy, which is exactly what we want.
    """
    soup = make_soup(html)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    links = set()
    for selector in NAV_SELECTORS:
        try:
            containers = soup.select(selector)
        except Exception:
            continue
        for nav in containers:
            for a in nav.find_all("a", href=True):
                normalized = _normalize_link(a["href"], page_url)
                if normalized:
                    links.add(normalized)
    return links


def extract_all_page_links(html, page_url):
    """Broad fallback: every internal link on the page, regardless of container.

    Use when nav extraction yields too few links (site doesn't match known
    sidebar selectors). Noisier — may include footer/header links.
    """
    soup = make_soup(html)
    links = set()
    for a in soup.find_all("a", href=True):
        normalized = _normalize_link(a["href"], page_url)
        if normalized:
            links.add(normalized)
    return links


def _walk_json_strings(value):
    """Yield every string nested inside JSON-ish app data."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _walk_json_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_json_strings(item)


def extract_structured_links(html, page_url):
    """Extract links from SSR framework data and preload tags.

    Some server-rendered documentation sites keep route trees in JSON or RSC
    script payloads rather than in a recognizable sidebar container. This does
    not execute JavaScript, but it catches links already shipped in the HTML.
    """
    soup = make_soup(html)
    links = set()

    for tag in soup.find_all(["link", "meta"]):
        candidate = tag.get("href") or tag.get("content")
        if not candidate or not looks_like_url_candidate(candidate):
            continue
        normalized = normalize_discovered_url(candidate, page_url)
        if normalized:
            links.add(normalized)

    link_pattern = re.compile(
        r"""(?P<quote>["'`])(?P<link>(?:https?://|/)[^"'`<>\s]+)(?P=quote)"""
    )

    for script in soup.find_all("script"):
        text = script.string or script.get_text(" ", strip=False)
        if not text:
            continue

        if (script.get("type") or "").lower() in {
            "application/json",
            "application/ld+json",
        }:
            try:
                parsed = json.loads(text)
                for value in _walk_json_strings(parsed):
                    if not looks_like_url_candidate(value):
                        continue
                    normalized = normalize_discovered_url(value, page_url)
                    if normalized:
                        links.add(normalized)
            except json.JSONDecodeError:
                pass

        unescaped = (
            text.replace("\\/", "/")
            .replace("\\u002F", "/")
            .replace("\\u002f", "/")
            .replace('\\"', '"')
            .replace("&quot;", '"')
        )
        for match in link_pattern.finditer(unescaped):
            normalized = normalize_discovered_url(match.group("link"), page_url)
            if normalized:
                links.add(normalized)

    return links


# --- Filtering ------------------------------------------------


def filter_by_base_path(urls, base_path, origin=None):
    """Keep only page URLs whose path is exactly base_path or below it."""
    filtered = []
    for url in urls:
        canonical = canonicalize_page_url(url)
        if not canonical:
            continue
        if origin and not url_in_scope(canonical, origin, base_path):
            continue
        if not origin:
            parsed = urlparse(canonical)
            if not path_matches_base(parsed.path or "/", base_path):
                continue
            if not is_probable_page_url(canonical):
                continue
        filtered.append(canonical)
    return unique_in_order(filtered)


def deduplicate_localized(urls, base_path):
    """Remove localized duplicates where first path segment is a locale code."""
    canonical_paths = set()
    for url in urls:
        path = urlparse(url).path
        canonical_paths.add(path.rstrip("/"))

    deduplicated = []
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        segments = path.split("/")

        if len(segments) >= 2 and segments[0] in LOCALE_CODES:
            non_localized_path = "/" + "/".join(segments[1:])
            if non_localized_path.rstrip("/") in canonical_paths:
                continue

        deduplicated.append(url)

    return deduplicated


# --- File tree building ---------------------------------------


def url_to_filepath(url, base_path):
    """Convert a URL to a relative .md file path based on the base path."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    bp = base_path.rstrip("/")
    if path == bp or path == bp + "/":
        return "index.md"

    relative = path[len(bp) :].lstrip("/")
    if not relative:
        return "index.md"

    return relative + ".md"


# --- Content extraction (BS4 cleanup + markitdown) ------------

STRIP_SELECTORS = [
    "nav",
    "header",
    "footer",
    "aside",
    "script",
    "style",
    "noscript",
    "svg",
    '[role="navigation"]',
    '[role="banner"]',
    '[role="contentinfo"]',
    ".sidebar",
    ".toc",
    ".table-of-contents",
    ".nav-sidebar",
    ".navbar",
    ".top-bar",
    ".site-header",
    ".site-footer",
    ".breadcrumb",
    ".breadcrumbs",
    ".prev-next",
    ".pagination",
    ".pager",
    ".page-nav",
    ".edit-page",
    ".edit-on-github",
    ".page-edit",
    ".feedback",
    ".was-helpful",
    ".thumbs-up",
    ".page-feedback",
    ".cookie-banner",
    ".announcement-bar",
    ".banner",
    ".search-bar",
    ".search",
    ".algolia-search",
    ".skip-to-content",
    ".skip-link",
    ".theme-toggle",
    ".color-mode",
    ".on-this-page",
    ".toc-sidebar",
]

MAIN_SELECTORS = [
    "main article",
    "article",
    "main",
    '[role="main"]',
    ".markdown-body",
    ".docs-content",
    ".main-content",
    ".content",
    ".prose",
    "#content",
    "#main-content",
    ".doc-content",
    ".page-content",
]

EMBEDDED_SKIP_STRINGS = frozenset(
    {
        "$",
        "$undefined",
        "children",
        "className",
        "currentColor",
        "data",
        "data-card",
        "depth",
        "div",
        "errorScripts",
        "errorStyles",
        "external",
        "false",
        "file",
        "forbidden",
        "href",
        "h1",
        "h2",
        "head",
        "height",
        "html",
        "icon",
        "id",
        "isMenu",
        "items",
        "geometricPrecision",
        "Link to section",
        "meta",
        "name",
        "next",
        "next-size-adjust",
        "null",
        "notFound",
        "page",
        "parallelRouterKey",
        "path",
        "promise",
        "ref",
        "rel",
        "search",
        "shapeRendering",
        "single",
        "slug",
        "svg",
        "style",
        "strokeLinecap",
        "strokeLinejoin",
        "strokeWidth",
        "target",
        "templateScripts",
        "templateStyles",
        "toc",
        "title",
        "true",
        "type",
        "unauthorized",
        "url",
        "viewBox",
        "width",
        "xmlns",
        "noreferrer noopener",
    }
)


def to_markdown(html_str):
    """Convert an HTML string to markdown using markitdown."""
    global _converter
    if _converter is None:
        try:
            from markitdown import MarkItDown
        except (ImportError, AttributeError):
            return html_to_markdown_basic(html_str)
        _converter = MarkItDown()

    stream = io.BytesIO(html_str.encode("utf-8"))
    try:
        result = _converter.convert_stream(stream, file_extension=".html")
        return result.text_content
    except Exception:
        return html_to_markdown_basic(html_str)


def clean_inline_text(text):
    """Normalize inline whitespace."""
    return re.sub(r"\s+", " ", text).strip()


def render_table(table):
    """Render a basic markdown table."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [
            clean_inline_text(cell.get_text(" ", strip=True))
            for cell in tr.find_all(["th", "td"])
        ]
        if cells:
            rows.append(cells)
    if not rows:
        return []

    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines = ["| " + " | ".join(rows[0]) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def render_html_node(node, lines):
    """Render a subset of HTML blocks as markdown."""
    name = getattr(node, "name", None)
    if not name:
        return

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        text = clean_inline_text(node.get_text(" ", strip=True))
        if text:
            level = int(name[1])
            lines.append("#" * level + " " + text)
        return

    if name == "p":
        text = clean_inline_text(node.get_text(" ", strip=True))
        if text:
            lines.append(text)
        return

    if name == "pre":
        code = node.get_text("\n", strip=False).strip()
        if code:
            lines.extend(["```", code, "```"])
        return

    if name in {"ul", "ol"}:
        ordered = name == "ol"
        for index, li in enumerate(node.find_all("li", recursive=False), start=1):
            text = clean_inline_text(li.get_text(" ", strip=True))
            if text:
                prefix = f"{index}. " if ordered else "- "
                lines.append(prefix + text)
        return

    if name == "blockquote":
        text = node.get_text("\n", strip=True)
        for line in text.splitlines():
            clean = clean_inline_text(line)
            if clean:
                lines.append("> " + clean)
        return

    if name == "table":
        lines.extend(render_table(node))
        return

    for child in getattr(node, "children", []):
        render_html_node(child, lines)


def html_to_markdown_basic(html_str):
    """Small dependency-light fallback for environments without MarkItDown."""
    soup = make_soup(html_str)
    root = soup.body or soup
    lines = []
    for child in root.children:
        before = len(lines)
        render_html_node(child, lines)
        if len(lines) > before and lines[-1] != "":
            lines.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def fetch_page(url):
    """Fetch an HTML page and return its content."""
    html, _final_url = fetch_page_with_final_url(url)
    return html


def fetch_page_with_final_url(url):
    """Fetch an HTML page and return (content, final URL after redirects)."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
    )
    with open_url(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace"), resp.geturl()


def extract_main_content(html):
    """Extract main documentation content from HTML and return as markdown."""
    soup = make_soup(html)

    for selector in STRIP_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    main = None
    for selector in MAIN_SELECTORS:
        main = soup.select_one(selector)
        if main:
            break
    if not main:
        main = soup.body or soup

    raw_md = to_markdown(str(main))

    cleaned = re.sub(r"\n{3,}", "\n\n", raw_md).strip()
    if cleaned:
        return cleaned
    return extract_embedded_markdown(html)


def decode_js_string_literal(value):
    """Decode the inside of a JavaScript string literal."""
    try:
        return json.loads('"' + value + '"')
    except json.JSONDecodeError:
        return value


def should_keep_embedded_text(value):
    """Filter framework metadata from embedded SSR/RSC strings."""
    value = clean_inline_text(html_lib.unescape(value))
    if not value or value in EMBEDDED_SKIP_STRINGS:
        return False
    if len(value) == 1:
        return False
    if len(value) > 2000:
        return False
    if not any(ch.isalpha() for ch in value):
        return False
    if looks_like_url_candidate(value) or value.startswith(("data:", "mailto:", "tel:")):
        return False
    if value.startswith("#") or "[" in value or "]" in value:
        return False
    if ":" in value and " " not in value:
        return False
    if value.startswith(("$", "_next/", "static/", "chunks/", "lucide ")):
        return False
    if value.startswith(("--", "_", "<")) or value.startswith("aria-"):
        return False
    if re.match(r"^[0-9a-f]+:I\[", value) or value.startswith(":HL["):
        return False
    if re.fullmatch(r"[0-9][A-Za-z0-9_-]+", value):
        return False
    if re.fullmatch(r"[a-z][a-z0-9_-]+", value):
        return False
    if re.fullmatch(r"[A-Za-z]+(?:Scripts|Styles)", value):
        return False
    if re.fullmatch(r"#[0-9a-fA-F]{3,8}", value):
        return False
    if re.search(r"\.(?:css|js|json|mdx|png|svg|webp|woff2?)$", value):
        return False
    if re.fullmatch(r"[A-Za-z0-9_-]{12,}", value) and not re.search(r"[aeiouAEIOU]", value):
        return False
    if re.fullmatch(r"[A-Za-z0-9_-]{13,}", value) and " " not in value:
        return False
    if len(value) > 5 and value[0] in {"M", "m"}:
        digit_count = sum(ch.isdigit() for ch in value)
        if digit_count > len(value) * 0.15:
            return False
    if "_" in value and " " not in value and len(value) > 20:
        return False
    if len(value) > 80 and any(marker in value for marker in ("[", "]", ":", "/", "&", "*")):
        return False
    if re.fullmatch(r"[-_A-Za-z0-9:/\[\]!'().%# ]+", value):
        tokens = value.split()
        if len(tokens) >= 2 and any(any(ch in token for ch in "-:/[]!%#") for token in tokens):
            return False
    if value.count("{") + value.count("}") > 8:
        return False
    return True


def extract_script_payloads(script_text):
    """Decode Next/RSC pushed string payloads from a script."""
    payloads = []
    pattern = re.compile(r"self\.__next_f\.push\(\[1,\"((?:\\.|[^\"\\])*)\"\]\)")
    for match in pattern.finditer(script_text):
        payloads.append(decode_js_string_literal(match.group(1)))
    return payloads


def extract_embedded_markdown(html):
    """Last-resort text extraction for SSR/RSC pages without normal body HTML."""
    soup = make_soup(html)
    lines = []
    seen = set()

    title = soup.find("title")
    if title:
        text = clean_inline_text(title.get_text(" ", strip=True))
        if text:
            lines.extend(["# " + text, ""])
            seen.add(text)

    description = soup.find("meta", attrs={"name": "description"})
    if description and description.get("content"):
        text = clean_inline_text(description["content"])
        if text and text not in seen:
            lines.extend([text, ""])
            seen.add(text)

    string_pattern = re.compile(r'"((?:\\.|[^"\\])*)"')
    for script in soup.find_all("script"):
        script_text = script.string or script.get_text(" ", strip=False)
        if "__next_f" not in script_text:
            continue

        for payload in extract_script_payloads(script_text):
            content_start = payload.find('"toc"')
            if content_start == -1:
                content_start = payload.find('"children":[["$","h1"')
            if content_start == -1:
                continue
            payload = payload[content_start:]

            for match in string_pattern.finditer(payload):
                value = decode_js_string_literal(match.group(1))
                for part in value.splitlines():
                    text = clean_inline_text(part)
                    if not should_keep_embedded_text(text):
                        continue
                    if text in seen:
                        continue
                    lines.append(text)
                    seen.add(text)
                    if len(lines) >= 800:
                        break
                if len(lines) >= 800:
                    break
            if len(lines) >= 800:
                break

    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


# --- Crawling -------------------------------------------------


def rewrite_links(content, url_to_local, path_to_local, base_url):
    """Replace doc URLs in markdown content with relative local paths.

    Handles absolute URLs (https://...), root-relative paths (/docs/...),
    and preserves #fragment anchors.
    """
    origin = urlparse(base_url)
    origin_base = f"{origin.scheme}://{origin.netloc}"

    def replace_url(m):
        matched = m.group(0)
        raw = matched.split("#")[0].rstrip("/")
        fragment = "#" + matched.split("#", 1)[1] if "#" in matched else ""
        local = url_to_local.get(raw)
        if local:
            return local + fragment
        return matched

    def replace_path(m):
        matched = m.group(1)
        raw = matched.split("#")[0].rstrip("/")
        fragment = "#" + matched.split("#", 1)[1] if "#" in matched else ""
        local = path_to_local.get(raw)
        if local:
            return "(" + local + fragment + ")"
        return m.group(0)

    # Pass 1: full absolute URLs (https://domain.com/docs/page)
    abs_pattern = re.escape(origin_base) + r"/[^\s\)\]\"\'><]*"
    content = re.sub(abs_pattern, replace_url, content)

    # Pass 2: root-relative paths in markdown links — ](/docs/page)
    rel_pattern = r"\((/[^\s\)\"\'><]+)\)"
    content = re.sub(rel_pattern, replace_path, content)

    return content


def sort_urls(urls):
    """Sort URLs in a stable docs-friendly order."""
    def key(url):
        parsed = urlparse(url)
        path = parsed.path or "/"
        return (path.count("/"), path)

    return sorted(unique_in_order(urls), key=key)


def discover_html_urls(entry_url, origin, base_path, discover_limit):
    """Discover in-scope docs pages from server-rendered/static HTML."""
    queue = deque([entry_url])
    visited = set()
    discovered = set()
    pages_fetched = 0
    first_error = None

    while queue and len(visited) < discover_limit:
        current = canonicalize_page_url(queue.popleft())
        if not current or current in visited:
            continue
        if not url_in_scope(current, origin, base_path):
            continue

        visited.add(current)
        try:
            html, final_url = fetch_page_with_final_url(current)
        except Exception as e:
            if first_error is None:
                first_error = str(e)
            continue

        pages_fetched += 1
        discovered.add(current)
        context = final_url.split("#", 1)[0] if final_url else current

        nav_links = extract_nav_links(html, context)
        structured_links = extract_structured_links(html, context)
        broad_links = extract_all_page_links(html, context)

        candidates = nav_links | structured_links
        if len(candidates) < 5:
            candidates |= broad_links

        for link in candidates:
            if not url_in_scope(link, origin, base_path):
                continue
            discovered.add(link)
            if link not in visited:
                queue.append(link)

    return discovered, pages_fetched, first_error


def discover_urls(url, discover_limit):
    """Discover crawl targets by merging sitemap and static HTML results."""
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    base_path = parsed.path.rstrip("/") or "/"
    entry_url = canonicalize_page_url(url) or origin

    with ThreadPoolExecutor(max_workers=3) as executor:
        path_future = None
        if base_path != "/":
            path_future = executor.submit(
                fetch_sitemap_urls, sitemap_candidates(origin, base_path, "path")
            )
        origin_future = executor.submit(
            fetch_sitemap_urls, sitemap_candidates(origin, base_path, "origin")
        )
        html_future = executor.submit(
            discover_html_urls, entry_url, origin, base_path, discover_limit
        )

        path_raw, path_found = path_future.result() if path_future else ([], [])
        origin_raw, origin_found = origin_future.result()
        html_urls, html_pages_fetched, html_error = html_future.result()

    path_urls = set(filter_by_base_path(path_raw, base_path, origin))
    origin_urls = set(filter_by_base_path(origin_raw, base_path, origin))

    combined = path_urls | origin_urls | html_urls
    deduplicated = deduplicate_localized(sort_urls(combined), base_path)

    return DiscoveryReport(
        urls=deduplicated,
        path_sitemap_urls=path_urls,
        origin_sitemap_urls=origin_urls,
        html_urls=html_urls,
        path_sitemaps_found=path_found,
        origin_sitemaps_found=origin_found,
        html_pages_fetched=html_pages_fetched,
        html_error=html_error,
    )


def crawl_pages(urls, skill_dir, base_path, limit=None):
    """Fetch all URLs, extract main content, write .md files. Returns list of successful filepaths."""
    if limit:
        urls = urls[:limit]

    # Build lookup maps for link rewriting
    url_to_local = {}  # full URL -> local path
    path_to_local = {}  # root-relative path -> local path
    for url in urls:
        filepath = url_to_filepath(url, base_path)
        normalized = url.split("#")[0].rstrip("/")
        url_to_local[normalized] = filepath
        path_to_local[urlparse(url).path.rstrip("/") or "/"] = filepath

    pages = []
    raw_contents = {}
    total = len(urls)
    print(f"\nCrawling {total} pages...")

    # Pass 1: fetch and convert all pages
    for i, url in enumerate(urls):
        filepath = url_to_filepath(url, base_path)
        print(f"  [{i + 1}/{total}] {filepath}...", end=" ", flush=True)

        try:
            html = fetch_page(url)
            content = extract_main_content(html)
            if content:
                raw_contents[url] = (filepath, content)
                pages.append(filepath)
                print(f"ok ({len(content)} chars)")
            else:
                print("empty (no content extracted)")
        except Exception as e:
            print(f"fail ({e})")

    # Pass 2: rewrite links and write files
    origin = urlparse(urls[0])
    base_url = f"{origin.scheme}://{origin.netloc}"
    print(f"\nRewriting links in {len(raw_contents)} pages...")

    for url, (filepath, content) in raw_contents.items():
        full_path = skill_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        content = rewrite_links(content, url_to_local, path_to_local, base_url)
        full_path.write_text(content, encoding="utf-8")

    return pages


# --- Main -----------------------------------------------------


def derive_skill_name(url):
    """Derive a skill name from the URL domain."""
    parsed = urlparse(url)
    host = parsed.hostname or ""
    for prefix in ["docs.", "doc.", "developer.", "developers.", "api.", "www."]:
        if host.startswith(prefix):
            host = host[len(prefix) :]
    name = host.split(".")[0]
    return slugify_skill_name(name or "crawled-docs")


def slugify_skill_name(name):
    """Normalize a user-provided or derived skill name."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "crawled-docs"


def build_skill_md(skill_name, base_url, domain, pages):
    """Generate a raw SKILL.md with frontmatter and page listing."""
    lines = [
        "---",
        f"name: {skill_name}",
        f'description: "Documentation for {domain}. Use when the user asks about {skill_name}, references {domain}, or needs docs from {base_url}."',
        "---",
        "",
        f"# {skill_name} Documentation",
        "",
        f"> {len(pages)} pages crawled from [{base_url}]({base_url})",
        "",
        "## Pages",
        "",
    ]

    # Group pages by directory for a hierarchical listing
    dirs = {}
    for filepath in sorted(pages):
        parent = str(Path(filepath).parent)
        if parent == ".":
            parent = ""
        dirs.setdefault(parent, []).append(filepath)

    for dir_name in sorted(dirs.keys()):
        if dir_name:
            lines.append(f"### {dir_name}/")
            lines.append("")
        for filepath in dirs[dir_name]:
            title = Path(filepath).stem.replace("-", " ").replace("_", " ").title()
            lines.append(f"- [{title}]({filepath})")
        lines.append("")

    lines.append("## Lookup")
    lines.append("")
    lines.append("1. Find the relevant section in Pages above")
    lines.append("2. Read that file with the Read tool")
    lines.append("3. If the answer spans sections, read multiple files")
    lines.append("")

    return "\n".join(lines)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Crawl a documentation website into .agents/skills/<name>"
    )
    parser.add_argument(
        "positionals",
        nargs="+",
        metavar="ARG",
        help="'check <URL>' to list pages, or '<URL>' to crawl",
    )
    parser.add_argument("--name", help="Skill name (default: derived from domain)")
    parser.add_argument("--limit", type=int, help="Max pages to crawl")
    parser.add_argument(
        "--discover-limit",
        type=int,
        default=250,
        help="Max HTML pages to fetch while discovering SSR/static links",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only discover and print page URLs; do not crawl or write files",
    )
    args = parser.parse_args(argv)

    positionals = args.positionals
    if positionals[0] == "check":
        args.check = True
        if len(positionals) < 2:
            parser.error("check mode requires a URL")
        url = positionals[1]
        extras = positionals[2:]
    else:
        url = positionals[0]
        extras = positionals[1:]
        if extras == ["check"]:
            args.check = True
            extras = []

    if extras:
        parser.error("unexpected positional argument(s): " + " ".join(extras))

    args.url = ensure_url(url)
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        parser.error(f"invalid URL: {url}")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be greater than 0")
    if args.discover_limit < 1:
        parser.error("--discover-limit must be greater than 0")
    return args


def print_discovery_summary(report, base_path):
    """Print concise discovery counts."""
    if base_path != "/":
        if report.path_sitemaps_found:
            print(
                f"Path sitemap:   {len(report.path_sitemap_urls)} in-scope URLs "
                f"from {len(report.path_sitemaps_found)} sitemap(s)"
            )
        else:
            print("Path sitemap:   none found")
    else:
        print("Path sitemap:   same as origin for root path")

    if report.origin_sitemaps_found:
        print(
            f"Origin sitemap: {len(report.origin_sitemap_urls)} in-scope URLs "
            f"from {len(report.origin_sitemaps_found)} sitemap(s)"
        )
    else:
        print("Origin sitemap: none found")

    print(
        f"HTML discovery: {len(report.html_urls)} URLs "
        f"from {report.html_pages_fetched} fetched page(s)"
    )
    if report.html_error and report.html_pages_fetched == 0:
        print(f"HTML error:     {report.html_error}")

    sources = [
        ("path sitemap", len(report.path_sitemap_urls)),
        ("origin sitemap", len(report.origin_sitemap_urls)),
        ("HTML discovery", len(report.html_urls)),
    ]
    best_name, best_count = max(sources, key=lambda item: item[1])
    if best_count:
        print(f"Best source:    {best_name} ({best_count} URLs)")
    print(f"Combined:       {len(report.urls)} unique URLs")


def main():
    args = parse_args()

    parsed = urlparse(args.url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    base_path = parsed.path.rstrip("/") or "/"
    domain = parsed.netloc
    base_url = origin if base_path == "/" else origin + base_path

    skill_name = slugify_skill_name(args.name) if args.name else derive_skill_name(args.url)
    skill_dir = Path.cwd() / ".agents" / "skills" / skill_name

    print(f"Origin:    {origin}")
    print(f"Base path: {base_path}")
    print(f"Skill:     {skill_name}")
    print(f"Output:    {skill_dir}")

    print("\nDiscovering pages...")
    report = discover_urls(args.url, args.discover_limit)
    print_discovery_summary(report, base_path)

    if not report.urls:
        print("ERROR: No URLs found for the given base path.")
        print(
            "The site may require client-side JavaScript rendering, or the entry URL "
            "may not point at the docs section."
        )
        sys.exit(1)

    urls_to_use = report.urls
    if args.limit:
        urls_to_use = urls_to_use[: args.limit]
        print(f"Limit:     using first {len(urls_to_use)} of {len(report.urls)} URLs")

    if args.check:
        print(f"\nPages found ({len(urls_to_use)}):")
        for url in urls_to_use:
            print(url)
        print(f"\nCRAWL_CHECK|{len(urls_to_use)}")
        return

    skill_dir.mkdir(parents=True, exist_ok=True)
    pages = crawl_pages(urls_to_use, skill_dir, base_path)

    if not pages:
        print("ERROR: No pages were successfully crawled.")
        sys.exit(1)

    skill_md = build_skill_md(skill_name, base_url, domain, pages)
    skill_path = skill_dir / "SKILL.md"
    skill_path.write_text(skill_md, encoding="utf-8")
    print(f"\nSKILL.md written to {skill_path}")

    print(f"\nCRAWL_COMPLETE|{skill_dir}|{len(pages)}")


if __name__ == "__main__":
    main()
