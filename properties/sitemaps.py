# properties/sitemaps.py

from django.contrib.sitemaps import Sitemap
# Project model ko import karein
from projects.models import Project 
# Property, Blog, aur StaticSitemap classes bhi yahan honi chahiye
from properties.models import Property

from blog.models import Post 
from django.urls import reverse
# ...

from django.urls import reverse

# Sitemaps: Projects (Developments)
class ProjectSitemap(Sitemap):
    # Search engines ko batata hai ki yeh data kitni baar badalta hai
    changefreq = "monthly"
    # Is content ki priority kya hai (1.0 sabse zyada hai)
    priority = 0.7 

    def items(self):
        """Sitemap mein shamil hone wale Project objects ko return karta hai."""
        # Sirf 'active' projects ko shamil karein
        return Project.objects.filter(active=True)

    def location(self, obj):
        """Har Project object ke liye absolute URL return karta hai."""
        # 'project_details' URL name aur uske required kwargs (id aur slug) use karein
        return reverse('project_details', kwargs={'id': obj.id, 'slug': obj.slug})

# Note: Is file mein PropertySitemap, BlogSitemap, aur StaticSitemap classes bhi shamil honi chahiye.




class PropertySitemap(Sitemap):
    # ... (rest of the logic) ...
    def items(self):
        return Property.objects.filter(is_published=True)
    


# properties/sitemaps.py (PASTE THIS FULL CODE)
from django.contrib.sitemaps import Sitemap
from properties.models import Property


# --- 1. Property Listings Sitemap ---
class PropertySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    def items(self):
        return Property.objects.filter(is_published=True)
    def location(self, obj):
        return reverse('property_detail', args=[obj.id]) 

# --- 2. Blog Posts Sitemap ---
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        # Ensure Blog posts are fetched from your Blog model
        return Post.objects.filter(is_published=True)
    def location(self, obj):
        return reverse('post_detail', args=[obj.slug])

# --- 3. Static Pages Sitemap ---
class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    def items(self):
        # List all core URL names here
        return ['index', 'properties', 'projects', 'blog_posts', 'register', 'login']
    def location(self, item):
        return reverse(item)