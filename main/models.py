from django.db import models
from django.db.models import Count, Q
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from django.template import Context, loader

from datetime import datetime
import random
import string
import re

''' Constants '''

RECENT_LIMIT = 25
SEARCH_LIMIT = 25
FEED_LIMIT = 10


''' Helper methods '''

def randomstring(length=16):
    return ''.join(random.choice(string.letters) for i in xrange(length))

def get_query_terms(query):
    if query is None:
	return ()

    query = query.strip()
    if query == '':
	return ()

    return re.split(r' +', query)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
	HackerProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

''' Core models '''

class HackerProfile(models.Model):
    user = models.OneToOneField(User)

    display_name = models.SlugField(max_length=50, blank=True, null=True, unique=True)
    twitter_name = models.SlugField(max_length=50, blank=True, null=True)
    blog_url = models.URLField('Blog URL', blank=True, null=True)
    homepage_url = models.URLField('Homepage URL', blank=True, null=True)

    def twitter_url(self):
	return 'http://twitter.com/%s/' % self.twitter_name

    def get_username(self):
	return self.user.username

    def get_email(self):
	return self.user.email

    def get_date_joined(self):
	return self.user.date_joined

    def get_display_name(self):
	return self.display_name or self.user.username

    def __unicode__(self):
	return ', '.join([x for x in (self.user.username, self.user.email) if x])

    class Meta:
	ordering = ('-id',)


class OneLiner(models.Model):
    user = models.ForeignKey(User)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField()
    limitations = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)
    was_tweeted = models.BooleanField(default=False)

    created_dt = models.DateTimeField(default=datetime.now, blank=True)

    def vote_up(self, user):
	Vote.vote_up(user, self)

    def vote_down(self, user):
	Vote.vote_down(user, self)

    def get_votes(self):
	return (self.get_votes_up(), self.get_votes_down())

    def get_votes_up(self):
	return self.vote_set.filter(up=True).count()

    def get_votes_down(self):
	return self.vote_set.filter(up=False).count()

    def questions(self):
	return self.answer_set.filter(question__is_published=True)

    def alternatives(self):
	return self.alternativeoneliner_set.filter(alternative__is_published=True)

    def add_alternative(self, alternative):
	AlternativeOneLiner(alternative=alternative, oneliner=self).save()

    def relateds(self):
	return self.related_set.filter(oneliner__is_published=True)

    @staticmethod
    def get(pk):
	return OneLiner.objects.get(pk=pk)

    @staticmethod
    def feed(limit=FEED_LIMIT):
	return OneLiner.recent(limit)

    @staticmethod
    def recent(limit=RECENT_LIMIT):
	return OneLiner.objects.filter(is_published=True)[:limit]

    @staticmethod
    def top(limit=SEARCH_LIMIT):
	return OneLiner.objects.filter(vote__up=True).annotate(votes=Count('vote')).order_by('-votes')[:limit]

    @staticmethod
    def simplesearch(query=None, limit=SEARCH_LIMIT):
	qq = Q()
	for term in get_query_terms(query):
	    sub_qq = Q()
	    sub_qq |= Q(summary__icontains=term)
	    sub_qq |= Q(line__icontains=term)
	    sub_qq |= Q(explanation__icontains=term)
	    sub_qq |= Q(limitations__icontains=term)
	    qq &= Q(sub_qq)
	return OneLiner.objects.filter(is_published=True).filter(qq)[:limit]

    @staticmethod
    def search(form, limit=SEARCH_LIMIT):
	query = form.cleaned_data.get('query')
	match_summary = form.cleaned_data.get('match_summary')
	match_line = form.cleaned_data.get('match_line')
	match_explanation = form.cleaned_data.get('match_explanation')
	match_limitations = form.cleaned_data.get('match_limitations')
	match_whole_words = form.cleaned_data.get('match_whole_words')

	terms = get_query_terms(query)
	qq = Q()
	for term in terms:
	    sub_qq = Q()
	    if match_summary:
		sub_qq |= Q(summary__icontains=term)
	    if match_line:
		sub_qq |= Q(line__icontains=term)
	    if match_explanation:
		sub_qq |= Q(explanation__icontains=term)
	    if match_limitations:
		sub_qq |= Q(limitations__icontains=term)
	    if len(sub_qq.children) > 0:
		qq &= Q(sub_qq)

	if len(qq.children) > 0:
	    results = OneLiner.objects.filter(is_published=True).filter(qq)

	    if match_whole_words:
		results = [x for x in results if x.matches_words(terms, match_summary, match_line, match_explanation, match_limitations)]

	    return results[:limit]
	else:
	    return ()

    def matches_words(self, terms, match_summary, match_line, match_explanation, match_limitations):
	for term in terms:
	    if match_summary and re.search(r'\b%s\b' % term, self.summary):
		return True
	    if match_line and re.search(r'\b%s\b' % term, self.line):
		return True
	    if match_explanation and re.search(r'\b%s\b' % term, self.explanation):
		return True
	    if match_limitations and re.search(r'\b%s\b' % term, self.limitations):
		return True

    def get_absolute_url(self):
	return "/main/oneliner/%i/" % self.pk

    def __unicode__(self):
	return self.summary

    class Meta:
	get_latest_by = 'pk'
	ordering = ('-id',)


class AlternativeOneLiner(models.Model):
    alternative = models.ForeignKey(OneLiner, related_name='related_set')
    oneliner = models.ForeignKey(OneLiner)

    class Meta:
	unique_together = (('alternative', 'oneliner',),)


class Question(models.Model):
    user = models.ForeignKey(User)
    summary = models.CharField(max_length=200)
    explanation = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)
    created_dt = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
	return '%s @%s' % (self.summary, self.user)

    def add_answer(self, oneliner):
	Answer(question=self, oneliner=oneliner).save()

    def oneliners(self):
	return self.answer_set.filter(oneliner__is_published=True)

    def accept_answer(self, oneliner):
	self.is_answered = True
	self.save()
	try:
	    AcceptedAnswer(question=self, oneliner=oneliner).save()
	except:
	    pass

    def clear_all_answers(self):
	self.is_answered = False
	self.save()

    def save(self, *args, **kwargs):
	if not self.is_answered:
	    AcceptedAnswer.objects.filter(question=self).delete()
	return super(Question, self).save(*args, **kwargs)

    @staticmethod
    def get(pk):
	return Question.objects.get(pk=pk)

    @staticmethod
    def feed(limit=FEED_LIMIT):
	return Question.objects.filter(is_published=True)[:limit]

    @staticmethod
    def recent(limit=RECENT_LIMIT):
	return Question.objects.filter(is_published=True).exclude(is_answered=True)[:limit]

    @staticmethod
    def latest():
	try:
	    return Question.recent(1)[0]
	except:
	    pass

    def get_absolute_url(self):
	return "/main/question/%i/" % self.pk

    class Meta:
	get_latest_by = 'pk'
	ordering = ('-id',)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    oneliner = models.ForeignKey(OneLiner)


class AcceptedAnswer(models.Model):
    question = models.ForeignKey(Question)
    oneliner = models.ForeignKey(OneLiner)

    class Meta:
	unique_together = (('question', 'oneliner',),)


class Vote(models.Model):
    user = models.ForeignKey(User)
    oneliner = models.ForeignKey(OneLiner)
    up = models.BooleanField(default=True)

    created_dt = models.DateTimeField(default=datetime.now)

    @staticmethod
    def vote(user, oneliner, updown):
	if oneliner.user == user:
	    return

	try:
	    oneliner.vote_set.get(user=user, up=updown)
	    return
	except:
	    pass

	oneliner.vote_set.filter(user=user).delete()
	Vote(user=user, oneliner=oneliner, up=updown).save()

    @staticmethod
    def vote_up(user, oneliner):
	Vote.vote(user, oneliner, True)

    @staticmethod
    def vote_down(user, oneliner):
	Vote.vote(user, oneliner, False)

    def __unicode__(self):
	return '%s %s %s' % (self.user.full_name, ('--', '++')[self.up], self.oneliner.summary)

    class Meta:
	unique_together = (('user', 'oneliner',),)


# eof
