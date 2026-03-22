"""TinyFish client — wraps the official SDK + raw SSE fallback."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx

from dia.config import TINYFISH_API_KEY

TINYFISH_URL = "https://agent.tinyfish.ai/v1/automation/run-sse"


async def run_agent(
    url: str,
    goal: str,
    *,
    stealth: bool = False,
    proxy_country: str | None = None,
    timeout: int = 300,
    max_steps: int = 8,
) -> dict[str, Any]:
    """
    Run a single TinyFish agent task via SSE.

    Args:
        url: The starting URL for the agent.
        goal: The natural language goal/instructions.
        stealth: Whether to use stealth browser profile.
        proxy_country: Optional ISO country code for proxy.
        timeout: Total timeout in seconds.
        max_steps: Maximum number of autonomous steps/actions.
    """
    payload: dict[str, Any] = {
        "url": url,
        "goal": goal,
        "browser_profile": "stealth" if stealth else "lite",
        "max_steps": max_steps,
    }
    if proxy_country:
        payload["proxy_config"] = {"enabled": True, "country_code": proxy_country}

    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream(
            "POST",
            TINYFISH_URL,
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json",
            },
            json=payload,
        ) as resp:
            resp.raise_for_status()
            result: dict[str, Any] | None = None
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                try:
                    event = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "COMPLETE":
                    result = event
                    break
                elif event.get("type") == "ERROR":
                    return {"error": event.get("message", "Unknown error")}
        return result or {"error": "No COMPLETE event received"}


async def run_parallel(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Fan out many TinyFish tasks concurrently."""
    coros = [
        run_agent(
            t["url"],
            t["goal"],
            stealth=t.get("stealth", False),
            proxy_country=t.get("proxy_country"),
        )
        for t in tasks
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    return [r if isinstance(r, dict) else {"error": str(r)} for r in results]
