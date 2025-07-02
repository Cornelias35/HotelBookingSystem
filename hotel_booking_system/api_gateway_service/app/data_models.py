from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Float, UniqueConstraint
from sqlalchemy import Enum as SqlEnum
from app.session import Base
from sqlalchemy.orm import relationship
from enum import Enum
from typing import Optional

class UserDTO(BaseModel):
    username : str
    password : str


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)

