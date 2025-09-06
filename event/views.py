from django.contrib.admin.templatetags.admin_modify import register
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from device.models import Device, Event
from device_registry import DeviceRegistry
from event.serializer import EventSerializer
from event.utils import get_models_with_supported_actions
from utils.web_socket_message import update_frontend_device


class CreateDeleteEvent(APIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Device.objects.filter(room__user=self.request.user)

    def post(self, request, *args, **kwargs):
        event = Event.objects.create(
            device=get_object_or_404(Device, pk=request.data["device"]),
            target_device=get_object_or_404(Device, pk=request.data["target_device"]),
            action=request.data["action"],
            event=request.data["event"],
            extra_settings=request.data["extra_settings"],
        )
        update_frontend_device(event.device)
        return Response(EventSerializer(event).data, 201)

    def delete(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        device_id = event.device.id
        event.delete()
        device = get_object_or_404(Device, pk=device_id)
        update_frontend_device(device)
        return Response({}, 200)


class GetActionsAndEvents(APIView):

    def get(self, request):
        id = request.query_params.get("id")
        fun = request.query_params.get("fun")
        models = get_models_with_supported_actions(request.user)
        register = DeviceRegistry()
        model = register.get_model(fun)
        device = get_object_or_404(model, home__users=request.user, pk=id)
        events = EventSerializer(device.events.all(), many=True).data
        return Response(
            {
                "models": models,
                "available_events": device.available_events(),
                "active_events": events,
            },
            200,
        )


class GetDeviceByFunction(APIView):

    def get(self, request):
        fun = request.query_params.get("function")
        register = DeviceRegistry()
        model = register.get_model(fun.lower())
        if not model:
            return Response([], 404)
        return Response(model.available_actions(), 200)
