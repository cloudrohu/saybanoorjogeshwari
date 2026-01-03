from django.urls import path
from . import views

urlpatterns = [
    path("api/cities/", views.city_locality_search, name="city_locality_search"),
]
