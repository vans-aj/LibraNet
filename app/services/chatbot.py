"""
LibraNet AI Chatbot Service
Powered by LangChain and Google Gemini
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore 
from langchain_core.prompts import ChatPromptTemplate # type:ignore
from langchain_core.output_parsers import StrOutputParser # type:ignore
from datetime import datetime

# Load environment variables
load_dotenv()

class LibraNetChatbot:
    def __init__(self):
        """Initialize the chatbot with Gemini model"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.output_parser = StrOutputParser()
        self._setup_prompt()
        
    def _setup_prompt(self):
        """Setup the system prompt for LibraNet assistant"""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are LibraNet Assistant, a helpful AI librarian for the LibraNet digital library management system.

Your role:
- Help students find books, ebooks, and audiobooks
- Explain subscription plans (FREE, BASIC, PRO, MAX)
- Answer questions about borrowing, fines, and due dates
- Provide guidance on using the library system
- Be friendly, concise, and student-focused
- and they can ask you to meaning of any word while reading or listing of audio book so tell them ( it may be in english or hindi)

Current context:
- Date: {current_date}
- User: {user_name} ({user_tier})
- Active Loans: {active_loans}
- Library Stats: {library_stats}
- Developers: TeamX
             Members: Vansaj Rawat, Mansi Daramwal, Kritika Basera
- Mentor: Mr. Kapil Rajput
- about code go to -> https://gihub.com/vans-aj/libranet

Rules:
- Keep responses under 150 words unless detailed explanation needed
- Don't use emojis sparingly ( for books,  for audio,  for ebooks)
- If you don't know, admit it and suggest contacting support
- Format prices in ₹ (Indian Rupees)
- Subscription prices: BASIC ₹49, PRO ₹150, MAX ₹300 (6 months)
- Fine rate: ₹500 per week overdue (recently updated from ₹10/day)
- For anything other than books, library services, LibraNet or meaning of words  give appropriate answer like ask something relevent'
- LibraNet is open to everyone - anyone can create an account and start reading!
Always be helpful, accurate, and encourage reading!"""),
            ("user", "{question}")
        ])
        
        self.chain = self.prompt | self.llm | self.output_parser
    
    def get_library_context(self, current_user, db):
        """Get relevant library context for the user"""
        from app.models.physical_book import PhysicalBook
        from app.models.ebook import Ebook
        from app.models.audiobook import Audiobook
        from app.models.loan import Loan
        
        context = {
            "current_date": datetime.utcnow().strftime("%B %d, %Y"),
            "user_name": current_user.name if current_user.is_authenticated else "Guest",
            "user_tier": current_user.subscription_tier.value.upper() if current_user.is_authenticated else "NONE",
            "active_loans": "0",
            "library_stats": ""
        }
        
        if current_user.is_authenticated:
            # Get active loans count
            active_loans = Loan.query.filter_by(
                student_id=current_user.id,
                returned_date=None
            ).count()
            context["active_loans"] = str(active_loans)
        
        # Get library statistics
        total_books = PhysicalBook.query.count()
        total_ebooks = Ebook.query.count()
        total_audiobooks = Audiobook.query.count()
        
        context["library_stats"] = f"{total_books} physical books, {total_ebooks} ebooks, {total_audiobooks} audiobooks"
        
        return context
    
    def chat(self, question, current_user, db):
        """
        Process a chat question and return AI response
        
        Args:
            question (str): User's question
            current_user: Flask-Login current_user object
            db: SQLAlchemy database session
            
        Returns:
            str: AI-generated response
        """
        try:
            # Get library context
            context = self.get_library_context(current_user, db)
            context["question"] = question
            
            # Generate response
            response = self.chain.invoke(context)
            
            return response
            
        except Exception as e:
            print(f"Chatbot error: {str(e)}")
            return "I'm having trouble processing your question right now. Please try again or contact our support team. 😊"
    
    def get_book_recommendations(self, current_user, db, genre=None, limit=5):
        """Get personalized book recommendations"""
        from app.models.physical_book import PhysicalBook
        from app.models.loan import Loan
        
        try:
            # Get user's reading history
            if current_user.is_authenticated:
                past_loans = Loan.query.filter_by(
                    student_id=current_user.id
                ).limit(10).all()
                
                past_titles = [loan.book.title for loan in past_loans if loan.book]
                reading_history = ", ".join(past_titles[:5]) if past_titles else "No history"
            else:
                reading_history = "No history (Guest user)"
            
            # Get available books
            available_books = PhysicalBook.query.filter(
                PhysicalBook.available_copies > 0
            ).limit(20).all()
            
            book_list = "\n".join([
                f"- {book.title} by {book.author}"
                for book in available_books[:10]
            ])
            
            # Generate recommendations
            rec_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a book recommendation expert for LibraNet library.

User's reading history: {reading_history}
Genre preference: {genre}

Available books:
{book_list}

Recommend {limit} books from the available list that match the user's interests.
Format each as: "📚 **Title** by Author - Brief reason (1 sentence)"

Be enthusiastic and specific!"""),
                ("user", "Please recommend some books for me.")
            ])
            
            rec_chain = rec_prompt | self.llm | self.output_parser
            
            response = rec_chain.invoke({
                "reading_history": reading_history,
                "genre": genre or "any genre",
                "book_list": book_list,
                "limit": limit
            })
            
            return response
            
        except Exception as e:
            print(f"Recommendation error: {str(e)}")
            return "I'm having trouble generating recommendations right now. Browse our catalog to discover great books! 📚"


# Create singleton instance
chatbot_service = LibraNetChatbot()