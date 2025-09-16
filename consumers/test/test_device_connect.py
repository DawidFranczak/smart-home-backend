import pytest
from aquarium.models import Aquarium
from consumers.communication_protocol.Message import Message
from consumers.communication_protocol.message_event import MessageEvent
from consumers.communication_protocol.message_type import MessageType
from consumers.events.device_connect import DeviceConnectEvent


@pytest.mark.django_db
class TestDeviceConnectEvent:
    def setup_method(self):
        self.event = DeviceConnectEvent()
        self.message = Message(
            message_type=MessageType.REQUEST,
            message_event=MessageEvent.DEVICE_CONNECT,
            device_id="00:11:22:34:44:55",
            payload={
                "fun": "aquarium",
                "ip": "1.1.1.1",
                "port": "1234",
                "wifi_strength": "-50",
            },
            message_id="12345",
        )

    def test_create_device_should_return_none(self, home):

        for key in ["fun", "ip", "port", "wifi_strength"]:
            if key in self.message.payload:
                del self.message.payload[key]
            result = self.event._create_new_device(self.message, home)
            assert result is None

    def test_create_device_should_return_device(self, home):
        result = self.event._create_new_device(self.message, home)
        assert result is not None
        assert type(result) is Aquarium
