"""
Chat routes for LibraNet AI Assistant
"""

from flask import render_template, request, jsonify
from flask_login import current_user
from app.routes import main_bp
from app import db
from app.services.chatbot import chatbot_service


@main_bp.route('/chat')
def chat_page():
    """Display the chat interface"""
    return render_template('chat.html', title='LibraNet Assistant')


@main_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """
    API endpoint for chat messages
    
    Expected JSON:
    {
        "message": "user's question"
    }
    
    Returns JSON:
    {
        "success": true,
        "response": "AI response",
        "user_name": "User Name"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Generate AI response
        ai_response = chatbot_service.chat(
            question=user_message,
            current_user=current_user,
            db=db
        )
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'user_name': current_user.name if current_user.is_authenticated else 'Guest'
        })
        
    except Exception as e:
        print(f"Chat API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Something went wrong. Please try again.'
        }), 500


@main_bp.route('/api/chat/recommendations', methods=['POST'])
def chat_recommendations():
    """
    API endpoint for book recommendations
    
    Expected JSON:
    {
        "genre": "Fiction" (optional),
        "limit": 5 (optional)
    }
    """
    try:
        data = request.get_json() or {}
        
        genre = data.get('genre')
        limit = data.get('limit', 5)
        
        recommendations = chatbot_service.get_book_recommendations(
            current_user=current_user,
            db=db,
            genre=genre,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Recommendations API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Could not generate recommendations'
        }), 500


@main_bp.route('/api/chat/quick-questions', methods=['GET'])
def quick_questions():
    """Get suggested quick questions based on user context"""
    
    if current_user.is_authenticated:
        tier = current_user.subscription_tier.value
        
        if tier == 'free':
            questions = [
                "What are the subscription plans?",
                "How do I upgrade my account?",
                "What books are available?",
                "How does borrowing work?"
            ]
        elif tier == 'basic':
            questions = [
                "How many books can I borrow?",
                "When are my books due?",
                "What are the fine rates?",
                "Can I access ebooks?"
            ]
        else:  # PRO or MAX
            questions = [
                "Recommend some books for me",
                "What audiobooks are new?",
                "How do I download ebooks?",
                "What's my subscription status?"
            ]
    else:
        questions = [
            "How do I register?",
            "What is LibraNet?",
            "What subscription plans are available?",
            "Can I browse books as a guest?"
        ]
    
    return jsonify({
        'success': True,
        'questions': questions
    })