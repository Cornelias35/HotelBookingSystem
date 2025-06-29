from sqlalchemy.orm import Session
from app.models.data_models import UserBookDTO, UserBookDB


def book_room_service(db: Session, book: UserBookDTO):
    new_book_room = UserBookDB(
        user_id = book.user_id,
        user_name=book.user_name,
        hotel_id = book.hotel_id,
        number_of_people =book.number_of_people,
        start_date = book.start_date,
        end_date = book.end_date,
        room_id = book.room_id,
        price = book.price
    )
    db.add(new_book_room)
    db.commit()
    db.refresh(new_book_room)
    return new_book_room