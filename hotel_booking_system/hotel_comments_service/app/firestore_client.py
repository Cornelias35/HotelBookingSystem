import os
from google.cloud import firestore
from app.models import Comment
from dotenv import load_dotenv

load_dotenv()

# Use GCP service credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccount.json"

db = firestore.Client()
collection = db.collection("hotel_comments")

def add_comment_to_firestore(comment: Comment):
    return collection.add(comment.model_dump())

def get_comments_by_hotel(hotel_id: int, limit: int = 10, skip: int = 0):
    all_comments = collection.where("hotel_id", "==", hotel_id).stream()
    all_list = [doc.to_dict() for doc in all_comments]
    return all_list[skip:skip + limit]

def get_average_rating(hotel_id: int):
    comments = collection.where("hotel_id", "==", hotel_id).stream()
    comments = [doc.to_dict() for doc in comments]

    if not comments:
        return {}

    def avg(key): return round(sum(c["rating"][key] for c in comments) / len(comments), 1)

    return {
        "avg_cleanliness": avg("cleanliness"),
        "avg_service": avg("service"),
        "avg_facilities": avg("facilities"),
        "avg_location": avg("location"),
        "avg_eco_friendly": avg("eco_friendly"),
        "total_comments": len(comments)
    }
