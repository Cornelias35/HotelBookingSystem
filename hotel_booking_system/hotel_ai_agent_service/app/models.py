from langgraph.graph import MessagesState
from datetime import date
from typing import Optional
from enum import Enum

class RoomType(Enum):
    economy = "economy"
    standard = "standard"
    deluxe = "deluxe"

class AIState(MessagesState):
    user_id : int
    city: str 
    country: str 
    start_date: date 
    end_date: date 
    room_type : RoomType
    number_of_rooms: int
    is_authenticated : bool
    summary : str
    