from django.db import models
from projects.models import Project

# Create your models here.

class AdditionalInfoResponse(models.Model):

    TYPE_CHOICES = (
        ('book_visit', 'Book Visit'),
        ('get_price', 'Get Price'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=15)
    visit_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.name}"
    
class ConfigurationResponse(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    configuration = models.CharField(max_length=50)  # 2 BHK / 3 BHK etc

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.configuration} - {self.name}"    
    

class BrochureLead(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project}"
    
class MetaLead(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    leadgen_id = models.CharField(max_length=100, unique=True)
    form_id = models.CharField(max_length=100, blank=True, null=True)
    page_id = models.CharField(max_length=100, blank=True, null=True)

    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    configuration = models.CharField(max_length=50, blank=True, null=True)
    budget = models.CharField(max_length=100, blank=True, null=True)
    visit_plan = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=120, blank=True, null=True)

    raw_payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"    