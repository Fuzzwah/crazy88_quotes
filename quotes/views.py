from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_tables2 import SingleTableView
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from quotes.serializers import (
    QuotesSerializer,
)

from quotes.models import (
    Quotes,
)

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

class QuotesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Quotes.objects.all()
    serializer_class = QuotesSerializer
