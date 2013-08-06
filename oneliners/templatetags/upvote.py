from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def upvoted(context, oneliner):
    user = context['user']
    try:
        vote = oneliner.vote_set.get(user=user)
        if vote.value > 0:
            return 'upvoted'
    except:
        pass
    return ''


@register.simple_tag(takes_context=True)
def downvoted(context, oneliner):
    user = context['user']
    try:
        vote = oneliner.vote_set.get(user=user)
        if vote.value < 0:
            return 'downvoted'
    except:
        pass
    return ''
