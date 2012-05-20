from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response


def maintenance_page(request):
    return render_to_response('maintenance.html')

urlpatterns = patterns('',
        (r'^$', maintenance_page),
        (r'^main/', maintenance_page),
        (r'^admin/', maintenance_page),
        (r'^comments/', maintenance_page),
        (r'^openid/', maintenance_page),
        )


# eof
