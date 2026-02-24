"""
Main URL Configuration for Hakimu Official
Includes all apps: core, blog, hakimu_ai_chat, and portfolio
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

# Custom admin site configuration
admin.site.site_header = "Hakimu Official Administration"
admin.site.site_title = "Hakimu Admin Portal"
admin.site.index_title = "Welcome to Hakimu Dashboard"
admin.site.site_url = "https://hakimu.onrender.com"

# URL Patterns
urlpatterns = [
    # ==================== ADMIN ====================
    path('admin/', admin.site.urls),
    path('hakimu-admin/', admin.site.urls),  # Alternative admin URL
    
    # ==================== PUBLIC PAGES ====================
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('features/', views.features_view, name='features'),
    path('pricing/', views.pricing_view, name='pricing'),
    
    # ==================== PORTFOLIO ====================
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio-debug/', views.portfolio_debug_view, name='portfolio_debug'),
    
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
    path('blog/', include('blog.urls')),
    
    # ==================== AI CHAT APP ====================
    path('ai-chat/', include('hakimu_ai_chat.urls')),
    path('chat/', include('hakimu_ai_chat.urls')),  # Short URL
    path('assistant/', include('hakimu_ai_chat.urls')),  # Alternative URL
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ==================== CUSTOM ERROR HANDLERS ====================
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'