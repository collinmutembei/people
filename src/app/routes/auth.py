from fastapi import APIRouter, Depends, Response

from app.core.users import fastapi_users, get_user_manager, jwt_authentication

router = APIRouter()


@router.post("/refresh")
async def refresh_jwt(
    response: Response, user=Depends(fastapi_users.current_user(active=True))
):
    return await jwt_authentication.get_login_response(
        user, response, user_manager=get_user_manager()
    )
