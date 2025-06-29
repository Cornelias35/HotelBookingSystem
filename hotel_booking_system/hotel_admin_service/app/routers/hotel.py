from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.data_models import HotelDTO, HotelDB, RoomDB
from app.services.hotel import add_hotel
from app.auth.dependencies import get_current_admin
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/hotels", tags=["Hotels"])

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

@router.get("/get_hotels")
async def get_hotels(
    city : str,
    country : str,
    start_date : datetime,
    end_date : datetime,
    number_of_people : int,
    district : Optional[str] = "",
    db: Session = Depends(get_db),
):
    hotel_query = db.query(HotelDB).join(RoomDB).filter(
        HotelDB.city == city,
        HotelDB.country == country,
        RoomDB.is_empty == True,
        RoomDB.start_date <= start_date,
        RoomDB.end_date >= end_date,
        RoomDB.room_size >= number_of_people
    )

    if district and district.lower() != "none":
        hotel_query = hotel_query.filter(HotelDB.district == district)

    hotel_query = hotel_query.distinct()

    hotels = hotel_query.all()
    return hotels

@router.get("/get_hotel_id")
def get_hotel_by_id(
    hotel_id: int, 
    db: Session = Depends(get_db)
    ):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel