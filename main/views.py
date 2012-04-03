from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout as django_logout
from django.contrib.comments.views import comments
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from bashoneliners.main.models import OneLiner, User, Comment_recent, Tag, Question
from bashoneliners.main.forms import EditHackerProfileForm, PostOneLinerForm, PostCommentOnOneLinerForm, PostQuestionForm, EditQuestionForm, SearchOneLinerForm, EditOneLinerForm
from bashoneliners.main.email import send_oneliner_answer, send_oneliner_alternative, send_oneliner_comment


''' helper methods '''


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
            }

    return params


def _common_initial(request):
    return {'next_url': request.META.get('HTTP_REFERER', '/'), }


def tweet(oneliner, force=False, test=False):
    if not oneliner.was_tweeted or force:
        long_url = 'http://bashoneliners.com/main/oneliner/%d' % oneliner.pk
        from bashoneliners.main.shorturl import get_goo_gl
        url = get_goo_gl(long_url) or long_url
        message = '%s %s' % (
                url,
                oneliner.line,
                )
        from bashoneliners.main.tweet import tweet as send_tweet
        result = send_tweet(message, test=test)
        if result:
            oneliner.was_tweeted = True
            oneliner.save()
            return result


def oneliner_list(request):
    params = _common_params(request)

    items = OneLiner.objects.filter(is_published=True)
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

    return render_to_response('main/pages/index.html', params)


def oneliner(request, pk):
    params = _common_params(request)
    params['oneliners'] = OneLiner.objects.filter(pk=pk)
    return render_to_response('main/pages/oneliner.html', params)


@login_required
def oneliner_edit(request, pk):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    try:
        oneliner0 = OneLiner.objects.get(pk=pk, user=request.user)
    except:
        return render_to_response('main/pages/access_error.html', params)

    if request.method == 'POST':
        form = EditOneLinerForm(request.user, request.POST, instance=oneliner0)
        if form.is_valid():
            if form.is_save:
                oneliner1 = form.save()
                if oneliner1.is_published:
                    tweet(oneliner1)
                return redirect(form.cleaned_data.get('next_url'))
            elif form.is_delete:
                oneliner0.delete()
                return redirect(profile)
        else:
            params['next_url'] = request.POST.get('next_url')
    else:
        form = EditOneLinerForm(request.user, instance=oneliner0, initial=initial)

    params['form'] = form

    return render_to_response('main/pages/oneliner_edit.html', params, context_instance=RequestContext(request))


def oneliner_new(request, question_pk=None, oneliner_pk=None):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    question = None
    oneliner0 = None

    if question_pk is not None:
        try:
            question = Question.objects.get(pk=question_pk)
            initial['summary'] = question.summary
        except:
            pass

    elif oneliner_pk is not None:
        try:
            oneliner0 = OneLiner.objects.get(pk=oneliner_pk)
            initial['summary'] = oneliner0.summary
        except:
            pass

    if request.method == 'POST':
        form = PostOneLinerForm(request.user, request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                new_oneliner = form.save()
                if new_oneliner.is_published:
                    tweet(new_oneliner)

                if question is not None:
                    question.add_answer(new_oneliner)
                    if new_oneliner.is_published:
                        send_oneliner_answer(question, new_oneliner)
                elif oneliner0 is not None:
                    oneliner0.add_alternative(new_oneliner)
                    if new_oneliner.is_published:
                        send_oneliner_alternative(oneliner0, new_oneliner)

                return redirect(oneliner, new_oneliner.pk)
            else:
                params['next_url'] = request.POST.get('next_url')
    else:
        form = PostOneLinerForm(request.user, initial=initial)

    params['form'] = form
    params['question'] = question
    params['oneliner'] = oneliner0

    return render_to_response('main/pages/oneliner_edit.html', params, context_instance=RequestContext(request))


def oneliner_answer(request, question_pk):
    return oneliner_new(request, question_pk=question_pk)


def oneliner_alternative(request, oneliner_pk):
    return oneliner_new(request, oneliner_pk=oneliner_pk)


def oneliner_comment(request, pk):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    try:
        oneliner0 = OneLiner.objects.get(pk=pk)
    except:
        return render_to_response('main/pages/access_error.html', params)

    if request.method == 'POST':
        if request.user.is_authenticated():
            data = request.POST.copy()
            data['name'] = request.user.get_full_name() or request.user.username
            data['email'] = request.user.email
            form = PostCommentOnOneLinerForm(oneliner0, data)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                send_oneliner_comment(oneliner0, request.user, comment)
                return comments.post_comment(request, next=oneliner0.get_absolute_url())
            else:
                params['next_url'] = request.POST.get('next_url')
        else:
            form = PostCommentOnOneLinerForm(oneliner0, request.POST)
    else:
        form = PostCommentOnOneLinerForm(oneliner0, initial=initial)

    params['form'] = form
    params['oneliner'] = oneliner0

    return render_to_response('main/pages/oneliner_comment.html', params, context_instance=RequestContext(request))


def question_list(request):
    params = _common_params(request)
    params['questions'] = Question.recent()
    return render_to_response('main/pages/question_list.html', params, context_instance=RequestContext(request))


def question(request, pk):
    params = _common_params(request)
    params['questions'] = Question.objects.filter(pk=pk)
    return render_to_response('main/pages/question.html', params)


@login_required
def question_edit(request, pk):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    try:
        question0 = Question.objects.get(pk=pk, user=request.user)
    except:
        return render_to_response('main/pages/access_error.html', params)

    if request.method == 'POST':
        form = EditQuestionForm(request.user, request.POST, instance=question0)
        if form.is_valid():
            if form.is_save:
                form.save()
                return redirect(form.cleaned_data.get('next_url'))
            elif form.is_delete:
                question0.delete()
                return redirect(profile)
        else:
            params['next_url'] = request.POST.get('next_url')
    else:
        form = EditQuestionForm(request.user, instance=question0, initial=initial)

    params['form'] = form

    return render_to_response('main/pages/question_edit.html', params, context_instance=RequestContext(request))


def question_new(request):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    if request.method == 'POST':
        form = PostQuestionForm(request.user, request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                form.save()
                return redirect(form.cleaned_data.get('next_url'))
            else:
                params['next_url'] = request.POST.get('next_url')
    else:
        form = PostQuestionForm(request.user, initial=initial)

    params['form'] = form

    return render_to_response('main/pages/question_edit.html', params, context_instance=RequestContext(request))


def comment_list(request):
    params = _common_params(request)
    params['comments'] = Comment_recent()
    return render_to_response('main/pages/comment_list.html', params)


def profile(request, pk=None):
    params = _common_params(request)

    if pk is not None:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    params['hacker'] = user

    if user.is_authenticated():
        oneliners = OneLiner.objects.filter(user=user)
        if user != request.user:
            oneliners = oneliners.filter(is_published=True)
        params['oneliners'] = oneliners

        questions = Question.objects.filter(user=user)
        if user != request.user:
            questions = questions.filter(is_published=True)
        params['questions_pending'] = questions.filter(is_answered=False)
        params['questions_answered'] = questions.filter(is_answered=True)

    return render_to_response('main/pages/profile.html', params)


def profile_edit(request):
    params = _common_params(request)
    initial = _common_initial(request)
    params['next_url'] = initial['next_url']

    if request.user.is_authenticated():
        hackerprofile = request.user.hackerprofile
        if request.method == 'POST':
            form = EditHackerProfileForm(request.POST, instance=hackerprofile)
            if form.is_valid():
                form.save()
                return redirect(profile)
            else:
                params['next_url'] = request.POST.get('next_url')
        else:
            form = EditHackerProfileForm(instance=hackerprofile, initial=initial)
    else:
        form = EditHackerProfileForm(initial=initial)

    params['form'] = form

    return render_to_response('main/pages/profile_edit.html', params, context_instance=RequestContext(request))


def search(request):
    params = _common_params(request)
    form = params['searchform']

    if form.is_valid():
        params['oneliners'] = OneLiner.search(form)
        params['data'] = form.data

    return render_to_response('main/pages/search.html', params)


def login(request):
    params = _common_params(request)
    return render_to_response('main/pages/login.html', params, context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    return oneliner_list(request)


''' simple pages '''


def feeds(request):
    params = _common_params(request)
    return render_to_response('main/pages/feeds.html', params)


def sourcecode(request):
    params = _common_params(request)
    return render_to_response('main/pages/sourcecode.html', params)


def mission(request):
    params = _common_params(request)
    return render_to_response('main/pages/mission.html', params)


def help_markdown(request):
    return render_to_response('main/help/markdown.html')

# eof
