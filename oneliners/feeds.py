from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from oneliners.models import OneLiner, Question, Comment_feed


# URL handlers


def oneliner(request):
    return OneLinerEntries()(request)


def question(request):
    return QuestionEntries()(request)


def comment(request):
    return CommentEntries()(request)


# Feed classes


class OneLinerEntries(Feed):
    title = "Bash One-Liners"
    link = reverse(oneliner)
    description = "Recently posted bash one-liners on bashoneliners.com"
    description_template = 'oneliners/feeds/oneliner.html'

    def items(self):
        return OneLiner.feed()


class QuestionEntries(Feed):
    title = "Questions for bash one-liners"
    link = reverse(question)
    description = "Recently posted questions on bashoneliners.com"
    description_template = 'oneliners/feeds/question.html'

    def items(self):
        return Question.feed()


class CommentEntries(Feed):
    title = "Comments on bash one-liners"
    link = reverse(comment)
    description = "Recently posted comments on bashoneliners.com"
    description_template = 'oneliners/feeds/comment.html'

    def items(self):
        return Comment_feed()

    def item_title(self, item):
        return self.ellipsize(item.comment)

    def ellipsize(self, text):
        if len(text) < 50:
            return text
        else:
            return text[:46] + ' ...'
