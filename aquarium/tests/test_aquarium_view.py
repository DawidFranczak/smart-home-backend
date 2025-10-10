import pytest
from django.urls import reverse
from aquarium.models import Aquarium
from django.contrib.auth.models import User
from room.models import Room
from user.models import Home


@pytest.mark.django_db
def test_aquarium_list_returns_user_aquariums(auth_client, aquarium, user):
    """
    Test that AquariumList returns only aquariums belonging to the authenticated user.
    """
    url = reverse("aquarium-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    data = response.json()

    # should return exactly one aquarium belonging to this user
    assert len(data) == 1
    assert data[0]["name"] == aquarium.name
    assert aquarium.room.user == user


@pytest.mark.django_db
def test_aquarium_list_does_not_include_other_users_data(
    auth_client, aquarium, user, db
):
    """
    Test that aquariums from other users are not visible.
    """

    # create second user and his aquarium
    other_user = User.objects.create_user(username="other", password="123")
    other_home = Home.objects.create()
    other_home.users.add(other_user)
    other_room = Room.objects.create(
        name="Other Room", user=other_user, home=other_home
    )
    Aquarium.objects.create(
        name="Other Aqua",
        room=other_room,
        home=other_home,
        fun="aquarium",
        mac="22:33:44:55:66:77",
        wifi_strength=-40,
    )

    url = reverse("aquarium-list")
    response = auth_client.get(url)
    data = response.json()

    # should only contain aquarium of logged user
    names = [a["name"] for a in data]
    assert "Other Aqua" not in names
    assert aquarium.name in names


@pytest.mark.django_db
def test_aquarium_update_no_changes_returns_empty_dict(auth_client, aquarium):
    """
    Test that update with no data changes returns an empty dict and 200 OK.
    """
    url = reverse("aquarium-retrieve-update-destroy", kwargs={"pk": aquarium.pk})

    payload = {
        "name": aquarium.name,  # same name → no changes
        "mac": aquarium.mac,
    }

    response = auth_client.put(url, data=payload, format="json")

    assert response.status_code == 200
    assert response.json() == {}  # no diff → empty response


@pytest.mark.django_db
def test_aquarium_update_with_changes_updates_instance(auth_client, aquarium):
    """
    Test that update with changed data updates the aquarium and returns 200 OK.
    """
    url = reverse("aquarium-retrieve-update-destroy", kwargs={"pk": aquarium.pk})

    payload = {
        "name": "Updated Aquarium",
        "mac": aquarium.mac,
    }

    response = auth_client.put(url, data=payload, format="json")

    assert response.status_code == 200

    aquarium.refresh_from_db()
    assert aquarium.name == "Updated Aquarium"


@pytest.mark.django_db
def test_aquarium_delete_removes_instance(auth_client, aquarium):
    """
    Test that DELETE removes the aquarium from database.
    """
    url = reverse("aquarium-retrieve-update-destroy", kwargs={"pk": aquarium.pk})

    response = auth_client.delete(url)
    assert response.status_code in [200, 204]

    # should be gone from DB
    assert not Aquarium.objects.filter(pk=aquarium.pk).exists()
