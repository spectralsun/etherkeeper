from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from etherkeeper.util.helpers import jsonify, srender
from etherkeeper.core.models import Author

def home_view(request):    
    author = False
    if request.user.id:
        author = Author.objects.filter(user=request.user).first()
    return render(request, 'index.html', {
        'brand': settings.BRAND,
        'user': request.user,
        'author': author,
        'documents': author.padauthor_set.all()
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
    documents = author.padauthor_set.all()
    return jsonify(
        success=True, 
        navbar=srender('user/navbar.jinja', user=user),
        home=srender('user/home.jinja', documents=documents)
    )


@ensure_csrf_cookie
def logout_view(request):
    logout(request)

    return jsonify(
        success=True, 
        navbar=srender('user/navbar.jinja')
    )