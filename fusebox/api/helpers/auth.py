import os
from functools import wraps
from django.http import JsonResponse, HttpRequest


def protected(view):
    @wraps(view)
    def inner(request: HttpRequest, *args, **kwargs):
        if os.getenv("AUTH_TOKEN", False) != request.GET.get("token", ""):
            return JsonResponse({"error": "Authentication required!"}, status=403)
        else:
            return view(request, *args, **kwargs)

    return inner
