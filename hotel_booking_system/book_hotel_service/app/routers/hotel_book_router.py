from fastapi import APIRouter, Depends
from app.models.data_models import UserBookDTO
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.services.book_room_service import book_room_service
import httpx

router = APIRouter(prefix="/v1/book_service", tags=["BookService"])

@router.post("/book_room")
async def hotel_book_router(
    user: UserBookDTO,
    db: Session = Depends(get_db)    
):
    url = "http://127.0.0.1:8000/v1/hotels/book_room"
    json = {
        "hotel_id" : user.hotel_id,
        "room_type" : user.room_type.name,
        "start_date" : user.start_date,
        "end_date" : user.end_date,
    }
    response = httpx.get(url=url, params=json)
    response = response.json()
    new_book_room = book_room_service(db=db, book=user, room_id=response["room_id"], price=response["price"])
    return new_book_room
