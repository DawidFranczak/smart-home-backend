from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from .models import Rfid, Card


class RfidSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Rfid
        exclude = [
            "port",
            "mac",
        ]

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


class RfidSerializerDevice(RfidSerializer):
    class Meta:
        model = Rfid
        fields = ["name"]
