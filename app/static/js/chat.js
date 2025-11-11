/**
 * Chat Widget Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initChatWidget();
});

/**
 * Initialize Chat Widget
 */
function initChatWidget() {
    const chatToggle = document.getElementById('chatToggle');
    const chatWindow = document.getElementById('chatWindow');
    const chatClose = document.getElementById('chatClose');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const quickReplyButtons = document.querySelectorAll('.quick-reply-btn');
    
    if (!chatToggle || !chatWindow) return;
    
    // Show welcome message if chat is empty and user just logged in
    showWelcomeMessageIfNeeded();
    
    // Toggle chat window
    chatToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            chatInput.focus();
            markMessagesAsRead();
        }
    });
    
    // Close chat
    if (chatClose) {
        chatClose.addEventListener('click', () => {
            chatWindow.classList.remove('active');
        });
    }
    
    // Send message
    if (chatForm) {
        chatForm.addEventListener('submit', handleSendMessage);
    }
    
    // Quick replies
    quickReplyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.getAttribute('data-message');
            sendMessage(message);
        });
    });
    
    // Auto-resize textarea
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
}

/**
 * Handle Send Message
 */
function handleSendMessage(e) {
    e.preventDefault();
    
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    sendMessage(message);
    chatInput.value = '';
    chatInput.style.height = 'auto';
}

/**
 * Send Message
 */
async function sendMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Add user message
    addMessageToChat('user', message);
    
    // Scroll to bottom
    scrollToBottom();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        hideTypingIndicator();
        
        // Add bot response
        if (data.response) {
            setTimeout(() => {
                addMessageToChat('bot', data.response);
                scrollToBottom();
            }, 500);
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTypingIndicator();
        addMessageToChat('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

/**
 * Add Message to Chat
 */
function addMessageToChat(type, message) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'bot' ? '🤖' : '👤';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    // Handle multi-line messages
    bubble.style.whiteSpace = 'pre-line';
    bubble.textContent = message;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = formatTime(new Date());
    
    content.appendChild(bubble);
    content.appendChild(time);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
}

/**
 * Show Typing Indicator
 */
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

/**
 * Hide Typing Indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll to Bottom
 */
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Mark Messages as Read
 */
function markMessagesAsRead() {
    const chatBadge = document.getElementById('chatBadge');
    if (chatBadge) {
        chatBadge.style.display = 'none';
    }
}

/**
 * Format Time
 */
function formatTime(date) {
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    return `${formattedHours}:${formattedMinutes} ${ampm}`;
}

/**
 * Show Welcome Message if Needed
 */
function showWelcomeMessageIfNeeded() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Check if chat is empty (no messages)
    if (chatMessages && chatMessages.children.length === 0) {
        // Check if welcome message was already shown in this session
        const welcomeShown = sessionStorage.getItem('chatWelcomeShown');
        
        if (!welcomeShown) {
            // Add welcome message
            setTimeout(() => {
                const welcomeMessage = "Hi! I'm Sweetie 🤖\n\nI'm your LibraNet assistant! I can help you with:\n\n📚 Finding books and checking availability\n💳 Subscription plans and benefits\n📖 Understanding words or paragraphs (English/Hindi)\n❓ Any questions about the library\n\nHow can I assist you today?";
                addMessageToChat('bot', welcomeMessage);
                
                // Mark as shown for this session
                sessionStorage.setItem('chatWelcomeShown', 'true');
            }, 800);
        }
    }
}