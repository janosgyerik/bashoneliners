from django.conf.urls.defaults import *

urlpatterns = patterns('bashoneliners.main.views',
    (r'^$', 'index'),
    (r'^sourcecode/$', 'sourcecode'),
    (r'^mission/$', 'mission'),
    (r'^wishlist/$', 'wishlist'),
    #(r'^wishlist/ask/$', 'wishlist'),
    #(r'^wishlist/answer/$', 'wishlist'),

    (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
    (r'^oneliner/edit/(?P<pk>\d+)/$', 'edit_oneliner'),
    (r'^oneliner/new/$', 'new_oneliner'),

    (r'^profile/(?P<user_id>\d+)/$', 'profile'),
    (r'^profile/$', 'profile'),

    (r'^top/(?P<num>\d+)/$', 'top_n'),

    (r'^search/$', 'search'),
    (r'^search_ajax/$', 'search_ajax'),

    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
)

# eof
