# projects/sitemaps.py

from django.contrib.sitemaps import Sitemap
from projects.models import Project 
from django.urls import reverse

class ProjectSitemap(Sitemap):
    # Search engines ko batata hai ki yeh data kitni baar badalta hai
    changefreq = "monthly"
    # Is content ki SEO priority (0.0 se 1.0 tak)
    priority = 0.7 

    def items(self):
        """Returns all active project objects to be included in the sitemap."""
        # Sirf 'active' projects ko shamil karein
        return Project.objects.filter(active=True)

    def location(self, obj):
        """Generates the full URL for the project detail page."""
        # Uses the 'project_details' URL name and passes the required ID and SLUG
        return reverse('project_details', kwargs={'id': obj.id, 'slug': obj.slug})