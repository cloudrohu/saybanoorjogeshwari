from django.contrib import admin
from .models import AdditionalInfoResponse, ConfigurationResponse,BrochureLead
# Register your models here.


@admin.register(AdditionalInfoResponse)
class AdditionalInfoResponseAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "name",
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
class ConfigurationResponseAdmin(admin.ModelAdmin):
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
class BrochureLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "mobile", "project", "created_at")
    search_fields = ("name", "email", "mobile")