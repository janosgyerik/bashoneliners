from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounts.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^status/$', 'status', name='status'),
)
