import uuid
from fastapi import APIRouter, Depends
import core.crud as crud
from db.models import User, Roles
from core.depends import access_marking

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/user_status")
async def user_status(data: dict, user = Depends(access_marking(["Admin", "Owner"], "Users", "read"))):
    _id = data.get("id")

    if not _id:
        return {"msg": "No id provided"}

    _user = await crud.get(User, uuid.UUID(_id))

    if _user.role.name == "Owner":
        return {"msg": "You are not allowed to do this"}

    status = data.get("status")

    _user.is_active = status
    await crud.update(_user)

    return {"msg": f"User active status has been changed: {status}"}

@router.post("/edit_access")
async def edit_access(data: dict, user = Depends(access_marking(["Admin", "Owner"], "Users", "update"))):
    role_name = data.get("role")

    if not role_name:
        return {"msg": "No role provided"}

    _role = await crud.get_by_param(Roles, name=role_name)

    if not _role:
        return {"msg": "No role provided"}

    _rules = _role.rules

    for key, value in data.items():
        for rule in _rules:
            if rule.production_element.name == key:
                for _key, _value in value.items():
                    if hasattr(rule, _key) and _value:
                        setattr(rule, _key, _value)

    await crud.update(_role)

    return {"msg": f"Access for role {_role.name} has been changed"}

@router.get("/role_permission/")
async def role_permission(role: str, user = Depends(access_marking(["Admin", "Owner"], "Rules", "read"))):
    db_role = await crud.get_by_param(Roles, name=role)

    return {
        "Role": role,
        "Rules": {
            rule.production_element.name: {
                key: value for key, value in vars(rule).items() if "permission" in key
            } for rule in db_role.rules
        }
    }
