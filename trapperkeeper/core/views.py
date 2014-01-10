import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings



def jsonify(*args, **kwargs):
    data = args[0] if args else dict(kwargs)

    return HttpResponse(json.dumps(data),
        content_type='application/json')

def jsonerror(error):
    return jsonify(dict(success=False, error=error))

def home(request):
    return render(request, 'index.html', {
        'brand': settings.BRAND
    })

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    if settings.AUTH_TYPE == 'xmpp':
        try:
            xmpp_auth(username, password)
        except Exception as exp:
            return jsonerror(exp)
        return jsonify