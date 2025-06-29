from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy import Enum as SqlEnum
from app.database.session import Base
from sqlalchemy.orm import relationship
from enum import Enum
from typing import Optional

class RoomType(Enum):
    economy = "economy"
    standard = "standard"
    deluxe = "deluxe"


class RoomDTO(BaseModel):
    start_date : datetime 
    end_date : datetime
    room_type : RoomType
    is_empty : bool
    price : float
    room_size : int

class RoomCreate(RoomDTO):
    hotel_id : int
    room_count : int

class RoomRead(RoomDTO):
    id : int
    hotel_id : int

    class Config:
        orm_mode = True 


class HotelDTO(BaseModel):
    hotel_name : str
    hotel_picture : str 
    district : Optional[str] = None
    city : str 
    country : str
    contains_pool : bool
    contains_wifi : bool
    contains_aircooler : bool
    contains_park : bool
    is_pet_accepted : bool
    admin_id : int
    latitude: float
    longitude: float

class RoomDB(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    room_type = Column(SqlEnum(RoomType), nullable=False)
    is_empty = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    room_size = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    hotel = relationship("HotelDB", back_populates="rooms")

class HotelDB(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    hotel_name = Column(String, nullable=False)
    hotel_picture = Column(String)
    district = Column(String, nullable=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    contains_pool = Column(Boolean, nullable=False)
    contains_wifi = Column(Boolean, nullable=False)
    contains_aircooler = Column(Boolean, nullable=False)
    contains_park = Column(Boolean, nullable=False)
    is_pet_accepted = Column(Boolean, nullable=False)
    latitude = Column(Float, nullable=False) 
    longitude = Column(Float, nullable=False)

    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    rooms = relationship("RoomDB", back_populates="hotel")
    admin = relationship("AdminDB", back_populates="hotels")



class AdminDTO(BaseModel):
    username : str
    password : str


class AdminDB(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)

    hotels = relationship("HotelDB", back_populates="admin")