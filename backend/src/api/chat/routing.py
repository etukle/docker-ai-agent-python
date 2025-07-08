from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..ai.services import generate_email_message
from ..ai.schemas import EmailMessageSchema
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem

router = APIRouter()


# /api/chat/
@router.get('/')
def chat_health():
    return {'status': "ok"}


# /api/chats/recent
# curl http://localhost:8080/api/chats/recent/
@router.get("/recent/", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]

    return results


# HTTP POST -> payload = {"message": "Hello World"} -> {"message": "Hello World", "id": 1}
# curl -X POST -d '{"message": "Give me a summary of why it is good to go outside"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post('/', response_model=EmailMessageSchema)
def chat_create_message(
        payload: ChatMessagePayload,
        session: Session = Depends(get_session)
):
    data = payload.model_dump()
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    # session.refresh(obj)

    response = generate_email_message(payload.message)

    return response
