from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import UserManager

from datetime import datetime
import random, string, re


''' Helper methods '''

def randomstring(length=16):
    return ''.join(random.choice(string.letters) for i in xrange(length))


''' Core models '''

class Hacker(DjangoUser):
    twitter = models.SlugField(max_length=100, blank=True, null=True)
    #stackoverflow
    #blog
    #homepage

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()


class OneLiner(models.Model):
    hacker = models.ForeignKey(Hacker)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField(blank=True)
    caveats = models.TextField('Limitations', blank=True)

    is_published = models.BooleanField(default=True)

    created_dt = models.DateTimeField(default=datetime.now, blank=True)

    def lines(self):
	return [x for x in self.line.split('\n') if x.strip() != '']

    def vote_up(self, hacker):
	Vote.vote_up(hacker, self)

    def vote_down(self, hacker):
	Vote.vote_down(hacker, self)

    def get_votes(self):
	return (self.get_votes_up(), self.get_votes_down())

    def get_votes_up(self):
	return self.vote_set.filter(up=True).count()

    def get_votes_down(self):
	return self.vote_set.filter(up=False).count()

    @staticmethod
    def top(limit=50):
	return OneLiner.objects.filter(vote__up=True).annotate(votes=Count('vote')).order_by('-votes')[:limit]

    def __unicode__(self):
	return self.summary

    class Meta:
	get_latest_by = 'pk'


class Vote(models.Model):
    hacker = models.ForeignKey(Hacker)
    oneliner = models.ForeignKey(OneLiner)
    up = models.BooleanField(default=True)

    created_dt = models.DateTimeField(default=datetime.now)

    @staticmethod
    def vote(hacker, oneliner, updown):
	if oneliner.hacker == hacker:
	    return

	try:
	    oneliner.vote_set.get(hacker=hacker, up=updown)
	    return
	except:
	    pass

	oneliner.vote_set.filter(hacker=hacker).delete()
	Vote(hacker=hacker, oneliner=oneliner, up=updown).save()

    @staticmethod
    def vote_up(hacker, oneliner):
	Vote.vote(hacker, oneliner, True)

    @staticmethod
    def vote_down(hacker, oneliner):
	Vote.vote(hacker, oneliner, False)

    def __unicode__(self):
	return '%s %s %s' % (self.hacker.full_name, ('--', '++')[self.up], self.oneliner.summary)

    class Meta:
	unique_together = (('hacker', 'oneliner',),)


# eof
