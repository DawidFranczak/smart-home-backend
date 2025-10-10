import pytest
from django.urls import reverse
from user.models import User, Home, Favourite
from room.models import Room
from device.models import Device
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_register_and_login(client):
    url_register = reverse("register")
    data = {"username": "testuser", "password": "pass123", "password2": "pass123"}
    response = client.post(url_register, data)
    assert response.status_code == 201
    user = User.objects.get(username="testuser")
    assert user is not None
    home = user.home.first()
    assert home is not None

    # login
    url_login = reverse("login")
    response_login = client.post(
        url_login, {"username": "testuser", "password": "pass123"}
    )
    assert response_login.status_code == 200
    assert "access" in response_login.data


@pytest.mark.django_db
def test_favourite_add_remove(auth_client, user, room, aquarium):
    # GET favourites
    url_get = reverse("favourite")
    res = auth_client.get(url_get)
    assert res.status_code == 200

    # PUT add room
    url_put = reverse("favourite")
    res_put = auth_client.put(
        url_put, {"type": "room", "id": room.id, "is_favourite": False}, format="json"
    )
    assert res_put.status_code == 200

    # PUT add device
    res_put_dev = auth_client.put(
        url_put,
        {"type": "device", "id": aquarium.id, "is_favourite": False},
        format="json",
    )
    assert res_put_dev.status_code == 200


@pytest.mark.django_db
def test_home_put_delete(auth_client, user, home):
    home = user.home.first()
    url = reverse("home")
    # PUT with invalid code
    res_invalid = auth_client.put(url, {"code": "invalid"})
    assert res_invalid.status_code == 400

    # DELETE home
    res_del = auth_client.delete(url)
    assert res_del.status_code == 204
    assert user.home.first() is not None
