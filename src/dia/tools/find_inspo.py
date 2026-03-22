"""Primary tool — fan-out search across inspiration platforms."""

from __future__ import annotations

import asyncio
import json

from fastmcp import Context

from dia.clients import firecrawl as fc
from dia.clients import tinyfish as tf
from dia.sources import SOURCES, pick_sources
from dia.config import MOBBIN_EMAIL, MOBBIN_PASSWORD

DESIGN_GUIDANCE = (
    "You are a Senior Design Systems Architect. "
    "When reviewing these references, focus on the 'Design DNA': "
    "1. Information Hierarchy: How is the most important action emphasized? "
    "2. Proportional Relationships: What is the ratio between heading and body text? "
    "3. Spatial Logic: How is negative space used to group related elements? "
    "4. Component Patterns: Are there reusable UI patterns you can abstract? "
    "Do not just copy the visuals; synthesize the underlying PRINCIPLES."
)


async def find_inspo(
    query: str,
    platform: str = "auto",
    ui_type: str = "any",
    limit: int = 12,
    ctx: Context | None = None,
) -> str:
    """
    🎨 Find the best UI/UX inspiration images for any design need.

    Searches multiple curated platforms in parallel and returns
    screenshot images with design analysis.

    Args:
        query: e.g. "onboarding flow", "dark mode dashboard",
               "pricing page SaaS", "mobile navigation bottom sheet"
        platform: "auto" | "mobbin" | "dribbble" | "refero" | "godly"
                  | "screenlane" | "collectui" | "behance" | "all"
        ui_type: "web" | "mobile" | "ios" | "android" | "any"
        limit: target number of results (default 12)
    """
    if platform == "auto":
        source_keys = pick_sources(query, ui_type)
    elif platform == "all":
        source_keys = list(SOURCES.keys())
    else:
        source_keys = [platform]

    if ctx:
        await ctx.report_progress(
            0, 3
        )  # ── Fan out ────────────────────────────────────────────
    fc_tasks: list[dict] = []
    tf_tasks: list[dict] = []
    per_source = max(limit // len(source_keys), 2)

    for key in source_keys:
        src = SOURCES.get(key)
        if src is None:
            continue
        if src.needs == "firecrawl":
            fc_tasks.append(
                {
                    "source": key,
                    "query": f"{query} UI UX design site:{src.url.replace('https://', '')}",
                    "limit": per_source,
                }
            )
        else:
            search_url = src.search_url or src.url
            if "{query}" in search_url:
                search_url = search_url.format(
                    query=query.replace(" ", "+"),
                    platform=ui_type if ui_type != "any" else "web",
                )
            
            login_instructions = ""
            if key == "mobbin":
                email = MOBBIN_EMAIL
                password = MOBBIN_PASSWORD
                if email and password:
                    login_instructions = (
                        f"First, navigate to the login page and authenticate using "
                        f"email '{email}' and password '{password}'. Wait to confirm login. Then, "
                    )

            tf_tasks.append(
                {
                    "url": search_url,
                    "goal": (
                        f"{login_instructions}You are a Senior Visual Designer. Search for '{query}' UI/UX designs. "
                        f"Curate the top {per_source} most relevant and visually interesting results. "
                        f"Extract details as high-quality JSON: "
                        f'{{"results": [{{"title": "descriptive name", "image_url": "direct URL", '
                        f'"app_name": "source app", "screen_type": "UI context", '
                        f'"page_url": "source URL", '
                        f'"design_rationale": "expert analysis of the layout and styling"}}]}}'
                    ),
                    "stealth": key in ("mobbin", "refero"),
                }
            )

    fc_results: list[dict] = []
    tf_results: list[dict] = []

    async def _run_fc_task(task):
        try:
            # Firecrawl SDK is synchronous, so we run it in a thread
            res = await asyncio.to_thread(
                fc.search,
                task["query"],
                limit=task["limit"],
                formats=["markdown", "screenshot", "links"],
            )
            return {"source": task["source"], "results": res}
        except Exception as e:
            return {"source": task["source"], "error": str(e)}

    async def _fc_search():
        nonlocal fc_results
        tasks = [_run_fc_task(t) for t in fc_tasks]
        if tasks:
            fc_results = await asyncio.gather(*tasks)

    async def _tf_search():
        nonlocal tf_results
        raw = await tf.run_parallel(tf_tasks)
        for i, r in enumerate(raw):
            tf_results.append({"source": tf_tasks[i]["url"], "data": r})

    await asyncio.gather(_fc_search(), _tf_search())

    if ctx:
        await ctx.report_progress(1, 3)

    # ── Collect URLs for batch screenshot ──────────────────
    screenshot_urls: list[str] = []
    for fc_res in fc_results:
        for r in fc_res.get("results") or []:
            url = r.get("url") or r.get("metadata", {}).get("url", "")
            if url:
                screenshot_urls.append(url)

    screenshots: dict[str, bool] = {}
    if screenshot_urls:
        try:
            batch = await asyncio.to_thread(fc.batch_scrape, screenshot_urls[:limit])
            items = batch.get("data", []) if isinstance(batch, dict) else batch
            for doc in items:
                d = doc if isinstance(doc, dict) else doc.__dict__
                u = d.get("metadata", {}).get("sourceURL", "")
                screenshots[u] = d.get("screenshot") is not None
        except Exception:
            pass

    if ctx:
        await ctx.report_progress(2, 3)
    # ── Compile board ──────────────────────────────────────
    board: list[dict] = []
    seen: set[str] = set()

    for fc_res in fc_results:
        for r in fc_res.get("results") or []:
            url = r.get("url") or r.get("metadata", {}).get("url", "")
            if url in seen:
                continue
            seen.add(url)
            board.append(
                {
                    "source_platform": fc_res["source"],
                    "url": url,
                    "title": r.get("metadata", {}).get("title", ""),
                    "preview": (r.get("markdown") or "")[:300],
                    "has_screenshot": screenshots.get(url, False),
                }
            )

    for tf_res in tf_results:
        data = tf_res.get("data", {})
        rj = data.get("resultJson") if isinstance(data, dict) else None
        if rj:
            board.append(
                {
                    "source_platform": tf_res["source"],
                    "agent_extracted": rj,
                }
            )

    if ctx:
        await ctx.report_progress(3, 3)

    return json.dumps(
        {
            "query": query,
            "sources_searched": source_keys,
            "total_results": len(board),
            "inspiration_board": board[:limit],
            "design_guidance": DESIGN_GUIDANCE,
        },
        indent=2,
    )
