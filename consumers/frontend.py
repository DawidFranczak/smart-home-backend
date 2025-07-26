import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
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
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # print("receive", text_data)
        pass

    async def send_to_frontend(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, code):
        print("disconnect", code)

    @database_sync_to_async
    def validate_user(self, token):
        try:
            access_token = AccessToken(token)
        except TokenError:
            return None

        user_id = access_token.payload.get("user_id", 0)

        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None

    @sync_to_async
    def get_home_id(self, user):
        return user.home.first().id
