import os
import pika
import json
import asyncio
from app.notifier import notify_clients
from dotenv import load_dotenv
import threading
import time # Import the time module for delays
from pika.exceptions import AMQPConnectionError

def start_rabbitmq_consumer(sio, loop):
    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("[x] Received reservation:", data)
        asyncio.run_coroutine_threadsafe(notify_clients(sio, data), loop)

    def run():
        host = "rabbitmq"
        max_retries = 10 
        retry_delay = 5   

        for i in range(max_retries):
            try:
                print(f"[*] Attempting to connect to RabbitMQ at {host} (Attempt {i + 1}/{max_retries})...")
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
                channel = connection.channel()

                channel.queue_declare(queue="reservation_queue", durable=True)

                channel.basic_consume(queue="reservation_queue", on_message_callback=callback, auto_ack=True)

                print("[*] Waiting for messages in reservation_queue. To exit press CTRL+C")
                channel.start_consuming()
            except AMQPConnectionError as e:
                print(f"[!] RabbitMQ connection error: {e}")
                if i < max_retries - 1:
                    print(f"[*] Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay) # Wait before retrying
                else:
                    print("[!] Max retries reached. Could not connect to RabbitMQ.")
            except Exception as e:
                print(f"[!] An unexpected error occurred: {e}")
                raise

    thread = threading.Thread(target=run, daemon=True)
    thread.start()