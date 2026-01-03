from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.html import mark_safe
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin

from .models import City, Locality, PropertyType, PossessionIn, ProjectAmenities, Bank


# 🟡 Placeholder image URL (fallback)
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

# =======================================================
# 🏙 City Admin (MPTT)
# =======================================================
@admin.register(City)
class CityAdmin(MPTTModelAdmin):
    list_display = ('name', 'level_type', 'parent')
    list_filter = ('level_type',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 20

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'parent', 'level_type')
        }),
    )

# =======================================================
# 📍 Locality Admin (MPTT)
# =======================================================
@admin.register(Locality)
class LocalityAdmin(DraggableMPTTAdmin):
    list_display = ('id','tree_actions', 'indented_title', 'city', 'featured_locality')
    list_display_links = ('indented_title',)
    search_fields = ('name', 'city__name')
    list_filter = ('city', 'featured_locality')
# =======================================================
# 🏠 PropertyType Admin (MPTT)
# =======================================================
@admin.register(PropertyType)
class PropertyTypeAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'is_top_level', 'is_selectable')
    list_filter = ('is_top_level', 'is_selectable')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 20

    fieldsets = (
        ('Property Type Info', {
            'fields': ('name', 'slug', 'parent', 'is_top_level', 'is_selectable')
        }),
    )

# =======================================================
# 📅 PossessionIn Admin
# =======================================================
@admin.register(PossessionIn)
class PossessionInAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('year',)
    search_fields = ('year',)

@admin.register(ProjectAmenities)
class ProjectAmenitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview')

    def preview(self, obj):
        """Display safe image preview in Django admin."""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return mark_safe(
                    f'<img src="{obj.image.url}" width="80" height="80" '
                    f'style="object-fit:cover;border-radius:8px;" />'
                )
        except Exception:
            pass
        return mark_safe(
            '<img src="https://via.placeholder.com/80x80.png?text=No+Image" '
            'style="object-fit:cover;border-radius:8px;" />'
        )

    preview.short_description = "Preview"



# =======================================================
# 🏦 Bank Admin
# =======================================================
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('title', 'safe_image_preview')
    search_fields = ('title',)
    readonly_fields = ('safe_image_preview',)

    def safe_image_preview(self, obj):
        """Safe logo preview (never crashes even if image missing)."""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                url = obj.image.url
            else:
                url = NO_IMAGE_URL
        except Exception:
            url = NO_IMAGE_URL
        return mark_safe(f'<img src="{url}" width="60" height="60" '
                         f'style="object-fit:contain;border-radius:6px;" />')

    safe_image_preview.short_description = "Logo"


