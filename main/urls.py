from django.conf.urls.defaults import *

urlpatterns = patterns('bashoneliners.main.views',
    (r'^$', 'index'),
    (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
    (r'^mission/$', 'mission'),
    (r'^post/$', 'post'),
    (r'^profile/(?P<user_id>\d+)/$', 'profile'),
    (r'^profile/$', 'profile'),
    (r'^top/(?P<num>\d+)/$', 'top_n'),
)

# eof
