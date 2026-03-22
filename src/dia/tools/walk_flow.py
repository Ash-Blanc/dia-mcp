"""Walk a real multi-step UI flow with TinyFish."""

from __future__ import annotations

import json

from dia.clients import tinyfish as tf


async def walk_flow(url: str, flow: str) -> str:
    """
    🔬 Walk through a real UI flow on a live product and document every step.

    Args:
        url: Starting URL (e.g. "notion.so")
        flow: What flow to walk, e.g.
              "the signup/onboarding flow"
              "navigate to settings, find dark mode toggle"
              "open pricing, click Pro, go through checkout"
    """
    goal = (
        f"You are a Senior UI/UX Researcher. Walk through this flow: {flow}. "
        f"At each step, carefully document what you see and interact with. "
        f"Document the visual hierarchy, micro-interactions, and information architecture. "
        f"Return as valid JSON: "
        f'{{"flow_name": "{flow}", "steps": [{{'
        f'"step_number": int, '
        f'"screen_title": "clear, descriptive screen name", '
        f'"url": "current URL", '
        f'"description": "comprehensive description of what the screen shows", '
        f'"key_ui_elements": ["notable UI components with their roles"], '
        f'"interaction": "precise action taken (e.g. click button with text X)", '
        f'"design_observations": "expert analysis of UX patterns, friction, or delight", '
        f'"screenshot_url": "URL to the screenshot for this step (if available)"'
        f"}}]}}"
    )

    result = await tf.run_agent(url, goal, stealth=True)

    return json.dumps(
        {
            "url": url,
            "flow": flow,
            "walkthrough": result.get("resultJson", result),
            "status": result.get("status", "unknown"),
            "reminder": (
                "This documents HOW a top product solved this UX problem. "
                "Extract PRINCIPLES: step count, progressive disclosure, "
                "info hierarchy per step, friction points, delight moments."
            ),
        },
        indent=2,
    )
