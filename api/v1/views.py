import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from joints.models import Joint


@csrf_exempt
@require_http_methods(['POST'])
def shorten_url(request):
    try:
        data = json.loads(request.body)
        target_url = data['target_url']
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON format.', status=400)
    except KeyError:
        return HttpResponse('Target URL is required.', status=400)
    joint = Joint.add_joint(target_url)
    response = {
        'shorten_url': joint.shorten_url,
        'target_url': joint.target_url,
        'hits': joint.hits,
        'created_at': joint.created_at.isoformat(),
        'updated_at': joint.updated_at.isoformat(),
        'expires_at': joint.expires_at.isoformat() if joint.expires_at else None,
    }
    return JsonResponse(response)
