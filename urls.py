from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from bashoneliners.main.models import LatestEntries

urlpatterns = patterns('',
    # Example:
    (r'^$', include('bashoneliners.main.urls')),
    (r'^main/', include('bashoneliners.main.urls')),
    (r'^accounts/', include('bashoneliners.accounts.urls')),
    (r'^openid/', include('bashoneliners.django_openid_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'feed/$', LatestEntries()),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
	    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

