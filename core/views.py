from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.message import  send_message, login
# Create your views here.

@csrf_exempt
def event(request):

    data = json.loads(request.body)
    chat_id = data['message']['chat']['id']
    user_id = data['message']['from']['id']
    first_name = data['message']['from']['first_name']
    last_name = data['message']['from']['last_name']

    user = {
        'user_id':user_id,
        'first_name':first_name,
        'last_name':last_name,
    }


    # print(user)

    # send_message('Bem-vindo, por favor digite seu número', chat_id)
    login(user, data)


    return HttpResponse()
