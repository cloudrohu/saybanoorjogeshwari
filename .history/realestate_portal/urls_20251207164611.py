# realestate_portal/urls.py

from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.sitemaps.views import sitemap 

# Import sitemaps from their modular locations
from projects.sitemaps import ProjectSitemap 
from properties.sitemaps import PropertySitemap, BlogSitemap, StaticSitemap 

# Define the dictionary of sitemaps
sitemaps = {
    'static': StaticSitemap,
    'properties': PropertySitemap,
    'projects': ProjectSitemap, 
    'blog': BlogSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path("", include("utility.urls")),  # ✅ Add this
    path('projects/', include('projects.urls')),
    path('properties/', include('properties.urls')),
    path('accounts/', include('user.urls')),
    path('blog/', include('blog.urls')),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)