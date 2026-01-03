# blog/admin.py
from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish_date', 'is_published')
    list_filter = ('is_published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Title type karte hi slug auto-fill ho jayega
    date_hierarchy = 'publish_date'

admin.site.register(Post, PostAdmin)