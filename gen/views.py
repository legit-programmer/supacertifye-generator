from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status, response
from .supagen import *

# from.import fetch

# Legacy code

# def index(request):
#     if request.method == 'GET':
#         fetch.runner()
#         print("certificates generateed succesfully✅")
#         return HttpResponse("generated")


def index(request):
    return HttpResponse('Grinding...🔨🔨🔨')

@api_view(['POST'])
def generate(request):
    data = dict(request.data)
    arr = supagenerate(data['eventid'][0])
    uploadAllToBucket(data['eventid'][0], arr)
    return response.Response(data, status=status.HTTP_200_OK)