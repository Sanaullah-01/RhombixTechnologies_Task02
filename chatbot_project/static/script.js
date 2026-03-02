document.addEventListener('DOMContentLoaded', () => {
    const chatLauncher = document.getElementById('chatLauncher');
    const chatContainer = document.getElementById('chatContainer');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatbox = document.getElementById('chatbox');
    const contactModal = document.getElementById('contactModal');

    // Toggle Chat
    chatLauncher.addEventListener('click', () => {
        chatContainer.classList.remove('hidden');
        userInput.focus();
    });

    closeChatBtn.addEventListener('click', () => {
        chatContainer.classList.add('hidden');
    });

    // Handle Form Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        // Basic input sanitization to prevent empty messages
        if (!message) return;

        // Clear input
        userInput.value = '';

        // Add user message to UI
        addMessage(message, 'user');

        // Show typing indicator
        const typingId = showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Remove typing indicator
            removeElement(typingId);

            if (response.ok) {
                // Determine if it was a fallback response
                const isFallback = (data.intent === 'fallback' || data.confidence < 0.6);
                addMessage(data.response, 'bot', isFallback);
            } else {
                addMessage("Sorry, I'm having trouble connecting to the server.", 'bot', true);
            }
        } catch (error) {
            console.error("Error communicating with server:", error);
            removeElement(typingId);
            addMessage("Network error. Please try again later.", 'bot', true);
        }
    });

    // DOM Manipulation Functions
    function addMessage(text, sender, isFallback = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;
        
        msgDiv.appendChild(bubble);
        
        // Add "Talk to Human" button if fallback
        if (isFallback && sender === 'bot') {
            const btn = document.createElement('button');
            btn.className = 'talk-human-btn';
            btn.textContent = 'Talk to Human';
            btn.onclick = openModal;
            
            // Container for bubble + button
            const container = document.createElement('div');
            container.appendChild(bubble);
            container.appendChild(btn);
            
            msgDiv.innerHTML = '';
            msgDiv.appendChild(container);
        }

        chatbox.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message bot-message`;
        msgDiv.id = id;
        
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        
        bubble.appendChild(indicator);
        msgDiv.appendChild(bubble);
        chatbox.appendChild(msgDiv);
        scrollToBottom();
        
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Modal behavior functions
    window.openModal = function() {
        contactModal.style.display = 'flex';
    };

    window.closeModal = function() {
        contactModal.style.display = 'none';
        // Mock successful submission
        if(contactModal.querySelector('textarea').value) {
            addMessage("Support request sent! A human agent will email you shortly.", 'bot');
            contactModal.querySelector('textarea').value = '';
            contactModal.querySelector('input').value = '';
        }
    };

    // Close modal if clicking outside content
    contactModal.addEventListener('click', (e) => {
        if (e.target === contactModal) {
            closeModal();
        }
    });

    const closeBtn = document.querySelector('.close-modal');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
});
