"""
Main URL Configuration for MyApp Pro
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

# URL Patterns
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # ==================== PUBLIC PAGES ====================
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    
    # ==================== AUTHENTICATION ====================
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-change/', views.password_change_view, name='password_change'),
    
    # ==================== DASHBOARD ====================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('analytics/', views.analytics_view, name='analytics'),
    
    # ==================== BLOG APP ====================
    # Make sure 'blog' is in INSTALLED_APPS in settings.py
    path('blog/', include('blog.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'