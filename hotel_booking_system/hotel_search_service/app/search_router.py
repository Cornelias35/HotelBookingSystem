from fastapi import APIRouter, HTTPException, status, Depends
import httpx



router = APIRouter(prefix="/v1/search", tags=["search"])

@router.get("/get_hotels", status_code=status.HTTP_201_CREATED)
def get_hotels(
    city : str,
    country : str,
    start_date : str,
    end_date : str,
    number_of_people : int,
):
    try:
        url = "http://127.0.0.1:8001/v1/hotels/get_hotels"
        params={
                "city": city,
                "country": country,
                "start_date": start_date,
                "end_date": end_date,
                "number_of_rooms":number_of_people,
            }
        
        response = httpx.get(url=url, params=params)
        print(response)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        print(f"Hotel service request failed: {exc}")
        return []
    except httpx.HTTPStatusError as exc:
        print(f"Hotel service returned error: {exc.response.status_code}")
        return []