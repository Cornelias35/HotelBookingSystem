from fastapi import APIRouter, Depends
from app.models.data_models import UserBookDTO
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.services.book_room_service import book_room_service

router = APIRouter(prefix="/book_service", tags=["BookService"])

@router.post("/book_room")
async def hotel_book_router(
    user: UserBookDTO,
    db: Session = Depends(get_db)    
):
    new_book_room = book_room_service(db=db, book=user)
    return new_book_room
