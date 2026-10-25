from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_admin_user, get_db
from app.models import ChatMessage, User
from app.schemas import DashboardStats

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=DashboardStats)
async def admin_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    total_users = await db.scalar(select(func.count(User.id)))
    total_messages = await db.scalar(select(func.count(ChatMessage.id)))
    unique_cities = await db.scalar(
        select(func.count(func.distinct(ChatMessage.city)))
    )

    avg_temperature = await db.scalar(
        select(func.avg(ChatMessage.temperature))
    ) or 0.0

    return DashboardStats(
        total_users=total_users or 0,
        total_messages=total_messages or 0,
        cities_queried=unique_cities or 0,
        avg_temperature=float(avg_temperature),
    )
