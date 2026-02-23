from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Public Pages
def home_view(request):
    return render(request, "pages/home.html")

def about_view(request):
    return render(request, "pages/about.html")

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        messages.success(request, f"Thank you {name}! Your message has been sent.")
        return redirect("contact")
    return render(request, "pages/contact.html")

def faq_view(request):
    return render(request, "pages/faq.html")

def features_view(request):
    return render(request, "pages/features.html")

def pricing_view(request):
    return render(request, "pages/pricing.html")

# Authentication
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f"Welcome to Hakimu, {username}!")
        return redirect("dashboard")

    return render(request, "auth/signup.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect("login")

def password_reset_view(request):
    return render(request, "auth/password_reset.html")

def password_change_view(request):
    return render(request, "auth/password_change.html")

# Dashboard
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def profile(request):
    return render(request, "dashboard/profile.html")

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")

@login_required
def notifications_view(request):
    return render(request, "dashboard/notifications.html")

@login_required
def analytics_view(request):
    return render(request, "dashboard/analytics.html")

# Error handlers
def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_500(request):
    return render(request, "errors/500.html", status=500)

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)