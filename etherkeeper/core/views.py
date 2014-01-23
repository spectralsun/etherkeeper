from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from etherkeeper.util.helpers import jsonify, srender, jsonerror
from etherkeeper.core.models import Author

@ensure_csrf_cookie
def home_view(request):    
    author = False
    print request.user
    if request.user.id:
        author = Author.get_by_user(request.user)

    return render(request, 'index.html', {
        'brand': settings.BRAND,
        'author': author
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
    author = Author.get_by_user(request.user)
    return jsonify(
        success=True, 
        navbar=srender('user/navbar.jinja', user=user),
        home=srender('user/home.jinja', author=author))


@ensure_csrf_cookie
def logout_view(request):
    logout(request)

    return jsonify(
        success=True, 
        navbar=srender('user/navbar.jinja')
    )