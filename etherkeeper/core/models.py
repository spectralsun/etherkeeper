from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from etherkeeper.util.helpers import get_etherpad_client

class Author(models.Model):
    user = models.OneToOneField(User, related_name='author')
    etherpad_id = models.CharField(max_length=42)

    @classmethod
    def get_by_user(self, user):
        return self.objects.filter(user=user).first()

    @classmethod
    def get_by_username(self, username):
        return self.get_by_user(User.objects.filter(username=username).first())
    
    def get_padmember(self, id):
        return self.pads.filter(id=id).first()

    def get_documents(self):
        return self.pads.all()

def on_user_save(sender, instance, **kwargs):
    if not Author.get_by_user(instance):
        e = get_etherpad_client()
        author = Author(user=instance)
        author.etherpad_id = e.createAuthor(name=instance.username)['authorID']
        author.save()



post_save.connect(on_user_save, sender=User)