import pytest
from django.core.management import call_command
from django.contrib.auth.models import User
from user.models import Home, Favourite
from room.models import Room
from aquarium.models import Aquarium
from device.models import Device

@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    Favourite.objects.create(user=user)
    return user

@pytest.fixture
def home(db, user):
    home = Home.objects.create()
    home.users.add(user)
    return home

@pytest.fixture
def room(db, home, user):
    return Room.objects.create(name="Test", user=user, home=home)

@pytest.fixture
def aquarium(room,home):
    return Aquarium.objects.create(
        name="Test Aquarium",
        room = room,
        home = home,
        ip = "123.123.123.123",
        port = 1234,
        fun = "aquarium",
        mac = "00:11:22:33:44:55",
        wifi_strength =-50,
    )
@pytest.fixture
def device(room,home):
    return Device.objects.create(
        name="Test Device",
        room = room,
        home = home,
        ip = "123.123.123.13",
        port = 1234,
        fun = "aquarium",
        mac = "00:11:22:33:45:55",
        wifi_strength =-50,
    )
