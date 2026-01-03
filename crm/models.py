# crm/models.py
from django.db import models
from properties.models import Property # Property model import karein

class Inquiry(models.Model):
    # Foreign Key to link the inquiry to a specific property
    property = models.ForeignKey(Property, on_delete=models.DO_NOTHING) 
    
    # User Details
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    
    # Status and Date Tracking
    inquiry_date = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False) # Admin track karega

    def __str__(self):
        return f'Inquiry for {self.property.title} from {self.name}'
    
    class Meta:
        verbose_name_plural = "Inquiries"