from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from Chat.linkbuiilder import ChatLinkMaker
from MediaManagement.file_name import get_name_of_file


# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    chat_url = models.TextField()

    def on_save(self, *args, **kwargs):
        link = ChatLinkMaker(self.user.username, self.friend.username)
        link = link.make_link()
        self.chat_url = link

    def __str__(self):
        return f'{self.user} - {self.friend}'


class Community(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    description = models.CharField(max_length=2048, null=True)
    profile_img = models.ImageField(upload_to=get_name_of_file, null=True)
    admins = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        if self.file:
            img = Image.open(self.file)
            img = img.convert("RGB")
            img.thumbnail((800, 800))
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            self.file = ContentFile(buffer.read(), name=self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Group(models.Model):
    name = models.CharField(max_length=1024, blank=False)
    profile_img = models.ImageField(upload_to=get_name_of_file, null=True)
    members = models.ManyToManyField(User)
    chat_url = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=False)

    def save(self, *args, **kwargs):
        if self.file:
            img = Image.open(self.file)
            img = img.convert("RGB")
            img.thumbnail((800, 800))
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            self.file = ContentFile(buffer.read(), name=self.file.name)
        super().save(*args, **kwargs)

    def get_members(self):
        return [x for x in self.members.all()]

    def on_save(self, *args, **kwargs):
        link = ChatLinkMaker(self.name, self.community.name)
        link = link.make_link()
        self.chat_url = link

    def __str__(self):
        return f'{self.name} - {self.community.name}'
