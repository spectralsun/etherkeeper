import xmpp
import os
from random import randint
from django.conf import settings
from django.contrib.auth.models import User


class XmppBackend(object):
    def authenticate(self, username, password):
        client = xmpp.Client(settings.XMPP_SERVER, debug=[])
        conn = client.connect()
        if not conn:
            return None
        auth = client.auth(username, password)
        if not auth:
            return None
        print auth
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(
                username=username, 
                password=''.join(chr(randint(97, 122)) for _ in range(50))
            )
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None