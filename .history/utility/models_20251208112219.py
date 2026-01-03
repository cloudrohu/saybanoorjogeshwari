# utility/models.py
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
import admin_thumbnails
from django.utils.html import mark_safe

class City(MPTTModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    
    # MPTT Hierarchy Field: Yeh field define karta hai ki kaun kiska parent hai.
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Parent Location (State/City)'
    )
    
    # Level Type se aap identify kar sakte hain ki yeh entry kya hai (City, Locality, etc.)
    level_choices = (
        ('STATE', 'State/Province'),
        ('CITY', 'City'),
        ('LOCALITY', 'Locality/Sector'),
        ('AREA', 'Sub-Area/Zone'),
    )
    level_type = models.CharField(max_length=20, choices=level_choices, default='LOCALITY')

    class MPTTMeta:
        # Hierarchy ko name ke hisaab se sort karega
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = "Location (City/Locality)"
        verbose_name_plural = "Locations (Cities/Localities)"

    def __str__(self):
        # Admin mein hierarchy path dikhayega (e.g., Delhi / Vasant Kunj)
        full_path = [node.name for node in self.get_ancestors(include_self=True)]
        return ' / '.join(full_path)
# --- 2. Locality Model (MPTT Child Structure) ---

# --- 2. Locality Model (MPTT Child Structure) ---
class Locality(MPTTModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent Locality/Zone'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('city', 'name')  # ✅ Correct placement
        verbose_name_plural = "Localities"

    def __str__(self):
        path = [node.name for node in self.get_ancestors(include_self=True)]
        return f"{' / '.join(path)} ({self.city.name})"



class PropertyType(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Parent Type/Category'
    )
    
    is_top_level = models.BooleanField(default=False) 
    
    is_selectable = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "Property Types"

    def __str__(self):
        full_path = [node.name for node in self.get_ancestors(include_self=True)]
        return ' / '.join(full_path)
    
    
class PossessionIn(models.Model):
    year = models.PositiveIntegerField(
        unique=True,
        help_text="e.g. 2025"
    )

    class Meta:
        verbose_name = "Possession Year"
        verbose_name_plural = "Possession Years"
        ordering = ['year']

    def __str__(self):
        return str(self.year)

from django.db import models
from django.utils.html import mark_safe

class ProjectAmenities(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='amenities/', blank=True, null=True)
    
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title


class Bank(models.Model):
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='03. Bank'

class PropertyAmenities(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='property/amenities/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Property Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

    def icon_tag(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="40" height="40" />')
        return ""
    icon_tag.short_description = "Icon"
