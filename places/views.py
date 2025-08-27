from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place


def show_index(request):
    features = []
    for place in Place.objects.all():
        details_url = reverse('place_details', args=[place.pk])
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': f'place_{place.pk}',
                'detailsUrl': details_url
            }
        })
    geojson = {
        'type': 'FeatureCollection',
        'features': features,
    }
    context = {'places_geojson': geojson}
    return render(request, 'index.html', context)


def get_place_details(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related(Prefetch('images')), pk=place_id)
    images = [request.build_absolute_uri(img.image.url) for img in place.images.all()]
    place_details = {
        'title': place.title,
        'imgs': images,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }
    return JsonResponse(place_details)
