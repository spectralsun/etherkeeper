from django.conf.urls import patterns, include, url


urlpatterns = patterns('etherkeeper.core.views',
    url(r'^login', 'login_view', name='login'),
    url(r'^logout', 'logout_view', name='logout'),
    url(r'^search/users', 'search_users_view', name='search_users'),
    url(r'.*', 'home_view', name='home'),
)