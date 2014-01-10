from django.db import models
from django.contrib.auth.models import User


class Author(User):
    user = models.OneToOneField(User)

