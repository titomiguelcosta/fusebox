import socket
from django.http import JsonResponse, HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from api.helpers.auth import protected


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@protected
@csrf_exempt
@require_http_methods(["POST"])
def proxy(request: HttpRequest) -> JsonResponse:
    valid_commands = ["ratesong", "lastsongs", "subscribe", "unsubscribe", "help"]
    command = request.POST.get("text", "help") if request.POST.get("text", "help") in valid_commands else "help"

    handler = import_string("api.handlers.slack.%s" % command)

    return handler(request)
