import socket
from django.forms import ValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from lamp.models import Lamp

from .models import Rfid, Card


class RfidSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    controlled_lamp = serializers.SerializerMethodField()

    class Meta:
        model = Rfid
        exclude = [
            "port",
            "mac",
        ]

    def get_controlled_lamp(self, obj: Rfid):
        try:
            return {"name": obj.controlled_lamp.name, "id": obj.controlled_lamp.id}
        except Lamp.DoesNotExist:
            return None

    def get_cards(self, obj: Rfid):
        cards = obj.cards.all()
        serializer = CardSerializer(cards, many=True)
        return serializer.data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ["uid"]
        validators = [
            UniqueTogetherValidator(
                queryset=Card.objects.all(),
                fields=[
                    "rfid",
                    "name",
                ],
                message="Karta o tej nazwie już istnieje",
            ),
        ]

    def validate(self, attrs):
        rfid = attrs["rfid"]
        uid = self._get_uid(rfid)
        if rfid.cards.filter(uid=uid).exists():
            raise ValidationError("Karta już jest dodana")
        attrs["uid"] = uid
        return attrs

    def _get_uid(self, rfid: Rfid):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(str.encode("add-tag"), (rfid.ip, rfid.port))
            sock.settimeout(11)
            data = sock.recvfrom(128)
            uid = int(data[0].decode("UTF-8"))
            return uid
        except TimeoutError:
            sock.close()
            raise ValidationError("Brak połączenia z urządzeniem")
