from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',   
    url(r'^login', 'etherkeeper.core.views.login_view', name='login'),
    url(r'^logout', 'etherkeeper.core.views.logout_view', name='logout'),
    url(r'^search/users', 'etherkeeper.core.views.search_users_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^etherpad/', include('etherkeeper.etherpad.urls'))

    url(r'.*', 'etherkeeper.core.views.home_view', name='home'),
)
