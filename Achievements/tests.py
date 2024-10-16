from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from Groups.models import Contacts
from Achievements.models import Achievements
import datetime


class AchievementTests(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(
            username='testuser1',
            email='testuser@example.com',
            password='testpassword'
        )

        self.test_user_2 = User.objects.create_user(
            username='testuser2',
            email='testuser@example.com',
            password='testpassword'
        )

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.post_url = reverse('postAchievement')

        Contacts.objects.create(user=self.test_user_1, friend=self.test_user_2)
        Achievements.objects.create(user_id=self.test_user_1,
                                    title='wrote tests',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.two)

        Achievements.objects.create(user_id=self.test_user_1,
                                    title='wrote tests 1',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.one)

        Achievements.objects.create(user_id=self.test_user_1,
                                    title='wrote tests 2',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.zero)

        Achievements.objects.create(user_id=self.test_user_2,
                                    title='wrote tests 3',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.two)

        Achievements.objects.create(user_id=self.test_user_2,
                                    title='wrote tests 4',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.one)

        Achievements.objects.create(user_id=self.test_user_2,
                                    title='wrote tests 5',
                                    achieved_at=datetime.date(year=2000, month=5, day=3),
                                    Privacy_level=Achievements.PrivacyLevel.zero)

    def test_create_new_achievement(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                                    'Privacy_level': Achievements.PrivacyLevel.zero})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_achievements_user_1_gets_user_2(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        get_url = reverse('getAchievement', kwargs={'id': self.test_user_2.id})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = response.json()
        self.assertEqual(len(json_data), 1)

    def test_get_achievements_user_2_gets_user_1(self):
        self.client.post(self.login_url, {'username': 'testuser2', 'password': 'testpassword'})
        get_url = reverse('getAchievement', kwargs={'id': self.test_user_1.id})
        response = self.client.get(get_url)
        json_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_data), 2)

    def test_user_unauthorized_post(self):
        response = self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                                    'Privacy_level': Achievements.PrivacyLevel.zero})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_achievements_unauthorized_gets_user_1(self):
        get_url = reverse('getAchievement', kwargs={'id': self.test_user_1.id})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_achievements_user_1_gets_user_1(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        get_url = reverse('getAchievement', kwargs={'id': self.test_user_1.id})
        response = self.client.get(get_url)
        json_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_data), 3)

    def test_same_achievement_for_multiple_users(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                                    'Privacy_level': Achievements.PrivacyLevel.zero})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.post(self.logout_url)
        self.client.post(self.login_url, {'username': 'testuser2', 'password': 'testpassword'})
        response = self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                                    'Privacy_level': Achievements.PrivacyLevel.zero})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_same_achievement_multiple_times(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                         'Privacy_level': Achievements.PrivacyLevel.zero})
        response = self.client.post(self.post_url, {'title': 'testAchivement', 'achieved_at': datetime.date.today(),
                                                    'Privacy_level': Achievements.PrivacyLevel.zero})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unknown_user_achievement(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        url = reverse('getAchievement', kwargs={"id": 10000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_achievement_authorized(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'Privacy_level': 2, 'id': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], "Achievement updated")
        self.assertEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, 2)

    def test_put_achievement_unauthorized(self):
        response = self.client.put(self.post_url, {'Privacy_level': 2, 'id': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, 1)

    def test_put_achievements_change_other_fields(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'id': 2, 'Privacy_level': 2, 'title': 'hoola boola hoo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(response.json()['message'], 'Achievement updated')
        self.assertNotEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, 2)
        self.assertNotEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).title, 'hoola boola hoo')

    def test_put_achievements_change_other_fields_unauthorized(self):
        response = self.client.put(self.post_url, {'id': 2, 'Privacy_level': 2, 'title': 'hoola boola hoo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_achievements_privacy_level_invalid_positive(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'Privacy_level': 200, 'id': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, 200)

    def test_put_achievements_privacy_level_invalid_negative(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'Privacy_level': -200, 'id': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, -200)

    def test_put_achievements_privacy_level_empty_string(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'Privacy_level': '', 'id': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Achievements.objects.get(user_id=self.test_user_1, id=2).Privacy_level, '')

    def test_put_achievements_not_exist(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.put(self.post_url, {'Privacy_level': 2, 'id': 200})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_achievement(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.delete(self.post_url, {'id': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Achievements.objects.filter(id=2, user_id=self.test_user_1).exists())

    def test_delete_invalid_achievement(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.delete(self.post_url, {'id': 200})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_some_other_user_achievement(self):
        self.client.post(self.login_url, {'username': 'testuser1', 'password': 'testpassword'})
        response = self.client.delete(self.post_url, {'id': 4})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Achievements.objects.filter(id=4, user_id=self.test_user_2).exists())

