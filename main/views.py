from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext

from bashoneliners.main.models import Hacker, OneLiner
from bashoneliners.main.forms import PostOneLinerForm

from datetime import datetime


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

@login_required
def post(request):
    params = get_common_params(request)

    if request.method == 'POST':
	form = PostOneLinerForm(request.POST)
	if form.is_valid():
	    new_oneliner = form.save(request.user.hacker)
	    return redirect(index)
    else:
	form = PostOneLinerForm()

    params['form'] = form

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))


# eof
