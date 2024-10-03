from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Achievements(models.Model):
    class PrivacyLevel(models.IntegerChoices):
        zero = 0, 'Public'
        one = 1, 'Private'
        two = 2, 'Contacts'

    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    achieved_at = models.DateField()
    Privacy_level = models.IntegerField(
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.zero
    )

    class Meta:
        ordering = ['-achieved_at']
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
        db_table = 'user_achievements'
        unique_together = (('title', 'user_id'),)
