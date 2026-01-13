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
    Convert Meta field_data to dict
    field_data example: [{"name":"full_name","values":["abc"]}, ...]
    """
    out = {}
    for item in field_data or []:
        key = item.get("name")
        values = item.get("values") or []
        out[key] = values[0] if values else None
    return out


@csrf_exempt
def meta_lead_webhook(request):

    # ✅ 1) Verification (GET)
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        # ✅ Your verify token (same as Meta dashboard)
        VERIFY_TOKEN = settings.SAYBANOOR_WEBHOOK_TOKEN_2026

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Invalid verify token", status=403)

    # ✅ 2) Lead Event (POST)
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponse("Invalid JSON", status=400)

        # Meta sends entries
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                leadgen_id = value.get("leadgen_id")

                if leadgen_id:
                    lead_details = fetch_lead_details_from_meta(leadgen_id)
                    fields = extract_fields(lead_details.get("field_data", []))

                    # ✅ Here you will save fields into DB
                    print("✅ New lead received:", fields)

        return HttpResponse("EVENT_RECEIVED", status=200)

    return HttpResponse("Method not allowed", status=405)   
    """
    1) GET: Webhook verification
    2) POST: Leadgen event => fetch full lead data => save to DB
    """

    # ✅ Verification
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == settings.META_VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Invalid verify token", status=403)

    # ✅ Lead event
    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))

        try:
            entry = payload.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})
            leadgen_id = value.get("leadgen_id")

            if not leadgen_id:
                return JsonResponse({"status": "no leadgen_id"}, status=200)

            # already saved?
            lead_obj, created = MetaLead.objects.get_or_create(
                leadgen_id=leadgen_id,
                defaults={"raw_payload": payload}
            )

            # Fetch + update (only if newly created or missing fields)
            if created or not lead_obj.phone_number:
                lead_data = fetch_lead_details_from_meta(leadgen_id)
                fields = extract_fields(lead_data.get("field_data", []))

                # Map Meta fields (Meta forms mostly: full_name, phone_number, email)
                lead_obj.form_id = lead_data.get("form_id")
                lead_obj.page_id = lead_data.get("page_id")

                lead_obj.full_name = fields.get("full_name") or fields.get("first_name")
                lead_obj.phone_number = fields.get("phone_number")
                lead_obj.email = fields.get("email")

                # Your custom questions
                lead_obj.configuration = fields.get("which_configuration_are_you_looking_for") or fields.get("configuration")
                lead_obj.budget = fields.get("your_budget_range") or fields.get("budget")
                lead_obj.visit_plan = fields.get("when_are_you_planning_to_visit") or fields.get("visit_plan")
                lead_obj.profession = fields.get("your_profession") or fields.get("profession")

                lead_obj.raw_payload = lead_data
                lead_obj.save()

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=200)

    return JsonResponse({"error": "method not allowed"}, status=405)   