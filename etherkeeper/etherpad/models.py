from datetime import datetime
from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255, default='')
    title_author = models.OneToOneField(Author, null=True)
    title_modified = models.DateField(null=True)
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

    # converts a PadMember.ROLE to its integer index; ex: 'owner' = 0
    role_int = lambda s, c: [x for x, r in enumerate(s.ROLES) if r[0] == c][0]
    
    def check_access(self, check):
        try: 
            return self.role_int(check) >= self.role_int(self.role)
        except:
            return None
