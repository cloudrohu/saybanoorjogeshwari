# crm/admin.py
from django.contrib import admin
from .models import Inquiry
from import_export.admin import ImportExportModelAdmin


class InquiryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'property', 'name', 'email', 'phone', 'inquiry_date', 'is_contacted')
    list_display_links = ('id', 'property')
    list_editable = ('is_contacted',) # Admin se direct status change kar saken
    list_filter = ('is_contacted',)
    search_fields = ('name', 'email', 'phone', 'message', 'property__title')
    list_per_page = 20

admin.site.register(Inquiry, InquiryAdmin)