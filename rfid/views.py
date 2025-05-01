from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from channels.layers import get_channel_layer
from rest_framework.response import Response
from communication_protocol.message_event import MessageEvent
from device.serializers.device import DeviceSerializer
from user.frontend_message_type import FrontendMessageType
from utils.web_socket_message import update_frontend_device
from .command import add_card
from .serializer import CardSerializer
from .models import Card, Rfid


class RfidListCreate(ListCreateAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Rfid.objects.filter(room__user=self.request.user)


class RfidRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Rfid.objects.filter(room__user=self.request.user)


class CardDestroy(DestroyAPIView):

    def get_queryset(self):
        return Card.objects.filter(
            rfid__room__user=self.request.user, id=self.kwargs["pk"]
        )

    def delete(self, request, *args, **kwargs):
        home_id = self.get_object().rfid.room.home.id
        rfid_id = self.get_object().rfid.id
        super().delete(request, *args, **kwargs)
        new_data = DeviceSerializer(Rfid.objects.get(id=rfid_id)).data
        update_frontend_device(home_id, new_data)
        return Response(status=204)


class CardListCreate(ListCreateAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        rfid = get_object_or_404(
            Rfid, id=self.request.data.get("rfid_id", 0), room__user=self.request.user
        )
        return rfid

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        rfid = validated_data["rfid"]
        if not MessageEvent.ADD_TAG.value in rfid.pending:
            rfid.pending.append(MessageEvent.ADD_TAG.value)
        rfid.save()
        serializer_data = DeviceSerializer(rfid).data
        add_card(rfid, validated_data["name"])
        return Response(serializer_data, 200)
