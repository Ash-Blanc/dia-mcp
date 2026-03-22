"""Tool — intelligent color palette recommendations based on design trends."""

from __future__ import annotations

import json
import asyncio
from dia.clients import firecrawl as fc


async def recommend_colors(
    query: str,
    limit: int = 5,
) -> str:
    """
    🎨 Get expert color palette recommendations for a specific design context.

    Uses a 'Senior Color Strategist' persona to find trending palettes across design
    platforms and synthesizes them with color theory rationale.

    Args:
        query: e.g. "fintech trust and security", "vibrant social app", "minimalist organic skincare"
        limit: Number of distinct palette options to return
    """
    prompt = (
        f"You are a Senior Color Strategist and Brand Architect. Search the web for "
        f"trending and high-quality color palettes related to: '{query}'. "
        f"Look at sites like Coolors, Muzli, Dribbble, and Adobe Color. "
        f"For each recommended palette, extract: "
        f"1. A list of HEX codes. "
        f"2. A name for the palette. "
        f"3. Color Theory Rationale: Why do these colors work for this specific query? "
        f"What emotions do they evoke? How do they balance contrast and accessibility?"
    )

    # Use Firecrawl Search to find actual trending results
    search_query = f"{query} color palette trends 2026 design inspiration"
    results = await asyncio.to_thread(
        fc.search,
        search_query,
        limit=limit,
        prompt=prompt,
        formats=["markdown"]
    )

    palettes = []
    for r in results:
        # We use the markdown content which now contains the 'Senior Color Strategist' analysis
        palettes.append({
            "source_url": r.get("url"),
            "source_title": r.get("metadata", {}).get("title"),
            "expert_recommendation": r.get("markdown")
        })

    return json.dumps(
        {
            "query": query,
            "palettes": palettes,
            "accessibility_note": (
                "Remember to check contrast ratios (WCAG 2.1) when pairing these "
                "colors for text and background elements. Use tools like 'Are My Colors Accessible' "
                "to verify the specific HEX combinations."
            )
        },
        indent=2,
    )
