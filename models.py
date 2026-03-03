"""Models for the API."""
from pydantic import BaseModel
"""Schema for the request body of the API endpoint."""
class RepoRequest(BaseModel):
    github_url: str