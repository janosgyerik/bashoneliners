import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_slug, ValidationError
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from oneliners.models import OneLiner, Vote
from oneliners.forms import SearchOneLinerForm

HTTP_BAD_REQUEST = HttpResponse(status=400)
HTTP_NO_CONTENT = HttpResponse(status=204)


@login_required
def oneliner_vote(request, oneliner_pk):
    if request.method != 'POST':
        return HTTP_BAD_REQUEST

    try:
        oneliner = OneLiner.objects.get(pk=oneliner_pk)
    except OneLiner.DoesNotExist:
        return HTTP_BAD_REQUEST

    if request.POST.get('upvoted') == 'true':
        Vote.vote_up(request.user, oneliner)
    elif request.POST.get('downvoted') == 'true':
        Vote.vote_down(request.user, oneliner)
    else:
        Vote.vote_clear(request.user, oneliner)

    return HTTP_NO_CONTENT


def search(request):
    params = {}

    if request.method == 'GET':
        form = SearchOneLinerForm(request.GET)
    else:
        form = None

    if form is not None:
        if form.is_valid():
            params['oneliners'] = OneLiner.search(form)
            params['user'] = request.user
            params['data'] = form.data

    return render(request, 'oneliners/elements/oneliners_searchresults.html', params)


@require_http_methods(["GET"])
def search_by_filters(request):
    params = {'user': request.user}

    try:
        category = request.GET.get('category')
        command = request.GET.get('command')
        ordering = request.GET.get('ordering')
        if ordering == 'newest':
            order_by = '-published_dt'
        elif ordering == 'active':
            order_by = '-updated_dt'
        elif ordering == 'popular':
            order_by = '-vote_sum'
        else:
            order_by = '-id'

        items = OneLiner.filter_by_category_and_command(category, command, order_by=order_by)
        params['oneliners'] = items
    except ValidationError:
        params['oneliners'] = ()

    return render(request, 'oneliners/elements/oneliners.html', params)


@require_http_methods(["GET"])
def search_by_filters_static(request, category, command):
    params = {'user': request.user}

    if command == 'undefined':
        command = None

    if category == 'undefined':
        category = None

    try:
        order_by = '-published_dt'
        items = OneLiner.filter_by_category_and_command(category, command, order_by=order_by)
        params['oneliners'] = items
    except ValidationError:
        params['oneliners'] = ()

    return render(request, 'oneliners/elements/oneliners.html', params)
