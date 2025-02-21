import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from fastapi import FastAPI, Header, HTTPException, Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("webhooks.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WebhookSource(str, Enum):
    GITHUB = "github"
    GITLAB = "gitlab"

app = FastAPI(
    title="Webhook Logger API",
    description="An API that logs GitHub and GitLab webhook events for PR/MR",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    """Return a hello world message."""
    return {"message": "Hello World"}

async def log_webhook_payload(source: WebhookSource, event_type: str, payload: Dict[Any, Any]):
    """Log webhook payload with metadata."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "event_type": event_type,
        "payload": payload
    }
    logger.info(f"Received {source} webhook: {log_entry}")

@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None, alias="X-GitHub-Event")
):
    """Handle GitHub webhook events."""
    if not x_github_event:
        raise HTTPException(status_code=400, detail="X-GitHub-Event header is required")

    if x_github_event not in ["pull_request", "pull_request_review"]:
        raise HTTPException(status_code=400, detail="Unsupported GitHub event type")

    payload = await request.json()
    await log_webhook_payload(WebhookSource.GITHUB, x_github_event, payload)
    
    return {"status": "success", "message": f"GitHub {x_github_event} event logged"}

@app.post("/webhook/gitlab")
async def gitlab_webhook(
    request: Request,
    x_gitlab_event: Optional[str] = Header(None, alias="X-Gitlab-Event")
):
    """Handle GitLab webhook events."""
    if not x_gitlab_event:
        raise HTTPException(status_code=400, detail="X-Gitlab-Event header is required")

    if x_gitlab_event not in ["Merge Request Hook"]:
        raise HTTPException(status_code=400, detail="Unsupported GitLab event type")

    payload = await request.json()
    await log_webhook_payload(WebhookSource.GITLAB, x_gitlab_event, payload)
    
    return {"status": "success", "message": f"GitLab {x_gitlab_event} event logged"}