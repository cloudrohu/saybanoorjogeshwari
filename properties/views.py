# properties/views.py

from django.shortcuts import render, get_object_or_404
from .models import Property 
from django.core.paginator import Paginator 
from django.db.models import Q 
# from crm.models import Inquiry # If you're using this model in the index view

def index(request): # <--- Ensure this function name is 'index'
    # Sirf published properties se shuru karo
    queryset_list = Property.objects.order_by('-list_date').filter(is_published=True)

    # --- Search Implementation (from Step 12) ---
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(Q(description__icontains=keywords) | Q(title__icontains=keywords))

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
            
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)


    # --- Pagination ---
    paginator = Paginator(queryset_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'values': request.GET 
    }
    
    return render(request, 'properties/properties.html', context)


def property_detail(request, property_id):
    # ... (rest of the property_detail function)
    pass # Add your property_detail code here