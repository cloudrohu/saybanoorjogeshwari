# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model

# CustomUser model ko dynamically fetch karta hai
User = get_user_model() 

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True) # URLs ke liye clean title
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    # Image field
    photo = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True) 
    
    publish_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish_date'] # Naye posts upar dikhenge
        
    def __str__(self):
        return self.title