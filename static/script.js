document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const modelSelect = document.getElementById('model-select');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessageToChat('You', message);
        userInput.value = '';

        const selectedModel = modelSelect.value;

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, model: selectedModel }),
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat('RadheBot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('RadheBot', 'Oops! Kuch gadbad ho gayi. Phir se try karo.');
        });
    }

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
