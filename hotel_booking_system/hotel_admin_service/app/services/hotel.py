from sqlalchemy.orm import Session
from app.models.data_models import HotelDB, HotelDTO

def add_hotel(db: Session, hotel_create: HotelDTO):
    new_hotel = HotelDB(
        hotel_name=hotel_create.hotel_name,
        hotel_picture=hotel_create.hotel_picture,
        district = hotel_create.district,
        city = hotel_create.city,
        country=hotel_create.country,
        contains_pool=hotel_create.contains_pool,
        contains_wifi=hotel_create.contains_wifi,
        contains_aircooler = hotel_create.contains_aircooler,
        contains_park=hotel_create.contains_park,
        is_pet_accepted=hotel_create.is_pet_accepted,
        latitude=hotel_create.latitude,
        longitude=hotel_create.longitude,
        admin_id=hotel_create.admin_id
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

