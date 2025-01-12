from django.contrib.auth.models import User

from . import models


def get_objects(objects):
    for item in objects.all():
        yield {
            'pk': item.pk
        }


def get_oneliners():
    yield from get_objects(models.OneLiner.objects)


def get_users():
    yield from get_objects(User.objects)

