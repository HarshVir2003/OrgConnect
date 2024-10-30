from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from Feeds.models import Posts, Comments, Likes


class FeedsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Login data for user1
        self.login_data = {'username': 'user1', 'password': 'password1'}

        # Create posts
        self.post1 = Posts.objects.create(user_id=self.user1, content="First Post", image_url="http://example.com/1.jpg")
        self.post2 = Posts.objects.create(user_id=self.user2, content="Second Post", image_url="http://example.com/2.jpg")

        # Create comment
        self.comment = Comments.objects.create(user_id=self.user1, post_id=self.post1, content="Nice Post!")

        # Create like
        self.like = Likes.objects.create(user_id=self.user1, post_id=self.post1)

    def authenticate(self):
        """Log in the user and return the authentication status."""
        response = self.client.post(reverse('login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)

    def test_get_feeds(self):
        """Test retrieving all posts for the authenticated user."""
        self.authenticate()
        response = self.client.get(reverse('feeds'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_post(self):
        """Test creating a new post."""
        self.authenticate()
        post_data = {'content': 'New post', 'image_url': 'http://example.com/new.jpg', 'Privacy_level': 0}
        response = self.client.post(reverse('post-create'), data=post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], 'New post')

    def test_create_post_invalid_data(self):
        """Test creating a post with invalid data."""
        self.authenticate()
        response = self.client.post(reverse('post-create'), data={})
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        """Test deleting a post."""
        self.authenticate()
        response = self.client.delete(reverse('post-detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Posts.objects.filter(id=self.post1.id).exists())

    def test_delete_non_existent_post(self):
        """Test deleting a non-existent post."""
        self.authenticate()
        response = self.client.delete(reverse('post-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_create_comment(self):
        """Test adding a comment to a post."""
        self.authenticate()
        comment_data = {'post_id': self.post2.id, 'content': 'Great post!'}
        response = self.client.post(reverse('comment-create'), data=comment_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], 'Great post!')

    def test_get_comments_for_post(self):
        """Test retrieving all comments for a post."""
        self.authenticate()
        response = self.client.get(reverse('comment-detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_comment(self):
        """Test deleting a comment."""
        self.authenticate()
        response = self.client.delete(reverse('comment-detail', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comments.objects.filter(id=self.comment.id).exists())

    def test_delete_non_existent_comment(self):
        """Test deleting a non-existent comment."""
        self.authenticate()
        response = self.client.delete(reverse('comment-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_like_post(self):
        """Test liking a post."""
        self.authenticate()
        like_data = {'post_id': self.post2.id}
        response = self.client.post(reverse('like-create'), data=like_data)
        self.assertEqual(response.status_code, 201)

    def test_unlike_post(self):
        """Test unliking a post."""
        self.authenticate()
        response = self.client.delete(reverse('like-create'), data={'id': self.like.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Likes.objects.filter(id=self.like.id).exists())

    def test_unlike_non_existent_post(self):
        """Test unliking a non-existent post."""
        self.authenticate()
        response = self.client.delete(reverse('like-create'), data={'id': 999})
        self.assertEqual(response.status_code, 404)

    def test_feed_without_authentication(self):
        """Test access to feeds without authentication."""
        response = self.client.get(reverse('feeds'))
        self.assertEqual(response.status_code, 403)

    def test_create_post_without_authentication(self):
        """Test creating a post without authentication."""
        post_data = {'content': 'Unauthorized post', 'image_url': 'http://example.com/unauth.jpg', 'Privacy_level': 0}
        response = self.client.post(reverse('post-create'), data=post_data)
        self.assertEqual(response.status_code, 403)
