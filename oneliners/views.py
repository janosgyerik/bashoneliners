from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.db.models import Sum
from oneliners.models import OneLiner, User, Comment_recent, Tag, Question
from oneliners.forms import EditHackerProfileForm, PostOneLinerForm, SearchOneLinerForm, EditOneLinerForm


# decorators


def render_with_context(custom_params=False):
    def _inner(view_method):
        def _decorator(request, *args, **kwargs):
            if custom_params:
                (template_path, params) = view_method(request, *args, **kwargs)
            else:
                params = _common_params(request)
                template_path = view_method(request, *args, **kwargs)
            return render(request, template_path, params)

        return wraps(view_method)(_decorator)

    return _inner


# helper methods


def format_canonical_url(request, relpath=''):
    return 'http://%s:%s%s' % (request.META.get('SERVER_NAME'), request.META.get('SERVER_PORT'), relpath)


def _common_params(request):
    if request.method == 'GET':
        if request.GET.get('is_advanced'):
            searchform = SearchOneLinerForm(request.GET)
        else:
            data = {
                'match_whole_words': False,
                'match_summary': True,
                'match_line': True,
                'match_explanation': True,
                'match_limitations': True,
                'query': request.GET.get('query'),
            }
            searchform = SearchOneLinerForm(data)
    else:
        searchform = SearchOneLinerForm()

    params = {
        'user': request.user,
        'searchform': searchform,
        'SERVER_NAME': request.META['SERVER_NAME'],
    }

    return params


def format_tweet(oneliner, baseurl):
    long_url = baseurl + oneliner.get_absolute_url()
    from oneliners.shorturl import get_goo_gl

    url = get_goo_gl(long_url) or long_url
    message = '%s %s' % (
        url,
        oneliner.line,
    )
    return message


def tweet(oneliner, baseurl, force=False, test=False):
    if not oneliner.was_tweeted or force:
        from oneliners.tweet import tweet as send_tweet

        message = format_tweet(oneliner, baseurl)
        result = send_tweet(message, test=test)
        if result:
            oneliner.was_tweeted = True
            oneliner.save()
            return result


def index(request):
    return oneliners_default(request)


def oneliners_default(request):
    return oneliners_newest(request)


def _common_oneliners_params(request, items):
    params = _common_params(request)

    paginator = Paginator(items, 25)  # Show 25 items per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page_number = int(request.GET.get('page', '1'))
    except ValueError:
        page_number = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    params['oneliners_page'] = page
    params['tagcloud'] = Tag.tagcloud()
    return params


@render_with_context(custom_params=True)
def oneliners_newest(request):
    items = OneLiner.objects.filter(is_published=True).annotate(score=Sum('vote__value'))
    params = _common_oneliners_params(request, items)
    params['active_newest'] = 'active'
    params['ordering'] = 'newest'
    return 'oneliners/pages/index.html', params


@render_with_context(custom_params=True)
def oneliners_popular(request):
    items = OneLiner.objects.filter(is_published=True).annotate(score=Sum('vote__value')).order_by('-score', '-id')
    params = _common_oneliners_params(request, items)
    params['active_popular'] = 'active'
    params['ordering'] = 'popular'
    return 'oneliners/pages/index.html', params


def oneliner(request, pk):
    params = _common_params(request)
    # TODO: move the logic to the model
    items = OneLiner.objects.filter(pk=pk).annotate(score=Sum('vote__value'))
    params['oneliners'] = items
    return render(request, 'oneliners/pages/oneliner.html', params)


@login_required
def oneliner_edit(request, pk):
    params = _common_params(request)
    params['cancel_url'] = reverse(oneliner, args=(pk,))

    try:
        oneliner0 = OneLiner.objects.get(pk=pk, user=request.user)
        oneliner0.score = sum([x.value for x in oneliner0.vote_set.all()])
    except OneLiner.DoesNotExist:
        return render(request, 'oneliners/pages/access_error.html', params)

    if request.method == 'POST':
        form = EditOneLinerForm(request.user, request.POST, instance=oneliner0)
        if form.is_valid():
            if form.is_save:
                oneliner1 = form.save()
                if oneliner1.is_published:
                    tweet(oneliner1, format_canonical_url(request))
                return redirect(oneliner1)
            elif form.is_delete:
                oneliner0.delete()
                return redirect(profile)
    else:
        form = EditOneLinerForm(request.user, instance=oneliner0)

    params['form'] = form

    return render(request, 'oneliners/pages/oneliner_edit.html', params)


def oneliner_new(request, question_pk=None, oneliner_pk=None, cancel_url=None):
    params = _common_params(request)
    if not cancel_url:
        cancel_url = reverse(oneliners_newest)
    params['cancel_url'] = cancel_url

    question = None
    oneliner0 = None
    initial = {}

    if question_pk is not None:
        try:
            question = Question.objects.get(pk=question_pk)
            initial['summary'] = question.summary
        except Question.DoesNotExist:
            pass

    elif oneliner_pk is not None:
        try:
            oneliner0 = OneLiner.objects.get(pk=oneliner_pk)
            oneliner0.score = sum([x.value for x in oneliner0.vote_set.all()])
            initial['summary'] = oneliner0.summary
        except OneLiner.DoesNotExist:
            pass

    if request.method == 'POST':
        form = PostOneLinerForm(request.user, request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                new_oneliner = form.save()
                if new_oneliner.is_published:
                    tweet(new_oneliner, format_canonical_url(request))

                if question is not None:
                    question.add_answer(new_oneliner)
                elif oneliner0 is not None:
                    oneliner0.add_alternative(new_oneliner)

                if new_oneliner.is_published:
                    return redirect(oneliners_newest)
                else:
                    return redirect(new_oneliner)
    else:
        form = PostOneLinerForm(request.user, initial=initial)

    params['form'] = form
    params['question'] = question
    params['oneliner'] = oneliner0

    return render(request, 'oneliners/pages/oneliner_edit.html', params)


def oneliner_alternative(request, oneliner_pk):
    cancel_url = reverse(oneliner, args=(oneliner_pk,))
    return oneliner_new(request, oneliner_pk=oneliner_pk, cancel_url=cancel_url)


@render_with_context(custom_params=True)
def question_list(request):
    params = _common_params(request)
    params['questions'] = Question.recent()
    return 'oneliners/pages/question_list.html', params


@render_with_context(custom_params=True)
def comment_list(request):
    params = _common_params(request)
    params['comments'] = Comment_recent()
    return 'oneliners/pages/comment_list.html', params


def profile(request, pk=None):
    return profile_oneliners(request, pk)


def profile_edit(request):
    params = _common_params(request)
    params['cancel_url'] = reverse(profile)

    if request.user.is_authenticated():
        hackerprofile = request.user.hackerprofile
        if request.method == 'POST':
            form = EditHackerProfileForm(request.POST, instance=hackerprofile)
            if form.is_valid():
                form.save()
                return redirect(profile)
        else:
            form = EditHackerProfileForm(instance=hackerprofile)
    else:
        form = EditHackerProfileForm()

    params['form'] = form

    template_path = 'oneliners/pages/profile_edit.html'
    return render(request, template_path, params)


def _common_profile_params(request, pk):
    params = _common_params(request)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        user = request.user

    params['hacker'] = user
    return params


@render_with_context(custom_params=True)
def profile_oneliners(request, pk=None):
    params = _common_profile_params(request, pk)
    hacker = params['hacker']
    oneliners = OneLiner.objects.filter(user=hacker).annotate(score=Sum('vote__value'))
    if hacker != request.user:
        oneliners = oneliners.filter(is_published=True)
    params['oneliners'] = oneliners
    return 'oneliners/pages/profile_oneliners.html', params


@render_with_context(custom_params=True)
def profile_questions(request, pk=None):
    params = _common_profile_params(request, pk)
    hacker = params['hacker']
    questions = Question.objects.filter(user=hacker)
    if hacker != request.user:
        questions = questions.filter(is_published=True)
    params['questions'] = questions
    return 'oneliners/pages/profile_questions.html', params


@render_with_context(custom_params=True)
def profile_votes(request):
    params = _common_params(request)
    user = request.user
    oneliners = OneLiner.objects.annotate(score=Sum('vote__value')).filter(vote__user=user)
    params['oneliners'] = oneliners
    params['hacker'] = user
    return 'oneliners/pages/profile_votes.html', params


@render_with_context(custom_params=True)
def search(request):
    params = _common_params(request)
    form = params['searchform']

    if form.is_valid():
        params['oneliners'] = OneLiner.search(form)
        params['data'] = form.data

    return 'oneliners/pages/search.html', params


@render_with_context()
def login(request):
    return 'oneliners/pages/login.html'


def logout(request):
    django_logout(request)
    return index(request)


''' simple pages '''


@render_with_context()
def feeds(request):
    return 'oneliners/pages/feeds.html'


@render_with_context()
def sourcecode(request):
    return 'oneliners/pages/sourcecode.html'


@render_with_context()
def mission(request):
    return 'oneliners/pages/mission.html'


def help_markdown(request):
    return render(request, 'oneliners/help/markdown.html')
