from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Rating(BaseModel):
    cleanliness: int = Field(..., ge=0, le=10)
    service: int = Field(..., ge=0, le=10)
    facilities: int = Field(..., ge=0, le=10)
    location: int = Field(..., ge=0, le=10)
    eco_friendly: int = Field(..., ge=0, le=10)

class Comment(BaseModel):
    user_id: int
    hotel_id: int
    username: str
    country: str
    travel_date: datetime
    nights: int
    comment: str
    rating: Rating
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
