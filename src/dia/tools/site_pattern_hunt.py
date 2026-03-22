"""Tool — smart extensive search for UI/UX patterns across a whole site."""

from __future__ import annotations

import json
import asyncio
from dia.clients import firecrawl as fc


async def site_pattern_hunt(
    url: str,
    limit: int = 10,
    focus: str = "core product experience and visual language",
) -> str:
    """
    🕵️ Smartly and extensively hunt for UI/UX patterns across a particular website.

    Uses an autonomous crawler to find the most high-signal pages (pricing, onboarding,
    dashboard, settings) and extracts design DNA + expert observations from each.

    Args:
        url: Starting URL (e.g. "https://linear.app")
        limit: Max number of pages to analyze (default 10)
        focus: Specific design area to focus on
    """
    prompt = (
        f"You are a Senior Design Critic. Explore this site to find the most "
        f"representative UI/UX patterns related to: {focus}. "
        f"Identify high-signal pages like pricing, feature overviews, and app screens. "
        f"For each page, extract the visual hierarchy, unique design tokens, "
        f"and core interaction patterns."
    )

    # Firecrawl V2 crawl with prompt and branding extraction
    crawl_result = await asyncio.to_thread(
        fc.crawl,
        url,
        limit=limit,
        prompt=prompt,
        formats=["markdown", "screenshot", "branding"],
    )

    pages = []
    # crawl_result is typically a list of documents in v2 SDK
    items = crawl_result if isinstance(crawl_result, list) else getattr(crawl_result, "data", [])

    for doc in items:
        d = doc if isinstance(doc, dict) else getattr(doc, "__dict__", {})
        meta = d.get("metadata", {})
        if isinstance(meta, object) and not isinstance(meta, dict):
            meta = getattr(meta, "__dict__", {})

        pages.append({
            "url": d.get("url") or meta.get("sourceURL"),
            "title": meta.get("title"),
            "design_dna": d.get("branding"),
            "analysis_preview": (d.get("markdown") or "")[:500],
            "has_screenshot": d.get("screenshot") is not None
        })

    return json.dumps(
        {
            "site_url": url,
            "pages_analyzed": len(pages),
            "hunt_results": pages,
            "summary_instruction": (
                "Review these pages to synthesize the site's overall DESIGN SYSTEM. "
                "Look for consistency in spacing, typography scales, and component "
                "behavior across different contexts (landing vs. app)."
            )
        },
        indent=2,
    )
