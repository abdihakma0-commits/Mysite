"""
AI Chat App URL Configuration for Hakimu Official
"""
from django.urls import path
from . import views

app_name = 'hakimu_ai_chat'

urlpatterns = [
    # Main chat interface
    path('', views.ai_chat_view, name='chat'),
    
    # API endpoints
    path('api/send/', views.chat_api, name='chat_api'),
    path('api/history/', views.chat_history, name='chat_history'),
    
    # Session management
    path('api/clear/', views.clear_session, name='clear_session'),
    path('api/export/', views.export_chat, name='export_chat'),
]