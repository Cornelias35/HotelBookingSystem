![ER Diagram](https://github.com/user-attachments/assets/21baef53-2ae9-4f38-85ea-36185342f594)

Public URLs:

http://35.234.118.93/ -> API Gateway

http://35.234.118.93/v1/book/ -> For booking
http://35.234.118.93/v1/admin/ -> For admin services
http://35.234.118.93/v1/ai_agent/ -> For ai agent services
http://35.234.118.93/v1/comments/ -> For comments services
http://35.234.118.93/v1/search/ -> For search services
http://35.234.118.93/v1/notification/ -> For notification services


Example gateway usage: 

http://35.234.118.93/v1/search/search_hotels?city=izmir&country=t%C3%BCrkiye&start_date=2025-07-03&end_date=2025-07-05&number_of_people=2

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
