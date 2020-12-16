from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

def test(request):
    resp = {
        "response_type": "in_channel",
        "text": "Hello, world",
            "attachments": [
                {
                "text": "Attachment text is here"
                }
            ]
        }
    return JsonResponse(resp)

def index(request):
    return HttpResponse("Hi there.")
