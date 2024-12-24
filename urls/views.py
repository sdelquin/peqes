from django.shortcuts import redirect

from .models import URL


def plug(request, *args, **kwargs):
    shorten_url = request.build_absolute_uri().rstrip('/')
    target_url = URL.objects.get(shorten_url=shorten_url).target_url
    return redirect(target_url)
