from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
    (r'^$', 'login'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^logout_then_login/$', 'logout_then_login'),
    (r'^password_change/$', 'password_change'),
    (r'^password_change_done/$', 'password_change_done'),
    (r'^password_reset/$', 'password_reset'),
    (r'^password_reset_done/$', 'password_reset_done'),
    (r'^password_reset_confirm/(?P<uidb36>.*)/(?P<token>.*)$', 'password_reset_confirm'),
    (r'^password_reset_complete/$', 'password_reset_complete'),
)

urlpatterns += patterns('bashoneliners.accounts.views',
    (r'^create_user/$', 'create_user'),
    (r'^profile/$', 'profile'),
)

# eof
