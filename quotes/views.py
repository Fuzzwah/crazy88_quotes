from random import choice
from urllib.parse import unquote
import json
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework import status
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
            "text": f"Quote #{quote_id} not found in the database",
        }
    return JsonResponse(data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def search_quote(request):
    quote_id = False
    payload_list = str(request.body).split('&')
    for item in payload_list:
        key, val = item.split('=')
        if key == 'text':
            search_string = val
            break
    if not search_string:
        data = {
            "response_type": "in_channel",
            "text": f"You need to provide a string to search for!",
        }
        return JsonResponse(data)


    quotes = Quote.objects.all().filter(text__contains=search_string)
    serializer = QuoteSerializer(quotes, many=True)
    try:
        i = choice(range(len(serializer.data)))
        data = {
            "response_type": "in_channel",
            "text": f"Quote #{serializer.data[i]['id']}",
            "attachments": [{"text": serializer.data[i]['text']}]
        }
    except IndexError:
        data = {
            "response_type": "in_channel",
            "text": f"No quote found containing '{search_string}' in the database",
        }
    return JsonResponse(data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_quote(request):
    body = str(request.body)
    if body.find('&') == -1:
        payload = json.loads(unquote(body)[10:-1])
        print(payload)
        try:
            added_by_userid = payload['user']['id']
            added_by_username = payload['user']['name']
            teamid = payload['user']['team_id']
            quote = payload['message']['text'].replace('+', ' ')
        except KeyError:
            data = {
                "response_type": "in_channel",
                "text": f"You need to provide a quote to add!",
            }
            return JsonResponse(data)
    else:
        payload = dict(item.split("=") for item in body.split('&'))
        try:
            added_by_userid = payload['user_id']
            added_by_username = payload['user_name']
            teamid = payload['team_id']
            quote = payload['text']
        except KeyError:
            data = {
                "response_type": "in_channel",
                "text": f"You need to provide a quote to add!",
            }
            return JsonResponse(data)

    q = Quote(added_by_userid=added_by_userid, added_by_username=added_by_username, teamid=teamid, text=quote, channel="#slack")
    q.save()

    data = {
        "response_type": "in_channel",
        "text": f"Quote added as #{q.id}",
    }
    return JsonResponse(data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_quote_shortcut(request):
    payload = json.loads(unquote(str(request.body))[10:-1])
    print(payload)
    added_by_userid = payload['user']['id']
    added_by_username = payload['user']['name']
    teamid = payload['user']['team_id']
    quote = payload['message']['text'].replace('+', ' ')
    q = Quote(added_by_userid=added_by_userid, added_by_username=added_by_username, teamid=teamid, text=quote, channel="#slack")
    q.save()

    return HttpResponse("Quote added", status=status.HTTP_200_OK)
