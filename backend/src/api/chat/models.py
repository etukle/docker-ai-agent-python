from sqlmodel import SQLModel, Field

class ChatMessagePayload(SQLModel):
    # pydantic model
    message: str

class ChatMessage(SQLModel, table=True):
    # database table
    id: int | None = Field(default=None, primary_key=True)
    message: str
