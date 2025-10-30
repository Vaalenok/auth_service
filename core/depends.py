from jose import jwt, JWTError
from fastapi import Request, Depends, HTTPException, Response
import core.crud as crud
from db.models import Roles
from security import config

SECRET_KEY = config.JWT_TOKEN
ALGORITHM = "HS256"

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return {"role": "Guest"}

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("subject", {})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def access_marking(allowed_roles: list[str], element_name: str, method_name: str):
    async def dependency(user = Depends(get_current_user)):
        role = user.get("role", "Guest")

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        db_role = await crud.get_by_param(Roles, name=role)
        print(db_role.rules)

        rule = next((r for r in db_role.rules if r.production_element.name == element_name), None)
        print(rule)

        if not getattr(rule, f"{method_name}_permission"):
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return dependency
