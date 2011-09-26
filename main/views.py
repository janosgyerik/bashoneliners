from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext

from bashoneliners.main.models import Hacker, OneLiner, DjangoUser
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
    return index(request)

def mission(request):
    params = get_common_params(request)

    return render_to_response('main/mission.html', params)

def profile(request, user_id=None):
    params = get_common_params(request)

    if user_id is None:
	user_id = request.user.pk

    try:
	hacker = Hacker.objects.get(pk=user_id)
    except:
	user = DjangoUser.objects.get(pk=user_id)
	hacker = Hacker(user_ptr_id=user.pk)
	hacker.__dict__.update(user.__dict__)
	hacker.save()

    params['hacker'] = hacker
    params['oneliners'] = OneLiner.objects.filter(hacker=hacker).order_by('-pk')
    if hacker.pk == request.user.pk:
	params['owner'] = True

    return render_to_response('main/profile.html', params)

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
