import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from langchain_core.messages import AIMessage

from main import app
from ai_handler import create_llm

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def mock_llm():
    """Mock the LLM to avoid making real API calls during tests."""
    with patch('ai_handler.create_llm') as mock:
        mock_instance = AsyncMock()
        mock_response = AIMessage(content="Mocked AI response for code review")
        mock_instance.ainvoke = AsyncMock(return_value=mock_response)
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def github_pr_payload():
    """Sample GitHub pull request payload."""
    return {
        "action": "opened",
        "pull_request": {
            "title": "Test PR",
            "number": 1,
            "html_url": "https://github.com/test/repo/pull/1",
            "user": {
                "login": "testuser"
            },
            "body": "Test pull request description"
        }
    }

@pytest.fixture
def gitlab_mr_payload():
    """Sample GitLab merge request payload."""
    return {
        "object_kind": "merge_request",
        "event_type": "merge_request",
        "object_attributes": {
            "title": "Test MR",
            "id": 1,
            "url": "https://gitlab.com/test/repo/-/merge_requests/1",
            "state": "opened",
            "description": "Test merge request description"
        },
        "user": {
            "username": "testuser"
        }
    }