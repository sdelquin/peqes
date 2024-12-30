from django.shortcuts import get_object_or_404, redirect

from .models import Joint


def plugin(request, *args, **kwargs):
    shorten_url = request.build_absolute_uri().rstrip('/')
    joint = get_object_or_404(Joint, shorten_url=shorten_url)
    joint.hits += 1
    joint.save()
    return redirect(joint.target_url)
