from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from bashoneliners.main.models import LatestEntries

def feed(request):
    return LatestEntries()(request)

urlpatterns = patterns('',
    # Example:
    (r'^$', include('bashoneliners.main.urls')),
    (r'^main/', include('bashoneliners.main.urls')),
    (r'^openid/', include('bashoneliners.django_openid_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'feed/$', feed),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.USE_DJANGO_STATIC_SERVE_FOR_MEDIA:
    urlpatterns += patterns('',
	    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

