from django.db import models
from etherkeeper.core.models import Author


class Document(models.Model):
    """
    An abstract document model.
    """
    TYPES = (
        ('etherpad','ep'),
        ('ethercalc', 'ec')
    )
    type = models.CharField(max_length=10, choices=TYPES)
    creator = models.ForeignKey(Author, related_name='owned_documents')

class DocumentMember(models.Model):
    """
    A member of a Document.
    """
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('write', 'Write'),
        ('read', 'Read')
    )
    document = models.ForeignKey(Document, related_name='members')
    role = models.CharField(max_length=10, choices=ROLES)
    joined = models.DateTimeField(default=lambda: datetime.today())
    author = models.ForeignKey(Author, null=True, related_name='documents')
    tags = models.ManyToManyField(Tag, related_name='documents')
    
    def role_int(self, role):
        """
        Converts a role into its integer index
        """
        return [x[0] for x in self.ROLES].index(role.lower())
    
    def check_access(self, access):
        """
        Check if member has adequate access
        """
        try: 
            return self.role_int(access) >= self.role_int(self.role)
        except:
            return None

class DocumentInvite(models.Model):
    """
    An invitation to become a DocumentMember.
    """
    document = models.ForeignKey(Document, related_name='invites')
    sender = models.ForeignKey(Author, related_name='sent_invites')
    to = models.ForeignKey(Author, related_name='invites')
    message = models.TextField(null=True)
    role = models.CharField(max_length=10, choices=PadMember.ROLES)
    sent = models.DateTimeField(default=lambda: datetime.today())
    #seen = models.BooleanField(default=False)    

class Tag(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, null=True)
