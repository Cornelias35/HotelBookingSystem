import asyncio
import json
from datetime import datetime, timedelta

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aio_pika
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
#from models import HotelCapacityDB, AdminDB  # your ORM models here

DATABASE_URL = "postgresql+asyncpg://user:password@host/dbname"
RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Socket.IO Async Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_methods=["*"],
    allow_headers=["*"],
)
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# DB Setup (example sync engine for illustration; async recommended)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Connected admin clients storage (simplified)
connected_admins = {}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    # Remove from connected_admins if tracked

@sio.event
async def register_admin(sid, data):
    """
    Client should send their admin_id on connect to join room
    """
    admin_id = data.get("admin_id")
    if admin_id:
        connected_admins[admin_id] = sid
        await sio.save_session(sid, {"admin_id": admin_id})
        await sio.enter_room(sid, room=f"admin_{admin_id}")
        await sio.emit("registered", {"message": f"Registered admin {admin_id}"}, to=sid)
    else:
        await sio.disconnect(sid)


async def notify_admin(admin_id: int, message: str):
    room = f"admin_{admin_id}"
    print(f"Sending notification to admin {admin_id}: {message}")
    await sio.emit("notification", {"message": message}, room=room)

"""
async def check_capacity_and_notify():
    print("Running nightly capacity check...")
    async with SessionLocal() as db:
        # This example is sync; adapt for async ORM if used.
        now = datetime.utcnow().date()
        next_month = now + timedelta(days=30)
        capacities = db.query(HotelCapacityDB).filter(
            HotelCapacityDB.date >= now,
            HotelCapacityDB.date <= next_month
        ).all()

        # For each hotel, aggregate capacity by date & room type
        # Notify admins if capacity < 20%
        hotels_to_notify = {}
        for c in capacities:
            if c.capacity < c.total_capacity * 0.2:
                hotels_to_notify.setdefault(c.hotel_id, set()).add(c.date)

        for hotel_id, dates in hotels_to_notify.items():
            admin = db.query(AdminDB).join(HotelCapacityDB, HotelCapacityDB.hotel_id == hotel_id).first()
            if admin:
                msg = f"Hotel {hotel_id} has low capacity on dates: {', '.join(str(d) for d in dates)}"
                await notify_admin(admin.id, msg)
"""
async def consume_reservations():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("reservation_queue", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body)
                admin_id = data.get("admin_id")
                reservation_info = data.get("reservation_details", "New reservation")
                if admin_id:
                    await notify_admin(admin_id, f"New reservation: {reservation_info}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_capacity_and_notify, "cron", hour=0, minute=0)  # every midnight UTC
    scheduler.start()

@app.on_event("startup")
async def startup_event():
    print("Starting scheduler and RabbitMQ consumer...")
    start_scheduler()
    asyncio.create_task(consume_reservations())

