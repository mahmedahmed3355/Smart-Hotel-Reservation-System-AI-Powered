# app/chat_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot import reply

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatIn(BaseModel):
    message: str
    last_score: float = 0.7
    loyalty_points: int = 0

@router.post("/")
def chat(in_: ChatIn):
    return {"reply": reply(in_.message, in_.last_score, in_.loyalty_points)}
