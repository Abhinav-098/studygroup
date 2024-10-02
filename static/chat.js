var socket = io();

// Send message when user clicks "Send" button
function sendMessage() {
    var message = document.getElementById("chat-input").value;
    if (message) {
        socket.emit('chat_message', message);  // Emit chat message to the server
        document.getElementById("chat-input").value = "";  // Clear input field
    }
}

// Listen for chat messages from the server
socket.on('message', function(msg) {
    displayMessage(msg);
});

// Function to display chat messages in the chat section
function displayMessage(msg) {
    var chatMessages = document.getElementById("chat-messages");
    var newMessage = document.createElement("div");
    newMessage.textContent = msg;
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;  // Scroll to the bottom
}