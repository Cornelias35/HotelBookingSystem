from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.data_models import AdminDTO
from app.services.admin import add_admin

"""
router = APIRouter(prefix="/admins", tags=["Admins"])

@router.post("/add_admin", status_code=status.HTTP_201_CREATED)
def create_admin(admin : AdminDTO,  db: Session = Depends(get_db)):
    new_admin = add_admin(db, admin)
    return new_admin
"""