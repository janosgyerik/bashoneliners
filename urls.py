from django.conf.urls.defaults import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        (r'^$', include('bashoneliners.main.urls')),
        (r'^main/', include('bashoneliners.main.urls')),

        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'^comments/', include('django.contrib.comments.urls')),
        )

try:
    import openid
    openid.VERSION
    urlpatterns += patterns('',
            (r'^openid/', include('django_openid_auth.urls')),
            )
except:
    pass

from bashoneliners.main.feeds import OneLinerEntries

urlpatterns += patterns('',
        (r'feed/$', OneLinerEntries()),
        )


from django.conf import settings

if settings.USE_DJANGO_STATIC_SERVE_FOR_MEDIA:
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

# eof
