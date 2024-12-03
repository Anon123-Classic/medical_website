from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError

# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_country_code = request.POST.get('phone_country_code')
        phone = request.POST.get('phone')
        job_type = request.POST.get('job_type')
        is_staff = request.POST.get('is_staff') == 'on'  # Convert checkbox to boolean
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                # Check if username or email already exists
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                if is_staff:
                    user.is_staff = True  # Set staff status
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('medicall:index')
            except IntegrityError:
                messages.error(request, "Username or email already exists.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match")
    
    return render(request, 'accounts/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('medicall:index')  # Adjust as necessary
        else:
            messages.error(request, "Invalid username or password")
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')
