"""
Blog App URL Configuration
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list page (shows all posts)
    path('', views.blog_list, name='blog_list'),
    
    # Blog detail page (individual post)
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Blog category page (filter by category)
    path('category/<slug:slug>/', views.blog_category, name='blog_category'),
]