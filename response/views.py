from django.shortcuts import redirect, render
from .forms import AdditionalInfoForm, ConfigurationResponseForm
from django.http import JsonResponse
from .models import BrochureLead
from projects.models import Project

    
# Create your views here.

def submit_additional_info(request):
    if request.method == "POST":
        form = AdditionalInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thank_you")

    return redirect("/")

def thank_you(request):
    return render(request, "response/thank_you.html")

def error_page(request):
    return render(request, "response/error_page.html")


def submit_configuration(request):
    if request.method == "POST":
        form = ConfigurationResponseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thank_you")
        else:
            # Error print karein console mein
            print("Form Errors:", form.errors) 
            
    return redirect("error_page")  # Replace with your error page URL or view name


def brochure_lead(request):
    if request.method == "POST":
        BrochureLead.objects.create(
            project_id=request.POST.get("project_id"),
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile")
        )
        return JsonResponse({"status": "success"})