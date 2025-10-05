import os
from threading import Lock
from enum import Enum
from pydantic import BaseModel
import pika


class QueueNames(str, Enum):
    SENSORS = "sensors_queue"
    NOTIFICATION = "notification_queue"


class RabbitMQPublisher:
    _instance = None
    _initialized = False
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.user = os.getenv("RABBITMQ_DJANGO_USER")
        self.password = os.getenv("RABBITMQ_DJANGO_PASSWORD")
        self.address = os.getenv("RABBITMQ_ADDRESS")
        self.ampq_url = f"amqp://{self.user}:{self.password}@{self.address}/"
        self.connection = None
        self.channel = None
        self._setup_connection()

    def _setup_connection(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.URLParameters(self.ampq_url)
                )
                self.channel = self.connection.channel()

                # Declare all queues
                for queue_name in QueueNames:
                    self.channel.queue_declare(queue=queue_name.value, durable=True)

                print("RabbitMQ connection established successfully")
                return

            except Exception as e:
                print(f"Failed to connect to RabbitMQ  {e}")
                # Wait before retry
                import time

                time.sleep(5)

    def send_message(self, queue_name: QueueNames, message: BaseModel):
        if not self.channel or self.connection.is_closed:
            self._setup_connection()

        if not self.channel:
            raise Exception("Failed to establish RabbitMQ connection")

        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name.value,
                body=message.model_dump_json().encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )
            print(f"Sent to {queue_name}: {message}")

        except Exception as e:
            print(f"Failed to send message to {queue_name}: {e}")
            try:
                if self.connection and not self.connection.is_closed:
                    self.connection.close()
            except:
                pass
            self.connection = None
            self.channel = None
            raise

    def is_connected(self):
        return self.connection and not self.connection.is_closed and self.channel

    def close(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                print("RabbitMQ connection closed")
        except Exception as e:
            print(f"Error closing RabbitMQ connection: {e}")
        finally:
            self.connection = None
            self.channel = None


connection = RabbitMQPublisher()
