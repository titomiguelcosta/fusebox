import os
from functools import wraps
from django.http import JsonResponse, HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User


def query_auth(view):
    @wraps(view)
    def inner(request: HttpRequest, *args, **kwargs):
        if os.getenv("AUTH_TOKEN", False) != request.GET.get("token", ""):
            return JsonResponse({"error": "Authentication required!"}, status=401)
        else:
            return view(request, *args, **kwargs)

    return inner


def jwt_auth(view):
    @wraps(view)
    def inner(request: HttpRequest, *args, **kwargs):
        try:
            get_user_from_jwt_token(request)
        except Exception as e:
            return JsonResponse({'error': 'not authenticated' + str(e)}, status=401)

        return view(request, *args, **kwargs)

    return inner


def get_user_from_jwt_token(request: HttpRequest) -> User:
    auth = JWTAuthentication()

    return auth.get_user(auth.get_validated_token(auth.get_raw_token(auth.get_header(request))))
