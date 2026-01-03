from django.shortcuts import render

from django.http import JsonResponse
from .models import City, Locality

def city_locality_search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if len(query) >= 3:
        # Get Cities
        city_qs = City.objects.filter(name__icontains=query).values("name", "level_type")[:10]

        # Get Localities (with related city)
        locality_qs = Locality.objects.filter(name__icontains=query).select_related("city").values("name", "city__name")[:10]

        # Merge results
        for c in city_qs:
            results.append({
                "name": c["name"],
                "type": c["level_type"].title() if c["level_type"] else "City"
            })

        for l in locality_qs:
            results.append({
                "name": f"{l['name']}, {l['city__name']}",
                "type": "Locality"
            })

    return JsonResponse(results, safe=False)

