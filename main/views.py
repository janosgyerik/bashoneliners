from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *

from bashoneliners.main.models import Hacker, OneLiner


''' constants '''

#


''' helper methods '''

def get_common_params(request):
    params = {
	    'user': request.user,
	    }
    return params


''' url handlers '''

def index(request):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True).order_by('-pk')

    return render_to_response('main/index.html', params)

def oneliner(request, pk):
    return index(request)

def rules(request):
    params = get_common_params(request)

    return render_to_response('main/rules.html', params)


# eof
