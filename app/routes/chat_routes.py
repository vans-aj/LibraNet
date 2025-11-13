"""
Chat routes for LibraNet AI Chatbot
"""

from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.routes import main_bp
from app.services.chatbot import chatbot_service


@main_bp.route('/chat')
@login_required
def chat_page():
    """Render the chat page"""
    return render_template('chat.html', title='AI Assistant')


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def chat_message():
    """Handle chat messages"""
    try:
        if not chatbot_service:
            return jsonify({
                'success': False,
                'error': 'Chatbot service is not available'
            }), 503
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Get response from chatbot
        response = chatbot_service.chat(
            user_message=user_message,
            user_name=current_user.name if current_user.is_authenticated else None
        )
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to process message'
        }), 500


@main_bp.route('/api/chat/clear', methods=['POST'])
@login_required
def clear_chat():
    """Clear chat history"""
    try:
        if chatbot_service:
            chatbot_service.clear_history()
        
        return jsonify({
            'success': True,
            'message': 'Chat history cleared'
        })
        
    except Exception as e:
        print(f"Clear chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear chat'
        }), 500
