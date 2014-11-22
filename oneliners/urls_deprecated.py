from django.conf.urls import patterns

urlpatterns = patterns('oneliners.views',
                       (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
                       (r'^question/(?P<pk>\d+)/$', 'question'),
)

# eof
