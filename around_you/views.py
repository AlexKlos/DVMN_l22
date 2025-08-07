from django.http import JsonResponse
from django.shortcuts import render

from places.models import Place


def show_index(request):
    return render(request, 'index.html')


def get_place_details(request, place_id):
    place = Place.objects.get(pk=place_id)
    images = [request.build_absolute_uri(img.image.url) for img in place.images.all()]
    place_details = {
        "title": place.title,
        "imgs": images,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }
    return JsonResponse(place_details)