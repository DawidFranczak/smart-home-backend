from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from threading import Lock

from consumers.frontend_message.frontend_message import FrontendMessage
from consumers.frontend_message.frontend_message_type import FrontendMessageType
from device.models import Device


class FrontendMessenger:
    """Singleton class for sending messages to the frontend via Django Channels."""

    _instance = None
    _initialized = False
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(FrontendMessenger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the Channels layer."""
        self.channel_layer = get_channel_layer()

    def update_device(self, device: Device, status=200):
        """Send an update message for a specific device to the frontend.

        Args:
            device: The Device instance that has been updated.
            status: The status code to include in the message (default is 200).
        """
        from device.serializers.device import DeviceSerializer

        message = FrontendMessage(
            action=FrontendMessageType.UPDATE_DEVICE,
            status=status,
            data=DeviceSerializer(device).data,
        )
        self.send(device.home.id, message)

    async def send_async(self, home_id: int, message: FrontendMessage) -> None:
        """Asynchronously send a message to the frontend.

        Args:
            home_id: The ID of the home for the Channels group (e.g., forms 'home_123').
            message: The FrontendMessage object to send.
        """
        await self.channel_layer.group_send(
            f"home_{home_id}",
            {
                "type": "send_to_frontend",
                "data": message.model_dump(),
            },
        )

    def send(self, home_id: int, message: FrontendMessage) -> None:
        """Synchronously send a message to the frontend.

        Args:
            home_id: The ID of the home for the Channels group (e.g., forms 'home_123').
            message: The FrontendMessage object to send.
        """
        async_to_sync(self.send_async)(home_id, message)
