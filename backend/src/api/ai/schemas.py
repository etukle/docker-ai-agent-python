import os
from pydantic import BaseModel, Field


class EmailMessageSchema(BaseModel):
    subject: str
    contents: str
    invalid_requests: bool | None = Field(default=False)
