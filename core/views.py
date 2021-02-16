from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.message import create_user, send_message
# Create your views here.

@csrf_exempt
def event(request):

    data = json.loads(request.body)
    chat_id = data['message']['chat']['id']
    send_message('Bem-vindo, por favor digite seu número', chat_id)
    create_user(data)

    return HttpResponse()
