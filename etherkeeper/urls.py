from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    

    url(r'^$', 'etherkeeper.core.views.home_view', name='home'),
    url(r'^login', 'etherkeeper.core.views.login_view', name='login'),
    url(r'^logout', 'etherkeeper.core.views.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^etherpad/create', 'etherkeeper.etherpad.views.create_view')
)
