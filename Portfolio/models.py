from django.db import models
from django.contrib.auth.models import User


class PortfolioModel(models.Model):
    id = models.AutoField(User, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=2048, blank=False)
    location = models.CharField(max_length=1024, null=True)
    website = models.URLField(max_length=1024, null=True)
    birth_date = models.DateField(blank=False)
    linkedin_url = models.URLField(null=True)
    github_url = models.URLField(null=True)
    kaggle_url = models.URLField(null=True)
    google_scholar_url = models.URLField(null=True)

    class Meta:
        verbose_name = 'Portfolio Model'
        db_table = 'user_portfolio'

    def __str__(self):
        return f'User - {self.id}'
