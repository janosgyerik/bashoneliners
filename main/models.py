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

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()


# eof
