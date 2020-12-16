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
    quote_id = False
    payload_list = str(request.body).split('&')
    for item in payload_list:
        key, val = item.split('=')
        if key == 'text':
            quote_id = val
            break
    if not quote_id:
        data = {
            "response_type": "in_channel",
            "text": f"You need to provide a quote number!",
        }
        return JsonResponse(data)


    quote = Quote.objects.all().filter(id=quote_id)
    serializer = QuoteSerializer(quote, many=True)
    try:
        data = {
            "response_type": "in_channel",
            "text": f"Quote #{serializer.data[0]['id']}",
            "attachments": [{"text": serializer.data[0]['text']}]
        }
    except IndexError:
        data = {
            "response_type": "in_channel",
            "text": f"Quote {quote_id} not found in the database",
        }
    return JsonResponse(data)

