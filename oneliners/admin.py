from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from social_django.models import UserSocialAuth

from oneliners import models as site_models


admin.site.unregister(User)


class OnelinerCommandInline(admin.StackedInline):
    model = site_models.OnelinerCommand


class UserSocialAuthInline(admin.StackedInline):
    model = UserSocialAuth
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'oneliners', 'is_staff', 'last_login', 'oneliner_count')
    list_display_links = ('username',)
    inlines = (UserSocialAuthInline,)
    ordering = ('-last_login',)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('oneliner'))
        return qs

    def oneliner_count(self, obj):
        return obj.oneliner__count

    def oneliners(self, obj):
        url = reverse("profile_oneliners_of", args=(obj.pk,))
        label = f"oneliners ({obj.oneliner__count})"
        return format_html(f'<a href="{url}">{label}</a>')

    oneliner_count.admin_order_field = 'oneliner__count'


@admin.register(site_models.OneLiner)
class OneLinerAdmin(admin.ModelAdmin):
    inlines = [OnelinerCommandInline]
    list_display = ('user', 'is_published', 'was_tweeted', 'unpublished', 'summary', 'updated_dt')
    list_display_links = ('summary',)
    list_filter = ('was_tweeted', 'is_published', 'unpublished')
    ordering = ('-updated_dt',)


@admin.register(site_models.OneLinerSnapshot)
class OneLinerSnapshotAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'was_tweeted', 'unpublished', 'summary', 'created_dt')
    list_display_links = ('summary',)
    list_filter = ('was_tweeted', 'is_published', 'unpublished')
    ordering = ('-created_dt',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(site_models.HackerProfile)
class HackerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_date_joined', 'display_name', 'twitter_name',)


@admin.register(site_models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'oneliner', 'vote', 'created_dt')
    list_filter = ('value', )

    def vote(self, obj):
        return 'Up' if obj.value > 0 else 'Down'


class OnelinerCategoryInline(admin.StackedInline):
    model = site_models.OnelinerCategory


@admin.register(site_models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'onelinercategory_count', 'created_dt')
    inlines = [OnelinerCategoryInline]
    ordering = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(models.Count('onelinercategory'))
        return qs

    def onelinercategory_count(self, obj):
        return obj.onelinercategory__count


@admin.register(site_models.Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'onelinercommand_count', 'created_dt')
    inlines = [OnelinerCommandInline]
    ordering = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(models.Count('onelinercommand'))
        return qs

    def onelinercommand_count(self, obj):
        return obj.onelinercommand__count
