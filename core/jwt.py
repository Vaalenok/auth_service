from jose import jwt, JWTError
from fastapi import Request, Depends, HTTPException
from fastapi_jwt import JwtAccessBearer
from security import config

SECRET_KEY = config.JWT_TOKEN
ALGORITHM = "HS256"

auth_scheme = JwtAccessBearer(secret_key=config.JWT_TOKEN)

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return {"role": "Guest"}

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("subject", {})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def role_required(allowed_roles: list[str]):
    async def dependency(user=Depends(get_current_user)):
        role = user.get("role", "Guest")

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return dependency
