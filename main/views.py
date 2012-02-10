from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext
from django.contrib.auth import logout as django_logout

from bashoneliners.main.models import HackerProfile, OneLiner, User, Answer
from bashoneliners.main.forms import *

from datetime import datetime


''' helper methods '''

def _common_params(request):
    if request.method == 'GET':
	searchform = SearchOneLinerForm(request.GET)
    else:
	searchform = SearchOneLinerForm()

    params = {
	    'user': request.user,
	    'searchform': searchform,
	    }

    return params

def tweet(oneliner, test=False, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    if not oneliner.was_tweeted:
	if oneliner.is_published:
	    try:
		import tweepy # 3rd party lib, install with: easy_install tweepy
		import settings
		if consumer_key is None:
		    consumer_key = settings.TWITTER.get('consumer_key')
		if consumer_secret is None:
		    consumer_secret = settings.TWITTER.get('consumer_secret')
		if access_token is None:
		    access_token = settings.TWITTER.get('access_token')
		if access_token_secret is None:
		    access_token_secret = settings.TWITTER.get('access_token_secret')

		# set up credentials to use Twitter api.
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		tweetmsg = 'http://bashoneliners.com/main/oneliner/%d %s: %s' % (
			oneliner.pk,
			oneliner.summary,
			oneliner.line,
			)
		if len(tweetmsg) > 160:
		    tweetmsg = tweetmsg[:156] + ' ...'
		
		if test:
		    print tweetmsg
		    print
		    return True
		else:
		    oneliner.was_tweeted = True
		    oneliner.save()
		    return api.update_status(tweetmsg)
	    except:
		pass


def oneliner_list(request):
    params = _common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True)
    return render_to_response('main/pages/index.html', params)

def oneliner(request, pk):
    params = _common_params(request)
    params['oneliners'] = OneLiner.objects.filter(pk=pk)
    return render_to_response('main/pages/oneliner.html', params)

@login_required
def oneliner_edit(request, pk):
    params = _common_params(request)

    try:
	oneliner0 = OneLiner.objects.get(pk=pk, user=request.user)
    except:
	return render_to_response('main/pages/access_error.html', params)

    if request.method == 'POST':
	form = EditOneLinerForm(request.user, request.POST, instance=oneliner0)
	if form.is_valid():
	    if form.is_save:
		oneliner1 = form.save()
		tweet(oneliner1)
		return redirect(form.cleaned_data.get('next_url'))
	    elif form.is_delete:
		oneliner0.delete()
		return redirect(profile)
    else:
	next_url = request.META.get('HTTP_REFERER', None) or '/'
	form = EditOneLinerForm(request.user, instance=oneliner0, initial={'next_url': next_url})

    params['form'] = form

    return render_to_response('main/pages/oneliner_edit.html', params, context_instance=RequestContext(request))

def oneliner_new(request, question_pk=None, oneliner_pk=None):
    params = _common_params(request)
    initial = {}

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

    if request.user.is_authenticated():
	if request.method == 'POST':
	    form = PostOneLinerForm(request.user, request.POST)
	    if form.is_valid():
		new_oneliner = form.save()
		tweet(new_oneliner)

		if question is not None:
		    question.add_answer(new_oneliner)
		elif oneliner0 is not None:
		    oneliner0.add_alternative(new_oneliner)

		return redirect(oneliner, new_oneliner.pk)
	else:
	    next_url = request.META.get('HTTP_REFERER', None) or '/'
	    initial['next_url'] = next_url
	    form = PostOneLinerForm(request.user, initial=initial)
    else:
	form = PostOneLinerForm(request.user)

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

    try:
	oneliner0 = OneLiner.objects.get(pk=pk)
    except:
	return render_to_response('main/pages/access_error.html', params)

    params['oneliner'] = oneliner0

    return render_to_response('main/pages/oneliner_comment.html', params, context_instance=RequestContext(request))


def question_list(request):
    params = _common_params(request)
    params['questions'] = Question.top()
    return render_to_response('main/pages/question_list.html', params, context_instance=RequestContext(request))

def question(request, pk):
    params = _common_params(request)
    params['questions'] = Question.objects.filter(pk=pk)
    return render_to_response('main/pages/question.html', params)

@login_required
def question_edit(request, pk):
    params = _common_params(request)

    try:
	question0 = Question.objects.get(pk=pk, user=request.user)
    except:
	return render_to_response('main/pages/access_error.html', params)

    if request.method == 'POST':
	form = EditQuestionForm(request.user, request.POST, instance=question0)
	if form.is_valid():
	    if form.is_save:
		question1 = form.save()
		return redirect(form.cleaned_data.get('next_url'))
	    elif form.is_delete:
		question0.delete()
		return redirect(profile)
    else:
	next_url = request.META.get('HTTP_REFERER', None) or '/'
	form = EditQuestionForm(request.user, instance=question0, initial={'next_url': next_url})

    params['form'] = form

    return render_to_response('main/pages/question_edit.html', params, context_instance=RequestContext(request))

def question_new(request):
    params = _common_params(request)

    if request.user.is_authenticated():
	if request.method == 'POST':
	    form = PostQuestionForm(request.user, request.POST)
	    if form.is_valid():
		new_question = form.save()
		return redirect(form.cleaned_data.get('next_url'))
	else:
	    next_url = request.META.get('HTTP_REFERER', None) or '/'
	    form = PostQuestionForm(request.user, initial={'next_url': next_url})
    else:
	form = PostQuestionForm(request.user)

    params['form'] = form

    return render_to_response('main/pages/question_edit.html', params, context_instance=RequestContext(request))


def profile(request, pk=None):
    params = _common_params(request)

    if request.user.is_authenticated():
	if pk is None:
	    pk = request.user.pk

	user = User.objects.get(pk=pk)

	params['hacker'] = user

	oneliners = OneLiner.objects.filter(user=user)
	if user != request.user:
	    oneliners = oneliners.filter(is_published=True)
	params['oneliners'] = oneliners

	questions = Question.objects.filter(user=user)
	if user != request.user:
	    questions = questions.filter(is_published=True)
	params['questions_pending'] = questions.filter(is_answered=False)
	params['questions_answered'] = questions.filter(is_answered=True)
    else:
	params['hacker'] = request.user

    return render_to_response('main/pages/profile.html', params)

def profile_edit(request):
    params = _common_params(request)
    params['next'] = request.META.get('HTTP_REFERER', None) or '/'

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

    return render_to_response('main/pages/profile_edit.html', params, context_instance=RequestContext(request))


def search(request):
    params = _common_params(request)
    form = params['searchform']

    if form.is_valid():
	params['oneliners'] = OneLiner.search(form.cleaned_data.get('query'))

    return render_to_response('main/pages/search.html', params)

def login(request):
    params = _common_params(request)
    return render_to_response('main/pages/login.html', params, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return oneliner_list(request)


''' simple pages '''

def sourcecode(request):
    params = _common_params(request)
    return render_to_response('main/pages/sourcecode.html', params)

def mission(request):
    params = _common_params(request)
    return render_to_response('main/pages/mission.html', params)

def help_markdown(request):
    return render_to_response('main/help/markdown.html')

# eof
