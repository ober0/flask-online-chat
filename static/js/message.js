document.getElementById('send').addEventListener('click', function () {

    let messageInput = document.getElementById('message-input')
    let messageText = messageInput.value
    messageInput.value = ''

    const data = {
        message_to: this.getAttribute('ForUserId'),
        text_message: messageText
    }

    fetch('/sendMsg', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            if (result.result == false) {
                alert('Сообщение не отправлено!')
            }
            else{
                let newMessageDiv = document.createElement('div');
                newMessageDiv.classList.add('message');
                newMessageDiv.classList.add('sender');
                newMessageDiv.innerHTML = messageText;
                document.getElementById('messages').appendChild(newMessageDiv);
                let chatContainer = document.getElementById("chat-container");
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        })

})