from django.contrib import admin
from Achievements.models import Achievements


# Register your models here.

class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'achieved_at')
    search_fields = ('title',)
    list_filter = ('achieved_at',)
    ordering = ('-achieved_at',)
    fieldsets = (
        ('Data', {
            'fields': ('user_id', 'title'),
        }),
        ('Achievement Details', {
            'fields': ('achieved_at', 'Privacy_level'),
        }),
    )


admin.site.register(Achievements, AchievementsAdmin)
