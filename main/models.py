from django.db import models
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

    line = models.TextField()
    summary = models.TextField()
    explanation = models.TextField(blank=True)
    caveats = models.TextField(blank=True)

    is_published = models.BooleanField(default=False)

    created_dt = models.DateTimeField(default=datetime.now)

    def lines(self):
	return [x for x in self.line.split('\n') if x.strip() != '']

    def __unicode__(self):
	return self.line


# eof
