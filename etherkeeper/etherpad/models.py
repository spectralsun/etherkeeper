from datetime import datetime
from django.db import models
from etherkeeper.core.models import Author
from etherkeeper.organize.models import Document


class Pad(models.Model):
    """
    An etherpad-lite document
    Instances are created with a padid id and a groupid
    """
    document = models.ForeignKey(Document, unique=True)
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
        """
        Returns the title of a pad. If not set, returns "Untitled Document".
        """
        return 'Untitled Document' if self.title == '' else self.title


