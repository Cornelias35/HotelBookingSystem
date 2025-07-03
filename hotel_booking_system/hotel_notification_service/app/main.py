import os
import asyncio
from fastapi import FastAPI
import socketio
from app.consumer import start_rabbitmq_consumer
from app.scheduler import router as scheduler_router
from contextlib import asynccontextmanager

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    start_rabbitmq_consumer(sio, loop)
    print("[✅] RabbitMQ consumer started")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(scheduler_router)
app.mount("/ws", socketio.ASGIApp(sio))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Notification Service"}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
