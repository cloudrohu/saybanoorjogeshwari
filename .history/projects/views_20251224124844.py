# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
from .models import Project
from home.models import Setting
from properties.models import Property # Needed for project_details if included
# Import related models for dropdowns
from utility.models import City, Locality , PropertyType# Locality and City imported
# Import related models for dropdowns
from .models import (
    Project, Configuration, Gallery, RERA_Info, BookingOffer, Overview,
    USP, Amenities, Header, WelcomeTo, Connectivity, WhyInvest,Enquiry,ProjectFAQ
) 
from django.contrib import messages

from django.db.models import Min, Max



# --- 1. All Projects Listing Page (Optimized Index) ---
def index(request):
    # Start with all active projects
    queryset_list = Project.objects.filter(active=True).order_by('project_name')

    # --- Filtering Logic ---
    
    # 1. City Filter (Standard Foreign Key)
    if 'city_id' in request.GET and request.GET['city_id']:
        city_id = request.GET['city_id']
        queryset_list = queryset_list.filter(city_id=city_id)

    # 2. Locality Filter (MPTT Descendants Implementation)
    if 'locality_id' in request.GET and request.GET['locality_id']:
        locality_id = request.GET['locality_id']
        try:
            # Get the selected Locality node (e.g., Phase 1)
            selected_locality = Locality.objects.get(pk=locality_id)
            
            # Fetch all descendants (sub-localities) including the node itself
            descendant_localities = selected_locality.get_descendants(include_self=True)
            
            # Filter projects whose locality FK is within the fetched MPTT tree
            queryset_list = queryset_list.filter(locality__in=descendant_localities)
            
        except Locality.DoesNotExist:
            pass # Ignore if invalid ID is passed


    # 3. Status Filter
    if 'status' in request.GET and request.GET['status']:
        status = request.GET['status']
        queryset_list = queryset_list.filter(construction_status__iexact=status)

    # 4. Keyword Search (Project Name or Developer Name)
    if 'keywords' in request.GET and request.GET['keywords']:
        keywords = request.GET['keywords']
        queryset_list = queryset_list.filter(
            Q(project_name__icontains=keywords) | 
            Q(developer__name__icontains=keywords)
        )
        
    # --- Context ---
    
    available_cities = City.objects.all().order_by('name')
    # Fetch all *top-level* Localities for the main dropdown (or all of them if preferred)
    available_localities = Locality.objects.filter(parent__isnull=True).order_by('name')
    construction_statuses = Project.Construction_Status
    
    context = {
        'projects': queryset_list,
        'available_cities': available_cities,
        'available_localities': available_localities,
        'construction_statuses': construction_statuses,
        'values': request.GET, # Passes submitted values back to the form
    }
    
    return render(request, 'projects/projects.html', context)




from django.db.models import Q

def search_projects(request):
    settings_obj = Setting.objects.first()

    query = request.GET.get("q", "").strip()
    selected_type = request.GET.get("type", "").strip().lower()

    projects = Project.objects.filter(active=True)

    # ✅ Property type filter
    if selected_type:
        try:
            parent_type = PropertyType.objects.get(
                name__iexact=selected_type.capitalize()
            )
            all_types = parent_type.get_descendants(include_self=True)
            projects = projects.filter(propert_type__in=all_types)
        except PropertyType.DoesNotExist:
            pass

    # ✅ CITY + LOCALITY SMART SPLIT
    if query:
        parts = [p.strip() for p in query.split(",")]

        if len(parts) == 2:
            locality_part, city_part = parts
            projects = projects.filter(
                Q(locality__name__icontains=locality_part) &
                Q(city__name__icontains=city_part)
            )
        else:
            projects = projects.filter(
                Q(project_name__icontains=query) |
                Q(locality__name__icontains=query) |
                Q(city__name__icontains=query)
            )

    projects = projects.distinct()

    # ✅ Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(projects, 9)

    try:
        projects_page = paginator.page(page)
    except:
        projects_page = paginator.page(1)

    context = {
        "settings_obj": settings_obj,
        "projects": projects_page,
        "query": query,
        "property_type": selected_type,
        "paginator": paginator,
    }

    template = (
        "projects/commercial_list.html"
        if selected_type == "commercial"
        else "projects/residential_list.html"
    )

    return render(request, template, context)


def residential_projects(request):
    query = request.GET.get('q', '')

    projects = Project.objects.filter(
        propert_type__parent__name__iexact='Residential',
        active=True
    ).annotate(
        min_price=Min("configurations__price_in_rupees"),
        max_price=Max("configurations__price_in_rupees"),
    ).select_related('city', 'locality', 'propert_type')

    if query:
        projects = projects.filter(project_name__icontains=query)

    context = {
        'projects': projects,
        'page_title': 'Residential Projects',
        'breadcrumb': 'Residential',
    }

    return render(request, 'projects/residential_list.html', context)


# 🏢 Commercial Projects
def commercial_projects(request):
    query = request.GET.get('q', '')
    projects = Project.objects.filter(
        propert_type__parent__name__iexact='Commercial',
        active=True
    ).select_related('city', 'locality', 'propert_type')

    if query:
        projects = projects.filter(project_name__icontains=query)

    context = {
        'projects': projects,
        'page_title': 'Commercial Projects',
        'breadcrumb': 'Commercial',
    }
    return render(request, 'projects/commercial_list.html', context)


def project_details(request, id, slug):

    # ✅ STEP 1: FETCH PROJECT FIRST
    project = get_object_or_404(Project, id=id, slug=slug, active=True)

    # ✅ STEP 2: SETTINGS
    settings_obj = Setting.objects.first()
    rs = Setting.objects.first()

    # ✅ STEP 3: CARPET RANGE
    carpet_range = project.configurations.aggregate(
        min_area=Min("area_sqft"),
        max_area=Max("area_sqft")
    )

    # ✅ STEP 4: RELATED PROJECTS (LOCALITY FIRST)
    related_projects = Project.objects.filter(
        locality=project.locality,
        active=True
    ).exclude(id=project.id)

    # 👉 Fallback: agar same locality me aur project na mile
    if not related_projects.exists():
        related_projects = Project.objects.filter(
            city=project.city,
            active=True
        ).exclude(id=project.id)

    related_projects = related_projects[:8]

    # ✅ STEP 5: FAQ
    project_faqs = project.faqs.all().order_by("order")

    # ✅ STEP 6: FINAL CONTEXT
    context = {
        "project": project,
        "active": project,

        "settings_obj": settings_obj,
        "rs": rs,

        "min_carpet": carpet_range["min_area"],
        "max_carpet": carpet_range["max_area"],

        "welcome": project.welcomes.all(),
        "usps": project.usps.all(),
        "configurations": project.configurations.all().order_by("bhk_type"),
        "gallery": project.gallery.all(),
        "amenities": project.amenities.all(),
        "rera": project.rera.all(),
        "BookingOffer": project.BookingOffer.all(),
        "headers": project.headers.all(),
        "configs": project.configs.all(),
        "why_invest": project.why_invest.all(),

        # ✅ RELATED + FAQ
        "project_faqs": project_faqs,
        "related_projects": related_projects,

        # OPTIONAL
        "properties": Property.objects.filter(project=project),
    }

    return render(request, "projects/project_detail.html", context)

def submit_enquiry(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save enquiry
        Enquiry.objects.create(
            project=project,
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        messages.success(request, "Thank you! Your enquiry has been submitted successfully.")
        return redirect('thank_you')  # or use project detail slug redirect

    return redirect('project_details', id=project.id, slug=project.slug)



def thank_you(request):
    return render(request, 'projects/thank_you.html')