from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Joint


def test_url(obj):
    return mark_safe(f'<a target="blank" href="{obj.shorten_url}">test</a>')


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    search_fields = ('target_url', 'shorten_url', 'description')
    list_display = ('shorten_path', 'description', 'target_url', test_url)
    list_filter = ('tags', 'expires_at')
    filter_horizontal = ('tags',)
