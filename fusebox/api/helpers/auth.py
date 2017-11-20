import os
from functools import wraps
from django.http import JsonResponse, HttpRequest


def protected(view):
    @wraps(view)
    def inner(request: HttpRequest, *args, **kwargs):
        if os.getenv("AUTH_TOKEN", False) != request.GET.get("token", ""):
            response = JsonResponse({"error": "Authentication required!"})
            response.status_code = 403

            return response
        else:
            return view(request, *args, **kwargs)
    return inner
