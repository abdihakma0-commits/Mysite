from django.urls import path
from . import views

app_name = 'hakimu_ai_chat'

urlpatterns = [
    path('', views.ai_chat_view, name='chat'),
    path('api/send/', views.chat_api, name='chat_api'),
    path('api/history/', views.chat_history, name='chat_history'),
    path('api/clear/', views.clear_session, name='clear_session'),
]