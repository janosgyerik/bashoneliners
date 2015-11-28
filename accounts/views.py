from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def login(request):
    return render_to_response('login.html', {'next': request.GET.get('next')},
                              context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    return redirect('home')


@login_required
def status(request):
    return render_to_response('status.html', context_instance=RequestContext(request))
