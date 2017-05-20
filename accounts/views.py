from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'login.html', {'next': request.GET.get('next')})


def logout(request):
    django_logout(request)
    return redirect('home')


@login_required
def status(request):
    return render(request, 'status.html')
