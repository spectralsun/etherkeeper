from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from etherkeeper.util.helpers import jsonify

def home_view(request):    
    print request.user
    return render(request, 'index.html', {
        'brand': settings.BRAND,
        'user': request.user
    })

@ensure_csrf_cookie
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
    else:
        return jsonerror()        

    return jsonify(dict(
        success=True, 
        navbar=loader.render_to_string('user/navbar.jinja', dict(user=user))
    ))


@ensure_csrf_cookie
def logout_view(request):
    logout(request)

    return jsonify(dict(
        success=True, 
        navbar=loader.render_to_string('user/navbar.jinja')
    ))