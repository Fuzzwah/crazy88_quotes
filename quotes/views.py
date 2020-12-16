from random import choice
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from django_tables2 import SingleTableView
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view

class SlackSingleQuoteRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            "response_type": "in_channel",
            "text": data,
            #"attachments": [{"text": data[0]['text']}]
        }
        return super(SlackSingleQuoteRenderer, self).render(data, accepted_media_type, renderer_context)

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
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class RandomQuoteView(generics.ListAPIView):
    renderer_classes = (SlackSingleQuoteRenderer, )
    permission_classes = []
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_queryset(self, *args, **kwargs):
        pks = Quote.objects.values_list('pk', flat=True).order_by('id')
        random_pk = choice(pks)

        return self.queryset.filter(id=random_pk)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def random_quote(request):

    pks = Quote.objects.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    quote = Quote.objects.all().filter(id=random_pk)
    serializer = QuoteSerializer(quote, many=True)
    data = {
        "response_type": "in_channel",
        "text": f"Quote #{serializer.data[0]['id']}",
        "attachments": [{"text": serializer.data[0]['text']}]
    }
    return JsonResponse(data)


class QuoteView(generics.ListAPIView):
    renderer_classes = (SlackSingleQuoteRenderer, )
    permission_classes = []
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.kwargs.get('id'))
