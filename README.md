![ER Diagram](https://github.com/user-attachments/assets/21baef53-2ae9-4f38-85ea-36185342f594)

Public URLs:

http://35.234.118.93/ -> API Gateway

http://35.234.118.93/book_service -> For booking
http://35.234.118.93/admin_service -> For admin services
http://35.234.118.93/ai-agent_service -> For ai agent services
http://35.234.118.93/comments_service -> For comments services
http://35.234.118.93/search_service -> For search services
http://35.234.118.93/notification_service -> For notification services


Example gateway usage: 

http://35.234.118.93/search_service/v1/search/get_hotels?city=izmir&country=t%C3%BCrkiye&start_date=2025-07-03&end_date=2025-07-05&number_of_people=2

Out: 

[
  {
    "is_pet_accepted": true,
    "district": "çeşme",
    "latitude": 0,
    "city": "izmir",
    "longitude": 0,
    "country": "türkiye",
    "admin_id": 2,
    "contains_pool": true,
    "hotel_picture": "string",
    "contains_wifi": true,
    "max_capacity_for_economy": 50,
    "hotel_name": "Best",
    "id": 1,
    "contains_aircooler": true,
    "max_capacity_for_standard": 50,
    "contains_park": true,
    "max_capacity_for_deluxe": 50
  }
]
