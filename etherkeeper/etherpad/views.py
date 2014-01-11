from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from etherpad_lite import EtherpadLiteClient
from etherkeeper.etherpad.models import Pad, PadAuthor
from etherkeeper.core.models import Author
from etherkeeper.util.helpers import jsonify, set_cookie, epoch_time


@ensure_csrf_cookie
def create_view(request):
    e = EtherpadLiteClient(
        base_params={'apikey': settings.ETHERPAD_KEY},
        base_url=settings.ETHERPAD_URL + '/api'
    )
    pad = Pad()
    pad.groupid = e.createGroup()['groupID']
    pad.padid = e.createGroupPad(groupID=pad.groupid, padName='tk')['padID']
    pad.save()
    padauthor = PadAuthor()
    padauthor.pad = pad
    padauthor.role = 'owner'
    author = Author.get_by_user(request.user)
    user = request.user
    if not author:
        author = Author(user=user)
        author.etherpad_id = e.createAuthor(name=user.username)['authorID']
        author.save()
    padauthor.author = author
    padauthor.save()
    sessionid = e.createSession(
        groupID=pad.groupid, 
        authorID=author.etherpad_id, 
        validUntil=epoch_time(7*24*60*60)
    )['sessionID']
    response = jsonify(dict(
        success=True,
        pad='%s/p/%s' % (settings.ETHERPAD_URL, pad.padid)))
    set_cookie(response, 'sessionID', sessionid)
    return response


@ensure_csrf_cookie
def open_view(request):
    author = Author.get_by_user(request.user)
    pad = author.padauthor_set.filter(id=request.POST['id']).first().pad
    e = EtherpadLiteClient(
        base_params={'apikey': settings.ETHERPAD_KEY},
        base_url=settings.ETHERPAD_URL + '/api'
    )
    sessionid = e.createSession(
        groupID=pad.groupid, 
        authorID=author.etherpad_id, 
        validUntil=epoch_time(7*24*60*60)
    )['sessionID']
    response = jsonify(dict(
        success=True,
        pad='%s/p/%s' % (settings.ETHERPAD_URL, pad.padid)))
    set_cookie(response, 'sessionID', sessionid)
    return response