import socket
from django.http import JsonResponse
from django.utils import timezone


def index(request):
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})
