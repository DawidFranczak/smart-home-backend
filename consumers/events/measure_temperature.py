from consumers.events.base_event import BaseEventRequest
from consumers.rabbitmq_publisher import RabbitMQPublisher, QueueNames


class MeasureTemperature(BaseEventRequest):
    publisher = RabbitMQPublisher()

    def handle_request(self, consumer, message):
        # print(f"Temperature measurement event: {message}")
        self.publisher.send_message(QueueNames.SENSORS, message)
