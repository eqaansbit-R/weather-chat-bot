from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_admin_user, get_db
from app.models import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": str(user.created_at),
        }
        for user in users
    ]
