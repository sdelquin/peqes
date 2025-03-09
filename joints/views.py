from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddJointForm
from .models import Joint


def plugin(request, *args, **kwargs):
    shorten_url = request.build_absolute_uri().lower().rstrip('/')
    joint = get_object_or_404(Joint, shorten_url=shorten_url)
    joint.hits += 1
    joint.save()
    return redirect(joint.target_url)


def shorten(request):
    if (form := AddJointForm(request.POST or None)).is_valid():
        joint = form.save()
        print(form.helper.layout)
        form.fields['target_url'].widget.attrs['readonly'] = True
        return render(request, 'joints/shorten.html', {'form': form, 'joint': joint})
    return render(request, 'joints/shorten.html', {'form': form})
