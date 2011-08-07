from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse as reverse_url
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login

from bashoneliners.main.models import Hacker

def create_user(request, template_name='registration/create_user_form.html'):
    if request.method == 'POST':
	form = UserCreationForm(request.POST)
	if form.is_valid():
	    hacker = Hacker.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])

	    django_user = django_authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
	    django_login(request, django_user)

	    return HttpResponseRedirect('/')
    else:
	form = UserCreationForm()

    return render_to_response(template_name, {
	'form': form,
	}, context_instance=RequestContext(request))

def profile(request, template_name='registration/profile.html'):
    return render_to_response(template_name, { 'user': request.user })

# eof
