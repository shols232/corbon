from django.db import models

class File(models.Model):
    name = models.CharField(max_length = 100)
    zip_file = models.FileField(upload_to = 'zipfile/')

    def __str__(self):
        return self.name

# Create your models here.
