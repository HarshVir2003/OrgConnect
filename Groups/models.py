from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    class Meta:
        unique_together = (('user', 'friend'),)

    def __str__(self):
        return f'{self.user} - {self.friend}'


class Community(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    description = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return f'{self.name}'


class Group(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    profile_img = models.URLField()
    members = models.ManyToManyField(User)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.community.name}'
