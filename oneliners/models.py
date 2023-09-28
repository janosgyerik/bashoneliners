import random
import re
import string
from typing import List

from django.db import models
from django.db.models import Count, Q, Sum
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now

from oneliners.tools import tags as tag_tools
from oneliners import categorization

RECENT_LIMIT = 25
SEARCH_LIMIT = 25
FEED_LIMIT = 10
TAGCLOUD_MIN_COUNT = 3


def randomstring(length=16):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

    def get_absolute_url(self):
        return f"/oneliners/users/{self.pk}/"

    def __str__(self):
        return ', '.join([x for x in (self.user.username, self.user.email) if x])

    class Meta:
        ordering = ('-id',)


class OneLiner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField()
    limitations = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)
    was_tweeted = models.BooleanField(default=False)

    unpublished = models.BooleanField(default=False)

    published_dt = models.DateTimeField(null=True, blank=True)
    created_dt = models.DateTimeField(default=now, blank=True)
    updated_dt = models.DateTimeField(default=now, blank=True)

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

    def score(self):
        return self.vote_set.aggregate(score=Sum('value'))['score'] or 0

    def alternatives(self):
        return self.alternativeoneliner_set.filter(alternative__is_published=True).annotate(
            vote_sum=Sum('alternative__vote__value'))

    def add_alternative(self, alternative):
        AlternativeOneLiner(alternative=alternative, oneliner=self).save()

    def relateds(self):
        return self.related_set.filter(oneliner__is_published=True).annotate(vote_sum=Sum('oneliner__vote__value'))

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
    def filter_by_command(command, order_by=None, limit=RECENT_LIMIT):
        query = OneLiner.objects.filter(is_published=True).annotate(
            vote_sum=Sum('vote__value')).filter(onelinertag__tag__text=command)
        if order_by:
            query = query.order_by(order_by, '-id')
        return query[:limit]

    @staticmethod
    def filter_by_category(category_name, order_by=None, limit=RECENT_LIMIT):
        query = OneLiner.objects.filter(is_published=True).annotate(
            vote_sum=Sum('vote__value')).filter(onelinercategory__category__name=category_name)
        if order_by:
            query = query.order_by(order_by, '-id')
        return query[:limit]

    @staticmethod
    def filter_by_category_and_command(category_name, command, order_by=None, limit=RECENT_LIMIT):
        query = OneLiner.objects.filter(is_published=True).annotate(vote_sum=Sum('vote__value'))
        if category_name:
            query = query.filter(onelinercategory__category__name=category_name)
        if command:
            query = query.filter(onelinertag__tag__text=command)
        if order_by:
            query = query.order_by(order_by, '-id')
        return query[:limit]

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
            results = OneLiner.objects.filter(is_published=True).annotate(
                vote_sum=Sum('vote__value')).filter(qq).order_by('-vote_sum', '-id')

            if match_whole_words:
                results = [x for x in results if
                           x.matches_words(terms, match_summary, match_line, match_explanation, match_limitations)]

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
            for tagword in tag_tools.compute_tags_as_first_command(self.line):
                tag = Tag.create_or_get(tagword)
                OneLinerTag(oneliner=self, tag=tag).save()

    def get_tags(self):
        return [rel.tag.text for rel in self.onelinertag_set.all()]

    def set_categories(self, categories: List['Category']):
        self.onelinercategory_set.all().delete()
        for category in categories:
            OnelinerCategory(oneliner=self, category=category).save()

    def get_categories(self):
        return [rel.category for rel in self.onelinercategory_set.all()]

    def has_categories(self):
        return self.onelinercategory_set.exists()

    def save(self, *args, **kwargs):
        self.updated_dt = now()

        if self.is_published and self.published_dt is None:
            self.published_dt = now()

        ret = super(OneLiner, self).save(*args, **kwargs)

        self.update_tags()

        return ret

    def get_absolute_url(self):
        return "/oneliners/{}/".format(self.pk)

    def __str__(self):
        return self.summary

    class Meta:
        get_latest_by = 'pk'
        ordering = ('-id',)


class AlternativeOneLiner(models.Model):
    alternative = models.ForeignKey(OneLiner, related_name='related_set', on_delete=models.CASCADE)
    oneliner = models.ForeignKey(OneLiner, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('alternative', 'oneliner',),)


class OneLinerSnapshot(models.Model):
    """An immutable snapshot of the content of a oneliner"""
    oneliner = models.ForeignKey(OneLiner, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    summary = models.CharField(max_length=200)
    line = models.TextField()
    explanation = models.TextField()
    limitations = models.TextField()

    is_published = models.BooleanField()
    was_tweeted = models.BooleanField()

    unpublished = models.BooleanField()

    created_dt = models.DateTimeField(default=now)


class Tag(models.Model):
    text = models.SlugField(max_length=50)

    def __str__(self):
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
        tags = Tag.objects.annotate(count=Count('onelinertag')).filter(
            count__gte=TAGCLOUD_MIN_COUNT).order_by('text').values('text', 'count')
        return [tag for tag in tags if tag['text'] not in {'do', 'done', 'fi', 'then', 'in', 'copy'}]


class OneLinerTag(models.Model):
    oneliner = models.ForeignKey(OneLiner, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oneliner = models.ForeignKey(OneLiner, on_delete=models.CASCADE)
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

    def __str__(self):
        return '{} {} {:+}'.format(self.user.get_full_name(), self.oneliner.summary, self.value)

    class Meta:
        unique_together = (('user', 'oneliner',),)


class Category(models.Model):
    class CategoryType(models.TextChoices):
        FUNCTION = 'function', 'Function'
        AUDIENCE = 'audience', 'Audience'
        SCENARIO = 'scenario', 'Scenario'
        FEATURE = 'language-feature', 'Language feature'
        COMPLEXITY = 'complexity', 'Complexity'

    type = models.CharField(max_length=30, choices=CategoryType.choices)
    name = models.SlugField(max_length=30)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    created_dt = models.DateTimeField(default=now, blank=True)
    updated_dt = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.type}::{self.name}"

    @staticmethod
    def cloud():
        categories = Category.objects.annotate(count=Count('onelinercategory')).filter(
            count__gte=3).order_by('type', 'name').values('type', 'name', 'display_name', 'description', 'count')
        return categories

    class Meta:
        unique_together = [['type', 'name']]
        verbose_name_plural = 'categories'


class OnelinerCategory(models.Model):
    oneliner = models.ForeignKey(OneLiner, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['oneliner', 'category']]
        verbose_name_plural = 'oneliner categories'


class CategorizationAdapter:
    def convert_category(self, category: categorization.Category) -> List[Category]:
        type_ = Category.CategoryType[category.category_type.name]
        categories = []
        for tag in category.tags:
            known_categories = Category.objects.filter(type=type_, name=tag)
            if known_categories.exists():
                category = known_categories.first()
            else:
                category = Category(
                    type=type_,
                    name=tag,
                    display_name=tag,
                )
                category.save()
            categories.append(category)

        return categories
