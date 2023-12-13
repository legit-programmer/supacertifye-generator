from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status, response
from .supagen import *
from PIL import UnidentifiedImageError
from dotenv import load_dotenv

# from.import fetch

# Legacy code

# def index(request):
#     if request.method == 'GET':
#         fetch.runner()
#         print("certificates generateed succesfully✅")
#         return HttpResponse("generated")

load_dotenv()
def index(request):
    return HttpResponse('Grinding...🔨🔨🔨')

@api_view(['POST'])
def generate(request):
    data = dict(request.data)

    if data.get('token') == os.environ.get('REQUEST_TOKEN'):
        cords = {'name': data['name_cords'],
                 'class': data['class_cords'],
                 'eventname': data['eventname_cords'],
                 'date': data['date_cords'],
                 'position': data['postion_cords'],
                 }
        template_url = data['template_url']
        fontSize = data['fontSize']
        test = data['test']
        try:
            if not test:
                arr = supagenerate(
                    data['event_id'], cords, template_url, fontSize)
                zipAndUpload(data['event_id'], arr)
                # uploadAllToBucket(data['event_id'], arr)
            else:
                getTemplate(data['event_id'], template_url)
                img_bytes = generator(
                    'This is a test', 'TYIF', data['event_id'], 'Testing Certificate', '2005-04-18', 'Winner', cords, fontSize)

                supabase.storage.from_('certificates').upload(path=f'{data["event_id"]}.png', file=img_bytes, file_options={
                    'x-upsert': "true", 'content-type': 'image/png'})
                os.remove(f'{data["event_id"]}.png') # deleting template after generat
                
        except Exception as e:
            print(e)
            return response.Response("Please check your request format or the template url you posted.", status=status.HTTP_400_BAD_REQUEST)

        return response.Response(data, status=status.HTTP_200_OK)
    return response.Response("Forbidden", status.HTTP_403_FORBIDDEN)
