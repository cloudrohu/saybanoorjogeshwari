from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from utility.models import City, Locality, PropertyType, PossessionIn, PropertyAmenities
from projects.models import Project  # ✅ Correct import

# ================================
# ✅ CLEAN + FINAL Property Model
# ================================
class Property(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Sold", "Sold"),
        ("Upcoming", "Upcoming"),
    ]

    # --- Basic Info ---
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # --- Relationships ---
    project = models.ForeignKey(
        'projects.Project',   # ✅ Fixed: should match your app name "projects"
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT)
    possession_in = models.ForeignKey(PossessionIn, on_delete=models.SET_NULL, null=True, blank=True)

    # --- Core Details ---
    price = models.DecimalField(max_digits=15, decimal_places=2)
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    bhk = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")

    # --- Property Amenities ---
    amenities = models.ManyToManyField(PropertyAmenities, blank=True, related_name='properties')

    # --- Images ---
    main_image = models.ImageField(upload_to="properties/main/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="properties/cover/", blank=True, null=True)

    # --- Builder / Legal Info ---
    builder_name = models.CharField(max_length=255, blank=True, null=True)
    rera_number = models.CharField(max_length=100, blank=True, null=True)

    # --- SEO Meta ---
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    # --- System Fields ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]

    def __str__(self):
        if self.project:
            return f"{self.title} ({self.project.name})"
        return f"{self.title} ({self.city.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def main_image_tag(self):
        if self.main_image:
            return mark_safe(f'<img src="{self.main_image.url}" width="100" height="80" />')
        return ""
    main_image_tag.short_description = "Main Image"
