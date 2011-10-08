from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext

from bashoneliners.main.models import HackerProfile, OneLiner, User
from bashoneliners.main.forms import PostOneLinerForm

from datetime import datetime


''' constants '''

#


''' helper methods '''

def get_common_params(request):
    params = {
	    'user': request.user,
	    }

    try:
	if request.META['HTTP_USER_AGENT'].startswith('W3C_Validator'):
	    params['w3c'] = True
    except: 
	pass

    return params


''' url handlers '''

def index(request):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True).order_by('-pk')

    return render_to_response('main/index.html', params)

def top_n(request, num):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.top()

    return render_to_response('main/top_n.html', params)

def oneliner(request, pk):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(pk=pk)
    return render_to_response('main/index.html', params)

def mission(request):
    params = get_common_params(request)
    return render_to_response('main/mission.html', params)

def profile(request, user_id=None):
    params = get_common_params(request)

    if user_id is None:
	user_id = request.user.pk

    user = User.objects.get(pk=user_id)

    params['hacker'] = user
    params['oneliners'] = OneLiner.objects.filter(user=user).order_by('-pk')
    if user == request.user:
	params['owner'] = True

    return render_to_response('main/profile.html', params)

@login_required
def post(request):
    params = get_common_params(request)

    if request.method == 'POST':
	form = PostOneLinerForm(request.POST)
	if form.is_valid():
	    new_oneliner = form.save(request.user)
	    return redirect(index)
    else:
	form = PostOneLinerForm()

    params['form'] = form

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))


# eof
