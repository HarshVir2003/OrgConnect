from django.db import models
from MediaManagement.file_name import get_name_of_file

# Create your models here.
class JobUpdates(models.Model):
    title = models.CharField(max_length=1024, blank=False)
    company_name = models.CharField(max_length=1024, blank=False)
    location = models.CharField(max_length=1024, blank=False)
    job_url = models.URLField(blank=False)
    description = models.CharField(max_length=10000, null=True)
    posted_at = models.DateField(auto_now_add=True)
    job_type = models.CharField(max_length=1024, blank=False)
    image_url = models.ImageField(upload_to=get_name_of_file, null=True)

    class Meta:
        ordering = ['-posted_at']
        verbose_name = 'JobUpdate'
        verbose_name_plural = 'JobUpdates'
        db_table = 'Job_user'

