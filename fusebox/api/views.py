from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


def index(request):
    return JsonResponse({"status": "ok"})
