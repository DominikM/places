from django.shortcuts import render, redirect, reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from places.settings import GMAPS_API_KEY
from .models import Place, CheckIn
from datetime import datetime


# Create your views here.

@login_required
def index(request):
    places = serializers.serialize('json', request.user.place_set.filter(togo=False))
    togos = serializers.serialize('json', request.user.place_set.filter(togo=True))
    context = {
        'gmaps_api_key': GMAPS_API_KEY,
        'places': places,
        'togos': togos
    }
    return render(request, 'web/index.html', context)


@login_required
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
        new_place_data['user'] = request.user
        new_place = Place.objects.create(**new_place_data)
        new_checkin_data['place'] = new_place
        new_checkin = CheckIn.objects.create(**new_checkin_data)

        return JsonResponse({
            'status': 'OK',
            'message': 'Created place and CheckIn',
            'place': {'pk': new_place.id, 'fields': model_to_dict(new_place)},
            'checkin': {'pk': new_checkin.id, 'fields': model_to_dict(new_checkin)}
        })


@login_required
@require_http_methods(['POST'])
def post_create_togo(request):
    new_togo_data = {}
    error = ''

    if request.POST.get('name'):
        new_togo_data['name'] = request.POST['name']
    else:
        error += 'Need a name for the place. '

    if request.POST.get('address'):
        new_togo_data['address'] = request.POST['address']
    else:
        error += 'Need an address for the place. '

    if request.POST.get('lat'):
        new_togo_data['lat'] = float(request.POST['lat'])
    else:
        error += 'Need a latitude for the place. '

    if request.POST.get('lng'):
        new_togo_data['lng'] = float(request.POST['lng'])
    else:
        error += 'Need a longitude for the place. '

    if request.POST.get('notes'):
        new_togo_data['notes'] = request.POST['notes']
    else:
        new_togo_data['notes'] = ''


    if error:
        return JsonResponse({
            'status': 'FAIL',
            'message': error
        })

    else:
        new_togo_data['togo'] = True
        new_togo_data['user'] = request.user
        new_togo = Place.objects.create(**new_togo_data)

        return JsonResponse({
            'status': 'OK',
            'message': 'Created place and CheckIn',
            'place': {'pk': new_togo.id, 'fields': model_to_dict(new_togo)}
        })


@login_required
@require_http_methods(['POST'])
def post_delete_togo(request):
    if request.POST.get('id'):
        to_delete = int(request.POST['id'])
    else:
        return JsonResponse({
            'status': 'FAIL',
            'message': 'Must provide an id to delete. '
        })

    try:
        Place.objects.get(id=to_delete).delete()
    except Place.DoesNotExist:
        return JsonResponse({
            'status': 'FAIL',
            'message': 'ID provided does not exist.'
        })

    return JsonResponse({
        'status': 'OK',
        'message': 'Deleted ToGo'
    })



