const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');
const clearChatBtn = document.getElementById('clearChatBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
// const html = window.marked(someMarkdownText);

function createMessageElement(message, sender) {
const messageContainer = document.createElement('div');
messageContainer.classList.add('flex', 'items-end', 'gap-3', sender === 'user' ? 'justify-end' : 'justify-start');

const avatar = document.createElement('img');
avatar.classList.add('avatar');
avatar.src = sender === 'user'
    ? 'https://encrypted-tbn0.gstatic.com/images?q=tbni:ANd9GcR9iS4887MqYnErWEHhNy-G2i11h3mG8IG9-Q&s'
    : 'https://cdn-icons-png.flaticon.com/512/4712/4712109.png';

const messageBubble = document.createElement('div');
messageBubble.classList.add(
    'max-w-[70%]', 'px-4', 'py-3', 'rounded-2xl', 'shadow-md', 'text-sm',
    'leading-relaxed', 'font-medium', 'transition-all', 'duration-200'
);

if (sender === 'user') {
    messageBubble.classList.add('bg-gradient-to-r', 'from-pink-400', 'via-red-400', 'to-yellow-400', 'text-white', 'rounded-br-none');
} else {
    messageBubble.classList.add('bg-gradient-to-r', 'from-purple-300', 'via-indigo-400', 'to-blue-400', 'text-white', 'rounded-bl-none');
}

messageBubble.innerHTML = message; // Use innerHTML for HTML content

if (sender === 'user') {
    messageContainer.appendChild(messageBubble);
    messageContainer.appendChild(avatar);
} else {
    messageContainer.appendChild(avatar);
    messageContainer.appendChild(messageBubble);
}

chatMessages.appendChild(messageContainer);
chatMessages.scrollTop = chatMessages.scrollHeight;

return messageBubble; // Return bubble for streaming updates
}

async function sendToBot(message) {
loadingIndicator.style.display = 'block';

try {
    const response = await fetch('/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: message })
    });

    loadingIndicator.style.display = 'none';

    if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Create a single message bubble for the bot's response
    let botMessageBubble = createMessageElement('', 'bot');
    let fullMessage = '';

    // Read the streaming response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(line => line.trim());

    for (const line of lines) {
        try {
        const data = JSON.parse(line);
        if (data.error) {
            botMessageBubble.innerHTML = 'Error: ' + data.error;
            return;
        }
        if (data.chunk) {
            fullMessage += data.chunk + ' ';
            // Render the HTML directly
            botMessageBubble.innerHTML = fullMessage.trim();
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        if (data.done) {
            // Streaming complete
            return;
        }
        } catch (e) {
        console.error('Error parsing chunk:', e);
        }
    }
    }
} catch (error) {
    loadingIndicator.style.display = 'none';
    createMessageElement('Network error: ' + error.message, 'bot');
}
}

chatForm.addEventListener('submit', (e) => {
e.preventDefault();
const message = chatInput.value.trim();
if (message) {
    createMessageElement(message, 'user');
    chatInput.value = '';
    sendToBot(message);  // 🚀 Send message to Django backend
}
});

clearChatBtn.addEventListener('click', () => {
chatMessages.innerHTML = '';
});