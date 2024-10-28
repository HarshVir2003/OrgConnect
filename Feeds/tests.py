from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from Feeds.models import Posts, Comments, Likes


class FeedsAPITestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Login credentials
        self.login_data = {'username': 'user1', 'password': 'password1'}

        # Create some posts
        self.post1 = Posts.objects.create(user_id=self.user1, content="First Post", image_url="http://example.com/image1.jpg")
        self.post2 = Posts.objects.create(user_id=self.user2, content="Second Post", image_url="http://example.com/image2.jpg")

    def authenticate(self):
        """Helper method to log in the user."""
        response = self.client.post(reverse('login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)

    def test_get_feeds(self):
        """Test retrieving the user's feeds."""
        self.authenticate()
        response = self.client.get(reverse('LoadViews'))  # Using your URL pattern
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_post(self):
        """Test creating a new post."""
        self.authenticate()
        post_data = {
            'content': 'New Post Content',
            'image_url': 'http://example.com/new_image.jpg',
            'Privacy_level': 0
        }
        response = self.client.post(reverse('LoadViews'), data=post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], 'New Post Content')

    def test_create_comment(self):
        """Test adding a comment to a post."""
        self.authenticate()
        comment_data = {
            'post_id': self.post1.id,
            'content': 'Nice post!',
        }
        response = self.client.post(reverse('LoadViews'), data=comment_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], 'Nice post!')

    def test_delete_post(self):
        """Test deleting a post."""
        self.authenticate()
        response = self.client.delete(reverse('LoadViews'), data={'id': self.post1.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Posts.objects.filter(id=self.post1.id).exists())

    def test_dislike_post(self):
        """Test unliking a post."""
        self.authenticate()
        # Create a like
        like = Likes.objects.create(user_id=self.user1, post_id=self.post1)
        response = self.client.delete(reverse('LoadViews'), data={'id': like.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Likes.objects.filter(id=like.id).exists())
