from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from room.models import Room
from user.models import Home

from .serializer import RoomSerializer


class ListCreateRoomView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        home = user.home.all().first()
        serializer.save(home=home, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        method = self.request.method
        if method == "POST":
            return Home.objects.filter(users=self.request.user).first().rooms.all()

        all_rooms = Home.objects.filter(users=self.request.user).first().rooms.all()
        user_room = all_rooms.filter(user=self.request.user).union(
            all_rooms.filter(visibility="PU")
        )
        return user_room


class RetrieveUpdateDestroyRoomView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        id = self.kwargs.get("pk")
        return Room.objects.filter(id=id, home__users=self.request.user)
