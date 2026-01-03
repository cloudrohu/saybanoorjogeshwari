# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # 'username' aur 'password' fields 'UserCreationForm' se automatic aayenge
        # Hum 'user_type' field ko bhi add kar sakte hain ya default rehne de sakte hain
        fields = ('username', 'email', 'user_type')