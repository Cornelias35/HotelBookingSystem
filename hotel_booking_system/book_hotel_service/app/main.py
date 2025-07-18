from fastapi import FastAPI
from app import hotel_book_router
from fastapi.middleware.cors import CORSMiddleware
from app.session import Base, engine

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking Service"}