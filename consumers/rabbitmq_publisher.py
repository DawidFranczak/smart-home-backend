import os
from threading import Thread
from enum import Enum
from pydantic import BaseModel
import queue
import pika
from pika.exceptions import StreamLostError, ConnectionClosed, AMQPConnectionError
import time


class QueueNames(str, Enum):
    SENSORS = "sensors_queue"
    NOTIFICATION = "notification_queue"


class RabbitMQPublisher(Thread):

    def __init__(self, amqp_url: str):
        super().__init__(daemon=True)
        self.amqp_url = amqp_url
        self.message_queue = queue.Queue()
        self.running = True
        self.connection = None
        self.channel = None

    def run(self):
        while self.running:
            if not self.is_connected():
                self._reconnect()
                time.sleep(2)
            try:
                queue_name, message, delivery_mode = self.message_queue.get(timeout=5)
                print(f"Received from queue: {queue_name}")
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error reading message queue: {e}")
                continue
            for attempt in range(2):
                try:
                    self.channel.basic_publish(
                        exchange="",
                        routing_key=queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=delivery_mode,
                            content_type="application/json",
                        ),
                    )
                    print(f"Sent to {queue_name}: {message}")
                    break
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
                    time.sleep(1)
                    break

    def _setup_connection(self):
        for attempt in range(5):
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
                time.sleep(5)
        print("Could not connect to RabbitMQ after 5 attempts.")
        time.sleep(10)

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

    def is_connected(self):
        return (
            self.connection
            and not self.connection.is_closed
            and self.channel
            and self.channel.is_open
        )

    def send_message(self, queue_name: QueueNames, message: BaseModel, delivery_mode=2):
        self.message_queue.put(
            (queue_name.value, message.model_dump_json().encode("utf-8"), delivery_mode)
        )

    def close(self):
        self.running = False
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                print("RabbitMQ connection closed")
        except Exception as e:
            print(f"Error closing RabbitMQ connection: {e}")
        finally:
            self.connection = None
            self.channel = None


publisher = None


def start_publisher():
    global publisher
    if publisher is not None:
        return
    user = os.getenv("RABBITMQ_DJANGO_USER")
    password = os.getenv("RABBITMQ_DJANGO_PASSWORD")
    address = os.getenv("RABBITMQ_ADDRESS")
    amqp_url = f"amqp://{user}:{password}@{address}/"
    publisher = RabbitMQPublisher(amqp_url)
    publisher.start()


start_publisher()


def get_publisher():
    return publisher
