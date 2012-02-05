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

    @staticmethod
    def get(pk):
	return OneLiner.objects.get(pk=pk)

    @staticmethod
    def top(limit=50):
	return OneLiner.objects.filter(vote__up=True).annotate(votes=Count('vote')).order_by('-votes')[:limit]

    @staticmethod
    def search(query=None, limit=50):
	qq = Q()
	for term in get_query_terms(query):
	    sub_qq = Q()
	    sub_qq |= Q(summary__icontains=term)
	    sub_qq |= Q(line__icontains=term)
	    sub_qq |= Q(explanation__icontains=term)
	    sub_qq |= Q(limitations__icontains=term)
	    qq &= Q(sub_qq)
	return OneLiner.objects.filter(is_published=True).filter(qq)[:limit]

    def get_absolute_url(self):
	return "/main/oneliner/%i/" % self.pk

    def __unicode__(self):
	return self.summary

    class Meta:
	get_latest_by = 'pk'
	ordering = ('-id',)


class Question(models.Model):
    user = models.ForeignKey(User)
    summary = models.CharField(max_length=200)
    explanation = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)
    created_dt = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
	return '%s @%s' % (self.summary, self.user)

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
    def top(limit=50):
	return Question.objects.exclude(is_published=False).exclude(is_answered=True)[:limit]

    @staticmethod
    def latest():
	try:
	    return Question.top(1)[0]
	except:
	    return None

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


class LatestEntries(Feed):
    title = "Bash One-Liners"
    link = "/feed/"
    description = "Latest One-Liners posted on bashoneliners.com"
    description_template = 'feed_description.html'

    def items(self):
	return OneLiner.objects.filter(is_published=True)


# eof
