from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response


def maintenance_page(request):
    return render_to_response('maintenance.html')

urlpatterns = patterns('',
        (r'^$', maintenance_page),
        )

from django.conf import settings

if settings.USE_DJANGO_STATIC_SERVE_FOR_MEDIA:
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

urlpatterns += patterns('',
        (r'', maintenance_page),
        )


# eof
