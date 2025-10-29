from fastapi import APIRouter, Depends, HTTPException, Response
import core.crud as crud
from db.models import User, Roles
from core.jwt import role_required, get_current_user, auth_scheme
from security.password import verify_password, hash_password

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login")
async def login(response: Response, data: dict, user = Depends(get_current_user)):
    if user.get("email"):
        return {"msg": "Already logged in"}

    email = data.get("email")
    password = data.get("password")

    user = await crud.get_by_param(User, email=email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    payload = {"email": email, "role": user.role.name}
    token = auth_scheme.create_access_token(subject=payload)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=3600
    )

    return {"msg": "Logged in"}

@router.get("/logout")
async def logout(response: Response, user = Depends(get_current_user)):
    if not user.get("email"):
        return {"msg": "Didn't log in"}

    response.delete_cookie(key="access_token")
    return {"msg": "Logged out"}

@router.post("/register")
async def register(data: dict, user = Depends(get_current_user)):
    if user.get("email"):
        return {"msg": "Already registered"}

    db_user = await crud.get_by_param(User, email=data.get("email"))

    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = User(username=data.get("username"), email=data.get("email"))
    new_user.password_hash = hash_password(data.get("password"))
    user_role = await crud.get_by_param(Roles, name="User")
    new_user.role = user_role

    await crud.create(new_user)
    return {"msg": "Successfully registered"}

@router.get("/public")
async def public(user=Depends(role_required(["Guest", "User", "Admin", "Owner"]))):
    return {"message": "Доступно всем", "user": user}

@router.get("/user")
async def _user(user=Depends(role_required(["User", "Admin", "Owner"]))):
    return {"message": f"Профиль пользователя: {user['email']}"}

@router.get("/admin")
async def admin(user=Depends(role_required(["Admin", "Owner"]))):
    return {"message": f"Привет, {user['email']} (админ)"}
