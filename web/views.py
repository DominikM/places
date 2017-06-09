from django.shortcuts import render
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from places.settings import GMAPS_API_KEY
from .models import Place, CheckIn
from datetime import datetime


# Create your views here.

def index(request):
    places = serializers.serialize('json', Place.objects.all())
    context = {
        'gmaps_api_key': GMAPS_API_KEY,
        'places': places
    }
    return render(request, 'web/index.html', context)


@require_http_methods(['POST'])
def post_create_place(request):
    new_place_data = {}
    new_checkin_data = {}
    error = ''

    if request.POST.get('name'):
        new_place_data['name'] = request.POST['name']
    else:
        error += 'Need a name for the place. '

    if request.POST.get('address'):
        new_place_data['address'] = request.POST['address']
    else:
        error += 'Need an address for the place. '

    if request.POST.get('lat'):
        new_place_data['lat'] = float(request.POST['lat'])
    else:
        error += 'Need a latitude for the place. '

    if request.POST.get('lng'):
        new_place_data['lng'] = float(request.POST['lng'])
    else:
        error += 'Need a longitude for the place. '

    if request.POST.get('notes'):
        new_place_data['notes'] = request.POST['notes']
    else:
        new_place_data['notes'] = ''

    if request.POST.get('place_id'):
        new_place_data['place_id'] = request.POST['place_id']

    if request.POST.get('date'):
        new_checkin_data['date'] = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    else:
        error += 'Need a date. '

    if request.POST.get('checkin_notes'):
        new_checkin_data['notes'] = request.POST['checkin_notes']
    else:
        new_checkin_data['notes'] = ''

    if error:
        return JsonResponse({
            'status': 'FAIL',
            'message': error
        })

    else:
        new_place = Place.objects.create(**new_place_data)
        new_checkin_data['place'] = new_place
        new_checkin = CheckIn.objects.create(**new_checkin_data)

        return JsonResponse({
            'status': 'OK',
            'message': 'Created place and CheckIn',
            'place': {'fields': model_to_dict(new_place)},
            'checkin': {'fields': model_to_dict(new_checkin)}
        })



