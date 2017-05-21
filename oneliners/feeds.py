from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from oneliners.models import OneLiner


def oneliner(request):
    return OneLinerEntries()(request)


class OneLinerEntries(Feed):
    title = "Bash One-Liners"
    link = reverse(oneliner)
    description = "Recently posted bash one-liners on bashoneliners.com"
    description_template = 'oneliners/feeds/oneliner.html'

    def items(self):
        return OneLiner.feed()

