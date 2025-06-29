from fastapi import FastAPI
from app.routers import search_router
app = FastAPI(title="Hotel Search Service", version="1.0")

app.include_router(search_router.router)