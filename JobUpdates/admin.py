from django.contrib import admin
from JobUpdates.models import JobUpdates


# Register your models here.
class JobUpdatesAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at')
    search_fields = ('title',)
    list_filter = ('posted_at',)


admin.site.register(JobUpdates, JobUpdatesAdmin)
