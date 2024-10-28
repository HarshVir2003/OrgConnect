from Feeds.models import Posts
from django.db.models import Q
from Groups.models import Contacts
from django.db.models import Count


class DataBuilder:
    def __init__(self, request_user):
        self.request_user = request_user

    def get_data(self):
        friends = Contacts.objects.filter(friend=self.request_user)
        friends = [x.user.username for x in friends]
        all_friends = [x.friend for x in Contacts.objects.filter(user=self.request_user) if
                       x.friend.username in friends]
        posts_friends = Posts.objects.filter(user_id__in=all_friends).filter(
            Q(Privacy_level=Posts.PrivacyLevel.zero) |
            Q(Privacy_level=Posts.PrivacyLevel.two)).order_by()
        all_public_posts = Posts.objects.filter(Privacy_level=Posts.PrivacyLevel.zero).order_by()
        all_data = all_public_posts.union(posts_friends).order_by('created_at')
        return all_data
