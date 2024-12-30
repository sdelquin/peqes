from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Joint


def shorten_url(obj):
    return mark_safe(f'<a target="blank" href="{obj.shorten_url}">{obj.shorten_url}</a>')


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    search_fields = ('target_url', 'shorten_url')
    list_display = ('target_url', shorten_url, 'hits', 'expires_at')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
