import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from consumers.frontend_message_type import FrontendMessageType
from consumers.utils import validate_user


class UserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_instance = None
        self.token = None

    async def connect(self):
        token = self.scope["url_route"]["kwargs"]["token"]
        user = await validate_user(token)
        if not user:
            await self.close()
            return
        home_id = await self.get_home_id(user)
        self.user_instance = user
        await self.channel_layer.group_add(f"home_{home_id}", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_to_frontend(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, code):
        print("disconnect", code)

    @sync_to_async
    def get_home_id(self, user):
        return user.home.first().id

    @database_sync_to_async
    def get_router_mac(self):
        return self.user_instance.home.first().router.mac


