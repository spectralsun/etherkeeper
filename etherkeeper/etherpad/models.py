from datetime import datetime
from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255, default='')
    title_author = models.ForeignKey(Author, null=True, unique=False)
    title_modified = models.DateTimeField(null=True)
    created = models.DateTimeField(default=lambda: datetime.today())
        
    def get_members_in_order(self):
        ordered = []
        for role in PadMember.ROLES:
            ordered += self.get_members_by_role(role[0])
        return ordered

    def get_members_by_role(self, role):
        members = []
        for member in self.members.all():
            if member.role == role:
                members.append(member)

        return members

    def get_title(self):
        
        return 'Untitled Document' if self.title == '' else self.title

class PadMember(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('write', 'Write'),
        ('read', 'Read')
    )
    pad = models.ForeignKey(Pad, related_name='members')
    role = models.CharField(max_length=10, choices=ROLES)
    joined = models.DateTimeField(default=lambda: datetime.today())
    author = models.ForeignKey(Author, null=True, related_name='pads')
    tags = models.ManyToManyField(Tag)
    
    def role_int(self, check):
        'Converts a role into its integer index' 
        return [x[0] for x in self.ROLES].index(check.lower())
    
    def check_access(self, check):
        try: 
            return self.role_int(check) >= self.role_int(self.role)
        except:
            return None

class Invite(models.Model):
    pad = models.ForeignKey(Pad)
    sender = models.ForeignKey(Author, related_name='sent_invites')
    to = models.ForeignKey(Author, related_name='invites')
    #message = models.TextField(null=True)
    role = models.CharField(max_length=10, choices=PadMember.ROLES)
    sent = models.DateTimeField(default=lambda: datetime.today())

