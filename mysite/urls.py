from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),              # Home/Login page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard for logged-in users
    path('accounts/', include('allauth.urls')),    # Allauth login
]