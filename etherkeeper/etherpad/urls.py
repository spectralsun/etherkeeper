from django.conf.urls import patterns, include, url



urlpatterns = patterns('etherkeeper.etherpad.views',
    url(r'^/create', 'create_view'),
    url(r'^/open', 'open_view'),
    url(r'^/title', 'title_view'),
    url(r'^/sharing', 'open_sharing_view'),
    url(r'^/share', 'share_view'),
    url(r'^/respond', 'respond_view'),
    url(r'^/set_title', 'set_title_view'),
)