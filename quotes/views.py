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
from django.db.models import Max
from random import choice

from quotes.serializers import (
    QuoteSerializer,
)

from quotes.models import (
    Quote,
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
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class RandomQuoteViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    pks = Quote.objects.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    serializer_class = QuoteSerializer
    quote = Quote.objects.get(pk=random_pk)

    def get_queryset(self, *args, **kwargs):
        return self.quote

class QuoteView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.kwargs.get('id'))
