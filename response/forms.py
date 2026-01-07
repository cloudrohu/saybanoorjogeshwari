from django import forms
from .models import AdditionalInfoResponse, ConfigurationResponse

class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = AdditionalInfoResponse
        fields = [
            'type',
            'name',
            'email',
            'phone',
            'visit_date'
        ]
        widgets = {
            'type': forms.HiddenInput(),
        }   


class ConfigurationResponseForm(forms.ModelForm):
    class Meta:
        model = ConfigurationResponse
        fields = [
            "name",
            "email",
            "phone",
            "configuration",
        ]
        widgets = {
            "configuration": forms.HiddenInput(),
        }