from sqlalchemy.orm import Session
from app.models.data_models import RoomDB, RoomCreate

def add_room(db: Session, room_create: RoomCreate):
    rooms = []
    for _ in range(room_create.room_count):
        new_room = RoomDB(
            start_date=room_create.start_date,
            end_date=room_create.end_date,
            room_type=room_create.room_type,
            is_empty=room_create.is_empty,
            price=room_create.price,
            room_size=room_create.room_size,
            hotel_id=room_create.hotel_id
        )
        db.add(new_room)
        rooms.append(new_room)

    db.commit()
    for room in rooms:
        db.refresh(room)
    return rooms