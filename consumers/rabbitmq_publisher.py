import os
from threading import Lock
import aio_pika
from enum import Enum
from pydantic import BaseModel


class QueueNames(str, Enum):
    TEMPERATURE = "temp_queue"
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
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.Channel | None = None
        self.queues = {}

    async def connect(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.ampq_url)
            self.channel = await self.connection.channel()
            for queue_name in QueueNames:
                await self.declare_queue(queue_name)

    async def declare_queue(self, queue_name: QueueNames):
        if queue_name.value not in self.queues:
            queue = await self.channel.declare_queue(queue_name.value, durable=True)
            self.queues[queue_name.value] = queue
        return self.queues[queue_name.value]

    async def send_message(self, queue_name: QueueNames, message: BaseModel):
        await self.connect()
        queue = await self.declare_queue(queue_name)
        # await self.channel.default_exchange.publish(
        #     aio_pika.Message(body=message.model_dump_json().encode("utf-8")),
        #     routing_key=queue.name,
        # )
        await self.channel.default_exchange.publish(
            aio_pika.Message(message.encode("utf-8")),
            routing_key=queue.name,
        )

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
