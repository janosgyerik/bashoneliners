from django.contrib import admin

from bashoneliners.main.models import HackerProfile, OneLiner

class OneLinerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'was_tweeted', 'summary', )


admin.site.register(HackerProfile)
admin.site.register(OneLiner, OneLinerAdmin)

# eof
