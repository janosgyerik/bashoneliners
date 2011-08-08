from django.conf.urls.defaults import *

urlpatterns = patterns('bashoneliners.main.views',
    (r'^$', 'index'),
    (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
    (r'^rules/$', 'rules'),
    (r'^post/$', 'post'),
    (r'^top/(?P<num>\d+)/$', 'top_n'),
)

# eof
