from fastapi import APIRouter, Depends, Response
import core.crud as crud
from db.models import User, now_naive
from core.depends import access_marking

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/edit")
async def edit(response: Response, data: dict, user = Depends(access_marking(["User", "Admin", "Owner"], "User", "update"))):
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

    change_user.updated_at = now_naive()
    await crud.update(change_user)

    response.delete_cookie(key="access_token")

    return {"msg": "User changed successfully"}
