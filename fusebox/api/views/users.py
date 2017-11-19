import os
from django.http import JsonResponse
from api.models import UserProfile, User
from slackclient import SlackClient


def populate(request):
    sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    response = sc.api_call("users.list")
    data = []

    for slack_user in response["members"]:
        if "profile" in slack_user \
                and "email" in slack_user["profile"] \
                and slack_user["profile"]["email"].endswith("pixelfusion.co.nz"):
            try:
                user_profile = UserProfile.objects.get(slack_username=slack_user["id"])
                user = user_profile.user
            except UserProfile.DoesNotExist:
                user_profile = UserProfile()
                user = User()

            user.username = slack_user["id"]
            user.email = slack_user["profile"]["email"]
            user.first_name = slack_user["profile"]["real_name"]
            user.set_password("Q12w3esw1ddn")
            user.is_active = not slack_user["deleted"]
            user.is_superuser = slack_user["is_admin"] if "is_admin" in slack_user else False
            user.save()

            user_profile.slack_username = slack_user["id"]
            user_profile.user = user
            user_profile.save()

            data.append("User %s synced." % slack_user["profile"]["real_name"])

    return JsonResponse(data, safe=False)