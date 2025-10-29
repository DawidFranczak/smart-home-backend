from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from consumers.frontend_message.messenger import FrontendMessenger
from device.models import Device, Event
from device.serializers.device import DeviceSerializer
from device_registry import DeviceRegistry
from event.serializer import EventSerializer
from event.utils import get_models_with_supported_actions


class CreateDeleteEvent(APIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Device.objects.filter(room__user=self.request.user)

    def post(self, request, *args, **kwargs):
        device = get_object_or_404(Device, pk=request.data["device"])
        event = Event.objects.create(
            device=device,
            target_device=get_object_or_404(Device, pk=request.data["target_device"]),
            action=request.data["action"],
            event=request.data["event"],
            extra_settings=request.data["extra_settings"],
        )
        FrontendMessenger().update_frontend(
            device.home.id, DeviceSerializer(device).data, 200
        )
        return Response(EventSerializer(event).data, 201)

    def delete(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        device_id = event.device.id
        event.delete()
        device = get_object_or_404(Device, pk=device_id)
        FrontendMessenger().update_frontend(
            device.home.id, DeviceSerializer(device).data, 200
        )
        return Response({}, 200)


class GetActionsAndEvents(APIView):

    def get(self, request):
        id = request.query_params.get("id")
        fun = request.query_params.get("fun")
        models = get_models_with_supported_actions(request.user)
        register = DeviceRegistry()
        model = register.get_model(fun)
        device = get_object_or_404(model, home__users=request.user, pk=id)
        return Response(
            {
                "models": models,
                "available_events": device.available_events(),
            },
            200,
        )


class GetAvailableActionAndExtraSettings(APIView):

    def get(self, request):
        fun = request.query_params.get("function")
        register = DeviceRegistry()
        model = register.get_model(fun.lower())
        if not model:
            return Response([], 404)
        return Response(
            {"actions": model.available_actions(), "settings": model.extra_settings()},
            200,
        )
