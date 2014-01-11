from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255)
    created = models.DateField()
    

class PadAuthor(models.Model):
    class Meta:
        permissions = (
            ('owner', 'Owner'),
            ('admin', 'Admin'),
            ('write', 'Write'),
            ('read', 'Read')
        )
    pad = models.OneToOneField(Pad)
    role = models.CharField(max_length=10)
    author = models.ForeignKey(Author, null=True)
    #folder = models.ForeignKey(Folder, null=True)
    tags = models.ManyToManyField(Tag)