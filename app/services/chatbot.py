"""
LibraNet AI Chatbot Service
Powered by Groq + LangChain
"""

import os
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class LibraNetChatbot:
    def __init__(self):
        """Initialize the chatbot with Groq LLM"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq LLM with LangChain
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # Fast and powerful model
            temperature=0.7,
            max_tokens=1024,
            api_key=api_key
        )
        
        # System prompt for LibraNet chatbot
        self.system_prompt = """You are LibraNet Assistant, a helpful AI chatbot for LibraNet - a modern library management system.

Your role:
- Help users with questions about books, ebooks, and audiobooks
- Assist with library features like borrowing, returns, and subscriptions
- Provide book recommendations based on user preferences
- Answer general questions about using the library system
- Be friendly, helpful, and concise

Keep responses clear and under 150 words unless more detail is needed."""

        # Conversation history (simple in-memory storage)
        self.conversation_history = []

    def chat(self, user_message, user_name=None):
        """
        Send a message to the chatbot and get a response
        
        Args:
            user_message (str): The user's message
            user_name (str): Optional username for personalization
            
        Returns:
            str: The chatbot's response
        """
        try:
            # Create personalized greeting if user name provided
            greeting = f"Hello {user_name}! " if user_name else ""
            
            # Build message chain
            messages = [
                SystemMessage(content=self.system_prompt)
            ]
            
            # Add conversation history (last 5 messages for context)
            for msg in self.conversation_history[-5:]:
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                else:
                    messages.append(AIMessage(content=msg['content']))
            
            # Add current user message
            messages.append(HumanMessage(content=user_message))
            
            # Get response from Groq
            response = self.llm.invoke(messages)
            response_text = response.content
            
            # Store in conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now().isoformat()
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            return response_text
            
        except Exception as e:
            print(f"Chatbot error: {str(e)}")
            return "I'm having trouble processing your question right now. Please try again or contact our support team. 😊"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_book_recommendations(self, preferences):
        """
        Get personalized book recommendations
        
        Args:
            preferences (str): User's reading preferences
            
        Returns:
            str: Book recommendations
        """
        prompt = f"""Based on these reading preferences: "{preferences}"
        
Please suggest 3-5 books with:
- Title and author
- Brief reason why it matches their taste
- Genre

Keep it concise and engaging."""

        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Recommendation error: {str(e)}")
            return "I'm unable to generate recommendations right now. Please try again later."


# Create a singleton instance
try:
    chatbot_service = LibraNetChatbot()
except Exception as e:
    print(f"Warning: Could not initialize chatbot service: {str(e)}")
    chatbot_service = None
