from datetime import datetime
from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Folder, Tag

class Pad(models.Model):
    """
    An etherpad-lite document
    Instances are created with a padid id and a groupid
    """
    padid = models.CharField(max_length=42)
    groupid = models.CharField(max_length=42)
    title = models.CharField(max_length=255, default='')
    title_author = models.ForeignKey(Author, null=True, unique=False)
    title_modified = models.DateTimeField(null=True)
    created = models.DateTimeField(default=lambda: datetime.today())
        
    def get_members_in_order(self):
        'Returns all members in order of role as the appear in PadMember.Role'
        ordered = []
        members = self.members.all()
        for role in PadMember.ROLES:
            ordered += self.get_role_members(role[0], members)
        return ordered

    def get_role_members(self, role, members):
        'Returns filtered array by role of members (or invites)'
        return [member for member in members if member.role == role]

    def get_invites_in_order(self):
        'Returns all invites in order of role as the appear in PadMember.Role'
        ordered = []
        invites = self.invites.all()
        for role in PadMember.ROLES:
            ordered += self.get_role_members(role[0], invites)
        return ordered

    def get_title(self):
        'Returns the title of a pad. If not set, returns "Untitled Document"'
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
    
    def role_int(self, role):
        'Converts a role into its integer index' 
        return [x[0] for x in self.ROLES].index(role.lower())
    
    def check_access(self, access):
        'Check if member has adequate access'
        try: 

            return self.role_int(access) >= self.role_int(self.role)
        except:
            return None

class Invite(models.Model):
    pad = models.ForeignKey(Pad, related_name='invites')
    sender = models.ForeignKey(Author, related_name='sent_invites')
    to = models.ForeignKey(Author, related_name='invites')
    #message = models.TextField(null=True)
    role = models.CharField(max_length=10, choices=PadMember.ROLES)
    sent = models.DateTimeField(default=lambda: datetime.today())
    #seen = models.BooleanField(default=False)
