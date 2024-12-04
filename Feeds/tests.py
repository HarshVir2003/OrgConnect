from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from setuptools.command.alias import format_alias
from io import BytesIO
from Feeds.models import Posts, Comments, Likes
from PIL import Image
from django.core.files.base import ContentFile

img_io = BytesIO()
img = Image.open('/home/jass/Downloads/a-drop-of-pink-and-yellow-paint-in-water.jpg')
img.save(img_io, format='JPEG')
img_io.seek(0)
img = ContentFile(img_io.read(), name='test_img.jpg')

class FeedsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Login data for user1
        self.login_data = {'username': 'user1', 'password': 'password1'}

        # Create posts
        self.post1 = Posts.objects.create(user_id=self.user1, content="First Post",
                                          image_url=img)
        self.post2 = Posts.objects.create(user_id=self.user2, content="Second Post",
                                          image_url=img)

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
        post_data = {'content': 'New post', 'image_url': img, 'Privacy_level': 0}
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
        comment_data = {'post_id': self.post2.id, 'content': 'Great post!', 'user_id': self.user1.id}
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
        response = self.client.delete(reverse('comment-detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comments.objects.filter(id=self.comment.id).exists())

    def test_delete_non_existent_comment(self):
        """Test deleting a non-existent comment."""
        self.authenticate()
        response = self.client.delete(reverse('comment-create'))
        self.assertEqual(response.status_code, 404)

    def test_like_post(self):
        """Test liking a post."""
        self.authenticate()
        like_data = {'post_id': self.post2.id, 'user_id': self.user1.id}
        response = self.client.post(reverse('like-create'), data=like_data)
        self.assertEqual(response.status_code, 201)

    def test_unlike_post(self):
        """Test unliking a post."""
        self.authenticate()
        response = self.client.delete(reverse('like-create', args=[self.like.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Likes.objects.filter(id=self.like.id).exists())

    def test_unlike_non_existent_post(self):
        """Test unliking a non-existent post."""
        self.authenticate()
        response = self.client.delete(reverse('like-create'), args=[999])
        self.assertEqual(response.status_code, 404)

    def test_feed_without_authentication(self):
        """Test access to feeds without authentication."""
        response = self.client.get(reverse('feeds'))
        self.assertEqual(response.status_code, 403)

    def test_create_post_without_authentication(self):
        """Test creating a post without authentication."""
        post_data = {'content': 'Unauthorized post', 'image_url': img, 'Privacy_level': 0}
        response = self.client.post(reverse('post-create'), data=post_data)
        self.assertEqual(response.status_code, 403)


class FeedsAdditionalTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Login data for user1
        self.login_data = {'username': 'user1', 'password': 'password1'}

        # Create posts
        self.post1 = Posts.objects.create(user_id=self.user1, content="First Post",
                                          image_url=img)
        self.post2 = Posts.objects.create(user_id=self.user2, content="Second Post",
                                          image_url=img)

        # Create comments
        self.comment1 = Comments.objects.create(user_id=self.user1, post_id=self.post1, content="Nice Post!")
        self.comment2 = Comments.objects.create(user_id=self.user2, post_id=self.post2, content="Cool!")

        # Create likes
        self.like1 = Likes.objects.create(user_id=self.user1, post_id=self.post1)
        self.like2 = Likes.objects.create(user_id=self.user2, post_id=self.post2)

    def authenticate(self):
        """Log in the user and return the authentication status."""
        response = self.client.post(reverse('login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)

    """
    Post updating not part of first version words of His Holiness the team leader himself !!!.
    """

    # 1. Test updating a post (user should own the post)
    # def test_update_post(self):
    #     self.authenticate()
    #     response = self.client.put(
    #         reverse('post-detail', args=[self.post1.id]),
    #         data={'content': 'Updated Post', 'image_url': 'http://example.com/updated.jpg'},
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(self.post1.content, 'Updated Post')
    #
    # # 2. Test updating another user's post (should fail)
    # def test_update_another_users_post(self):
    #     self.authenticate()
    #     response = self.client.put(
    #         reverse('post-detail', args=[self.post2.id]),
    #         data={'content': 'Unauthorized Update', 'image_url': 'http://example.com/unauth.jpg'},
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 403)

    # 3. Test creating a post with long content (exceeding max_length)
    def test_create_post_with_long_content(self):
        self.authenticate()
        long_content = 'A' * 10001  # 1 character over the limit
        response = self.client.post(reverse('post-create'),
                                    data={'content': long_content, 'image_url': img})
        self.assertEqual(response.status_code, 403)

    # 4. Test creating a comment without a post reference
    def test_create_comment_without_post(self):
        self.authenticate()
        response = self.client.post(reverse('comment-create'), data={'content': 'Comment without post!'})
        self.assertEqual(response.status_code, 403)

    # 5. Test retrieving an empty list of comments for a post
    def test_get_comments_for_post_with_no_comments(self):
        self.authenticate()
        response = self.client.get(reverse('comment-detail', args=[self.post2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Only 1 comment exists

    # 6. Test liking a post multiple times (should be prevented)
    def test_duplicate_like(self):
        self.authenticate()
        response = self.client.post(reverse('like-create'), data={'post_id': self.post1.id})
        self.assertEqual(response.status_code, 403)  # Duplicate like should be forbidden

    # 7. Test unliking without providing like ID
    def test_unlike_without_id(self):
        self.authenticate()
        response = self.client.delete(reverse('like-create'), data={})
        self.assertEqual(response.status_code, 404)

    # 8. Test retrieving feeds for a user with no posts
    def test_get_feeds_for_new_user_with_no_posts(self):
        User.objects.create_user(username='user3', password='password3')
        self.client.post(reverse('login'), data={'username': 'user3', 'password': 'password3'})
        response = self.client.get(reverse('feeds'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # 9. Test unauthorized post deletion
    def test_delete_another_users_post(self):
        self.authenticate()
        response = self.client.delete(reverse('post-detail', args=[self.post2.id]))
        self.assertEqual(response.status_code, 404)

    # 10. Test liking a non-existent post
    def test_like_non_existent_post(self):
        self.authenticate()
        response = self.client.post(reverse('like-create'), data={'post_id': 999})
        self.assertEqual(response.status_code, 403)

    # 11. Test retrieving posts with pagination
    # Not needed in first version. -HVS
    # def test_pagination_in_feeds(self):
    #     self.authenticate()
    #     response = self.client.get(reverse('feeds') + '?page=1&limit=1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data), 1)  # Should return only 1 post

    # 12. Test deleting a post without providing ID
    def test_delete_post_without_id(self):
        self.authenticate()
        response = self.client.delete(reverse('post-create'))
        self.assertEqual(response.status_code, 404)

    # 13. Test comment deletion by a non-owner
    def test_delete_comment_by_non_owner(self):
        self.authenticate()
        response = self.client.delete(reverse('comment-detail', args=[self.comment2.id]))
        self.assertEqual(response.status_code, 404)

    # 14. Test liking a post without authentication
    def test_like_without_authentication(self):
        response = self.client.post(reverse('like-create'), data={'post_id': self.post1.id})
        self.assertEqual(response.status_code, 403)

    # 15. Test deleting a comment without providing ID
    def test_delete_comment_without_id(self):
        self.authenticate()
        response = self.client.delete(reverse('comment-create'), data={})
        self.assertEqual(response.status_code, 404)
