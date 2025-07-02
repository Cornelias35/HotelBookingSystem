from sqlalchemy.orm import Session
from app.data_models import UserBookDTO, UserBookDB

def book_room_service(
        db: Session, 
        book: UserBookDTO, 
        room_id : int, 
        price : float, 
        user_id: int, 
        is_authenticated: bool
        ) -> UserBookDB:
    if is_authenticated:
        price = 0.85 * price
    else:
        price = price

    new_book_room = UserBookDB(
        user_id = user_id,
        user_name=book.user_name,
        hotel_id = book.hotel_id,
        number_of_people =book.number_of_people,
        start_date = book.start_date,
        end_date = book.end_date,
        room_id = room_id,
        price = price
    )
    db.add(new_book_room)
    db.commit()
    db.refresh(new_book_room)
    return new_book_room