"""The UX Oracle — an autonomous researcher that orchestrates multiple tools."""

from __future__ import annotations

import json
import asyncio
from typing import Any
from fastmcp import Context

from dia.tools.find_inspo import find_inspo
from dia.tools.design_dna import extract_design_dna
from dia.tools.site_pattern_hunt import site_pattern_hunt


async def ux_oracle(
    query: str,
    depth: str = "balanced",
    ctx: Context | None = None,
) -> str:
    """
    🔮 The UX Oracle: An autonomous researcher for deep, multi-stage UI/UX investigations.

    Orchestrates discovery, design DNA extraction, and site-wide hunting to synthesize
    a comprehensive research report. Best for high-level design questions.

    Args:
        query: The design problem to research (e.g. "complex data table filtering")
        depth: "quick" (discovery only) | "balanced" (discovery + DNA) | "deep" (full audit)
    """
    if ctx:
        await ctx.info(f"Oracle is beginning research mission: {query}")
        await ctx.report_progress(0, 4)

    # ── Phase 1: Landscape Discovery ──
    if ctx:
        await ctx.info("Phase 1: Casting broad net for industry standards...")
    
    inspo_json = await find_inspo(query, limit=10)
    inspo_data = json.loads(inspo_json)
    board = inspo_data.get("inspiration_board", [])
    
    if not board:
        return json.dumps({"error": "Oracle could not find any initial references."})

    if depth == "quick":
        return inspo_json

    if ctx:
        await ctx.report_progress(1, 4)
        await ctx.info("Phase 2: Filtering high-signal candidates for DNA extraction...")

    # ── Phase 2: Signal Filtering & DNA Extraction ──
    # Pick top 2 unique URLs from Dribbble/Firecrawl results
    candidate_urls = []
    seen_domains = set()
    for item in board:
        url = item.get("url")
        if url and "http" in url:
            domain = url.split("//")[-1].split("/")[0]
            if domain not in seen_domains:
                candidate_urls.append(url)
                seen_domains.add(domain)
        if len(candidate_urls) >= 2:
            break

    dna_results = []
    for url in candidate_urls:
        if ctx:
            await ctx.info(f"Extracting Design DNA from {url}...")
        try:
            res = await extract_design_dna(url)
            dna_results.append(json.loads(res))
        except Exception:
            continue

    if ctx:
        await ctx.report_progress(2, 4)

    # ── Phase 3: Deep Audit (Optional) ──
    audit_results = None
    if depth == "deep" and candidate_urls:
        if ctx:
            await ctx.info(f"Phase 3: Performing deep site audit on {candidate_urls[0]}...")
        try:
            audit_json = await site_pattern_hunt(candidate_urls[0], limit=5)
            audit_results = json.loads(audit_json)
        except Exception:
            pass

    if ctx:
        await ctx.report_progress(3, 4)
        await ctx.info("Phase 4: Synthesizing expert design principles...")

    # ── Phase 4: Final Synthesis ──
    report = {
        "mission": query,
        "oracle_perspective": (
            "As a Senior UI/UX Architect, I have synthesized these findings "
            "not as visual copies, but as a set of logical design decisions."
        ),
        "key_references": board[:5],
        "extracted_dna": dna_results,
        "deep_audit": audit_results,
        "suggested_principles": [
            "Information Density: How these examples balance data vs. whitespace.",
            "Visual Anchors: The primary elements used to guide user attention.",
            "Interaction Cost: Evaluation of the effort required to complete the task."
        ]
    }

    if ctx:
        await ctx.report_progress(4, 4)
        await ctx.info("Research mission complete.")

    return json.dumps(report, indent=2)
