import uuid
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


# These fields will be populated by GCP Cloud Build trigger
class MetadataResponse(BaseModel):
    projectId: str = ""
    buildId: str = ""
    commitSha: str = ""
    branchName: str = ""
    tagName: str = ""
    appStartTimestamp: datetime = None


class MyResponse(BaseModel):
    response: str = ""


class MyRequest(BaseModel):
    request: float = 0.0
