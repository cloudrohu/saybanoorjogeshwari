from django.contrib import admin
from .models import AdditionalInfoResponse, ConfigurationResponse,BrochureLead,MetaLead
# Register your models here.
from import_export.admin import ImportExportModelAdmin



@admin.register(AdditionalInfoResponse)
class AdditionalInfoResponseAdmin(ImportExportModelAdmin):
    list_display = (
        "type",
        "name",
        "email",
        "phone",
        "visit_date",
        "created_at",
    )

    list_filter = (
        "type",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
    )

    ordering = ("-created_at",)

@admin.register(ConfigurationResponse)
class ConfigurationResponseAdmin(ImportExportModelAdmin):
    list_display = (
        "configuration",
        "name",
        "email",
        "phone",
        "created_at",
    )

    list_filter = ("configuration", "created_at")
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)


@admin.register(BrochureLead)
class BrochureLeadAdmin(ImportExportModelAdmin):
    list_display = ("name", "email", "mobile", "project", "created_at")
    search_fields = ("name", "email", "mobile")

@admin.register(MetaLead)
class MetaLeadAdmin(ImportExportModelAdmin):
    list_display = ("full_name", "phone_number", "email", "configuration", "budget", "visit_plan", "created_at")
    search_fields = ("full_name", "phone_number", "email", "leadgen_id")
    list_filter = ("configuration", "visit_plan", "created_at")    