"""Tool — index a multi-step UI flow with TinyFish."""

from __future__ import annotations

import hashlib
import json

from dia.clients import tinyfish as tf
from dia.index.db import save_pattern


async def index_flow(
    url: str,
    app_name: str,
    flow_name: str,
    category: str,
    description: str,
    tags: str = "",
) -> str:
    """
    🔬 Use TinyFish to walk through a flow and index EVERY step into the UI/UX Research Index.

    Args:
        url: Starting URL (e.g. "linear.app")
        app_name: Name of the product
        flow_name: e.g. "onboarding"
        category: pricing | onboarding | checkout | dashboard
        description: Brief overview of the flow
        tags: comma-separated, e.g. "dark-mode,minimalist,saas"
    """
    goal = (
        f"You are a Senior UI/UX Researcher. Walk through the {flow_name} flow on {url}. "
        f"At each step, carefully document what you see and take a mental snapshot. "
        f"Return as a list of steps in valid JSON: "
        f'{{"flow_name": "{flow_name}", "steps": [{{'
        f'"step_number": int, '
        f'"screen_title": "descriptive screen name", '
        f'"url": "current URL", '
        f'"description": "comprehensive description of what the screen shows", '
        f'"interaction": "precise action taken", '
        f'"design_observations": "expert analysis of UX patterns", '
        f'"screenshot_url": "URL to the screenshot if available"'
        f"}}]}}"
    )

    result = await tf.run_agent(url, goal, stealth=True)
    walkthrough = result.get("resultJson", {})
    steps = walkthrough.get("steps", [])

    if not steps:
        return json.dumps({"error": "No steps were found by the agent."})

    # Group all steps under a single flow_id hash
    flow_id = hashlib.md5(f"{url}:{flow_name}".encode()).hexdigest()
    indexed_pids = []

    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    for step in steps:
        pid = await save_pattern(
            {
                "flow_id": flow_id,
                "step_number": step.get("step_number", 0),
                "url": step.get("url", url),
                "app_name": app_name,
                "flow_name": flow_name,
                "category": category,
                "description": step.get("description", description),
                "tags": tag_list,
                "markdown": f"# {step.get('screen_title')}\n\n{step.get('design_observations')}",
                "screenshot_b64": step.get("screenshot_url", ""),  # Store URL or B64
                "metadata": {
                    "interaction": step.get("interaction"),
                    "screen_title": step.get("screen_title"),
                },
            }
        )
        indexed_pids.append(pid)

    return json.dumps(
        {
            "indexed": True,
            "flow_id": flow_id,
            "steps_indexed": len(indexed_pids),
            "app_name": app_name,
            "summary": description,
        },
        indent=2,
    )
