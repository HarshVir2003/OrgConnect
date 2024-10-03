from Achievements.models import Achievements
from django.db.models import Q
from Groups.models import Contacts


# User achievements
class DataBuilder:
    def __init__(self, request_user, target_user):
        self.request_user = request_user
        self.target_user = target_user

    def get_data(self):
        is_friend = Contacts.objects.filter(user=self.request_user,
                                            friend=self.target_user).exists()
        if self.target_user == self.request_user:
            return Achievements.objects.filter(user_id=self.target_user)
        if is_friend:
            return Achievements.objects.filter(user_id=self.target_user).filter(
                Q(Privacy_level=Achievements.PrivacyLevel.zero) |
                Q(Privacy_level=Achievements.PrivacyLevel.two))
        return Achievements.objects.filter(
            user_id=self.target_user,
            Privacy_level=Achievements.PrivacyLevel.zero
        )
