import json
from tokenize import TokenError

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User


class UserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_instance = None

    async def connect(self):
        token = self.scope["url_route"]["kwargs"]["token"]
        user = await self.validate_user(token)
        if not user:
            await self.close()
            return
        home_id = await self.get_home_id(user)
        self.user_instance = user
        await self.channel_layer.group_add(f"home_{home_id}", self.channel_name)
        print(self.channel_layer)
        print("connect", f"home_{home_id}")
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("receive", text_data)

    async def send_to_frontend(self, event):
        print("send_to_frontend", event)
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, code):
        print("disconnect", code)

    @sync_to_async
    def validate_user(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get("user_id", 0)
            user = User.objects.filter(id=user_id)
            if user.exists():
                return user.first()
            return None
        except Exception as e:
            print(e)
            return None

    @sync_to_async
    def get_home_id(self, user):
        return user.home.first().id
