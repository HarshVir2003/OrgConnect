from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserAuthTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.user_list_url = reverse('User', kwargs={'id': self.test_user.id})
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_user_registration_valid(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password_confirm': 'newpassword'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_invalid(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password_confirm': 'notnewpassword'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_login_valid(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_login_invalid(self):
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(self.client.session['_auth_user_id'])
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_get_user_profile_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_user_profile_unauthenticated(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_register_twice(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password_confirm': 'newpassword'
        }
        response2 = self.client.post(self.register_url, data)
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username='newuser').exists())
