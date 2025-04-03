from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from device.models import Device
from event.serializer import EventSerializer
from event.utils import get_models_with_supported_actions
from utils.get_model_serializer_by_fun import get_model_serializer_by_fun


class GetActionsAndEvents(APIView):

    def get(self, request):
        id = request.query_params.get("id")
        fun = request.query_params.get("fun")
        models = get_models_with_supported_actions(request.user)
        model, _ = get_model_serializer_by_fun(fun)
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
