from fastapi import APIRouter, Depends, Request
from app.data_models import UserBookDTO
from app.session import get_db
from sqlalchemy.orm import Session
from app.book_room_service import book_room_service
import httpx
import pika
import json

router = APIRouter(tags=["BookService"])

def publish_reservation_event(reservation_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="reservation_queue", durable=True)
    message = json.dumps(reservation_data)
    channel.basic_publish(exchange="", routing_key="reservation_queue", body=message)
    
    connection.close()

@router.post("/book_room")
async def hotel_book_router(
    user: UserBookDTO,
    request: Request,
    db: Session = Depends(get_db)    
):
    user_id_str = request.headers.get("X-User-Id")

    if user_id_str is not None:
        try:
            user_id = int(user_id_str)

        except ValueError:
            user_id = -1  
    else:
        user_id = -1

    is_authenticated = request.headers.get("X-Is-Authenticated", "false").lower() == "true"

    url = "http://hotel-admin-service:8000/book_room"
    json = {
        "hotel_id" : user.hotel_id,
        "room_type" : user.room_type.name,
        "start_date" : user.start_date,
        "end_date" : user.end_date,
    }
    response = httpx.get(url=url, params=json)
    response = response.json()
    new_book_room = book_room_service(
        db=db, 
        book=user, 
        room_id=response["room_id"], 
        price=response["price"],
        user_id=user_id,
        is_authenticated=is_authenticated
        )
    publish_reservation_event({
        "hotel_id": user.hotel_id,
        "user_id": user_id,
        "room_id": response["room_id"],
        "start_date": user.start_date,
        "end_date": user.end_date,
    })

    return new_book_room

