import json
import datetime
import time
from django.http import HttpResponse
from django.conf import settings

def epoch_time(add=0):
    return time.mktime(datetime.datetime.now().timetuple()) + add

def set_cookie(response, key, value, days_expire = 7,
    domain=settings.SESSION_COOKIE_DOMAIN):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=settings.SESSION_COOKIE_SECURE or None)

def jsonify(*args, **kwargs):
    data = args[0] if args else dict(kwargs)

    return HttpResponse(json.dumps(data),
        content_type='application/json')

def jsonerror(error=None):
    return jsonify(dict(success=False, error=error))

