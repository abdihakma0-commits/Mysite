from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings

# =========================
# PUBLIC PAGES
# =========================
def home_view(request):
    """Home page view"""
    return render(request, "pages/home.html")

def about_view(request):
    """About page view"""
    return render(request, "pages/about.html")

def contact_view(request):
    """Contact page view with form handling"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        try:
            send_mail(
                f"Contact Form Message from {name}",
                message,
                email,
                settings.CONTACT_EMAIL,
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "Failed to send message. Please try again.")
        
        return redirect("contact")
    
    return render(request, "pages/contact.html")

def faq_view(request):
    """FAQ page view"""
    return render(request, "pages/faq.html")

def features_view(request):
    """Features page view"""
    return render(request, "pages/features.html")

def pricing_view(request):
    """Pricing page view"""
    return render(request, "pages/pricing.html")

# =========================
# PORTFOLIO PAGE
# =========================
def portfolio_view(request):
    """Premium portfolio page with 3D animations"""
    return render(request, "portfolio/home.html")

# =========================
# AUTHENTICATION
# =========================
def login_view(request):
    """User login view"""
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
    """User signup view"""
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

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, f"Welcome to Hakimu, {username}!")
        return redirect("dashboard")

    return render(request, "auth/signup.html")

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect("login")

def password_reset_view(request):
    """Password reset view"""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            messages.success(request, "Password reset instructions sent to your email")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email")
        return redirect("login")
    
    return render(request, "auth/password_reset.html")

@login_required
def password_change_view(request):
    """Password change view"""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "auth/password_change.html", {"form": form})

# =========================
# DASHBOARD PAGES
# =========================
@login_required
def dashboard(request):
    """Main dashboard view"""
    context = {
        'page_title': 'Dashboard',
        'active_page': 'dashboard'
    }
    return render(request, "dashboard/dashboard.html", context)

@login_required
def profile(request):
    """User profile view"""
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        
        user = request.user
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    
    context = {
        'page_title': 'Profile',
        'active_page': 'profile'
    }
    return render(request, "dashboard/profile.html", context)

@login_required
def settings_view(request):
    """Account settings view"""
    context = {
        'page_title': 'Settings',
        'active_page': 'settings'
    }
    return render(request, "dashboard/settings.html", context)

@login_required
def notifications_view(request):
    """Notifications view"""
    context = {
        'page_title': 'Notifications',
        'active_page': 'notifications'
    }
    return render(request, "dashboard/notifications.html", context)

@login_required
def analytics_view(request):
    """Analytics view"""
    context = {
        'page_title': 'Analytics',
        'active_page': 'analytics'
    }
    return render(request, "dashboard/analytics.html", context)

# =========================
# ERROR HANDLERS
# =========================
def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, "errors/404.html", status=404)

def custom_500(request):
    """Custom 500 error page"""
    return render(request, "errors/500.html", status=500)

def custom_403(request, exception):
    """Custom 403 error page"""
    return render(request, "errors/403.html", status=403)