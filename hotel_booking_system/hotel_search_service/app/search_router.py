from fastapi import APIRouter, HTTPException, status, Depends
import httpx
import os
import redis
import json

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

router = APIRouter(prefix="/v1/search", tags=["search"])

@router.get("/get_hotels", status_code=status.HTTP_201_CREATED)
def get_hotels(
    city : str,
    country : str,
    start_date : str,
    end_date : str,
    number_of_people : int,
):
    cache_key = f"search:{city}:{country}:{start_date}:{end_date}:{number_of_people}"
    cached_result = redis_client.get(cache_key)

    if cached_result:
        hotels = json.loads(cached_result)
    else:    
        try:
            url = "http://hotel_admin_service:8000/v1/hotels/get_hotels"
            params={
                    "city": city,
                    "country": country,
                    "start_date": start_date,
                    "end_date": end_date,
                    "number_of_rooms":number_of_people,
                }

            response = httpx.get(url=url, params=params)
            response.raise_for_status()
            hotels = response.json()
            redis_client.setex(cache_key, 600, json.dumps(hotels))
            return hotels
        except httpx.RequestError as exc:
            print(f"Hotel service request failed: {exc}")
            return []
        except httpx.HTTPStatusError as exc:
            print(f"Hotel service returned error: {exc.response.status_code}")
            return []