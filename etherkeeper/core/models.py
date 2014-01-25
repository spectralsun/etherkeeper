from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User)
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