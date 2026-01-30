import json
import requests
from django.shortcuts import redirect, render
from .forms import AdditionalInfoForm, ConfigurationResponseForm
from django.http import JsonResponse
from .models import BrochureLead, MetaLead
from projects.models import Project
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    

def fetch_lead_details_from_meta(leadgen_id: str) -> dict:
    """
    Meta Graph API call: leadgen_id -> lead details (field_data)
    """
    url = f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/{leadgen_id}"
    params = {
        "access_token": settings.META_PAGE_ACCESS_TOKEN,
        "fields": "id,created_time,field_data,form_id,page_id",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def extract_fields(field_data: list) -> dict:
    """
    Convert Meta field_data list to dict
    """
    out = {}
    for item in field_data or []:
        name = item.get("name")
        values = item.get("values") or []
        out[name] = values[0] if values else None
    return out


@csrf_exempt
def meta_lead_webhook(request):
    """
    GET: Verification
    POST: Leadgen event => fetch lead details => save to DB
    """

    # ✅ 1) Verification
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == settings.META_WEBHOOK_VERIFY_TOKEN:
            return HttpResponse(challenge)

        return HttpResponse("Invalid verify token", status=403)

    # ✅ 2) Lead event
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponse("Invalid JSON", status=400)

        # ✅ safety: webhook can send multiple entries/changes
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                leadgen_id = value.get("leadgen_id")

                if not leadgen_id:
                    continue

                try:
                    # ✅ avoid duplicates
                    lead_obj, created = MetaLead.objects.get_or_create(
                        leadgen_id=leadgen_id,
                        defaults={"raw_payload": payload},
                    )

                    # ✅ fetch + update if needed
                    if created or not lead_obj.phone_number:
                        lead_data = fetch_lead_details_from_meta(leadgen_id)
                        fields = extract_fields(lead_data.get("field_data", []))

                        lead_obj.form_id = lead_data.get("form_id")
                        lead_obj.page_id = lead_data.get("page_id")
                        lead_obj.full_name = fields.get("full_name") or fields.get("name")
                        lead_obj.phone_number = fields.get("phone_number")
                        lead_obj.email = fields.get("email")

                        # ✅ Custom Qs (your form fields names)
                        lead_obj.configuration = (
                            fields.get("which_configuration_are_you_looking_for")
                            or fields.get("configuration")
                        )
                        lead_obj.budget = (
                            fields.get("your_budget_range")
                            or fields.get("budget")
                        )
                        lead_obj.visit_plan = (
                            fields.get("when_are_you_planning_to_visit")
                            or fields.get("visit_plan")
                        )
                        lead_obj.profession = (
                            fields.get("your_profession")
                            or fields.get("profession")
                        )

                        lead_obj.raw_payload = lead_data
                        lead_obj.save()

                except Exception as e:
                    # ✅ very important: always return 200 to stop FB retries
                    print("❌ Meta Webhook Error:", str(e))
                    continue

        # ✅ MUST return this exact text
        return HttpResponse("EVENT_RECEIVED", status=200)

    return HttpResponse("Method not allowed", status=405)