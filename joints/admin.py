from django.contrib import admin

from .models import Joint


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    search_fields = ('target_url', 'shorten_url')
    list_display = ('target_url', 'shorten_url', 'hits', 'expires_at')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
