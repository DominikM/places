from django.shortcuts import render
from django.core import serializers
from places.settings import GMAPS_API_KEY
from .models import Place, CheckIn


# Create your views here.

def index(request):
    places = serializers.serialize('json', Place.objects.all())
    context = {
        'gmaps_api_key': GMAPS_API_KEY,
        'places': places
    }
    return render(request, 'web/index.html', context)