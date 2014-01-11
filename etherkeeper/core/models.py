from django.db import models
from django.contrib.auth.models import User


class Author(User):
    user = models.OneToOneField(User)
    etherpad_id = models.CharField(max_length=42)
