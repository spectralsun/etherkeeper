from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from etherkeeper.etherpad.models import Pad, PadMember, Invite
from etherkeeper.etherpad.helpers import get_etherpad_client, open_etherpad
from etherkeeper.core.models import Author
from etherkeeper.util.helpers import jsonify, set_cookie, epoch_time, \
    srender


@ensure_csrf_cookie
def create_view(request):
    'Creates an Etherpad-Lite Pad'
    e = get_etherpad_client()

    # Create a group for sharing functionality
    groupid = e.createGroup()['groupID']
    # Create a pad on the group
    padid = e.createGroupPad(groupID=groupid, padName='ek')['padID']
    # Store reference to the group and pad
    pad = Pad(groupid=groupid, padid=padid)
    pad.save()

    user = request.user
    author = Author.get_by_user(user)
        
    # Set current 
    padmember = PadMember(pad=pad, role='owner', author=author)
    padmember.save()

    return open_etherpad(pad, author, epoch_time(604800), e, id=padmember.id)


@ensure_csrf_cookie
def open_view(request):
    'Open an etherpad-lite pad for writing'
    author = Author.get_by_user(request.user)
    member = author.get_padmember(request.POST['id'])
    if not member or not member.check_access('write'):
        return jsonify(success=False)

    return open_etherpad(member.pad, author, epoch_time(7 * 24 * 60**2))

@ensure_csrf_cookie
def read_view(request):
    'Read an etherpad-lite pad'
    author = Author.get_by_user(request.user)
    member = author.get_padmember(request.POST['id'])
    if not member or not member.check_access('write'):
        return jsonify(success=False)

    # TODO
    return jsonify(success=True) 

@ensure_csrf_cookie
def set_title_view(request):
    "Set a pad's and broadcast to active authors"
    author = Author.get_by_user(request.user)
    padmember = author.get_padmember(request.POST['id'])
    if not padmember or not padmember.check_access('write'):
        return jsonify(success=False)

    pad = padmember.pad
    pad.title = request.POST['title']
    pad.title_author = author
    pad.title_modified = datetime.today()
    pad.save()

    e = get_etherpad_client()
    e.sendClientsMessage(padID=pad.padid, msg='title_update')
    return jsonify(success=True)

@ensure_csrf_cookie
def title_view(request):
    author = Author.get_by_user(request.user)
    padmember = author.get_padmember(request.POST['id'])
    if not padmember or not padmember.check_access('read'):
        return jsonify(success=False)
    pad = padmember.pad
    return jsonify(
        success=True, 
        title=pad.title,
        title_author=pad.title_author.user.username,
        #title_modified=pad.title_modified
        )

@ensure_csrf_cookie
def open_sharing_view(request):
    'Returns the sharing html for a pad'
    author = Author.get_by_user(request.user)
    padmember = author.get_padmember(request.POST['id'])
    if not padmember or not padmember.check_access('read'):
        return jsonify(success=False)
    invites = padmember.pad.get_invites_in_order()

    return jsonify(
        success=True,
        sharing=srender('share/pad.jinja', 
            members=padmember.pad.get_members_in_order(),
            invites=invites
        ))

@ensure_csrf_cookie
def share_view(request):
    author = Author.get_by_user(request.user)
    padmember = author.get_padmember(request.POST['id'])
    if not padmember or not padmember.check_access('admin'):
        return jsonify(success=False)

    acl = dict(owner=['admin','write','read'], admin=['write','read'])
    if request.POST['access'] not in acl[padmember.role]:
        return jsonify(success=False)      
          
    members = request.POST['members'].split(',')
    for member in members:
        to = Author.get_by_username(member)
        invite = Invite(
            pad=padmember.pad, 
            role=request.POST['access'], 
            to=to,
            sender=author)
        invite.save()

    return jsonify(success=True)

@ensure_csrf_cookie
def respond_view(request):
    author = Author.get_by_user(request.user)
    invite = author.invites.filter(id=request.POST['id']).first()
    if not invite:
        return jsonify(success=False)

    if request.POST['accept'] == 'true':
        padmember = PadMember(pad=invite.pad, role=invite.role, author=author)
        padmember.save()
    invite.delete()
    return jsonify(success=True)

@ensure_csrf_cookie
def ignore_invite_view(request):
    pass