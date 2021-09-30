from fastapi import APIRouter, Depends

from app.core.users import current_active_user
from app.models.users import UserDB

router = APIRouter()


@router.get("/network")
async def your_network(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
