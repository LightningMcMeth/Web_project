const socket = new WebSocket("ws://127.0.0.1:8000/ws");


function sendMessage() {

    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;

    console.log("sending message: " + message);
    socket.send(message);

    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p>Sent: ${message}</p><br>`;
    messageInput.value = '';
}


socket.onopen = function (e ) {
    console.log('connection opened!');
}


socket.onmessage = function(e) {

    console.log("message from server: " + e.data);

    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p>Received: ${e.data}</p><br>`;
};


socket.onclose = function(e) {
    console.error('Socket closed unexpectedly :(');
};