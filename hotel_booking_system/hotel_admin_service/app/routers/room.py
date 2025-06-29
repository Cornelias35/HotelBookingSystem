from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.data_models import RoomRead, RoomCreate, RoomDB, HotelDB
from app.services.room import add_room
from app.auth.dependencies import get_current_admin

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/create_room", response_model=list[RoomRead], status_code=status.HTTP_201_CREATED)
async def create_room(
    room: RoomCreate, 
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin) 
):
    if room.end_date <= room.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    new_room = add_room(db, room)
    return new_room

@router.put("/update_room")
async def update_room(
    room_id: int,
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin)
):
    room = db.query(RoomDB).join(HotelDB).filter(
        RoomDB.id == room_id,
        HotelDB.admin_id == admin_id
    ).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in room_data.dict().items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room