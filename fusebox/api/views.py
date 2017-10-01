import json
import os
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from slackclient import SlackClient

def index(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request):
    return HttpResponse("Nothing. No song.")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def challenge(request):
    data = json.loads(request.body)
    print(data)

    # if "event" in data and "bot_id" not in data["event"]:
    #     sc = SlackClient(os.environ["SLACK_API_TOKEN"])
    #     if "channel" in data["event"]:
    #         sc.api_call(
    #             "chat.postMessage",
    #             channel=data["event"]["channel"],
    #             text="Hello from Python! :tada:"
    #         )

    return HttpResponse('adsasdasdas')
