from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from datetime import datetime
from typing import Optional
# from app.services.search_service import get_hotels
import httpx



router = APIRouter(prefix="/search", tags=["search"])

@router.get("/get_hotels", status_code=status.HTTP_201_CREATED)
def get_hotels(
    district : Optional[str],
    city : str,
    country : str,
    start_date : datetime,
    end_date : datetime,
    number_of_people : int,
):
    try:
        response = httpx.get(
            "http://127.0.0.1:8000/hotels/get_hotels",
            params={
                "district": district or "",
                "city": city,
                "country": country,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "number_of_people":number_of_people,
            },
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        print(f"Hotel service request failed: {exc}")
        return []
    except httpx.HTTPStatusError as exc:
        print(f"Hotel service returned error: {exc.response.status_code}")
        return []