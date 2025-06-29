from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.data_models import UserDB, UserDTO
from app.database.session import get_db
from dotenv import load_dotenv
import jwt
import os
from datetime import datetime, timedelta 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Authentication"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/user/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise HTTPException(status_code=404, detail="Key not found")
    ALGORITHM = "HS256" 

    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    user_obj = UserDTO(
        username=str(user.username),
        password=str(user.password)
    )
    if not user or not verify_password(form_data.password, user_obj.password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    to_encode = {"user_id": user.id, "exp": datetime.utcnow() + access_token_expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.post("/user/register")
def register(user_data: UserDTO, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    new_user = UserDB(
        username=user_data.username,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "user_id": new_user.id}

