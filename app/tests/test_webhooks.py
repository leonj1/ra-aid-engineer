import pytest
from fastapi import status

def test_github_webhook_without_event_header(test_client):
    """Test GitHub webhook fails without event header."""
    response = test_client.post("/webhook/github", json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "X-GitHub-Event header is required"

def test_github_webhook_invalid_event(test_client):
    """Test GitHub webhook fails with invalid event type."""
    response = test_client.post(
        "/webhook/github",
        headers={"X-GitHub-Event": "invalid_event"},
        json={}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Unsupported GitHub event type"

def test_github_webhook_success(test_client, github_pr_payload, mock_llm):
    """Test successful GitHub webhook processing."""
    response = test_client.post(
        "/webhook/github",
        headers={"X-GitHub-Event": "pull_request"},
        json=github_pr_payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    assert "ai_response" in response.json()
    assert mock_llm.ainvoke.called

def test_gitlab_webhook_without_event_header(test_client):
    """Test GitLab webhook fails without event header."""
    response = test_client.post("/webhook/gitlab", json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "X-Gitlab-Event header is required"

def test_gitlab_webhook_invalid_event(test_client):
    """Test GitLab webhook fails with invalid event type."""
    response = test_client.post(
        "/webhook/gitlab",
        headers={"X-Gitlab-Event": "invalid_event"},
        json={}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Unsupported GitLab event type"

def test_gitlab_webhook_success(test_client, gitlab_mr_payload, mock_llm):
    """Test successful GitLab webhook processing."""
    response = test_client.post(
        "/webhook/gitlab",
        headers={"X-Gitlab-Event": "Merge Request Hook"},
        json=gitlab_mr_payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    assert "ai_response" in response.json()
    assert mock_llm.ainvoke.called

def test_root_endpoint(test_client):
    """Test the root endpoint returns hello world message."""
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}