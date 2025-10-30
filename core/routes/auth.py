from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_jwt import JwtAccessBearer
import security.config as config
import core.crud as crud
from db.models import User, Roles, now_naive
from core.depends import get_current_user
from security.password import verify_password, hash_password

auth_scheme = JwtAccessBearer(secret_key=config.JWT_TOKEN)

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login(response: Response, data: dict, user = Depends(get_current_user)):
    if user.get("email"):
        return {"msg": "Already logged in"}

    email = data.get("email")
    password = data.get("password")

    user = await crud.get_by_param(User, email=email)

    if not user or not user.is_active:
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
        max_age=360000
    )

    user.last_login_at = now_naive()
    await crud.update(user)

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

@router.get("/delete")
async def delete(response: Response, user = Depends(get_current_user)):
    if not user.get("email"):
        return {"msg": "Didn't log in"}

    _user = await crud.get_by_param(User, email=user.get("email"))
    _user.is_active = False
    await crud.update(_user)

    response.delete_cookie(key="access_token")
    return {"msg": "Account deleted"}
