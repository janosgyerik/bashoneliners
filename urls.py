from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
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
    urlpatterns += patterns('',
	(r'^openid/', include('bashoneliners.django_openid_auth.urls')),
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

