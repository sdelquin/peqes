from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from .models import Joint


@admin.display(description='Test')
def test_url(obj):
    return mark_safe(f'<a target="blank" href="{obj.shorten_url}">🔗</a>')


@admin.display(description='Target URL')
def target_url_truncate(obj, max_length=200):
    return truncatechars(obj.target_url, max_length)


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    search_fields = ('target_url', 'shorten_url', 'description')
    list_display = ('shorten_path', 'description', target_url_truncate, test_url, 'custom')
    list_filter = ('tags', 'expires_at', 'custom')
    filter_horizontal = ('tags',)
