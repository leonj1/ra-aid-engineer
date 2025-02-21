from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI hello world application",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    """Return a hello world message."""
    return {"message": "Hello World"}