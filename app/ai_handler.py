import logging
from datetime import datetime
from typing import Dict, Any

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_llm():
    """Create and configure the LLM."""
    return ChatAnthropic(
        model="claude-3-opus-20240229",
        temperature=0.7,
        max_tokens=1000
    )

def create_prompt(message: Dict[Any, Any]) -> str:
    """Create a prompt from the webhook payload."""
    if "pull_request" in message:  # GitHub
        title = message["pull_request"]["title"]
        description = message["pull_request"]["body"] or ""
        url = message["pull_request"]["html_url"]
        return f"""
        Please review this GitHub Pull Request:
        
        Title: {title}
        Description: {description}
        URL: {url}
        
        Provide a thorough code review focusing on:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Security concerns
        4. Performance implications
        5. Suggestions for improvement
        """
    elif "object_attributes" in message:  # GitLab
        title = message["object_attributes"]["title"]
        description = message["object_attributes"]["description"] or ""
        url = message["object_attributes"]["url"]
        return f"""
        Please review this GitLab Merge Request:
        
        Title: {title}
        Description: {description}
        URL: {url}
        
        Provide a thorough code review focusing on:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Security concerns
        4. Performance implications
        5. Suggestions for improvement
        """
    else:
        return str(message)

async def process_message(message: Dict[Any, Any]) -> str:
    """
    Process a webhook message using LangChain.
    
    Args:
        message: Dictionary containing the message details
        
    Returns:
        str: Response from the AI model
    """
    try:
        # Create LLM instance
        llm = create_llm()
        
        # Create prompt
        prompt = create_prompt(message)
        
        # Create chat template
        chat_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert code reviewer. Provide clear, actionable feedback."),
            ("user", "{input}")
        ])
        
        # Format prompt
        formatted_prompt = chat_template.format_messages(input=prompt)
        
        # Get response
        response = await llm.ainvoke(formatted_prompt)
        
        return response.content
        
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(error_msg)
        return error_msg