from fastapi import FastAPI
from app.routers import auth_router
from app.routers import hotel_router, room_router
from app.session import Base, engine
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel admin service", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(room_router.router)
app.include_router(hotel_router.router)