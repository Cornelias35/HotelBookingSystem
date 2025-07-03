from fastapi import FastAPI
from app import comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hotel Comment Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comments.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Comment Service"}
