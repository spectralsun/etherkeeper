from django.db import models
from etherkeeper.core.models import Author

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Folder)
    author = models.ForeignKey(Author)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
