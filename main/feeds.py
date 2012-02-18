from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from bashoneliners.main.models import OneLiner, Question


### URL handlers

def oneliner(request):
    return OneLinerEntries()(request)

def question(request):
    return QuestionEntries()(request)


### Feed classes

class OneLinerEntries(Feed):
    title = "Bash One-Liners"
    link = reverse(oneliner)
    description = "Latest Bash One-Liners posted on bashoneliners.com"
    description_template = 'main/feeds/oneliner.html'

    def items(self):
	return OneLiner.feed()

class QuestionEntries(Feed):
    title = "Questions for Bash One-Liners"
    link = reverse(question)
    description = "Latest questions/requests for Bash One-Liners"
    description_template = 'main/feeds/question.html'

    def items(self):
	return Question.feed()


# eof
