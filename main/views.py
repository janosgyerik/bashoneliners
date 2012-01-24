from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext
from django.contrib.auth import logout as django_logout

from bashoneliners.main.models import HackerProfile, OneLiner, User, WishListAnswer
from bashoneliners.main.forms import *

from datetime import datetime


''' constants '''

#


''' helper methods '''

def get_common_params(request):
    if request.method == 'GET':
	searchform = SearchOneLinerForm(request.GET)
    else:
	searchform = SearchOneLinerForm()

    params = {
	    'user': request.user,
	    'searchform': searchform,
	    }

    try:
	if request.META['HTTP_USER_AGENT'].startswith('W3C_Validator'):
	    params['w3c'] = True
    except: 
	pass

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

		tweetmsg = 'http://bashoneliners.com/main/oneliner/%d %s -- %s' % (
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


''' url handlers '''

def index(request):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True)
    return render_to_response('main/index.html', params)

def top_n(request, num):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.top()
    return render_to_response('main/top_n.html', params)

def oneliner(request, pk):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(pk=pk)
    return render_to_response('main/oneliner.html', params)

@login_required
def new_oneliner(request, question_pk=None):
    params = get_common_params(request)

    try:
	question = WishListQuestion.objects.get(pk=question_pk)
    except:
	question = None

    if request.method == 'POST':
	form = PostOneLinerForm(request.user, request.POST)
	if form.is_valid():
	    new_oneliner = form.save()
	    tweet(new_oneliner)

	    if question is not None:
		WishListAnswer(question=question, oneliner=new_oneliner).save()

	    return redirect(oneliner, new_oneliner.pk)
    else:
	next_url = request.META.get('HTTP_REFERER', None) or '/'
	form = PostOneLinerForm(request.user, initial={'next_url': next_url})

    params['form'] = form
    params['question'] = question

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))

@login_required
def edit_oneliner(request, pk):
    params = get_common_params(request)

    try:
	oneliner0 = OneLiner.objects.get(pk=pk, user=request.user)
    except:
	return render_to_response('main/access-error.html', params)

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

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))

def sourcecode(request):
    params = get_common_params(request)
    return render_to_response('main/sourcecode.html', params)

def mission(request):
    params = get_common_params(request)
    return render_to_response('main/mission.html', params)

def profile(request, pk=None):
    params = get_common_params(request)

    if pk is None:
	pk = request.user.pk

    user = User.objects.get(pk=pk)

    params['hacker'] = user

    oneliners = OneLiner.objects.filter(user=user)
    if user != request.user:
	oneliners = oneliners.filter(is_published=True)
    params['oneliners'] = oneliners

    questions = WishListQuestion.objects.filter(user=user)
    if user != request.user:
	questions = questions.filter(is_published=True)
    params['questions'] = questions

    return render_to_response('main/profile.html', params)

@login_required
def edit_profile(request):
    params = get_common_params(request)
    params['next'] = request.META.get('HTTP_REFERER', None) or '/'

    hackerprofile = request.user.hackerprofile

    if request.method == 'POST':
	form = EditHackerProfileForm(request.POST, instance=hackerprofile)
	if form.is_valid():
	    form.save()
	    return redirect(profile)
    else:
	form = EditHackerProfileForm(instance=hackerprofile)

    params['form'] = form

    return render_to_response('main/edit-profile.html', params, context_instance=RequestContext(request))

def wishlist(request):
    params = get_common_params(request)

    if request.user.is_authenticated:
	if request.method == 'POST':
	    data = dict(request.POST)
	    data['summary'] = request.POST.get('summary')
	    data['explanation'] = request.POST.get('explanation')
	    data['is_published'] = request.POST.get('is_published')
	    data['is_answered'] = False
	    form = PostWishListQuestionForm(request.user, data)
	    if form.is_valid():
		new_question = form.save()
		return redirect(wishlist)
	else:
	    next_url = request.META.get('HTTP_REFERER', None) or '/'
	    form = PostWishListQuestionForm(request.user, initial={'next_url': next_url})
    else:
	form = None

    params['form'] = form
    params['questions'] = WishListQuestion.top()

    return render_to_response('main/wishlist.html', params, context_instance=RequestContext(request))

def question(request, pk):
    params = get_common_params(request)
    params['questions'] = WishListQuestion.objects.filter(pk=pk)
    return render_to_response('main/question.html', params)

@login_required
def edit_question(request, pk):
    params = get_common_params(request)

    try:
	question0 = WishListQuestion.objects.get(pk=pk, user=request.user)
    except:
	return render_to_response('main/access-error.html', params)

    if request.method == 'POST':
	form = EditWishListQuestionForm(request.user, request.POST, instance=question0)
	if form.is_valid():
	    if form.is_save:
		question1 = form.save()
		return redirect(form.cleaned_data.get('next_url'))
	    elif form.is_delete:
		question0.delete()
		return redirect(profile)
    else:
	next_url = request.META.get('HTTP_REFERER', None) or '/'
	form = EditWishListQuestionForm(request.user, instance=question0, initial={'next_url': next_url})

    params['form'] = form

    return render_to_response('main/edit-question.html', params, context_instance=RequestContext(request))

@login_required
def new_question(request):
    params = get_common_params(request)

    if request.method == 'POST':
	form = PostWishListQuestionForm(request.user, request.POST)
	if form.is_valid():
	    new_question = form.save()
	    #return redirect(wishlist)
	    return redirect(form.cleaned_data.get('next_url'))
    else:
	next_url = request.META.get('HTTP_REFERER', None) or '/'
	form = PostWishListQuestionForm(request.user, initial={'next_url': next_url})

    params['form'] = form

    return render_to_response('main/edit-question.html', params, context_instance=RequestContext(request))

def search(request):
    params = get_common_params(request)
    form = params['searchform']

    if form.is_valid():
	params['oneliners'] = OneLiner.search(form.cleaned_data.get('query'))

    return render_to_response('main/search.html', params)

def search_ajax(request):
    params = {}

    if request.method == 'GET':
	form = SearchOneLinerForm(request.GET)
    else:
	form = None

    if form is not None:
	if form.is_valid():
	    params['oneliners'] = OneLiner.search(form.cleaned_data.get('query'))

    return render_to_response('main/oneliners.html', params)

def login(request):
    params = get_common_params(request)
    return render_to_response('main/login.html', params, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return index(request)

# eof
