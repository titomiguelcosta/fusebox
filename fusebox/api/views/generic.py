import socket
from django.http import JsonResponse, HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@csrf_exempt
@require_http_methods(["POST"])
def proxy(request: HttpRequest) -> JsonResponse:
    return JsonResponse(request.POST.items(), safe=False)
