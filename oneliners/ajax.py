from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_slug, ValidationError

from oneliners.models import Question, OneLiner, Vote
from oneliners.forms import SearchOneLinerForm


@login_required
def question_answered(request, question_pk, oneliner_pk):
    question = Question.objects.get(pk=question_pk, user=request.user)
    oneliner = OneLiner.objects.get(pk=oneliner_pk)
    question.accept_answer(oneliner)

    return render_to_response('oneliners/ajax/json.js')


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
    params = {}
    params['user'] = request.user

    text = request.GET.get('text')
    try:
        validate_slug(text)
        params['oneliners'] = OneLiner.recent_by_tag(text)
    except ValidationError:
        params['oneliners'] = ()

    return render_to_response('oneliners/elements/oneliners.html', params)


# eof
