"""Tests for the report_issue tool."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from dia.tools.report_issue import report_issue


@pytest.mark.asyncio
async def test_report_issue_success():
    """Test successful issue creation."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "html_url": "https://github.com/Ash-Blanc/dia-mcp/issues/1",
        "number": 1,
    }

    # Use patch.object to mock AsyncClient as a context manager
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("dia.tools.report_issue.GITHUB_TOKEN", "fake-token"):
        
        mock_post.return_value = mock_response
        
        result = await report_issue(
            title="Test Bug",
            body="This is a test bug report.",
            issue_type="bug"
        )
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert data["issue_number"] == 1
        assert "Successfully reported bug" in data["message"]


@pytest.mark.asyncio
async def test_report_issue_no_token():
    """Test behavior when GITHUB_TOKEN is missing."""
    with patch("dia.tools.report_issue.GITHUB_TOKEN", ""):
        result = await report_issue(
            title="Test Bug",
            body="This is a test bug report."
        )
        
        data = json.loads(result)
        assert "error" in data
        assert "GITHUB_TOKEN is not configured" in data["error"]


@pytest.mark.asyncio
async def test_report_issue_api_error():
    """Test behavior when GitHub API returns an error."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("dia.tools.report_issue.GITHUB_TOKEN", "fake-token"):
        
        mock_post.return_value = mock_response

        result = await report_issue(
            title="Test Bug",
            body="This is a test bug report."
        )
        
        data = json.loads(result)
        assert data["status"] == "error"
        assert data.get("http_status") == 401
        assert "Failed to create GitHub issue" in data["message"]
