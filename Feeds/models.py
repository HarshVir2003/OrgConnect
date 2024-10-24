from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Posts(models.Model):
    class PrivacyLevel(models.IntegerChoices):
        zero = 0, 'Public'
        one = 1, 'Private'
        two = 2, 'Contacts'

    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now=True)
    Privacy_level = models.IntegerField(
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.zero
    )

    class Meta:
        ordering = ['-created_at']


class Comments(models.Model):
    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Likes(models.Model):
    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
