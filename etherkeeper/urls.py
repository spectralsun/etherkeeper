from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',      
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^etherpad', include('etherkeeper.etherpad.urls')),
    url('', include('etherkeeper.core.urls')) 
)
