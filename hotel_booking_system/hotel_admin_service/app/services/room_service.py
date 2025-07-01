from sqlalchemy.orm import Session
from app.data_models import RoomDB, RoomCreate, HotelCapacityDB, RoomType
from datetime import timedelta, date
from typing import Optional

def add_room(db: Session, room_create: RoomCreate):
    rooms = []
    current_date = room_create.start_date
    end_date = room_create.end_date
    hotel_id = room_create.hotel_id
    room_type = room_create.room_type
    room_count = room_create.room_count

    for _ in range(room_count):
        new_room = RoomDB(
            start_date=room_create.start_date,
            end_date=room_create.end_date,
            room_type=room_type,
            is_empty=True,
            price=room_create.price,
            room_size=room_create.room_size,
            hotel_id=hotel_id
        )
        db.add(new_room)
        rooms.append(new_room)

    while current_date <= end_date:
        capacity_entry = db.query(HotelCapacityDB).filter_by(
            hotel_id=hotel_id,
            date=current_date,
            room_type=room_type
        ).first()
        if capacity_entry:
            capacity_entry.capacity = capacity_entry.capacity + room_count # type: ignore
        else:
            capacity_entry = HotelCapacityDB(
                hotel_id=hotel_id,
                date=current_date,
                room_type=room_type,
                capacity=room_count
            )
            db.add(capacity_entry)
        current_date += timedelta(days=1)

    db.commit()
    for room in rooms:
        db.refresh(room)
    return rooms

def book_room_handle(
    db: Session,
    hotel_id: int,
    room_type: RoomType,
    start_date: date,
    end_date: date
):
    room = db.query(RoomDB).filter(
        RoomDB.hotel_id == hotel_id,
        RoomDB.room_type == room_type,
        RoomDB.start_date <= start_date,
        RoomDB.end_date >= end_date,
        RoomDB.is_empty == True
    ).first()

    if not room:
        return None

    room.is_empty = False
    db.commit()
    db.refresh(room)
    return (room.id, room.price)
