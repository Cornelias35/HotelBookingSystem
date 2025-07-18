from fastapi import FastAPI
from app.ai_service import router

app = FastAPI(title="AI Agent Service", version='1.0')
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Agent Service"}