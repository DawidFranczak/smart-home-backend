# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from user.models import Home, Favourite
# from room.models import Room
# from aquarium.models import Aquarium
#
# User = get_user_model()
#
# class AquariumViewsTestCase(TestCase):
#     def setUp(self):
#         """Create test users, rooms, and aquariums."""
#         self.home = Home.objects.create()
#         self.client = APIClient()
#
#         self.user = User.objects.create_user(username="testuser", password="pass123")
#         self.other_user = User.objects.create_user(username="otheruser", password="pass456")
#         Favourite.objects.create(user=self.user)
#         Favourite.objects.create(user=self.other_user)
#
#         # Rooms
#         self.room = Room.objects.create(name="Room 1", user=self.user, home=self.home)
#         self.other_room = Room.objects.create(name="Room 2", user=self.other_user, home=self.home)
#
#         # Aquariums
#         self.aquarium = Aquarium.objects.create(
#             name="Aquarium 1",
#             room=self.room,
#             home=self.home,
#             port=1234,
#             ip="123.123.123.123",
#             fun="aquarium"
#
#         )
#         self.other_aquarium = Aquarium.objects.create(
#             name="Aquarium 2",
#             room=self.other_room,
#             home=self.home
#             ,port=1234,
#             ip="123.123.123.124",
#             fun="aquarium"
#         )
#         # get JWT token for self.user
#         refresh = RefreshToken.for_user(self.user)
#         access_token = str(refresh.access_token)
#
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
#
#     def test_list_aquariums_returns_only_user_items(self):
#         """Ensure the list view returns only aquariums belonging to the logged-in user."""
#         url = reverse("aquarium-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         results = [a["id"] for a in response.data]
#         self.assertIn(self.aquarium.id, results)
#         self.assertNotIn(self.other_aquarium.id, results)
#
#     # def test_retrieve_aquarium(self):
#     #     """Ensure a user can retrieve their own aquarium by ID."""
#     #     url = reverse("aquarium-retrieve-update-destroy", args=[self.aquarium.id])
#     #     response = self.client.get(url)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data["id"], self.aquarium.id)
#     #
#     # def test_update_aquarium_with_changes(self):
#     #     """Ensure updating an aquarium with changed data works correctly."""
#     #     url = reverse("aquarium-retrieve-update-destroy", args=[self.aquarium.id])
#     #     response = self.client.patch(
#     #         url,
#     #         {"name": "Updated Aquarium"},
#     #         format="json",
#     #     )
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data["name"], "Updated Aquarium")
#     #
#     # def test_update_aquarium_without_changes_returns_same_data(self):
#     #     """Ensure updating an aquarium without any actual changes returns existing data."""
#     #     url = reverse("aquarium-retrieve-update-destroy", args=[self.aquarium.id])
#     #     response = self.client.patch(
#     #         url,
#     #         {"name": self.aquarium.name},  # no changes
#     #         format="json",
#     #     )
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data["name"], self.aquarium.name)
#     #
#     # def test_delete_aquarium(self):
#     #     """Ensure a user can delete their own aquarium."""
#     #     url = reverse("aquarium-retrieve-update-destroy", args=[self.aquarium.id])
#     #     response = self.client.delete(url)
#     #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#     #     self.assertFalse(Aquarium.objects.filter(id=self.aquarium.id).exists())