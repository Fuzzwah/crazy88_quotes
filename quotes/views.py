from random import choice
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view
from quotes.serializers import QuoteSerializer
from quotes.models import Quote

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

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_quote(request):
    print(request.body, flush=True)
    print(request.text, flush=True)

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

