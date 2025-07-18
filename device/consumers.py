import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync

from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.device_message import (
    set_settings_response,
    get_event_request,
)
from communication_protocol.message_event import MessageEvent
from device.models import Router, Device
from device.serializers.router import RouterSerializer
from rfid.consumer_utils import check_uid
from device.serializers.device import DeviceSerializer
from user.frontend_message_type import FrontendMessageType
from utils.get_model_serializer_by_fun import get_model_serializer_by_fun
from utils.get_to_device_model_serializer import get_to_device_model_serializer

from rfid.models import Card, Rfid


class RouterConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.queue = None
        self.mac = None
        self.router = None

    async def connect(self):
        self.mac = self.scope["url_route"]["kwargs"]["mac_address"]
        try:
            self.router: Router = await sync_to_async(
                Router.objects.select_related("home").get
            )(mac=self.scope["url_route"]["kwargs"]["mac_address"])

            self.router.last_seen = datetime.now()
            self.router.is_online = True
            await sync_to_async(self.router.save)(
                update_fields=["last_seen", "is_online"]
            )
            self.queue = {}
            await self.channel_layer.group_add(f"router_{self.mac}", self.channel_name)
            await self.accept()
            await self.send_to_frontend(
                200,
                FrontendMessageType.UPDATE_ROUTER,
                await self.get_router_serialized_data(),
            )
        except Router.DoesNotExist:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = DeviceMessage.from_json(text_data)
        except Exception as e:
            print("Error in message", e)
            return

        method_name = f"{data.message_event.lower()}_{data.message_type.lower()}"
        method = getattr(self, method_name, None)
        if not method:
            raise Exception("Method not found " + method_name)
        await method(data)

    async def disconnect(self, code):
        self.router.last_seen = datetime.now()
        self.router.is_online = False
        await sync_to_async(self.router.save)(update_fields=["last_seen", "is_online"])
        await self.send_to_frontend(
            200,
            FrontendMessageType.UPDATE_ROUTER,
            await self.get_router_serialized_data(),
        )

    async def router_send(self, event):
        if not isinstance(event, str):
            event = event["data"]
        await self.send(text_data=event)

    ########################### utils ########################################
    @sync_to_async
    def get_device_by_mac(self, mac):
        device = Device.objects.filter(mac=mac)
        if device.exists():
            return device.first()
        return None

    @sync_to_async
    def get_or_create_device(self, data: DeviceMessage):
        device = Device.objects.filter(mac=data.device_id)
        if device.exists():
            return device.first()
        try:
            model, _ = get_model_serializer_by_fun(data.payload["fun"])
            data.payload["mac"] = data.device_id
            data.payload["home"] = self.router.home
            data.payload["last_seen"] = datetime.now()
            data.payload["is_online"] = True
            device = model.objects.create(**data.payload)
            device_data = DeviceSerializer(device).data
            async_to_sync(self.send_to_frontend)(
                200, FrontendMessageType.NEW_DEVICE_CONNECTED, device_data
            )
        except Exception as e:
            print(e)
            return None

    @sync_to_async
    def serialized_device_to_device(self, device):
        model, serializer = get_to_device_model_serializer(device.fun)
        data = serializer(model.objects.get(id=device.id)).data
        return data

    @sync_to_async
    def get_router_serialized_data(self):
        return RouterSerializer(self.router).data

    @sync_to_async
    def get_device_serialized_data_to_frontend(self, device: Device):
        return DeviceSerializer(device).data

    @sync_to_async
    def get_event_request(self, device: Device, event: MessageEvent):
        events = device.events.filter(event=event.value)
        if not events.exists():
            return []
        return [get_event_request(event) for event in events]

    async def send_actions_request(self, actions: list[DeviceMessage]):
        for action in actions:
            await self.router_send(action.to_json())

    async def send_to_frontend(
        self, status: int, action: FrontendMessageType, data: dict
    ):
        await self.channel_layer.group_send(
            f"home_{self.router.home.id}",
            {
                "type": "send_to_frontend",
                "action": action.value,
                "data": {"status": status, "data": data},
            },
        )

    async def update_frontend_by_device_id(self, device_id: str):
        device = await self.get_device_by_mac(device_id)
        if not device:
            return
        await self.update_frontend_by_device(device)

    async def update_frontend_by_device(self, device: Device):
        device_data = await self.get_device_serialized_data_to_frontend(device)
        await self.send_to_frontend(200, FrontendMessageType.UPDATE_DEVICE, device_data)

    ########################### request ########################################

    async def device_connect_request(self, data: DeviceMessage):
        device = await self.get_or_create_device(data)
        if not device:
            return
        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        serialized_device_data = await self.serialized_device_to_device(device)
        message = set_settings_response(
            data.message_id, data.device_id, serialized_device_data
        )
        await sync_to_async(device.save)(
            update_fields=["last_seen", "is_online", "pending"]
        )
        await self.router_send(message.to_json())
        await self.update_frontend_by_device(device)

    async def device_disconnect_request(self, data: DeviceMessage):
        device = await self.get_device_by_mac(data.device_id)
        if not device:
            return
        device.last_seen = datetime.now()
        device.is_online = False
        device.pending = []
        await sync_to_async(device.save)(
            update_fields=["last_seen", "is_online", "pending"]
        )
        await self.update_frontend_by_device(device)

    async def health_check_request(self, data: DeviceMessage):
        device = await self.get_device_by_mac(data.device_id)
        device.last_seen = datetime.now()
        device.is_online = True
        device.wifi_strength = data.payload.get("wifi_strength", -100)
        await sync_to_async(device.save)(
            update_fields=["last_seen", "wifi_strength", "is_online"]
        )

    ############# EVENTS ###########################
    async def on_read_request(self, data: DeviceMessage):
        device = await sync_to_async(Rfid.objects.get)(mac=data.device_id)
        result = await check_uid(device, data.payload["uid"])
        event = MessageEvent.ON_READ_SUCCESS if result else MessageEvent.ON_READ_FAILURE
        actions_request = await self.get_event_request(device, event)
        await self.send_actions_request(actions_request)

    async def on_click_request(self, data: DeviceMessage):
        device = await self.get_device_by_mac(data.device_id)
        actions_request = await self.get_event_request(device, MessageEvent.ON_CLICK)
        await self.send_actions_request(actions_request)

    async def on_hold_request(self, data: DeviceMessage):
        device = await self.get_device_by_mac(data.device_id)
        actions_request = await self.get_event_request(device, MessageEvent.ON_HOLD)
        await self.send_actions_request(actions_request)

    ########################### response ########################################

    async def set_settings_response(self, data: DeviceMessage):
        await self.update_frontend_by_device_id(data.device_id)

    async def add_tag_response(self, data: DeviceMessage):
        device = await self.get_device_by_mac(data.device_id)
        rfid = await sync_to_async(Rfid.objects.get)(pk=device.id)
        uid = data.payload["uid"]
        status = 400
        if uid:
            cards = await sync_to_async(Card.objects.filter)(uid=uid)
            if await sync_to_async(cards.exists)():
                status = 409
            else:
                await sync_to_async(Card.objects.create)(
                    rfid=rfid,
                    uid=uid,
                    name=data.payload["name"],
                )
                status = 201
        rfid.pending.remove(MessageEvent.ADD_TAG.value)
        await sync_to_async(rfid.save)(update_fields=["pending"])
        device_data = await self.get_device_serialized_data_to_frontend(device)
        await self.send_to_frontend(
            status, FrontendMessageType.UPDATE_DEVICE, device_data
        )

    async def access_granted_response(self, data: DeviceMessage):
        # print("access_granted_response", data)
        pass

    async def access_denied_response(self, data: DeviceMessage):
        # print("access_denied_response", data)
        pass

    async def check_uid_response(self, data: DeviceMessage):
        # print("check_uid_response", data)
        pass

    async def turn_on_response(self, data: DeviceMessage):
        # print(data)
        pass

    async def blink_response(self, data: DeviceMessage):
        pass

    async def toggle_response(self, data: DeviceMessage):
        pass
