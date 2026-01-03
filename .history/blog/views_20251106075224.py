# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

# --- 1. Blog Listing Page (Index) ---
def index(request):
    # Sirf published posts ko publish_date ke hisaab se fetch karein
    published_posts = Post.objects.filter(is_published=True).order_by('-publish_date')

    context = {
        'posts': published_posts
    }
    
    return render(request, 'blog/blog_posts.html', context)


# --- 2. Individual Post Detail Page ---
def post_detail(request, post_slug):
    # Post ko slug aur published status ke hisaab se fetch karein
    post = get_object_or_404(Post, slug=post_slug, is_published=True) 

    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)