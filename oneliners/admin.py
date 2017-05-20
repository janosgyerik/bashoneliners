from django.contrib import admin

from oneliners.models import HackerProfile, OneLiner, Question


class OneLinerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'was_tweeted', 'summary', 'created_dt',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'is_answered', 'summary', 'created_dt',)


class HackerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_date_joined', 'display_name', 'twitter_name',)


admin.site.register(OneLiner, OneLinerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(HackerProfile, HackerProfileAdmin)
