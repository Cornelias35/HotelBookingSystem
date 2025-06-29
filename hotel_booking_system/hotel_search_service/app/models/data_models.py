from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from app.database.session import Base
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import relationship


class UserDTO(BaseModel):
    username : str
    password : str

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)