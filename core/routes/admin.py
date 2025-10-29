import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
import core.crud as crud
from db.models import User, Roles
from core.jwt import role_required, get_current_user, auth_scheme
from security.password import verify_password, hash_password

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/user_status")
async def user_status(data: dict, user = Depends(role_required(["Admin", "Owner"]))):
    _user = await crud.get(User, uuid.UUID(data.get("id")))

    if _user.role.name == "Owner":
        return {"msg": "You are not allowed to do this"}

    status = data.get("status")

    _user.is_active = status
    await crud.update(_user)

    return {"msg": f"User active status has been changed: {status}"}
