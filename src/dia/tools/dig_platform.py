"""Deep-dive a specific inspiration platform via TinyFish."""

from __future__ import annotations

import json

from dia.clients import tinyfish as tf
from dia.sources import SOURCES


async def dig_platform(
    platform: str,
    query: str,
    filters: str = "",
    limit: int = 8,
) -> str:
    """
    🕵️ Deep-dive into Mobbin / Refero / Godly using an AI web agent.

    The agent navigates filters, scrolls galleries, opens details,
    and extracts image URLs + metadata — like a human designer.

    Args:
        platform: "mobbin" | "refero" | "godly" | "screenlane" | "collectui"
        query: e.g. "onboarding flow fintech"
        filters: Extra filter instructions, e.g. "iOS only", "dark mode"
        limit: How many results to extract
    """
    src = SOURCES.get(platform)
    if src is None:
        return json.dumps({"error": f"Unknown platform: {platform}"})

    url = src.search_url or src.url
    if "{query}" in url:
        url = url.format(query=query.replace(" ", "+"), platform="web")

    goal = (
        f"You are a World-Class Design Curator. Navigate this inspiration platform and search for '{query}'. "
        f"{f'Apply these filters precisely: {filters}. ' if filters else ''}"
        f"Curate the top {limit} most inspirational and representative designs. "
        f"For each result, extract high-quality metadata as valid JSON: "
        f'{{"results": [{{'
        f'"title": "descriptive title", "image_url": "direct URL to the image", '
        f'"app_name": "name of the app or product", "screen_type": "type of screen (e.g. Empty State)", '
        f'"tags": ["relevant design tokens/tags"], "page_url": "source page URL", '
        f'"curator_note": "expert reasoning for why this design is noteworthy"'
        f"}}]}}"
    )

    result = await tf.run_agent(url, goal, stealth=True)

    return json.dumps(
        {
            "platform": platform,
            "query": query,
            "filters": filters,
            "agent_result": result.get("resultJson", result),
            "status": result.get("status", "unknown"),
            "usage_note": (
                "These are references from real shipped products. "
                "Analyze the PATTERNS and PRINCIPLES, not the pixels."
            ),
        },
        indent=2,
    )
