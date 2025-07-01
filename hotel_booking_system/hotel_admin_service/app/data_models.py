from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Float, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from app.session import Base
from sqlalchemy.orm import relationship
from enum import Enum
from typing import Optional

class RoomType(Enum):
    economy = "economy"
    standard = "standard"
    deluxe = "deluxe"


class RoomDTO(BaseModel):
    start_date : date 
    end_date : date
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
    max_capacity_for_economy: int
    max_capacity_for_standard: int
    max_capacity_for_deluxe: int

class RoomDB(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    room_type = Column(SqlEnum(RoomType), nullable=False)
    is_empty = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    room_size = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    hotel = relationship("HotelDB", back_populates="rooms")

class HotelCapacityDB(Base):
    __tablename__ = "hotel_capacity"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    date = Column(Date, nullable=False)
    room_type = Column(SqlEnum(RoomType), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)

    __table_args__ = (UniqueConstraint("hotel_id", "date", "room_type", name="uix_capacity_per_day"),)

    hotel = relationship("HotelDB", back_populates="capacities")

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
    max_capacity_for_economy = Column(Integer, nullable=False)
    max_capacity_for_standard = Column(Integer, nullable=False)
    max_capacity_for_deluxe = Column(Integer, nullable=False)

    rooms = relationship("RoomDB", back_populates="hotel")
    admin = relationship("AdminDB", back_populates="hotels")
    capacities = relationship("HotelCapacityDB", back_populates="hotel", cascade="all, delete-orphan")




class AdminDTO(BaseModel):
    username : str
    password : str


class AdminDB(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)

    hotels = relationship("HotelDB", back_populates="admin")