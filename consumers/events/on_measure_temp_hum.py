from consumers.events.base_event import BaseEventRequest
from consumers.rabbitmq_publisher import RabbitMQPublisher, QueueNames
from consumers.router_message.builders.measurements import (
    measurements_sleeping_time_response,
)
from utils.round_timestamp_to_nearest_hour import round_timestamp_to_nearest_hour
from utils.sleeping_time import sleeping_time
from temperature.models import TempHum


class OnMeasureTempHum(BaseEventRequest):
    from consumers.router_message.messenger import DeviceMessenger

    publisher = RabbitMQPublisher()
    device_messanger = DeviceMessenger()

    def handle_request(self, consumer, message):
        try:
            sensor = TempHum.objects.get(mac=message.device_id)
        except TempHum.DoesNotExist:
            return
        sensor.timestamp = round_timestamp_to_nearest_hour()
        sensor.temperature = message.payload.temperature
        sensor.humidity = message.payload.humidity
        self.publisher.send_message(QueueNames.SENSORS, message)
        message = measurements_sleeping_time_response(message, sleeping_time())
        self.device_messanger.send(consumer.mac, message)
        sensor.save(update_fields=["timestamp", "temperature", "humidity"])
