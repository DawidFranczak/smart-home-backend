from rest_framework import serializers

from utils.check_hour_in_range import check_hour_in_range
from .models import Aquarium
from .command import (
    change_rgb_request,
    change_fluo_lamp_state_request,
    change_led_state_request,
    check_and_change_led_time_request,
    check_and_change_fluo_lamp_time_request,
    change_mode,
)
from communication_protocol.message_event import MessageEvent


class AquariumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aquarium
        exclude = [
            "fun",
            "id",
            "port",
            "mac",
        ]

    def validate(self, attrs):
        self.validate_color(attrs)
        self.validate_led_time(attrs)
        self.validate_fluo_lamp_time(attrs)
        return attrs

    def validate_color(self, data):
        if not any([data.get("color_r"), data.get("color_g"), data.get("color_b")]):
            return data
        r = data.get("color_r", self.instance.color_r)
        g = data.get("color_g", self.instance.color_g)
        b = data.get("color_b", self.instance.color_b)
        change_rgb_request(self.instance, {"r": r, "g": g, "b": b})
        if not MessageEvent.SET_RGB.value in self.instance.pending:
            self.instance.pending.append(MessageEvent.SET_RGB.value)
        return data

    def validate_led_time(self, data):
        if not any([data.get("led_start"), data.get("led_stop")]):
            return data
        led_start = data.get("led_start", self.instance.led_start)
        led_stop = data.get("led_stop", self.instance.led_stop)
        led_mode = check_and_change_led_time_request(self.instance, led_start, led_stop)
        data["led_mode"] = led_mode
        if (
            led_mode != self.instance.led_mode
            and MessageEvent.SET_LED.value not in self.instance.pending
        ):
            self.instance.pending.append(MessageEvent.SET_LED.value)
        return data

    def validate_fluo_lamp_time(self, data):
        if not any([data.get("fluo_start"), data.get("fluo_stop")]):
            return data
        fluo_start = data.get("fluo_start", self.instance.fluo_start)
        fluo_stop = data.get("fluo_stop", self.instance.fluo_stop)
        fluo_mode = check_and_change_fluo_lamp_time_request(
            self.instance, fluo_start, fluo_stop
        )
        data["fluo_mode"] = fluo_mode
        if (
            fluo_mode != self.instance.fluo_mode
            and MessageEvent.SET_FLUO.value not in self.instance.pending
        ):
            self.instance.pending.append(MessageEvent.SET_FLUO.value)
        return data

    def validate_mode(self, data):
        change_mode(self.instance, data)
        return data

    def validate_led_mode(self, data):
        change_led_state_request(self.instance, data)
        return data

    def validate_fluo_mode(self, data):
        change_fluo_lamp_state_request(self.instance, data)
        return data


class AquariumSerializerDevice(serializers.ModelSerializer):
    led_mode = serializers.SerializerMethodField()
    fluo_mode = serializers.SerializerMethodField()

    class Meta:
        model = Aquarium
        fields = [
            "color_r",
            "color_g",
            "color_b",
            "led_mode",
            "fluo_mode",
        ]

    def get_led_mode(self, obj: Aquarium):
        if obj.mode:
            return check_hour_in_range(obj.led_start, obj.led_stop)
        return obj.led_mode

    def get_fluo_mode(self, obj: Aquarium):
        if obj.mode:
            return check_hour_in_range(obj.fluo_start, obj.fluo_stop)
        return obj.fluo_mode
