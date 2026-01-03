from django.contrib import admin
from django.utils.html import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import (
    Project, BookingOffer, WelcomeTo, WebSlider, Overview, AboutUs,
    USP, Configuration, Connectivity, Amenities, Gallery, Header,
    RERA_Info, WhyInvest, BankOffer, Enquiry, ProjectFAQ
)

NO_IMAGE_URL = "https://via.placeholder.com/80x50.png?text=No+Image"


# =======================
# INLINES
# =======================

class BookingOfferInline(admin.TabularInline):
    model = BookingOffer
    extra = 1


class WelcomeToInline(admin.StackedInline):
    model = WelcomeTo
    extra = 1


class ProjectFAQInline(admin.TabularInline):
    model = ProjectFAQ
    extra = 1
    fields = ("order", "question", "answer")


class WebSliderInline(admin.TabularInline):
    model = WebSlider
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">'
            )
        return mark_safe(f'<img src="{NO_IMAGE_URL}">')

    image_preview.short_description = "Preview"


class OverviewInline(admin.StackedInline):
    model = Overview
    extra = 1


class AboutUsInline(admin.StackedInline):
    model = AboutUs
    extra = 1


class USPInline(admin.TabularInline):
    model = USP
    extra = 1


class ConfigurationInline(admin.TabularInline):
    model = Configuration
    extra = 1
    fields = (
        'bhk_type',
        'area_sqft',
        'price_in_rupees',
        'parking',
        'balcony',
        'sold_out',
        'unit_plan',
    )


class ConnectivityInline(admin.TabularInline):
    model = Connectivity
    extra = 1


class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">'
            )
        return mark_safe(f'<img src="{NO_IMAGE_URL}">')

    image_preview.short_description = "Preview"


class HeaderInline(admin.StackedInline):
    model = Header
    extra = 1


class RERAInfoInline(admin.StackedInline):
    model = RERA_Info
    extra = 1


class WhyInvestInline(admin.StackedInline):
    model = WhyInvest
    extra = 1


class BankOfferInline(admin.TabularInline):
    model = BankOffer
    extra = 1


# =======================
# PROJECT ADMIN
# =======================

@admin.register(Project)
class ProjectAdmin(MPTTModelAdmin):

    list_display = (
        'project_name',
        'city',
        'locality',
        'developer',
        'construction_status',
        'featured_property',
        'active',
        'image_preview',
    )

    list_filter = (
        'city',
        'locality',
        'developer',
        'propert_type',
        'construction_status',
        'featured_property',
        'active',
    )

    search_fields = (
        'project_name',
        'city__name',
        'locality__name',
        'developer__title',
    )

    readonly_fields = (
        'slug',
        'image_preview',
        'youtube_preview',
        'create_at',
        'update_at',
    )

    fieldsets = (

        # =====================
        # BASIC PROJECT INFO
        # =====================
        ('Basic Project Info', {
            'fields': (
                'project_name',
                'slug',
                'parent',
                'developer',
                'propert_type',
                'city',
                'locality',
            )
        }),

        # =====================
        # CONFIGURATION & DETAILS
        # =====================
        ('Project Details', {
            'fields': (
                'construction_status',
                'bhk_type',
                'floor',
                'land_parce',
                'luxurious',
                'priceing',
            )
        }),

        # =====================
        # POSSESSION & LEGAL
        # =====================
        ('Possession & Legal', {
            'fields': (
                'possession_month',
                'possession_year',
                'Occupancy_Certificate',
                'Commencement_Certificate',
            )
        }),

        # =====================
        # FEATURES & STATUS
        # =====================
        ('Status & Flags', {
            'fields': (
                'featured_property',
                'active',
            )
        }),

        # =====================
        # MEDIA
        # =====================
        ('Images & Media', {
            'fields': (
                'image',
                'image_preview',
                'master_plan',
                'floor_plan',
                'youtube_embed_id',
                'youtube_preview',
            )
        }),

        # =====================
        # MAP
        # =====================
        ('Google Map', {
            'fields': (
                'google_map_iframe',
            )
        }),

        # =====================
        # TIMESTAMPS
        # =====================
        ('System Info', {
            'fields': (
                'create_at',
                'update_at',
            )
        }),
    )

    inlines = [
        BookingOfferInline,
        WelcomeToInline,
        WebSliderInline,
        OverviewInline,
        AboutUsInline,
        USPInline,
        ConfigurationInline,
        ConnectivityInline,
        AmenitiesInline,
        GalleryInline,
        HeaderInline,
        RERAInfoInline,
        WhyInvestInline,
        BankOfferInline,
        ProjectFAQInline,
    ]

    # =====================
    # PREVIEW METHODS
    # =====================
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="100" height="70" '
                f'style="object-fit:cover;border-radius:8px;">'
            )
        return mark_safe(f'<img src="{NO_IMAGE_URL}">')

    image_preview.short_description = "Main Image"

    def youtube_preview(self, obj):
        if obj.youtube_embed_id:
            vid = obj.youtube_embed_id.strip()
            thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            return mark_safe(
                f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank">'
                f'<img src="{thumb}" width="140" height="90" style="border-radius:8px;">'
                f'</a>'
            )
        return "No Video"

    youtube_preview.short_description = "YouTube Video"

# =======================
# ENQUIRY ADMIN
# =======================

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'email',
        'project',
        'contacted_on',
    )
    list_filter = ('project', 'contacted_on')
    search_fields = (
        'name',
        'phone',
        'email',
        'project__project_name',
    )
    ordering = ('-contacted_on',)
