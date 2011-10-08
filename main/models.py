from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User

from datetime import datetime
import random, string, re


''' Helper methods '''

def randomstring(length=16):
    return ''.join(random.choice(string.letters) for i in xrange(length))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
	HackerProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

''' Core models '''

class HackerProfile(models.Model):
    user = models.OneToOneField(User)

    #twitter = models.SlugField(max_length=100, blank=True, null=True)
    #stackoverflow
    #blog
    #homepage

    def __unicode__(self):
	return ', '.join([x for x in (self.user.username, self.user.email) if x])


class OneLiner(models.Model):
    user = models.ForeignKey(User)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField(blank=True)
    caveats = models.TextField('Limitations', blank=True)

    is_published = models.BooleanField(default=True)

    created_dt = models.DateTimeField(default=datetime.now, blank=True)

    def lines(self):
	return [x for x in self.line.split('\n') if x.strip() != '']

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

    @staticmethod
    def top(limit=50):
	return OneLiner.objects.filter(vote__up=True).annotate(votes=Count('vote')).order_by('-votes')[:limit]

    def get_absolute_url(self):
	return "/main/oneliner/%i/" % self.pk

    def __unicode__(self):
	return self.summary

    class Meta:
	get_latest_by = 'pk'


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
    title = "BashOneLiners Syndication Feed"
    link = "/feed/"
    description = "Latest Items posted to bashoneliners.com"

    def items(self):
	return OneLiner.objects.filter(is_published=True).order_by('-pk')


# eof
