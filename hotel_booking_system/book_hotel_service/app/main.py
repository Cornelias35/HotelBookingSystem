from fastapi import FastAPI
from app.routers import hotel_book_router
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Book Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotel_book_router.router)