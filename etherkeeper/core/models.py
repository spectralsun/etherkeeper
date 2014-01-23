from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User)
    etherpad_id = models.CharField(max_length=42)

    @classmethod
    def get_by_user(self, user):
        return self.objects.filter(user=user).first()

    
    def get_padmember(self, id):
        return self.padmember_set.filter(id=id).first()

    def get_documents(self):
        return self.padmember_set.all()