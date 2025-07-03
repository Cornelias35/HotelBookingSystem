# Hotel Booking System (Backend)  

## ER Diagram of system: 

![ER Diagram](https://github.com/user-attachments/assets/21baef53-2ae9-4f38-85ea-36185342f594)

---  
### Public URLs  
  
- [API Gateway](http://35.234.118.93/)  
- [Booking Service](http://35.234.118.93/v1/book/)  
- [Admin Service](http://35.234.118.93/v1/admin/)  
- [AI Agent Service](http://35.234.118.93/v1/ai_agent/)  
- [Comments Service](http://35.234.118.93/v1/comments/)  
- [Search Service](http://35.234.118.93/v1/search/)  
- [Notification Service](http://35.234.118.93/v1/notification/)  


### Example Usage (via Gateway)  

[Search Hotels Example](http://35.234.118.93/v1/search/search_hotels?city=izmir&country=t%C3%BCrkiye&start_date=2025-07-03&end_date=2025-07-05&number_of_people=2)  

---  

### Implementation Details  

You can watch the implementation walkthrough in this video:  
[YouTube Video](https://youtu.be/A4JysNw0J3c)  

---
### Technologies used:  
**Backend**:
  - FastAPI  
  - Redis  
  - RabbitMQ  
  - SQLAlchemy  
**Cloud**:  
  - Google Cloud  
  - GKE (Google Kubernetes Engine)  
  - Datastore (NoSQL Database)  
  - Google SQL (For Sql Database, Postgresql)  
**Deployment**:  
  - For local testing, docker compose  
  - Dockerfile  
  - Kubernetes (Multiple Service Deployment)  
**Frontend**:  
  - React (TypeScript)
---
