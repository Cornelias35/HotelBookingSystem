from fastapi import FastAPI, Request, Response, HTTPException, Depends
import httpx
from app.auth_router import user_router
from app.session import Base, engine
from typing import Optional
from app.dependencies import get_current_user_optional


Base.metadata.create_all(bind=engine)
app = FastAPI()

SERVICE_URLS = {
    "book_service": "http://book_hotel_service:8000",
    "admin_service": "http://hotel_admin_service:8000",
    "ai-agent_service": "http://hotel_ai_agent_service:8000",
    "comments_service": "http://hotel_comments_service:8000",
    "search_service": "http://hotel_search_service:8000",
    "notification_service": "http://hotel_notification_service:8000"
}

client = httpx.AsyncClient()
app.include_router(user_router)

@app.api_route("/{service}/{path:path}",methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(
    service: str, 
    path: str, 
    request: Request, 
    ):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{SERVICE_URLS[service]}/{path}"
    token = request.headers.get("authorization")
    user_id = get_current_user_optional(token=token)
    try:
        body = await request.body()
        headers = dict(request.headers)

        
        if user_id:
            headers["X-User-Id"] = str(user_id)
            headers["X-Is-Authenticated"] = "true"
        else:
            headers["X-User-d"] = "-1"
            headers["X-Is-Authenticated"] = "false"

        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
            timeout=10.0,
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=resp.headers,
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))
