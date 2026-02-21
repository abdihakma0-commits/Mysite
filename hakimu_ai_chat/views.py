from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import requests
import time

# Store temporary chat history in memory (not database)
chat_sessions = {}

@login_required(login_url='/login/')
def ai_chat_view(request):
    """Render the AI chat interface for logged-in users"""
    return render(request, 'hakimu_ai_chat/chat.html', {
        'gemini_api_key': settings.GEMINI_API_KEY,
        'user': request.user
    })

@login_required
@csrf_exempt
def chat_api(request):
    """Handle chat messages with Gemini API"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        session_id = data.get('session_id', request.user.username)
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Initialize session if not exists
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add user message to history
        chat_sessions[session_id].append({
            'role': 'user',
            'content': message,
            'timestamp': time.time()
        })
        
        # Call Gemini API
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.GEMINI_API_KEY}',
            json={
                'contents': [{
                    'parts': [{'text': message}]
                }]
            },
            timeout=30
        )
        
        if response.status_code != 200:
            return JsonResponse({'error': 'API error'}, status=response.status_code)
        
        result = response.json()
        ai_response = result['candidates'][0]['content']['parts'][0]['text']
        
        # Add AI response to history
        chat_sessions[session_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': time.time()
        })
        
        # Keep only last 50 messages per session
        if len(chat_sessions[session_id]) > 50:
            chat_sessions[session_id] = chat_sessions[session_id][-50:]
        
        return JsonResponse({
            'response': ai_response,
            'session_id': session_id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def chat_history(request):
    """Get chat history for current session"""
    session_id = request.user.username
    history = chat_sessions.get(session_id, [])
    return JsonResponse({'history': history})