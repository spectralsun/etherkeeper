from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trapperkeeper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'trapperkeeper.core.views.home', name='home'),
    url(r'^login', 'trapperkeeper.core.view.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
