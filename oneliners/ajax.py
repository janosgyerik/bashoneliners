from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_slug, ValidationError

from oneliners.models import OneLiner, Vote
from oneliners.forms import SearchOneLinerForm


@login_required
def oneliner_vote(request, oneliner_pk):
    oneliner = None
    try:
        oneliner = OneLiner.objects.get(pk=oneliner_pk)
    except OneLiner.DoesNotExist:
        pass

    if oneliner:
        if request.GET['upvoted'] == 'true':
            Vote.vote_up(request.user, oneliner)
        elif request.GET['downvoted'] == 'true':
            Vote.vote_down(request.user, oneliner)
        else:
            Vote.vote_clear(request.user, oneliner)

    return render_to_response('oneliners/ajax/json.js')


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
            order_by = '-score'
        else:
            order_by = None
        items = OneLiner.filter_by_tag(tagname, order_by=order_by)
        params['oneliners'] = items
    except ValidationError:
        params['oneliners'] = ()

    return render_to_response('oneliners/elements/oneliners.html', params)
