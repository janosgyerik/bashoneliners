from functools import wraps

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as django_logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import oneliners.models
from oneliners import models
from oneliners.models import OneLiner, User, Tag
from oneliners.forms import EditHackerProfileForm, PostOneLinerForm, SearchOneLinerForm, EditOneLinerForm


ITEMS_PER_PAGE = 25


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


def format_canonical_url(request, relpath=''):
    return f"https://{request.META.get('SERVER_NAME')}{relpath}"


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
        'next': request.GET.get('next')
    }

    return params


def tweet(oneliner, long_url, force=False, test=False):
    if not oneliner.was_tweeted or force:
        from oneliners.url_shortener import shorten
        url = shorten(long_url) or long_url

        from oneliners.tweet import format_message
        message = format_message(oneliner.summary, oneliner.line, url)

        from oneliners.tweet import send_tweet
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

    paginator = Paginator(items, ITEMS_PER_PAGE)  # Show 25 items per page

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
    params['oneliners_page_range'] = paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
    params['command_cloud'] = models.Command.cloud()
    params['category_cloud'] = models.Category.cloud().filter(type="function")
    return params


@render_with_context(custom_params=True)
def category(request, pk):
    category_name = get_object_or_404(oneliners.models.Category, pk=pk).name
    items = OneLiner.filter_by_category(category_name, '-id')
    params = _common_oneliners_params(request, items)
    params['active_newest'] = 'active'
    params['ordering'] = 'newest'
    return 'oneliners/pages/index.html', params


def published_oneliners():
    return OneLiner.objects.filter(is_published=True).annotate(vote_sum=Sum('vote__value'))


@render_with_context(custom_params=True)
def oneliners_newest(request):
    items = published_oneliners().order_by('-id')
    params = _common_oneliners_params(request, items)
    params['active_newest'] = 'active'
    params['ordering'] = 'newest'
    return 'oneliners/pages/index.html', params


@render_with_context(custom_params=True)
def oneliners_active(request):
    items = published_oneliners().order_by('-updated_dt')[:ITEMS_PER_PAGE]
    params = _common_oneliners_params(request, items)
    params['active_active'] = 'active'
    params['ordering'] = 'active'
    return 'oneliners/pages/index.html', params


@render_with_context(custom_params=True)
def oneliners_popular(request):
    items = published_oneliners().order_by('-vote_sum', '-id')[:ITEMS_PER_PAGE]
    params = _common_oneliners_params(request, items)
    params['active_popular'] = 'active'
    params['ordering'] = 'popular'
    return 'oneliners/pages/index.html', params


def oneliner(request, pk):
    params = _common_params(request)
    params['oneliner'] = get_object_or_404(OneLiner, pk=pk)
    return render(request, 'oneliners/pages/oneliner.html', params)


@login_required
def oneliner_edit(request, pk):
    params = _common_params(request)
    params['cancel_url'] = reverse(oneliner, args=(pk,))

    if request.user.is_staff:
        oneliner0 = get_object_or_404(OneLiner, pk=pk)
    else:
        oneliner0 = get_object_or_404(OneLiner, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EditOneLinerForm(oneliner0.user, request.POST, instance=oneliner0)
        if form.is_valid():
            if form.is_save:
                oneliner1 = form.save()
                return redirect(oneliner1)
            elif form.is_delete:
                oneliner0.delete()
                return redirect(profile, oneliner0.user.pk)
    else:
        form = EditOneLinerForm(request.user, instance=oneliner0)

    params['form'] = form

    return render(request, 'oneliners/pages/oneliner_edit.html', params)


def oneliner_new(request, oneliner_pk=None, cancel_url=None):
    params = _common_params(request)
    if not cancel_url:
        cancel_url = reverse(oneliners_newest)
    params['cancel_url'] = cancel_url

    oneliner0 = None
    initial = {}

    if oneliner_pk:
        try:
            oneliner0 = OneLiner.objects.get(pk=oneliner_pk)
            oneliner0.score = sum([x.value for x in oneliner0.vote_set.all()])
            initial['summary'] = oneliner0.summary
        except OneLiner.DoesNotExist:
            pass

    if request.method == 'POST':
        form = PostOneLinerForm(request.user, request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                new_oneliner = form.save()

                if oneliner0 is not None:
                    oneliner0.add_alternative(new_oneliner)

                return redirect(new_oneliner)
    else:
        form = PostOneLinerForm(request.user, initial=initial)

    params['form'] = form
    params['oneliner'] = oneliner0

    return render(request, 'oneliners/pages/oneliner_edit.html', params)


@user_passes_test(lambda u: u.is_staff)
def oneliner_tweet(request, pk):
    oneliner0 = OneLiner.objects.get(pk=pk)
    long_url = format_canonical_url(request, oneliner0.get_absolute_url())
    tweet(oneliner0, long_url, force=True)
    return oneliner(request, pk)


@user_passes_test(lambda u: u.is_staff)
def oneliner_unpublish(request, pk):
    oneliner0 = OneLiner.objects.get(pk=pk)
    oneliner0.unpublished = True
    oneliner0.is_published = False
    oneliner0.save()
    return redirect(oneliner0)


@user_passes_test(lambda u: u.is_staff)
def oneliner_snapshot(request, pk):
    oneliner0 = OneLiner.objects.get(pk=pk)
    snapshot = models.OneLinerSnapshot(
        oneliner=oneliner0,
        user=oneliner0.user,
        summary=oneliner0.summary,
        line=oneliner0.line,
        explanation=oneliner0.explanation,
        limitations=oneliner0.limitations,
        is_published=oneliner0.is_published,
        was_tweeted=oneliner0.was_tweeted,
        unpublished=oneliner0.unpublished,
    )
    snapshot.save()
    return redirect(oneliner0)


def oneliner_alternative(request, oneliner_pk):
    cancel_url = reverse(oneliner, args=(oneliner_pk,))
    return oneliner_new(request, oneliner_pk=oneliner_pk, cancel_url=cancel_url)


def profile(request, pk=None):
    return profile_oneliners(request, pk)


def profile_edit(request):
    params = _common_params(request)
    params['cancel_url'] = reverse(profile)

    if request.user.is_authenticated:
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
    oneliners = OneLiner.objects.filter(user=hacker).annotate(vote_sum=Sum('vote__value')).order_by('-id')
    if hacker != request.user and not request.user.is_staff:
        oneliners = oneliners.filter(is_published=True)
    params['oneliners'] = oneliners
    return 'oneliners/pages/profile_oneliners.html', params


@render_with_context(custom_params=True)
def profile_votes(request):
    params = _common_params(request)
    user = request.user
    oneliners = OneLiner.objects.annotate(vote_sum=Sum('vote__value')).filter(vote__user=user).order_by('-id')
    params['oneliners'] = oneliners
    params['hacker'] = user
    return 'oneliners/pages/profile_votes.html', params


@user_passes_test(lambda u: u.is_staff)
@render_with_context(custom_params=True)
def profile_votes_of(request, pk=None):
    params = _common_params(request)
    hacker = User.objects.get(pk=pk)
    oneliners = OneLiner.objects.annotate(vote_sum=Sum('vote__value')).filter(vote__user=hacker)
    params['oneliners'] = oneliners
    params['hacker'] = hacker
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


def help_markdown(request):
    return render(request, 'oneliners/help/markdown.html')
