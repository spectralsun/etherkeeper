from django.db import models
from trapperkeeper.core.models import Author

class Pad(models.Model):
    padid = models.CharField(max_length=20)
    groupid = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    #owner = models.OneToOneField(Author)
    author = models.ForeignKey(Author)

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