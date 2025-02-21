import pytest
from unittest.mock import AsyncMock, patch

from ai_handler import process_message, create_prompt

@pytest.mark.asyncio
async def test_process_github_pr(github_pr_payload, mock_llm):
    """Test processing GitHub pull request payload."""
    response = await process_message(github_pr_payload)
    assert response == "Mocked AI response for code review"
    assert mock_llm.ainvoke.called
    
    # Verify prompt contains PR details
    call_args = mock_llm.ainvoke.call_args[0][0]
    prompt_text = call_args[1].content  # Access content attribute directly
    assert github_pr_payload["pull_request"]["title"] in prompt_text
    assert github_pr_payload["pull_request"]["body"] in prompt_text
    assert github_pr_payload["pull_request"]["html_url"] in prompt_text

@pytest.mark.asyncio
async def test_process_gitlab_mr(gitlab_mr_payload, mock_llm):
    """Test processing GitLab merge request payload."""
    response = await process_message(gitlab_mr_payload)
    assert response == "Mocked AI response for code review"
    assert mock_llm.ainvoke.called
    
    # Verify prompt contains MR details
    call_args = mock_llm.ainvoke.call_args[0][0]
    prompt_text = call_args[1].content  # Access content attribute directly
    assert gitlab_mr_payload["object_attributes"]["title"] in prompt_text
    assert gitlab_mr_payload["object_attributes"]["description"] in prompt_text
    assert gitlab_mr_payload["object_attributes"]["url"] in prompt_text

@pytest.mark.asyncio
async def test_process_unknown_payload(mock_llm):
    """Test processing unknown payload type."""
    unknown_payload = {"type": "unknown", "data": "test"}
    response = await process_message(unknown_payload)
    assert response == "Mocked AI response for code review"
    assert mock_llm.ainvoke.called
    
    # Verify raw payload is included in prompt
    call_args = mock_llm.ainvoke.call_args[0][0]
    prompt_text = call_args[1].content  # Access content attribute directly
    assert str(unknown_payload) in prompt_text

@pytest.mark.asyncio
async def test_process_message_error_handling():
    """Test error handling in process_message."""
    with patch('ai_handler.create_llm') as mock_create_llm:
        # Simulate an error in LLM processing
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = Exception("Test error")
        mock_create_llm.return_value = mock_llm
        
        response = await process_message({"test": "data"})
        assert "Error processing message" in response

def test_create_prompt_github():
    """Test prompt creation for GitHub payload."""
    payload = {
        "pull_request": {
            "title": "Test PR",
            "body": "Test description",
            "html_url": "https://github.com/test/1"
        }
    }
    prompt = create_prompt(payload)
    assert "Test PR" in prompt
    assert "Test description" in prompt
    assert "https://github.com/test/1" in prompt

def test_create_prompt_gitlab():
    """Test prompt creation for GitLab payload."""
    payload = {
        "object_attributes": {
            "title": "Test MR",
            "description": "Test description",
            "url": "https://gitlab.com/test/1"
        }
    }
    prompt = create_prompt(payload)
    assert "Test MR" in prompt
    assert "Test description" in prompt
    assert "https://gitlab.com/test/1" in prompt

def test_create_prompt_unknown():
    """Test prompt creation for unknown payload type."""
    payload = {"type": "unknown"}
    prompt = create_prompt(payload)
    assert str(payload) in prompt