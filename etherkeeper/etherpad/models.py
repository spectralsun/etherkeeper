from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    folder = models.ForeignKey(Folder)
    tags = models.ManyToMany(Tag)

class Share(models.Model):
    class Meta:
        permissions = (
            ('admin', 'Admin'),
            ('write', 'Write'),
            ('read', 'Read')
        )
    pad = models.OneToOneField(Pad)
    role = models.CharField(max_length=10)
    author = models.ForeignKey(Author)