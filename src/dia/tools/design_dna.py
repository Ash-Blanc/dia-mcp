"""Extract visual design tokens from any live site."""

from __future__ import annotations

import json
from typing import Any

import asyncio
from dia.clients import firecrawl as fc


def _branding_to_dict(branding: Any) -> dict | None:
    """Convert a BrandingProfile Pydantic model or dict to a plain dict."""
    if branding is None:
        return None
    if isinstance(branding, dict):
        return branding
    if hasattr(branding, "model_dump"):
        return branding.model_dump(exclude_none=True)
    return vars(branding) if hasattr(branding, "__dict__") else None


async def extract_design_dna(url: str) -> str:
    """
    🧬 Extract the design system of any live website.

    Returns: color palette, typography, spacing, button styles.
    Understand the RELATIONSHIPS between tokens — not to copy values.
    """
    result = await asyncio.to_thread(fc.scrape, url, formats=["branding", "screenshot"])

    branding = result.get("branding")
    branding_dict = _branding_to_dict(branding)
    screenshot = result.get("screenshot")

    return json.dumps(
        {
            "url": url,
            "design_dna": branding_dict,
            "has_screenshot": screenshot is not None,
            "interpretation_guide": (
                "Study RELATIONSHIPS: heading-to-body size ratio, "
                "primary-to-accent color contrast, spacing scale. "
                "These proportional relationships make a system cohesive — "
                "use them as inspiration for YOUR OWN token system."
            ),
        },
        indent=2,
    )
