import pytest
from django.urls import reverse
from button.models import Button


@pytest.mark.django_db
def test_button_list_returns_only_user_buttons(auth_client, room, home, button):
    """
    GET /button/ should return only buttons belonging to the authenticated user
    """
    # Button for another user (should not appear)
    other_button = Button.objects.create(
        name="OtherButton", fun="button", mac="XX:YY:ZZ"
    )

    url = reverse("button-list")
    response = auth_client.get(url)
    assert response.status_code == 200
    names = [b["name"] for b in response.data]
    assert button.name in names
    assert other_button.name not in names


@pytest.mark.django_db
def test_button_retrieve_update_destroy(auth_client, button):
    """
    Should retrieve, update, and delete a button
    """
    url = reverse("button-retrieve-update-destroy", args=[button.id])

    # Retrieve
    res_get = auth_client.get(url)
    assert res_get.status_code == 200
    assert res_get.data["name"] == "TestButton"

    # Update
    res_put = auth_client.patch(url, {"name": "UpdatedButton"}, format="json")
    assert res_put.status_code == 200
    button.refresh_from_db()
    assert button.name == "UpdatedButton"

    # Delete
    res_del = auth_client.delete(url)
    assert res_del.status_code in [200, 204]
    assert not Button.objects.filter(id=button.id).exists()
