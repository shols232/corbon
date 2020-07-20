from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from corbonmain.storage_backends import PrivateMediaStorage

class Files(models.Model):
    file = models.FileField(upload_to='excel_file/', null=True)

    def __str__(self):
        return self.file.name


class PrivateDocument(models.Model):
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage())


class File(models.Model):
    name = models.CharField(max_length = 100)
    zip_file = models.FileField(upload_to = 'zipfile/')

    def __str__(self):
        return self.name

# Create your models here.
