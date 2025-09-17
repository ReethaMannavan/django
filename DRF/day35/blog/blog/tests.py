from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Blog
from rest_framework.authtoken.models import Token
from django.urls import reverse

class BlogAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.token = Token.objects.create(user=self.user)

        # Auth header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Sample blog
        self.blog = Blog.objects.create(author=self.user, title='Test Blog', content='Test content')

    # ---------- GET Blogs ----------
    def test_get_blogs_v1(self):
        url = reverse('blog-list-v1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])
        self.assertIn('content', response.data[0])
        self.assertNotIn('category', response.data[0])

    def test_get_blogs_v2(self):
        url = reverse('blog-list-v2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category', response.data[0])
        self.assertIn('tags', response.data[0])
        self.assertIn('view_count', response.data[0])

    # ---------- POST Blog ----------
    def test_create_blog_v1(self):
        url = reverse('blog-list-v1')
        data = {'title': 'New Blog', 'content': 'New content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Blog')

    def test_create_blog_v2(self):
        url = reverse('blog-list-v2')
        data = {'title': 'V2 Blog', 'content': 'V2 content', 'category': 'Tech', 'tags': 'django,drf'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], 'Tech')

    # ---------- PUT Blog ----------
    def test_update_blog_by_author(self):
        url = reverse('blog-detail-v1', args=[self.blog.id])
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_update_blog_by_non_author(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('blog-detail-v1', args=[self.blog.id])
        data = {'title': 'Hack Title'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- DELETE Blog ----------
    def test_delete_blog_by_author(self):
        url = reverse('blog-detail-v1', args=[self.blog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_blog_by_non_author(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('blog-detail-v1', args=[self.blog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Throttling ----------
    def test_post_blog_throttle_limit(self):
        url = reverse('blog-list-v1')
        data = {'title': 'Throttle Blog', 'content': 'Content'}

        # Post 5 times → should succeed
        for _ in range(5):
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 6th post → should be throttled
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 429)
        self.assertIn('Request was throttled', response.data['detail'])
