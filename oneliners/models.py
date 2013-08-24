from django.db import models
from django.db.models import Count, Q, Sum
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.dispatch import receiver
from django.utils.timezone import now

import random
import string
import re

''' Constants '''

RECENT_LIMIT = 25
SEARCH_LIMIT = 25
FEED_LIMIT = 10


''' Helper methods '''


def randomstring(length=16):
    return ''.join(random.choice(string.letters) for i in xrange(length))


def get_query_terms(query):
    if query is None:
        return ()

    query = query.strip()
    if query == '':
        return ()

    return re.split(r' +', query)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            HackerProfile.objects.get_or_create(user=instance)
        except HackerProfile.DoesNotExist:
            pass

post_save.connect(create_user_profile, sender=User)

''' Core models '''


class HackerProfile(models.Model):
    user = models.OneToOneField(User)

    display_name = models.SlugField(max_length=50, blank=True, null=True, unique=True)
    twitter_name = models.SlugField(max_length=50, blank=True, null=True)
    blog_url = models.URLField('Blog URL', blank=True, null=True)
    homepage_url = models.URLField('Homepage URL', blank=True, null=True)

    def twitter_url(self):
        if self.twitter_name:
            return 'http://twitter.com/%s/' % self.twitter_name

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_date_joined(self):
        return self.user.date_joined

    def get_display_name(self):
        return self.display_name or self.user.username

    def __unicode__(self):
        return ', '.join([x for x in (self.user.username, self.user.email) if x])

    class Meta:
        ordering = ('-id',)


class OneLiner(models.Model):
    user = models.ForeignKey(User)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField()
    limitations = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)
    was_tweeted = models.BooleanField(default=False)

    created_dt = models.DateTimeField(default=now, blank=True)

    def vote_up(self, user):
        Vote.vote_up(user, self)

    def vote_down(self, user):
        Vote.vote_down(user, self)

    def get_votes(self):
        return (self.get_votes_up(), self.get_votes_down())

    def get_votes_up(self):
        return self.vote_set.filter(value=1).count()

    def get_votes_down(self):
        return self.vote_set.filter(value=-1).count()

    def questions(self):
        return self.answer_set.filter(question__is_published=True)

    def alternatives(self):
        return self.alternativeoneliner_set.filter(alternative__is_published=True).annotate(score=Sum('alternative__vote__value'))

    def add_alternative(self, alternative):
        AlternativeOneLiner(alternative=alternative, oneliner=self).save()

    def relateds(self):
        return self.related_set.filter(oneliner__is_published=True).annotate(score=Sum('oneliner__vote__value'))

    @staticmethod
    def get(pk):
        return OneLiner.objects.get(pk=pk)

    @staticmethod
    def feed(limit=FEED_LIMIT):
        return OneLiner.recent(limit)

    @staticmethod
    def recent(limit=RECENT_LIMIT):
        return OneLiner.objects.filter(is_published=True)[:limit]

    @staticmethod
    def recent_by_tag(text, limit=RECENT_LIMIT):
        return OneLiner.objects.filter(is_published=True, onelinertag__tag__text=text)[:limit]

    @staticmethod
    def top(limit=SEARCH_LIMIT):
        return OneLiner.objects.filter(vote__up=True).annotate(votes=Count('vote')).order_by('-votes')[:limit]

    @staticmethod
    def simplesearch(query=None, limit=SEARCH_LIMIT):
        qq = Q()
        for term in get_query_terms(query):
            sub_qq = Q()
            sub_qq |= Q(summary__icontains=term)
            sub_qq |= Q(line__icontains=term)
            sub_qq |= Q(explanation__icontains=term)
            sub_qq |= Q(limitations__icontains=term)
            qq &= Q(sub_qq)
        return OneLiner.objects.filter(is_published=True).filter(qq)[:limit]

    @staticmethod
    def search(form, limit=SEARCH_LIMIT):
        query = form.cleaned_data.get('query')
        match_summary = form.cleaned_data.get('match_summary')
        match_line = form.cleaned_data.get('match_line')
        match_explanation = form.cleaned_data.get('match_explanation')
        match_limitations = form.cleaned_data.get('match_limitations')
        match_whole_words = form.cleaned_data.get('match_whole_words')

        terms = get_query_terms(query)
        qq = Q()
        for term in terms:
            sub_qq = Q()
            if match_summary:
                sub_qq |= Q(summary__icontains=term)
            if match_line:
                sub_qq |= Q(line__icontains=term)
            if match_explanation:
                sub_qq |= Q(explanation__icontains=term)
            if match_limitations:
                sub_qq |= Q(limitations__icontains=term)
            if len(sub_qq.children) > 0:
                qq &= Q(sub_qq)

        if len(qq.children) > 0:
            results = OneLiner.objects.filter(is_published=True).annotate(score=Sum('vote__value')).filter(qq)

            if match_whole_words:
                results = [x for x in results if x.matches_words(terms, match_summary, match_line, match_explanation, match_limitations)]

            return results[:limit]
        else:
            return ()

    def matches_words(self, terms, match_summary, match_line, match_explanation, match_limitations):
        for term in terms:
            if match_summary and re.search(r'\b%s\b' % term, self.summary):
                return True
            if match_line and re.search(r'\b%s\b' % term, self.line):
                return True
            if match_explanation and re.search(r'\b%s\b' % term, self.explanation):
                return True
            if match_limitations and re.search(r'\b%s\b' % term, self.limitations):
                return True

    def update_tags(self):
        self.onelinertag_set.all().delete()
        if self.is_published:
            words = re.split(r'[ ;|]+', self.line)
            tagwords = set([word for word in words if re.match(r'^[a-z_]{2,}$', word)])
            for tagword in tagwords:
                tag = Tag.create_or_get(tagword)
                OneLinerTag(oneliner=self, tag=tag).save()

    def get_tags(self):
        return [rel.tag.text for rel in self.onelinertag_set.all()]

    def save(self, *args, **kwargs):
        ret = super(OneLiner, self).save(*args, **kwargs)
        self.update_tags()
        return ret

    def get_absolute_url(self):
        return "/oneliners/oneliner/%i/" % self.pk

    def __unicode__(self):
        return self.summary

    class Meta:
        get_latest_by = 'pk'
        ordering = ('-id',)


class AlternativeOneLiner(models.Model):
    alternative = models.ForeignKey(OneLiner, related_name='related_set')
    oneliner = models.ForeignKey(OneLiner)

    class Meta:
        unique_together = (('alternative', 'oneliner',),)


class Tag(models.Model):
    text = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.text

    @staticmethod
    def create_or_get(text):
        try:
            return Tag.objects.get(text=text)
        except Tag.DoesNotExist:
            tag = Tag(text=text)
            tag.save()
            return tag

    @staticmethod
    def tagcloud():
        return Tag.objects.annotate(count=Count('onelinertag')).filter(count__gt=1).order_by('-count').values('text', 'count')
        #return Tag.objects.annotate(count=Count('onelinertag')).order_by('-count').values_list('text', 'count')


class OneLinerTag(models.Model):
    oneliner = models.ForeignKey(OneLiner)
    tag = models.ForeignKey(Tag)


class Question(models.Model):
    user = models.ForeignKey(User)
    summary = models.CharField(max_length=200)
    explanation = models.TextField()
    is_published = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)
    created_dt = models.DateTimeField(default=now, blank=True)

    def __unicode__(self):
        return self.summary

    def add_answer(self, oneliner):
        Answer(question=self, oneliner=oneliner).save()

    def oneliners(self):
        return self.answer_set.filter(oneliner__is_published=True).annotate(score=Sum('oneliner__vote__value'))

    def accept_answer(self, oneliner):
        self.is_answered = True
        self.save()
        try:
            AcceptedAnswer(question=self, oneliner=oneliner).save()
        except AcceptedAnswer.DoesNotExist:
            pass

    def clear_all_answers(self):
        self.is_answered = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.is_answered:
            AcceptedAnswer.objects.filter(question=self).delete()
        return super(Question, self).save(*args, **kwargs)

    @staticmethod
    def get(pk):
        return Question.objects.get(pk=pk)

    @staticmethod
    def feed(limit=FEED_LIMIT):
        return Question.objects.filter(is_published=True)[:limit]

    @staticmethod
    def recent(limit=RECENT_LIMIT):
        return Question.objects.filter(is_published=True).exclude(is_answered=True)[:limit]

    @staticmethod
    def latest():
        try:
            return Question.recent(1)[0]
        except IndexError:
            pass

    def get_absolute_url(self):
        return "/oneliners/question/%i/" % self.pk

    class Meta:
        get_latest_by = 'pk'
        ordering = ('-id',)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    oneliner = models.ForeignKey(OneLiner)


class AcceptedAnswer(models.Model):
    question = models.ForeignKey(Question)
    oneliner = models.ForeignKey(OneLiner)

    class Meta:
        unique_together = (('question', 'oneliner',),)


class Vote(models.Model):
    user = models.ForeignKey(User)
    oneliner = models.ForeignKey(OneLiner)
    value = models.IntegerField(default=0)

    created_dt = models.DateTimeField(default=now)

    @staticmethod
    def vote(user, oneliner, value):
        if oneliner.user == user:
            return

        try:
            oneliner.vote_set.get(user=user, value=value)
            return
        except Vote.DoesNotExist:
            pass

        oneliner.vote_set.filter(user=user).delete()
        Vote(user=user, oneliner=oneliner, value=value).save()

    @staticmethod
    def vote_up(user, oneliner):
        Vote.vote(user, oneliner, 1)

    @staticmethod
    def vote_down(user, oneliner):
        Vote.vote(user, oneliner, -1)

    @staticmethod
    def vote_clear(user, oneliner):
        oneliner.vote_set.filter(user=user).delete()

    def __unicode__(self):
        return '%s %s %s' % (self.user.get_full_name(), ('--', '++')[self.up], self.oneliner.summary)

    class Meta:
        unique_together = (('user', 'oneliner',),)


def Comment_recent(limit=RECENT_LIMIT):
    return Comment.objects.filter(is_public=True).exclude(is_removed=True).order_by('-submit_date')[:limit]


def Comment_feed(limit=FEED_LIMIT):
    return Comment_recent(limit)


# eof
