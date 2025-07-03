from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.data_models import AdminDTO, AdminDB
from app.session import get_db
from dotenv import load_dotenv
import jwt
import os
from datetime import datetime, timedelta 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["/v1/Authentication"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/admin/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise HTTPException(status_code=404, detail="Key not found")
    ALGORITHM = "HS256" 

    admin = db.query(AdminDB).filter(AdminDB.username == form_data.username).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    admin_obj = AdminDTO(
        username=str(admin.username),
        password=str(admin.password)
    )
    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    to_encode = {"admin_id": admin.id, "exp": datetime.utcnow() + access_token_expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.post("/admin/register")
def register(admin_data: AdminDTO, db: Session = Depends(get_db)):
    existing_admin = db.query(AdminDB).filter(AdminDB.username == admin_data.username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this username already exists")

    new_admin = AdminDB(
        username=admin_data.username,
        password=hash_password(admin_data.password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"msg": "Admin created successfully", "admin_id": new_admin.id}

