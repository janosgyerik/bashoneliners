from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bashoneliners.views.home', name='home'),
    # url(r'^bashoneliners/', include('bashoneliners.foo.urls')),

    (r'^$', include('oneliners.urls')),
    (r'^main/', include('oneliners.urls')),
    (r'^oneliners/', include('oneliners.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^openid/', include('django_openid_auth.urls')),
)

from oneliners.feeds import OneLinerEntries

urlpatterns += patterns('',
        (r'feed/$', OneLinerEntries()),
)
