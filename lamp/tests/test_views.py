import pytest
from django.urls import reverse
from lamp.models import Lamp


@pytest.mark.django_db
def test_get_all_lamps(auth_client, room, home):
    """
    GET /lamp/ should return all lamps (no filtering by user)
    """
    lamp1 = Lamp.objects.create(
        fun="lamp", name="Lamp1", room=room, home=home, mac="AA:BB", brightness=50
    )
    lamp2 = Lamp.objects.create(
        fun="lamp", name="Lamp2", room=room, home=home, mac="CC:DD", brightness=60
    )

    url = reverse("get-lamp")
    response = auth_client.get(url)

    assert response.status_code == 200
    names = [l["name"] for l in response.data]
    assert lamp1.name in names
    assert lamp2.name in names


@pytest.mark.django_db
def test_retrieve_update_destroy_lamp(auth_client, room, home):
    """
    GET, PATCH, DELETE on RetrieveUpdateDestroyLamp
    """
    lamp = Lamp.objects.create(
        fun="lamp",
        name="LampTest",
        room=room,
        home=home,
        mac="AA:BB:cb:dd:ee:ff",
        brightness=40,
    )
    url = reverse("retrieve-update-destroy-lamp", args=[lamp.id])

    # Retrieve
    res_get = auth_client.get(url)
    assert res_get.status_code == 200
    assert res_get.data["name"] == "LampTest"

    # Update
    res_patch = auth_client.patch(url, {"brightness": 70}, format="json")
    assert res_patch.status_code == 200
    lamp.refresh_from_db()
    assert lamp.brightness == 70

    # Delete
    res_del = auth_client.delete(url)
    assert res_del.status_code in [200, 204]
    assert not Lamp.objects.filter(id=lamp.id).exists()


@pytest.mark.django_db
def test_retrieve_update_destroy_lamp_filtered_by_user(auth_client, room, home, user):
    """
    Should only allow access to lamps belonging to the user's rooms
    """
    # Lamp for another user
    lamp_other = Lamp.objects.create(
        fun="lamp", name="OtherLamp", mac="AA:BB:cc:dd:ee:ff", brightness=50
    )
    # Lamp for current user
    lamp_user = Lamp.objects.create(
        fun="lamp", name="UserLamp", room=room, home=home, mac="CC:DD", brightness=60
    )

    url = reverse("retrieve-update-destroy-lamp", args=[lamp_user.id])
    res_get_user = auth_client.get(url)
    assert res_get_user.status_code == 200
    assert res_get_user.data["name"] == "UserLamp"

    url_other = reverse("retrieve-update-destroy-lamp", args=[lamp_other.id])
    res_get_other = auth_client.get(url_other)
    assert res_get_other.status_code == 404  # cannot access lamp of another user
