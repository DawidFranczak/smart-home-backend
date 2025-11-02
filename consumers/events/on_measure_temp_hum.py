from consumers.events.base_event import BaseEventRequest
from consumers.rabbitmq_publisher import RabbitMQPublisher, QueueNames, get_publisher
from consumers.router_message.builders.measurements import (
    measurements_sleeping_time_response,
)
from utils.sleeping_time import waiting_time
from temperature.models import TempHum


class OnMeasureTempHum(BaseEventRequest):
    from consumers.router_message.messenger import DeviceMessenger

    device_messanger = DeviceMessenger()

    def handle_request(self, consumer, message):
        try:
            sensor = TempHum.objects.get(mac=message.device_id)
        except TempHum.DoesNotExist:
            return
        sensor.timestamp = message.payload.timestamp
        sensor.temperature = message.payload.temperature
        sensor.humidity = message.payload.humidity
        sensor.save(update_fields=["timestamp", "temperature", "humidity"])
        self.device_messanger.send(
            consumer.mac, measurements_sleeping_time_response(message, waiting_time())
        )
        publisher = get_publisher()
        publisher.send_message(QueueNames.SENSORS, message)
