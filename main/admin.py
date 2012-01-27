from django.contrib import admin

from bashoneliners.main.models import HackerProfile, OneLiner, WishListQuestion, WishListAnswer

class OneLinerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'was_tweeted', 'summary', )

class WishListQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'is_answered', 'summary', )


admin.site.register(HackerProfile)
admin.site.register(OneLiner, OneLinerAdmin)
admin.site.register(WishListQuestion, WishListQuestionAdmin)

# eof
