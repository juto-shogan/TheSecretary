# ./main.py
import uvicorn
from fastapi import FastAPI
from app.github_webhook import router as github_router
from app.utils.logger import log

app = FastAPI()
app.include_router(github_router)

if __name__ == "__main__":
    log.info("Starting FastAPI server for GitHub Webhooks...")
    uvicorn.run(app, host="0.0.0.0", port=8000)