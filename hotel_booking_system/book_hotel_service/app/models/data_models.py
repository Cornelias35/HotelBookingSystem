from pydantic import BaseModel
from app.database.session import Base
from sqlalchemy import Column, Integer, DateTime, Float, String
from datetime import datetime
from enum import Enum

class RoomType(Enum):
    economy = "economy"
    standard = "standard"
    deluxe = "deluxe"

class UserBookDTO(BaseModel):
    user_id : int
    user_name : str
    hotel_id : int
    number_of_people : int
    room_type : RoomType
    start_date : str
    end_date : str
    is_authenticated : bool

class UserBookDB(Base):
    __tablename__ = "booked_users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String, nullable=False)
    hotel_id = Column(Integer, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    room_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    