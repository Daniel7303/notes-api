from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from .models import Note


class NoteAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and make sure it's active
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="password123",
            is_active=True
        )

        # Get JWT token
        response = self.client.post(reverse("token_obtain_pair"), {
            "email": "test@example.com",
            "password": "password123"
        })
        print("LOGIN RESPONSE:", response.status_code, response.data)|quitqqqqqqqqqqq                                                                                                                                                                                                                                                                                                                               
        self.token = response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Set base URL for notes
        self.note_url = reverse("note-list")

    def test_create_note(self):
        data = {
            "title": "Test Note",
            "content": "This is the content of the test note.",
        }
        response = self.client.post(self.note_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_get_notes(self):
        Note.objects.create(user=self.user, title="Note1", content="Content1")
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_other_user_cannot_update_note(self):
        other_user = CustomUser.objects.create_user(
            email="other@example.com",
            password="pass123",
            is_active=True
        )
        note = Note.objects.create(user=other_user, title="Private", content="Secret")

        update_data = {
            "title": "Hacked Title",
            "content": "Should not work."
        }
        url = reverse("note-detail", args=[note.id])
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

