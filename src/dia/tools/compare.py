"""Side-by-side competitive screenshot comparison."""

from __future__ import annotations

import json

import asyncio
from dia.clients import firecrawl as fc


async def compare_uis(
    urls: str,
    focus: str = "overall layout",
    mobile: bool = False,
) -> str:
    """
    🎯 Screenshot multiple live products side by side for comparison.

    Args:
        urls: Comma-separated URLs, e.g.
              "stripe.com/pricing, linear.app/pricing, notion.so/pricing"
        focus: What to study — "pricing cards", "nav structure", "CTA placement"
        mobile: Capture mobile versions
    """
    url_list = [u.strip() for u in urls.split(",") if u.strip()]

    batch = await asyncio.to_thread(
        fc.batch_scrape,
        url_list,
        formats=["screenshot@fullPage", "markdown"],
        mobile=mobile,
    )

    items = batch.get("data", []) if isinstance(batch, dict) else batch
    comparisons = []
    for doc in items:
        d = doc if isinstance(doc, dict) else doc.__dict__
        comparisons.append(
            {
                "url": d.get("metadata", {}).get("sourceURL", ""),
                "title": d.get("metadata", {}).get("title", ""),
                "has_screenshot": d.get("screenshot") is not None,
            }
        )

    return json.dumps(
        {
            "focus": focus,
            "mobile": mobile,
            "screenshots_captured": sum(1 for c in comparisons if c["has_screenshot"]),
            "comparisons": comparisons,
            "analysis_prompt": (
                f"Compare these {len(comparisons)} products on: {focus}. "
                "For each: 1) Visual hierarchy, 2) Info density, "
                "3) Unique decisions, 4) PRINCIPLES to borrow (not pixels)."
            ),
        },
        indent=2,
    )
