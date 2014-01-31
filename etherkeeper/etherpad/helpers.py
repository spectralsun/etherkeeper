from django.conf import settings
from etherpad_lite import EtherpadLiteClient
from etherkeeper.util.helpers import jsonify, set_cookie

def get_etherpad_client():
    return EtherpadLiteClient(
        base_url=settings.ETHERPAD_URL + '/api',
        api_version='1.2.7',
        base_params={ 'apikey': settings.ETHERPAD_KEY })

def open_etherpad(pad, author, validUntil, e=None, **kwargs):
    if not e:
        e = get_etherpad_client()
    data = e.createSession(
        groupID=pad.groupid,
        authorID=author.etherpad_id,
        validUntil=validUntil)
    response = jsonify(
        success=True,
        pad='%s/p/%s' % (settings.ETHERPAD_URL, pad.padid),
        title=pad.title,
        **kwargs)
    set_cookie(response, 'sessionID', data['sessionID'])
    return response
