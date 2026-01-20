from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from device.serializers.device import DeviceSerializer
from stairs.models import Stairs


class RetrieveUpdateDestroyStairs(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Stairs.objects.filter(room__user=self.request.user)
