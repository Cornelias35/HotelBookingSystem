from fastapi import FastAPI
from app import search_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hotel Search Service", version="1.0")

app.include_router(search_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)