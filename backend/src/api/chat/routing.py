from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from .models import ChatMessagePayload, ChatMessage

router = APIRouter()


# /api/chat/
@router.get('/')
def chat_health():
    return {'status': "ok"}

# /api/chats/recent
# curl http://localhost:8080/api/chats/recent/
@router.get("/recent/")
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]

    return results

# HTTP POST -> payload = {"message": "Hello World"} -> {"message": "Hello World", "id": 1}
# curl -X POST -d '{"message": "Hello World"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post('/', response_model=ChatMessage)
def chat_create_message(
        payload: ChatMessagePayload,
        session: Session = Depends(get_session)
):
    data = payload.model_dump()
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj
