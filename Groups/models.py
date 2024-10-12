from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    chat_url = models.URLField(null=False)

    class Meta:
        unique_together = (('user', 'friend'),)

    def __str__(self):
        return f'{self.user} - {self.friend}'


class Community(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    description = models.CharField(max_length=2048, null=True)
    profile_img = models.URLField(null=False)

    def __str__(self):
        return f'{self.name}'


class Group(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    profile_img = models.URLField()
    members = models.ManyToManyField(User)
    chat_url = models.URLField(null=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def get_members(self):
        return [x for x in self.members.all()]

    def __str__(self):
        return f'{self.name} - {self.community.name}'
