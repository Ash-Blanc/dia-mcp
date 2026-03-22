"""Firecrawl client — thin wrappers around the SDK."""

from __future__ import annotations

from typing import Any

from firecrawl import Firecrawl

from dia.config import FIRECRAWL_API_KEY

_fc: Firecrawl | None = None


def _client() -> Firecrawl:
    global _fc
    if _fc is None:
        _fc = Firecrawl(api_key=FIRECRAWL_API_KEY)
    return _fc


# ── Helpers ──────────────────────────────────────────────────


def _doc_to_dict(doc: Any) -> dict[str, Any]:
    """Convert a Firecrawl Document (Pydantic model or dict) to a plain dict."""
    if isinstance(doc, dict):
        return doc
    d: dict[str, Any] = {}
    d["markdown"] = getattr(doc, "markdown", None)
    d["screenshot"] = getattr(doc, "screenshot", None)
    d["links"] = getattr(doc, "links", None)
    d["branding"] = getattr(doc, "branding", None)
    d["url"] = getattr(doc, "url", None)
    # Normalise metadata to a plain dict
    meta = getattr(doc, "metadata", None)
    if meta is None:
        d["metadata"] = {}
    elif isinstance(meta, dict):
        d["metadata"] = meta
    else:
        # DocumentMetadata Pydantic model — use source_url (snake_case in v2)
        d["metadata"] = {
            "sourceURL": getattr(meta, "source_url", None)
            or getattr(meta, "url", None)
            or "",
            "title": getattr(meta, "title", None) or "",
            "description": getattr(meta, "description", None) or "",
        }
    return d


def _search_result_to_dict(item: Any) -> dict[str, Any]:
    """Convert a SearchResultWeb / SearchResultNews / Document to a plain dict."""
    if isinstance(item, dict):
        url = item.get("url", "")
        return {
            "url": url,
            "metadata": {
                "sourceURL": url,
                "title": item.get("title", ""),
                "description": item.get("description", ""),
            },
            "markdown": item.get("markdown", ""),
            "screenshot": item.get("screenshot"),
        }
    # Pydantic model (SearchResultWeb, SearchResultNews, Document etc.)
    url = getattr(item, "url", None) or ""
    markdown = getattr(item, "markdown", None) or ""
    screenshot = getattr(item, "screenshot", None)
    meta = getattr(item, "metadata", None)
    if meta is None:
        source_url = url
        title = getattr(item, "title", "") or ""
    elif isinstance(meta, dict):
        source_url = meta.get("sourceURL") or meta.get("source_url") or url
        title = meta.get("title", "")
    else:
        source_url = getattr(meta, "source_url", None) or url
        title = getattr(meta, "title", None) or getattr(item, "title", "") or ""
    return {
        "url": source_url or url,
        "metadata": {"sourceURL": source_url or url, "title": title},
        "markdown": markdown,
        "screenshot": screenshot,
    }


# ── Primitives ───────────────────────────────────────────────


def search(
    query: str,
    *,
    limit: int = 5,
    formats: list[str] | None = None,
    prompt: str | None = None,
    schema: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    opts: dict[str, Any] = {}
    if formats:
        opts["formats"] = formats
    if prompt:
        opts["prompt"] = prompt
    if schema:
        opts["schema"] = schema

    result = _client().search(query, limit=limit, scrape_options=opts)  # type: ignore[arg-type]
    if result is None:
        return []
    # SDK v2 returns SearchData(web=List[SearchResultWeb|Document], ...)
    if hasattr(result, "web") and result.web:
        return [_search_result_to_dict(item) for item in result.web]
    # Fallback: if it's already a list
    if isinstance(result, list):
        return [_search_result_to_dict(item) for item in result]
    return []


def scrape(
    url: str,
    *,
    formats: list[str] | None = None,
    actions: list[dict[str, Any]] | None = None,
    mobile: bool = False,
    prompt: str | None = None,
    schema: dict[str, Any] | None = None,
    model: str = "spark-1-mini",
) -> dict[str, Any]:
    formats = formats or ["markdown", "screenshot"]
    kwargs: dict[str, Any] = {"formats": formats, "model": model}
    if actions:
        kwargs["actions"] = actions
    if mobile:
        kwargs["mobile"] = True
    if prompt:
        kwargs["prompt"] = prompt
    if schema:
        kwargs["schema"] = schema

    result = _client().scrape(url, **kwargs)
    return _doc_to_dict(result)


def map_urls(url: str) -> list[str]:
    result = _client().map(url)  # type: ignore[return-value]
    if hasattr(result, "urls"):
        return result.urls or []  # type: ignore[return-value]
    return []


def batch_scrape(
    urls: list[str],
    *,
    formats: list[str] | None = None,
    mobile: bool = False,
) -> dict[str, Any]:
    formats = formats or ["screenshot", "markdown"]
    kwargs: dict[str, Any] = {
        "formats": formats,
        "poll_interval": 2,
        "wait_timeout": 120,
    }
    if mobile:
        kwargs["mobile"] = True
    result = _client().batch_scrape(urls, **kwargs)
    # SDK v2 returns a Pydantic model — normalise to {"data": [...]}
    if isinstance(result, dict):
        raw_data = result.get("data", []) or []
        return {"data": [_doc_to_dict(d) for d in raw_data]}
    if hasattr(result, "data") and result.data is not None:
        return {"data": [_doc_to_dict(d) for d in result.data]}
    return {"data": []}


def crawl(
    url: str,
    *,
    limit: int = 10,
    prompt: str | None = None,
    formats: list[str] | None = None,
) -> Any:
    """
    Crawl a website and extract data from multiple pages.

    Args:
        url: Starting URL.
        limit: Max pages to crawl.
        prompt: Optional prompt to guide the crawl/extraction.
        formats: Formats to extract (e.g. ["markdown", "screenshot"]).
    """
    kwargs: dict[str, Any] = {"limit": limit}
    if prompt:
        kwargs["scrape_options"] = {"prompt": prompt}
    if formats:
        if "scrape_options" not in kwargs:
            kwargs["scrape_options"] = {}
        kwargs["scrape_options"]["formats"] = formats

    # The SDK crawl() method in v2 handles the polling automatically
    # and returns the completed crawl data.
    return _client().crawl(url, **kwargs)


def extract_branding(url: str) -> Any:
    doc = scrape(url, formats=["branding", "screenshot"])
    return doc.get("branding")


def run_agent(
    prompt: str,
    *,
    urls: list[str] | None = None,
    schema: dict[str, Any] | None = None,
    model: str = "spark-1-mini",
    max_credits: int = 2500,
) -> Any:
    """
    Run the Firecrawl autonomous agent.

    Args:
        prompt: Natural language goal.
        urls: Optional list of URLs to focus on.
        schema: Optional JSON schema for extraction.
        model: "spark-1-mini" or "spark-1-pro".
        max_credits: Maximum credits to consume.
    """
    kwargs: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "max_credits": max_credits,
    }
    if urls:
        kwargs["urls"] = urls
    if schema:
        kwargs["schema"] = schema

    return _client().agent(**kwargs)
