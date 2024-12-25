from django.shortcuts import redirect

from .models import Joint


def plugin(request, *args, **kwargs):
    shorten_url = request.build_absolute_uri().rstrip('/')
    joint = Joint.objects.get(shorten_url=shorten_url)
    joint.hits += 1
    joint.save()
    return redirect(joint.target_url)
