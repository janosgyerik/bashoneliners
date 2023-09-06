from django.contrib.syndication.views import Feed

from oneliners.models import OneLiner


def oneliners(request):
    return LatestOneLinersFeed()(request)


class LatestOneLinersFeed(Feed):
    title = "Bash One-Liners"
    link = '/oneliners/feeds/oneliners/'
    description = "Recently posted Bash one-liners on bashoneliners.com"
    description_template = 'oneliners/feeds/oneliners.html'

    def items(self):
        return OneLiner.feed()

