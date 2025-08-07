import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from places.models import Place


def show_index(request):
    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": f"place_{place.pk}",
                "detailsUrl": f"/places/{place.pk}.json"
            }
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }
    context = {"places_geojson": json.dumps(geojson, ensure_ascii=False)}
    return render(request, 'index.html', context)


def get_place_details(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
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
