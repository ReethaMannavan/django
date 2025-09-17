# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get('/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_v1(self):
        response = self.client.get('/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

    def test_profile_v2(self):
        response = self.client.get('/v2/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bio', response.data)

    def test_throttle_limit(self):
        # Make requests exceeding the limit
        for _ in range(6):
            response = self.client.get('/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
