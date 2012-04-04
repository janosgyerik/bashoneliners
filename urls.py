from django.conf.urls.defaults import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        (r'^$', include('oneliners.urls')),
        (r'^main/', include('oneliners.urls')),

        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'^comments/', include('django.contrib.comments.urls')),
        (r'^openid/', include('django_openid_auth.urls')),
        )


from oneliners.feeds import OneLinerEntries

urlpatterns += patterns('',
        (r'feed/$', OneLinerEntries()),
        )


from django.conf import settings

if settings.USE_DJANGO_STATIC_SERVE_FOR_MEDIA:
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

# eof
