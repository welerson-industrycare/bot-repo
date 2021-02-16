from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.message import  proccess
# Create your views here.

@csrf_exempt
def event(request):
    data = json.loads(request.body)
    proccess(data)
    return HttpResponse()
