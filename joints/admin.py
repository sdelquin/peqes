from django.contrib import admin

from .models import Joint


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    list_display = ('target_url', 'shorten_url', 'hits')
