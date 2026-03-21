"""UI/UX Inspo MCP Server — find the best UI/UX inspiration as images, fast."""

from __future__ import annotations

import argparse
import os

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from dia.index.db import init as init_db
from dia.tools.find_inspo import find_inspo
from dia.tools.screenshot import screenshot_live_app
from dia.tools.dig_platform import dig_platform
from dia.tools.compare import compare_uis
from dia.tools.design_dna import extract_design_dna
from dia.tools.recommend_colors import recommend_colors
from dia.tools.ux_oracle import ux_oracle
from dia.tools.walk_flow import walk_flow
from dia.tools.site_pattern_hunt import site_pattern_hunt
from dia.tools.index_pattern import index_pattern
from dia.tools.index_flow import index_flow
from dia.tools.search_index import search_index
from dia.tools.report_issue import report_issue
from dia.prompts.inspo_hunt import inspo_hunt

# ── Lifespan ──────────────────────────────────────────────────


@lifespan
async def _lifespan(server: FastMCP):
    await init_db()
    yield


# ── Server ────────────────────────────────────────────────────

mcp = FastMCP(
    "UX Inspo Engine 🎨",
    instructions=(
        "You are a UI/UX inspiration engine. You find the best visual "
        "design references from across the web as IMAGES — screenshots "
        "of real shipped products and curated design platforms.\n\n"
        "CARDINAL RULE: Deliver inspiration alongside DESIGN REASONING "
        "(why it works, what pattern it uses, what principle it demonstrates). "
        "NEVER help copy a design. Help the user UNDERSTAND what makes it "
        "great so they create something original informed by the best.\n\n"
        "Always return images. Speed is everything. Hit multiple sources "
        "in parallel when possible."
    ),
    lifespan=_lifespan,
)

# ── Tools ─────────────────────────────────────────────────────

mcp.add_tool(find_inspo)
mcp.add_tool(screenshot_live_app)
mcp.add_tool(dig_platform)
mcp.add_tool(compare_uis)
mcp.add_tool(extract_design_dna)
mcp.add_tool(recommend_colors)
mcp.add_tool(ux_oracle)
mcp.add_tool(walk_flow)
mcp.add_tool(site_pattern_hunt)
mcp.add_tool(index_pattern)
mcp.add_tool(index_flow)
mcp.add_tool(search_index)
mcp.add_tool(report_issue)


# ── Prompt ────────────────────────────────────────────────────

mcp.prompt()(inspo_hunt)


# ── Entrypoint ────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="UX Inspo Engine MCP Server")
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Run in remote HTTP mode instead of stdio",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=os.getenv("MCP_TRANSPORT"),
        help=(
            "Transport to use. Defaults to stdio locally and streamable-http "
            "when --remote is set."
        ),
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="Host for remote mode (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port for remote mode (default: 8000)",
    )
    args = parser.parse_args()

    transport = args.transport
    if transport is None:
        transport = "streamable-http" if args.remote else "stdio"

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
