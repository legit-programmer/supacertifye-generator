from django.shortcuts import render
from django.http import HttpResponse

from.import fetch

def index(request):
    if request.method == 'GET':
        fetch.runner()
        print("certificates generateed succesfully✅")
        return HttpResponse("generated")


