import os
from threading import Lock
from enum import Enum
from pydantic import BaseModel
import pika
from pika.exceptions import StreamLostError, ConnectionClosed, AMQPConnectionError


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
        self.amqp_url = f"amqp://{self.user}:{self.password}@{self.address}/"
        self.connection = None
        self.channel = None
        self._setup_connection()

    def _setup_connection(self):
        while True:
            try:
                params = pika.URLParameters(self.amqp_url)
                params.heartbeat = 60
                params.blocked_connection_timeout = 300
                params.socket_timeout = 10
                params.connection_attempts = 3
                params.retry_delay = 5

                self.connection = pika.BlockingConnection(params)
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

    def _reconnect(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except:
            pass
        self.connection = None
        self.channel = None
        print("Reconnecting to RabbitMQ...")
        self._setup_connection()

    def send_message(self, queue_name: QueueNames, message: BaseModel):
        if not self.is_connected():
            self._reconnect()

        for attempt in range(2):
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
                return

            except (
                StreamLostError,
                ConnectionClosed,
                AMQPConnectionError,
                ConnectionResetError,
            ) as e:
                print(f"Connection error while sending: {e}")
                self._reconnect()

            except Exception as e:
                print(f"Failed to send message to {queue_name}: {e}")
                raise e

        raise Exception("Failed to send message after reconnect attempt.")

    def is_connected(self):
        return (
            self.connection
            and not self.connection.is_closed
            and self.channel
            and self.channel.is_open
        )

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
