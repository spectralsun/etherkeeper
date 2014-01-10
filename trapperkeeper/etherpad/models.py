from django.db import models
from trapperkeeper.core.models import Author

class Pad(models.Model):
    padid = models.CharField(max_length=20)
    groupid = models.CharField(max_length=20)
    title = models.CharField(max_length=255)

class Member(models.Model):
    PERMISSIONS = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('write', 'Write'),
        ('read', 'Read')
    )
    author = models.OneToOneField(Author)
    pad = models.OneToOneField(Pad)
