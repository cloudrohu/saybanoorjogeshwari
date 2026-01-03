from django.contrib import admin
from django.utils.html import mark_safe
from .models import CustomUser, Developer

# ✅ Placeholder image for missing logos
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"


# --------------------------------------------
# 1️⃣  CustomUser Admin
# --------------------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'email', 'password', 'user_type')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


# --------------------------------------------
# 2️⃣  Developer Admin
# --------------------------------------------
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'city',
        'locality',
        'featured_builder',
        'created_date',
        'updated_date',
        'logo_preview',
    )
    list_filter = ('city', 'featured_builder', 'create_at', 'update_at')
    search_fields = ('title', 'city__name', 'locality__name', 'keywords', 'contact_person')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('create_at', 'update_at', 'logo_preview')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'city', 'locality', 'featured_builder')
        }),
        ('Contact Details', {
            'fields': ('contact_person', 'contact_no', 'email', 'web_site', 'google_map', 'address')
        }),
        ('SEO & Content', {
            'fields': ('keywords', 'about_developer')
        }),
        ('Media', {
            'fields': ('logo', 'logo_preview')
        }),
        ('Timestamps', {
            'fields': ('create_at', 'update_at')
        }),
    )

    def logo_preview(self, obj):
        """
        Show developer logo or a default 'no image' placeholder.
        """
        if obj.logo and hasattr(obj.logo, 'url'):
            image_url = obj.logo.url
        else:
            image_url = NO_IMAGE_URL
        return mark_safe(
            f'<img src="{image_url}" width="80" height="80" '
            f'style="object-fit:contain; border:1px solid #ddd; border-radius:6px;" />'
        )
    logo_preview.short_description = "Logo Preview"

    def created_date(self, obj):
        return obj.create_at.strftime('%d %b %Y')
    created_date.short_description = "Created"

    def updated_date(self, obj):
        return obj.update_at.strftime('%d %b %Y')
    updated_date.short_description = "Updated"
