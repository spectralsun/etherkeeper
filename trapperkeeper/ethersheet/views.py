import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def proxy(request, url=None):
    print dir(request)
    print request.path
    print request.method
    path = request.path.replace('/ethersheet/','/')
    proxied = '%s%s' % (settings.ETHERSHEETS_URL, path)
    prefix = '/ethersheet'
    print proxied
    response = requests.request(request.method, proxied)
    content = response.content#.replace('src="/','src="%s/' % prefix).replace('href="/','href="%s/' % prefix).replace("href='/","href='%s/" % prefix)
    return HttpResponse(content, status=response.status_code)