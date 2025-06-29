from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        if not SECRET_KEY:
            raise HTTPException(status_code=404, detail="Key not found")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
