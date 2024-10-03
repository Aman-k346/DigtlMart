from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password



# Create your views here.

def home(request):
    return render(request, 'home.html')

def terms(request):
    return render(request, 'terms.html')

def VideoBundle(request):
    return render(request, 'videobundle.html')

def refund(request):
    return render(request, 'refund.html')

def privacy(request):
    return render(request, 'privacy.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('/')  # Redirect to home or dashboard after successful login
        else:
            # If authentication fails
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not email.endswith('@gmail.com'):
            messages.error(request, 'Only gmail.com emails are accepted.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')

        user = User.objects.create(
            username=email,  
            email=email,
            password=make_password(password) 
        )
        user.save()

        messages.success(request, 'Email registered successfully. Please log in.')

    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/') 

def checkout(request):
    return render(request, 'checkout.html')