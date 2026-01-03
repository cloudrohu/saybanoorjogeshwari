# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # /blog/ - Saare published posts ki listing
    path('', views.index, name='blog_posts'), 
    
    # /blog/post-title-slug/ - Specific post ki details (slug use karke)
    path('<slug:post_slug>/', views.post_detail, name='post_detail'), 
]