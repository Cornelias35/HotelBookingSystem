from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/User/Authentication/login")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

async def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> str | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return user_id
    except Exception:
        return None

