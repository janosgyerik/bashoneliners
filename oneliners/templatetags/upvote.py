from django import template

from oneliners.models import Vote

register = template.Library()

@register.simple_tag(takes_context=True)
def upvoted(context, oneliner):
    user = context['user']
    if user.is_authenticated():
        try:
            vote = oneliner.vote_set.get(user=user)
            if vote.value > 0:
                return 'upvoted'
        except Vote.DoesNotExist:
            pass
    return ''


@register.simple_tag(takes_context=True)
def downvoted(context, oneliner):
    user = context['user']
    if user.is_authenticated():
        try:
            vote = oneliner.vote_set.get(user=user)
            if vote.value < 0:
                return 'downvoted'
        except Vote.DoesNotExist:
            pass
    return ''
