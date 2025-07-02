from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/v1/notification_service", tags=["NotificationService"])

HOTEL_ADMIN_SERVICE_URL = "http://hotel_admin_service:8000/v1/hotels/capacity_percentage/"

@router.get("/check-capacity")
async def check_capacity(
    hotel_id : int
):

    alerts = []
    try:
        response = httpx.get(f"{HOTEL_ADMIN_SERVICE_URL}{hotel_id}")
        if response.status_code == 200:
            data = response.json()
            for room_type, percentage in data["capacity_percentages"].items():
                if percentage < 20.0:
                    alerts.append({
                        "hotel_id": hotel_id,
                        "room_type": room_type,
                        "percentage": percentage
                    })
    except Exception as e:
        print(f"Error fetching capacity for hotel {hotel_id}: {e}")

    if alerts:
        print("[⚠️] Low capacity detected:", alerts)
    else:
        print("[✅] All hotels above 20% capacity.")

    return {"alerts": alerts}
