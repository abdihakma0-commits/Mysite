"""
Blog App URL Configuration
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list page
    path('', views.blog_list, name='blog_list'),
    
    # Blog detail page
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Blog category page
    path('category/<slug:slug>/', views.blog_category, name='blog_category'),
]