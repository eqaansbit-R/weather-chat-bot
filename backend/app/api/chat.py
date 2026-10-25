from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, get_db
from app.models import ChatMessage
from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api", tags=["chat"])
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        result = await chat_service.handle_message(payload.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    new_message = ChatMessage(
        user_id=current_user.id,
        question=payload.message,
        answer=result["response"],
        city=result.get("city"),
        temperature=result.get("temperature"),
        feels_like=result.get("feels_like"),
        description=result.get("description"),
    )
    db.add(new_message)
    await db.commit()

    return ChatResponse(
        response=result["response"],
        city=result.get("city"),
        temperature=result.get("temperature"),
        feels_like=result.get("feels_like"),
        description=result.get("description"),
    )

@router.get("/history")
async def get_history(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
    )
    messages = result.scalars().all()

    return [
        {
            "id": msg.id,
            "question": msg.question,
            "answer": msg.answer,
            "city": msg.city,
            "temperature": msg.temperature,
            "description": msg.description,
            "created_at": str(msg.created_at),
        }
        for msg in messages
    ]
