import xmpp
import os
from django.conf import settings
from django.contrib.auth.models import User


class XmppBackend(object):
    def authenticate(self, username, password):
        client = xmpp.Client(settings.XMPP_SERVER, debug=[])
        conn = client.connect()
        if not con:
            raise Exception('Could not connect to server')
        auth = client.auth(username, password)
        if not auth:
            raise Exception('Invalid Username/Password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExcist:
            user = User(username=username, password=os.urandom(32))
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None