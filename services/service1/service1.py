import uvicorn
from fastapi import FastAPI, HTTPException, Response
import json
import os
import uuid
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from data_types import MyRequest, MyResponse, MetadataResponse
import signal
import sys
import logging
import google.cloud.logging

try:
    gcloud_logger = google.cloud.logging.Client()
    gcloud_logger.setup_logging()
except Exception as e:
    # If we can't set up google cloud logging, log to stdout
    # This is useful for local dev and automated tests
    logging.error(f"Error setting up google cloud logging: {e}")

load_dotenv()

start = datetime.now(timezone.utc).isoformat()


# docs_url is the URL for the Swagger UI.
app = FastAPI(
    title="Service 1",
    description="An example FastAPI application for a generic service running on GCP Cloud Run.",
    version="0.0.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get(
    path="/metadata",
    summary="get app metadata",
    description="Returns deployment metadata about the application.",
)
async def metadata() -> MetadataResponse:
    # Provided by https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
    return {
        "projectId": os.getenv("PROJECT_ID", ""),
        "buildId": os.getenv("BUILD_ID", ""),
        "commitSha": os.getenv("COMMIT_SHA", ""),
        "branchName": os.getenv("BRANCH_NAME", ""),
        "tagName": os.getenv("TAG_NAME", ""),
        "appStartTimestamp": start,
    }


@app.get(
    path="/health",
    status_code=204,
    response_class=Response,
    summary="run app healthcheck",
    description="add your own check here, such as for an active, working database connection",
)
async def healthcheck():
    # db = DataBase()
    healthy = True  # db.verify_connection()
    if not healthy:
        raise HTTPException(status_code=503, detail="Database connection is unhealthy")
    return


@app.post(
    path="/MyEndpoint",
    summary="Trigger some calculation.",
    description="Some extended description.",
)
async def batch_health_scores(request: MyRequest) -> MyResponse:
    # Do some calculation
    logging.info("Doing some fancy calculation")
    time.sleep(1)
    return {"response": f"Received request for {request.request}"}


def shutdown_handler(signal: int, frame: FrameType) -> None:
    """Gracefully shutdown app."""
    logging.info("Signal received, safely shutting down. Exiting process.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    # Handles Ctrl-C locally
    signal.signal(signal.SIGINT, shutdown_handler)
    # Running on port 8080 is default for Cloud Run. This automatically handles SSL on typical ports.
    uvicorn.run(app, host="0.0.0.0", port=8080)

else:
    # Handles SIGTERM when running in a container
    signal.signal(signal.SIGTERM, shutdown_handler)
