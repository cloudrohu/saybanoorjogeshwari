# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # /properties/ - Saari properties dikhayega
    path('', views.index, name='properties'), 
    
    # /properties/123 - Specific property ki details dikhayega (Primary Key se)
    path('<int:property_id>/', views.property_detail, name='property_detail'), 
]