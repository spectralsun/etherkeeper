from datetime import datetime
from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255, default='')
    created = models.DateField(default=lambda: datetime.today())
    

class PadMember(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('write', 'Write'),
        ('read', 'Read')
    )
    pad = models.OneToOneField(Pad)
    role = models.CharField(max_length=10, choices=ROLES)
    author = models.ForeignKey(Author, null=True)
    tags = models.ManyToManyField(Tag)

    roleint = lambda s, c: [x for x, r in enumerate(s.ROLES) if r[0] == c][0]
    
    def check_access(self, check):
        return self.roleint(check) >= self.roleint(self.role)
