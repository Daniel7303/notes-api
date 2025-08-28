from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Note

class NoteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.token_url = '/api-token-auth/'
        self.note_url = '/api/notes/'

        # Get token
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_note(self):
        data = {
            'title': 'Test Note',
            'content': 'This is the content of the test note.',
        }

        response = self.client.post(self.note_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_get_notes(self):
        Note.objects.create(user=self.user, title="Note1", content="Content1")
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_other_user_cannot_update_note(self):
        other_user = User.objects.create_user(username='other', password='pass')
        note = Note.objects.create(user=other_user, title="Private", content="Secret")

        update_data = {
            "title": "Hacked Title",
            "content": "Should not work."
        }

        response = self.client.put(f'{self.note_url}{note.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
