import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from uuid import uuid4
from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType
from consumers.utils import validate_user, send_to_router, get_camera_channel_name

class CameraConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.camera = None
        self.router_mac = None
        self.token = None

    async def connect(self):
        try:
            token = self.scope['url_route']['kwargs']['token']
            camera_id = self.scope['url_route']['kwargs']['pk']
        except KeyError:
            await self.close()
            return

        user = await validate_user(token)
        if not user:
            await self.close()
            return


        camera = await self._get_camera(user, camera_id)
        if not camera:
            await self.close()
            return

        self.user = user
        self.camera = camera
        self.token = uuid4().hex
        await self.setup_router_mac()
        await self.channel_layer.group_add(get_camera_channel_name(self.token), self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action_type = data.get("type", None)
        if not action_type:
            return
        if action_type == MessageEvent.CAMERA_OFFER.value:
            message = self.message_camera_offer(data)
        else:
            return
        await send_to_router(message, self.router_mac)

    async def disconnect(self, code):
        if self.token:
            await self.channel_layer.group_discard(get_camera_channel_name(self.token), self.channel_name)

    async def camera_send(self, event):
        print(event)
        if event['message_event'] == MessageEvent.CAMERA_ERROR.value:
            data = {
                "type": MessageEvent.CAMERA_ERROR.value,
                "error": event.get("data", "Unknown error"),
            }
            await self.send(text_data=json.dumps(data))
            await self.close()
            return
        data = event['data']
        if type(data) == dict:
            data = json.dumps(data)
        await self.send(text_data=data)

    @database_sync_to_async
    def _get_camera(self, user, camera_id):
        camera = user.home.first().cameras.filter(pk=camera_id)
        if camera.exists():
            return camera.first()
        return None

    def get_camera_rtsp(self):
        if self.camera.username and self.camera.password:
            return f"rtsp://{self.camera.username}:{self.camera.password}@{self.camera.ip_address}:{self.camera.port}{self.camera.path}"
        return f"rtsp://{self.camera.ip_address}:{self.camera.port}{self.camera.path}"

    @database_sync_to_async
    def setup_router_mac(self):
        self.router_mac = self.user.home.first().router.mac

    def message_camera_offer(self, data:dict)-> DeviceMessage:
        return DeviceMessage(
            message_type=MessageType.REQUEST,
            message_event=MessageEvent.CAMERA_OFFER,
            device_id="camera",
            payload={
                "token": self.token,
                "offer": data.get("offer"),
                "rtsp": self.get_camera_rtsp()
            },
            message_id=uuid4().hex,
        )