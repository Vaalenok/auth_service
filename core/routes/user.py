from fastapi import APIRouter, Depends, Response
import core.crud as crud
from db.models import User
from core.jwt import role_required

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/change")
async def change(response: Response, data: dict, user = Depends(role_required(["User", "Admin", "Owner"]))):
    _id = data.get("id")

    if not _id:
        return {"msg": "No id provided"}

    admin = False

    if user.get("role") in ("Admin", "Owner"):
        admin = True

    change_user = await crud.get(User, _id)

    if change_user.email != user.get("email") and not admin:
        return {"msg": "You are not allowed to do this"}

    for key, value in data.items():
        if hasattr(change_user, key) and value:
            setattr(change_user, key, value)

    await crud.update(change_user)

    response.delete_cookie(key="access_token")

    return {"msg": "User changed successfully"}
