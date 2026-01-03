from django.utils.html import mark_safe
# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from utility.models import City,Locality
from django.utils.text import slugify
from django.urls import reverse

class CustomUser(AbstractUser):
    # Add your own fields here if needed later (e.g., phone_number)
    user_type_choices = (
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
        ('admin', 'Administrator'),
    )
    user_type = models.CharField(max_length=10, choices=user_type_choices, default='buyer')

    def __str__(self):
        return self.email
    
class Developer(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True,blank=True)  # many to one relation with Brand
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True,blank=True)  # many to one relation with Brand
    title = models.CharField(max_length=150, unique=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    google_map = models.CharField(blank=True,max_length=1000)
    web_site = models.CharField(blank=True,max_length=150)
    address = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    about_developer = models.TextField(max_length=5000, null=True, blank=True)
    logo = models.ImageField(upload_to='images/')
    featured_builder = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='1. Developer'


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + ' ' + self.city.name)
        super(Developer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('developer_detail', kwargs={'slug': self.slug})

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
