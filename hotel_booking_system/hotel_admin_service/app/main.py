from fastapi import FastAPI
from app.routers import room, admin, hotel, auth_router
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel admin service", version="1.0")

app.include_router(auth_router.router)
app.include_router(room.router)
app.include_router(hotel.router)