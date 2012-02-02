from django.contrib import admin

from bashoneliners.main.models import HackerProfile, OneLiner, WishListQuestion, WishListAnswer

class OneLinerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'was_tweeted', 'summary', 'created_dt',)

class WishListQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'is_answered', 'summary', 'created_dt',)

class HackerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_date_joined', 'display_name', 'twitter_name',)


admin.site.register(OneLiner, OneLinerAdmin)
admin.site.register(WishListQuestion, WishListQuestionAdmin)
admin.site.register(HackerProfile, HackerProfileAdmin)

# eof
