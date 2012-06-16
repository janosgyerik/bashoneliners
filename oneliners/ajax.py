from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from oneliners.models import Question, OneLiner
from oneliners.forms import SearchOneLinerForm


@login_required
def question_answered(request, question_pk, oneliner_pk):
    question = Question.objects.get(pk=question_pk, user=request.user)
    oneliner = OneLiner.objects.get(pk=oneliner_pk)
    question.accept_answer(oneliner)

    return render_to_response('main/ajax/json.js')


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

    return render_to_response('main/elements/oneliners_searchresults.html', params)


def search_by_tag(request):
    params = {}
    params['user'] = request.user

    text = request.GET.get('text')
    from django.core.validators import validate_slug
    try:
        validate_slug(text)
        params['oneliners'] = OneLiner.recent_by_tag(text)
    except:
        params['oneliners'] = ()

    return render_to_response('main/elements/oneliners.html', params)


# eof
