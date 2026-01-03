# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm # Hum yeh form abhi banaenge
from django.contrib.auth.decorators import login_required # Required for protection
from crm.models import Inquiry # Inquiry model import karein
from django.shortcuts import render, get_object_or_404
from .models import Developer
# --- 1. User Registration View ---
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # User ko automatic login karwa dete hain registration ke baad
            login(request, user)
            messages.success(request, 'Registration Successful! Welcome to the portal.')
            return redirect('index') # 'home' app ke index page par redirect

        else:
            # Form mein errors hain, jaise password match nahi hua
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        form = UserRegistrationForm() # GET request, empty form dikhao

    return render(request, 'user/register.html', {'form': form})

# --- 2. User Login View ---
def user_login(request):
    if request.method == 'POST':
        # AuthenticationForm built-in hai, hum ise yahan directly use kar rahe hain
        from django.contrib.auth.forms import AuthenticationForm 
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index') 
            
        messages.error(request, 'Invalid username or password.')
    
    # GET request ya invalid POST data
    from django.contrib.auth.forms import AuthenticationForm 
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# --- 3. User Logout View ---
def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('index') # Home page par wapas bhej do



# ... (register, user_login, user_logout functions as before)

@login_required(login_url='login') # Only logged-in users can access this page
def dashboard(request):
    # Logged-in user ke email se related inquiries fetch karein
    user_inquiries = Inquiry.objects.filter(email=request.user.email).order_by('-inquiry_date')

    context = {
        'inquiries': user_inquiries,
    }
    return render(request, 'user/dashboard.html', context)



def developer_detail(request, slug):
    developer = get_object_or_404(Developer, slug=slug)
    return render(request, 'user/developer_detail.html', {'developer': developer})