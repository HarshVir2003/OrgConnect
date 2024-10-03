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
