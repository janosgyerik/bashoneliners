from django.contrib.auth.models import User

from . import models


def get_objects(objects):
    for item in objects.all():
        yield {
            'pk': item.pk
        }


def get_oneliners():
    yield from get_objects(models.OneLiner.objects)


def get_onliners_per_category():
    yield from get_objects(models.Category.objects)


def get_onliners_per_command():
    yield from get_objects(models.Command.objects)


def get_users():
    yield from get_objects(User.objects)


def get_category_command_pairs():
    categories = ['undefined']
    commands = categories[:]
    categories += [c['display_name'] for c in models.Category.cloud().filter(type="function")]
    commands += [c['name'] for c in models.Command.cloud()]

    for command in commands:
        for category in categories:
            yield {
                'category': category,
                'command': command,
            }

