from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Achievements(models.Model):
    class PrivacyLevel(models.IntegerChoices):
        zero = 0, 'Public'
        one = 1, 'Private'
        two = 2, 'Contacts'
    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # User Object is The Foreign key not The user id
    title = models.CharField(max_length=2000)
    achieved_at = models.DateField()
    Privacy_level = models.IntegerField(
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.zero
    )