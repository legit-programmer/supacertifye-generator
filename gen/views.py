from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status, response
import threading
from .tasks import generation_process
from .generation_controllers import *
from PIL import UnidentifiedImageError
from dotenv import load_dotenv

load_dotenv()
def index(request):
    return HttpResponse('Grinding...🔨🔨🔨')

@api_view(['POST'])
def generate(request):
    data = dict(request.data)

    if data.get('token') == os.environ.get('REQUEST_TOKEN'):
        
        try:
            clearOutputDir()
            generation_process(data)
            return response.Response({'message':"Generation Complete!"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return response.Response("Please check your request format or the template url you posted.", status=status.HTTP_400_BAD_REQUEST)

    return response.Response("Forbidden", status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def generate_sheet(request):
    data = dict(request.data)
    
    if data.get('token') == os.environ.get('REQUEST_TOKEN'):

        try:
            clearOutputDir()
            generateExcelSheet(data['event_id'])
            uploadSheet(data['event_id'])
            return response.Response({'message':"Generation Complete!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return response.Response("Error occured.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response.Response("Forbidden", status.HTTP_403_FORBIDDEN)

# Legacy code

# from.import fetch

# def index(request):
#     if request.method == 'GET':
#         fetch.runner()
#         print("certificates generateed succesfully✅")
#         return HttpResponse("generated")