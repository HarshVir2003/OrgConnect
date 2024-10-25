from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from Groups.models import Contacts, Community, Group
from rest_framework.test import APITestCase, APIClient


class ContactsModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.contact = Contacts.objects.create(user=self.user1, friend=self.user2)

    def test_contact_creation(self):
        self.assertEqual(str(self.contact), 'user1 - user2')
        self.assertEqual(self.contact.user, self.user1)
        self.assertEqual(self.contact.friend, self.user2)

    def test_chat_url_initialization(self):
        self.assertIsNone(self.contact.chat_url)


class CommunityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='password123')
        self.community = Community.objects.create(
            name='Test Community',
            description='A test community',
            profile_img='http://example.com/img.jpg',
        )
        self.community.admins.add(self.user)

    def test_community_creation(self):
        self.assertEqual(str(self.community), 'Test Community')
        self.assertEqual(self.community.admins.first(), self.user)
        self.assertEqual(self.community.name, 'Test Community')


class GroupModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.community = Community.objects.create(
            name='Community 1',
            profile_img='http://example.com/img.jpg',
        )
        self.group = Group.objects.create(
            name='Test Group',
            profile_img='http://example.com/group_img.jpg',
            chat_url='http://example.com/chat',
            community=self.community,
        )
        self.group.members.add(self.user1, self.user2)

    def test_group_creation(self):
        self.assertEqual(str(self.group), 'Test Group - Community 1')
        self.assertEqual(self.group.community, self.community)

    def test_get_members(self):
        members = self.group.get_members()
        self.assertIn(self.user1, members)
        self.assertIn(self.user2, members)
        self.assertEqual(len(members), 2)


class GroupsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.community = Community.objects.create(name='Test Community', profile_img='http://example.com/img.jpg')
        self.group = Group.objects.create(
            name='Test Group',
            profile_img='http://example.com/group_img.jpg',
            chat_url='http://example.com/chat',
            community=self.community,
        )
        self.group.members.add(self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('getGroups')

    def test_get_groups(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_group(self):
        data = {
            'name': 'New Group',
            'profile_img': 'http://example.com/new_img.jpg',
            'members': [1],
            'chat_url': 'http://example.com/new_img.jpg',
            'community': self.community.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CommunityAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adminuser', password='password123')
        self.community = Community.objects.create(name='Community 1', profile_img='http://example.com/img.jpg')
        self.community.admins.add(self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('getCommunities')

    def test_get_communities(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_community(self):
        data = {
            'name': 'New Community',
            'description': 'A new community description',
            'profile_img': 'http://example.com/new_img.jpg',
            'admins': [1]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ContactsAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.url = reverse('getContacts')

    def test_get_contacts(self):
        Contacts.objects.create(user=self.user1, friend=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contacts_no_added_contacts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        data = {'user': self.user1.id, 'friend': self.user2.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MembersAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = APIClient()
        self.community = Community.objects.create(name='test', description='test Description', admins=[self.user1])
        self.group = Group.objects.create(name='testGroup', members=[self.user1, self.user2], chat_url='testUrl',
                                          community=self.community)

    def test_get_members(self):
        self.client.post(reverse('login'), {'username': 'user1', 'password': 'password123'})
        response = self.client.get(reverse('getMembers', kwargs={'id': self.group.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_members_not_by_admin(self):
        self.client.post(reverse('login'), {'username': 'user2', 'password': 'password123'})
        response = self.client.get(reverse('getMembers', kwargs={'id': self.group.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
