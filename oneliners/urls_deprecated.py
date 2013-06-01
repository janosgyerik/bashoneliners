from django.conf.urls import patterns, url

urlpatterns = patterns('oneliners.views',
        (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
        (r'^question/(?P<pk>\d+)/$', 'question'),
        )

# eof
