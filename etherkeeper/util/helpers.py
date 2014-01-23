import json
import datetime
import time
from django.conf import settings
from django.http import HttpResponse
from django.template import loader

def epoch_time(add=0):
    return time.mktime(datetime.datetime.now().timetuple()) + add

def jsonify(*args, **kwargs):
    'Returns a json response'
    data = None
    if args:
        data = args[0] if len(args) == 1 else [arg for arg in args]
    if kwargs:
        if data:
            if type(data) != list:
                data = [data]
            data.append(dict(**kwargs))
        else:
            data = dict(**kwargs)
    return HttpResponse(json.dumps(data), content_type='application/json')

def jsonerror(error=None):
    'JSON error response shortcut'
    return jsonify(success=False, error=error)

def set_cookie(response, key, value, expire_days = 365,
    domain=settings.SESSION_COOKIE_DOMAIN):
    'Sets a cookie on a response for an amount of days'
    
    max_age = expire_days * 24 * 60 * 60 

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + 
        datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, max_age=max_age, expires=expires, 
        domain=domain, secure=settings.SESSION_COOKIE_SECURE or None)

def srender(template, **kwargs):
    'Render a template to string with given kwargs'
    return loader.render_to_string(template, dict(**kwargs))
