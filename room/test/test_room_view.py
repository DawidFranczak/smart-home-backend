import pytest
from django.urls import reverse
from room.models import Room, Home


@pytest.mark.django_db
def test_list_rooms(auth_client, room, home):
    url = reverse("room-list-create")
    response = auth_client.get(url)
    assert response.status_code == 200
    names = [r["name"] for r in response.data]
    assert room.name in names


@pytest.mark.django_db
def test_create_room(auth_client, user, home):
    url = reverse("room-list-create")
    data = {"name": "NewRoom", "visibility": "private"}
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201
    from room.models import Room

    room = Room.objects.get(name="NewRoom")
    assert room.user == user
    assert room.home in user.home.all()


@pytest.mark.django_db
def test_retrieve_update_destroy_room(auth_client, room):
    url = reverse("room-retrieve-update-destroy", args=[room.id])

    # Retrieve
    res_get = auth_client.get(url)
    assert res_get.status_code == 200
    assert res_get.data["name"] == room.name

    # Update
    res_patch = auth_client.patch(url, {"name": "UpdatedName"}, format="json")
    assert res_patch.status_code == 200
    room.refresh_from_db()
    assert room.name == "UpdatedName"

    # Delete
    res_del = auth_client.delete(url)
    assert res_del.status_code in [200, 204]
    from room.models import Room

    assert not Room.objects.filter(id=room.id).exists()


@pytest.mark.django_db
def test_cannot_access_other_user_room(auth_client, user):
    from user.models import User

    other_user = User.objects.create_user(username="other", password="pass")
    home = Home.objects.create()
    room_other = Room.objects.create(name="OtherRoom", user=other_user, home=home)
    url = reverse("room-retrieve-update-destroy", args=[room_other.id])
    res = auth_client.get(url)
    assert res.status_code == 404
