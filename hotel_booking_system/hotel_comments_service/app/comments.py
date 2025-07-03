from fastapi import APIRouter, HTTPException, Query
from app.models import Comment
from app.firestore_client import add_comment_to_firestore, get_comments_by_hotel, get_average_rating

router = APIRouter(tags=["Comments"])

@router.post("/create_comment")
def create_comment(comment: Comment):
    add_comment_to_firestore(comment)
    return {"message": "Comment added successfully"}

@router.get("/{hotel_id}")
def get_comments(hotel_id: int, skip: int = 0, limit: int = 10):
    return get_comments_by_hotel(hotel_id, limit, skip)

@router.get("/{hotel_id}/comment_stats")
def get_comment_summary(hotel_id: int):
    summary = get_average_rating(hotel_id)
    if not summary:
        raise HTTPException(status_code=404, detail="No comments found")
    return summary
