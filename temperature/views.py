import requests
from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from device.serializers.device import DeviceSerializer
from .models import TempHum


class TempHumList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[TempHum, TempHum]:
        return TempHum.objects.filter(room__user=self.request.user)


class TempHumRetrieve(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[TempHum, TempHum]:
        return TempHum.objects.filter(room__user=self.request.user)


class TempHumHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mac = get_object_or_404(TempHum, pk=pk).mac
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        query_str = f"?device_id={mac}"
        if start_date:
            query_str += f"&start_date={start_date}"
        if end_date:
            query_str += f"&end_date={end_date}"
        temperature_data = requests.get(
            f"http://sensor_service:8000/temperature/{query_str}"
        )
        humidity_data = requests.get(f"http://sensor_service:8000/humidity/{query_str}")
        response_data = {}
        if temperature_data.status_code == 200:
            response_data["temperature"] = temperature_data.json()
        if humidity_data.status_code == 200:
            response_data["humidity"] = humidity_data.json()
        return Response(response_data, status=200)
