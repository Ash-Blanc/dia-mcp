"""UI/UX Inspo MCP Server — find the best UI/UX inspiration as images, fast."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import os

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
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


# ── Health Check ──────────────────────────────────────────────


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    api_key_set = os.getenv("MCP_API_KEY") is not None
    return JSONResponse(
        {
            "status": "ok",
            "message": "UX Inspo Engine (Dev with Auth) is running",
            "auth_enabled": api_key_set,
        }
    )


# ── Authentication ──────────────────────────────────────────────


class AuthMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware to secure /sse, streamable paths, and /messages/ endpoints using
    standard API keys or Bearer tokens.
    """

    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        from fastmcp import settings

        # Only protect SSE, streamable-http, and messages endpoints
        path = request.url.path
        if not (
            path == settings.sse_path
            or path == settings.streamable_http_path
            or path.startswith(settings.message_path)
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        api_key_header = request.headers.get("X-API-Key")

        is_authenticated = False
        if api_key_header and api_key_header == self.api_key:
            is_authenticated = True
        elif auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            if token == self.api_key:
                is_authenticated = True

        if not is_authenticated:
            # NOTE: Bypassing the report_issue tool at the HTTP level is complex
            # because the tool execution payload is inside the encrypted/streamed
            # POST request body. Thus, authentication is required globally here.
            return JSONResponse(
                content={
                    "error": "Unauthorized",
                    "message": "Invalid or missing API key.",
                },
                status_code=401,
            )

        return await call_next(request)


# ── Entrypoint ────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="UX Inspo Engine MCP Server")
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Run in remote Streamable HTTP mode instead of stdio",
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

    if args.remote:
        middleware = []
        api_key = os.getenv("MCP_API_KEY")
        if api_key:
            middleware.append(Middleware(AuthMiddleware, api_key=api_key))

        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            middleware=middleware,
        )
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
