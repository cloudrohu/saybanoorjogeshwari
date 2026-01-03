from django.contrib import admin
from django.utils.html import mark_safe
from mptt.admin import MPTTModelAdmin
from .models import (
    Project, BookingOffer, WelcomeTo, WebSlider, Overview, AboutUs,
    USP, Configuration, Connectivity, Amenities, Gallery, Header,
    RERA_Info, WhyInvest, BankOffer,Enquiry
)


# 🟡 Placeholder image for fallback
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

# ----------------------------- #
# 📌 INLINE ADMIN DEFINITIONS
# ----------------------------- #

class BookingOfferInline(admin.TabularInline):
    model = BookingOffer
    extra = 1


class WelcomeToInline(admin.StackedInline):
    model = WelcomeTo
    extra = 1



class WebSliderInline(admin.TabularInline):
    model = WebSlider
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
        else:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">')
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


class ConnectivityInline(admin.TabularInline):
    model = Connectivity
    extra = 1


class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
        else:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">')
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


# ----------------------------- #
# 🏡 MAIN PROJECT ADMIN
# ----------------------------- #
@admin.register(Project)
class ProjectAdmin(MPTTModelAdmin):
    list_display = (
        'project_name', 'city', 'locality', 'developer',
        'construction_status', 'possession_month', 'possession_year',
        'featured_property', 'active', 'image_preview', 'youtube_preview'
    )

    list_filter = ('city', 'developer', 'propert_type', 'construction_status', 'featured_property', 'active')
    search_fields = ('project_name', 'city__name', 'locality__name', 'developer__title')
    prepopulated_fields = {"slug": ("project_name",)}
    readonly_fields = ('create_at', 'update_at', 'image_preview','youtube_preview')

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'project_name', 'slug', 'parent', 'developer', 'city', 'locality',
                'propert_type', 'construction_status', 'bhk_type', 'floor', 'land_parce',
                'luxurious', 'priceing'
            )
        }),
        ('Possession & Status', {
            'fields': (
                'possession_month', 'possession_year',
                'Occupancy_Certificate', 'Commencement_Certificate',
                'featured_property', 'active'
            )
        }),
        ('Media & Map', {
            'fields': ('image', 'image_preview', 'youtube_embed_id', 'google_map_iframe','youtube_preview')
        }),
        ('Timestamps', {
            'fields': ('create_at', 'update_at')
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
    ]

    class MPTTMeta:
        order_insertion_by = ['project_name']

    def image_preview(self, obj):
        """Admin list image preview — Safe for .webp and missing files."""
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="50" style="object-fit:cover;border-radius:6px;">'
            )
        return mark_safe(
            f'<img src="https://via.placeholder.com/80x50.png?text=No+Image" width="80" height="50">'
        )
    image_preview.short_description = "Preview"


    def image_tag(self, obj):
        """Bigger image preview in admin (e.g. readonly_fields)"""
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" height="60">')
        return mark_safe(f'<img src="{NO_IMAGE_URL}" height="60">')
    image_tag.short_description = 'Preview'

    def youtube_preview(self, obj):
        """Show YouTube video thumbnail or fallback."""
        if obj.youtube_embed_id:
            video_id = obj.youtube_embed_id.strip()
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return mark_safe(f'''
                <a href="{video_url}" target="_blank">
                    <img src="{thumbnail_url}" width="120" height="80" style="object-fit:cover;border-radius:6px;">
                </a>
            ''')
        return "No Video"
    youtube_preview.short_description = "YouTube Preview"




@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'phone', 'email', 'project', 'message', 'contacted_on']
    list_filter = ('project', 'contacted_on')
    search_fields = ('name', 'email', 'phone', 'message', 'project__project_name')
    ordering = ('-contacted_on',)
