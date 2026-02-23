from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import requests
import time

# Store temporary chat history in memory
chat_sessions = {}

@login_required
def ai_chat_view(request):
    """Render the AI chat interface for logged-in users"""
    return render(request, 'hakimu_ai_chat/chat.html')

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
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return JsonResponse({'error': 'Gemini API key not configured'}, status=500)
        
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}',
            json={
                'contents': [{
                    'parts': [{'text': message}]
                }]
            },
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            return JsonResponse({
                'error': f'Gemini API error: {response.status_code}',
                'details': response.text
            }, status=response.status_code)
        
        result = response.json()
        
        # Extract AI response
        if 'candidates' in result and len(result['candidates']) > 0:
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_response = "I'm sorry, I couldn't generate a response. Please try again."
        
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
        
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'Request to Gemini API timed out'}, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Failed to connect to Gemini API'}, status=503)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def chat_history(request):
    """Get chat history for current session"""
    session_id = request.GET.get('session_id', request.user.username)
    history = chat_sessions.get(session_id, [])
    return JsonResponse({'history': history, 'session_id': session_id})

@login_required
@csrf_exempt
def clear_session(request):
    """Clear chat history for current session"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', request.user.username)
        
        if session_id in chat_sessions:
            chat_sessions[session_id] = []
            return JsonResponse({'status': 'cleared', 'session_id': session_id})
        else:
            return JsonResponse({'status': 'no session found', 'session_id': session_id})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)