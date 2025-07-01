from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.session import get_db
from app.data_models import HotelDTO, HotelDB, RoomDB, HotelCapacityDB, RoomType
from app.services.hotel_service import add_hotel
from app.dependencies import get_current_admin
from typing import Optional
from datetime import date
from sqlalchemy import func
from datetime import timedelta
from typing import cast
from app.services.room_service import book_room_handle
router = APIRouter(prefix="/v1/hotels", tags=["Hotels"])

@router.post("/add_hotel", status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel : HotelDTO, 
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin) 
    ):
    new_hotel = add_hotel(db, hotel)
    return new_hotel


@router.put("/update_hotel")
async def update_hotel(
    hotel_data: HotelDTO,
    hotel_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin)
):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id, HotelDB.admin_id == admin_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    for key, value in hotel_data.dict().items():
        setattr(hotel, key, value)

    db.commit()
    db.refresh(hotel)
    return hotel

@router.get("/get_hotel_id")
def get_hotel_by_id(
    hotel_id: int, 
    db: Session = Depends(get_db)
    ):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@router.get("/get_hotels")
def find_hotels_with_capacity(
    city: str, 
    country: str, 
    start_date: date, 
    end_date: date, 
    number_of_rooms: int,
    db: Session = Depends(get_db)
    ):
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)

    subquery = (
        db.query(
            HotelCapacityDB.hotel_id,
            func.min(HotelCapacityDB.capacity).label("min_capacity")
        )
        .join(HotelDB)
        .filter(
            HotelDB.city == city,
            HotelDB.country == country,
            HotelCapacityDB.date.in_(date_range),
        )
        .group_by(HotelCapacityDB.hotel_id)
        .having(func.min(HotelCapacityDB.capacity) >= number_of_rooms)
        .subquery()
    )

    hotels = db.query(HotelDB).join(subquery, HotelDB.id == subquery.c.hotel_id).all()
    return hotels

@router.get("/book_room")
def book_room(
    hotel_id: int, 
    room_type: RoomType, 
    start_date: date, 
    end_date: date, 
    count: int = 1,
    db: Session = Depends(get_db)
):
    current_date = start_date
    room_id = -1
    price = -1
    # Check capacity for each day
    while current_date <= end_date:
        capacity_entry = db.query(HotelCapacityDB).filter_by(
            hotel_id=hotel_id,
            date=current_date,
            room_type=room_type
        ).first()

        if not capacity_entry or capacity_entry.capacity < count:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough capacity for {room_type.value} on {current_date}"
            )

        capacity_entry.capacity -= count
        current_date += timedelta(days=1)

    # Actually assign and reserve rooms
    for _ in range(count):
        room_id, price = book_room_handle(db, hotel_id, room_type, start_date, end_date)
        if room_id is None:
            raise HTTPException(
                status_code=400,
                detail="Available room not found despite capacity. Possible inconsistency."
            )
        

    return {"room_id":room_id, "price":price}