"""Report an issue or feature request directly to the GitHub repository."""

from __future__ import annotations

import json
import sys
import httpx
from typing import Literal

from dia.config import GITHUB_TOKEN

REPO_OWNER = "Ash-Blanc"
REPO_NAME = "dia-mcp"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"


async def report_issue(
    title: str,
    body: str,
    issue_type: Literal["bug", "feature_request"] = "bug",
) -> str:
    """
    📣 Report a bug or request a new feature for the Dia MCP server.

    Use this tool to submit feedback, report errors, or suggest improvements
    directly to the repository maintainers.

    Args:
        title: A concise, descriptive title for the issue
        body: Detailed description of the bug or feature request
        issue_type: "bug" (unexpected behavior) or "feature_request" (new idea)
    """
    if not GITHUB_TOKEN:
        return json.dumps(
            {
                "error": "GITHUB_TOKEN is not configured. Please set it in your environment."
            }
        )

    # Enhance the body with system info
    enhanced_body = (
        f"**Type**: {issue_type.replace('_', ' ').title()}\n"
        f"**Environment**: Python {sys.version.split()[0]} on {sys.platform}\n\n"
        f"### Description\n{body}\n\n"
        f"---\n*Reported autonomously via Dia MCP*"
    )

    labels = ["bug"] if issue_type == "bug" else ["enhancement"]

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "dia-mcp-reporter",
    }

    payload = {
        "title": f"[{issue_type.upper()}] {title}",
        "body": enhanced_body,
        "labels": labels,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GITHUB_API_URL,
                json=payload,
                headers=headers,
                timeout=10.0,
            )

        if response.status_code == 201:
            data = response.json()
            return json.dumps(
                {
                    "status": "success",
                    "issue_url": data.get("html_url"),
                    "issue_number": data.get("number"),
                    "message": f"Successfully reported {issue_type.replace('_', ' ')}.",
                },
                indent=2,
            )
        else:
            return json.dumps(
                {
                    "status": "error",
                    "http_status": response.status_code,
                    "response": response.text,
                    "message": "Failed to create GitHub issue.",
                },
                indent=2,
            )

    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}",
            },
            indent=2,
        )
