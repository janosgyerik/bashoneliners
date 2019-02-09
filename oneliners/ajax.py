import json

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_slug, ValidationError
from django.http import HttpResponse

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

    payload = json.loads(request.body)
    state = payload['newState']

    if state['upvoted']:
        Vote.vote_up(request.user, oneliner)
    elif state['downvoted']:
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

    return render_to_response('oneliners/elements/oneliners_searchresults.html', params)


def search_by_tag(request):
    params = {'user': request.user}

    tagname = request.GET.get('tag')
    ordering = request.GET.get('ordering')
    try:
        validate_slug(tagname)
        if ordering == 'popular':
            order_by = '-vote_sum'
        else:
            order_by = None
        items = OneLiner.filter_by_tag(tagname, order_by=order_by)
        params['oneliners'] = items
    except ValidationError:
        params['oneliners'] = ()

    return render_to_response('oneliners/elements/oneliners.html', params)
