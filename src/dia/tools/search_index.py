"""Tool — search the UI/UX Research Index."""

from __future__ import annotations

import json

from dia.index.db import search_patterns


async def search_index(
    query: str = "",
    category: str = "",
    tags: str = "",
    limit: int = 20,
) -> str:
    """🔎 Search the UI/UX Research Index."""
    results = await search_patterns(
        query=query, category=category, tags=tags, limit=limit
    )
    return json.dumps(results, indent=2)
