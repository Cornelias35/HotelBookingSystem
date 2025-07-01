import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="reservations", durable=True)

message = {
    "user_id": 1,
    "hotel_id": 42,
    "check_in": "2025-07-15",
    "nights": 3,
    "room_type": "deluxe"
}

channel.basic_publish(
    exchange='',
    routing_key="reservations",
    body=json.dumps(message),
    properties=pika.BasicProperties(delivery_mode=2)
)
print("✅ Test message sent")
connection.close()
