from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse as reverse_url
from django.http import HttpResponseRedirect
from django import forms

from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login

from bashoneliners.main.models import Hacker, DjangoUser

class UserCreationFormWithEmail(UserCreationForm):
    class Meta:
	model = User
	fields = (
		'username',
		'email',
		)
	
    def clean_email(self):
	email = self.cleaned_data['email']

	if email is None or len(email) == 0:
	    raise forms.ValidationError('This field is required.')

	if DjangoUser.objects.filter(email=email).count() > 0:
	    raise forms.ValidationError('This email address is already used.')

	return email


def create_user(request, template_name='registration/create_user_form.html'):
    if request.method == 'POST':
	form = UserCreationFormWithEmail(request.POST)
	if form.is_valid():
	    hacker = Hacker.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
	    hacker.email = form.cleaned_data['email']
	    hacker.save()

	    django_user = django_authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
	    django_login(request, django_user)

	    return HttpResponseRedirect('/')
    else:
	form = UserCreationFormWithEmail()

    return render_to_response(template_name, {
	'form': form,
	}, context_instance=RequestContext(request))

# eof
