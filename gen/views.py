from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status, response
from .supagen import *
from PIL import UnidentifiedImageError

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
    
    cords = {'name':data['name_cords'],
             'class':data['class_cords'],
             'eventname':data['eventname_cords'],
             'date':data['date_cords'],
             'position':data['postion_cords'],
             }
    template_url = data['template_url']    
    try:
        arr = supagenerate(data['event_id'], cords, template_url)
        uploadAllToBucket(data['event_id'], arr)

    except Exception:
        return response.Response("Please check your request format or the template url you posted.", status=status.HTTP_400_BAD_REQUEST)

    return response.Response(data, status=status.HTTP_200_OK)