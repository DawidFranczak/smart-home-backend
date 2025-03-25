from datetime import timedelta
from uuid import UUID, uuid4
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, render

from room.models import Room
from device.models import Device
from smart_home.settings import REFRESH_TOKEN_LIFETIME
from device.serializers.device import DeviceSerializer
from room.serializer import RoomSerializer
from .models import Favourite, Home


def index(request) -> HttpResponse:
    return render(request, "index.html")


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        username: str = request.data["username"]
        password: str = request.data["password"]
        user: AbstractUser | None = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"message": "Błędny login lub hasło."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh_token: Token = RefreshToken.for_user(user)
        print(refresh_token)
        response = Response()
        response.status_code = status.HTTP_200_OK
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            samesite="none",
            max_age=timedelta(seconds=REFRESH_TOKEN_LIFETIME),
            httponly=True,
            secure=True,
        )
        response.data = {"access": str(refresh_token.access_token)}
        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username: str = request.data.get("username", None)
        password: str = request.data.get("password", None)
        password2: str = request.data.get("password2", None)
        home_uuid: str = request.data.get("homeUuid", None)

        if not username or not password or not password2:
            return Response({"empty": "Proszę uzupełnić pola."}, 400)

        errors = {}
        if User.objects.filter(username=username).exists():
            errors["username"] = "Użytkownik już istnieje."

        if password != password2:
            errors["password2"] = "Hasła nie pasują do siebie."

        if home_uuid:
            try:
                parsed_uuid = UUID(home_uuid, version=4)
                home = Home.objects.get(add_uid=parsed_uuid)
            except:
                errors["homeUuid"] = "Błędny kod domu."
        else:
            home = Home.objects.create()

        if len(errors) > 0:
            return Response(errors, 400)

        user = User.objects.create_user(username=username, password=password)

        home.users.add(user)
        home.add_uid = uuid4()
        home.save()
        Favourite.objects.create(user=user)
        return Response({}, 201)


class RefreshAccessToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        try:
            refresh_token_str: str = request.COOKIES["refresh"]
            refresh_token = RefreshToken(refresh_token_str)
            return Response(
                {"access": str(refresh_token.access_token)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    def delete(self, request) -> Response:
        try:
            refresh_token: str = request.COOKIES["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie("refresh", path="/")
            return response
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class FavouriteView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user
        action = request.data["is_favourite"]
        if request.data["type"] == "room":
            obj = get_object_or_404(Room, pk=request.data["id"], user=user)
            (
                user.favourite.room.remove(obj)
                if action
                else user.favourite.room.add(obj)
            )
        elif request.data["type"] == "device":
            obj = get_object_or_404(Device, pk=request.data["id"])
            (
                user.favourite.device.remove(obj)
                if action
                else user.favourite.device.add(obj)
            )
        return Response({}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        favourite, _ = Favourite.objects.get_or_create(user=request.user)
        rooms = RoomSerializer(favourite.room.all(), many=True).data
        devices = DeviceSerializer(favourite.device.all(), many=True).data
        return Response({"rooms": rooms, "devices": devices}, status=status.HTTP_200_OK)
