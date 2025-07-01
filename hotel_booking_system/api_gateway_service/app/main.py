from fastapi import FastAPI, Request, Response, HTTPException
import httpx

app = FastAPI()

# Mapping paths to service URLs
SERVICE_URLS = {
    "bookings": "http://book_hotel_service:8000",
    "admin": "http://hotel_admin_service:8000",
    "ai-agent": "http://hotel_ai_agent_service:8000",
    "comments": "http://hotel_comments_service:8000",
    "search": "http://hotel_search_service:8000",
}

client = httpx.AsyncClient()

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{SERVICE_URLS[service]}/{path}"

    try:
        # Prepare request content
        body = await request.body()
        headers = dict(request.headers)

        # Forward the request to the microservice
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
