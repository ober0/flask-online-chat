function checkMessage() {
    let data = {
        from_id: document.getElementById('send').getAttribute('ForUserId')
    }


    fetch('/checkMsg', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                let message = result.message


                let newMessageDiv = document.createElement('div');
                newMessageDiv.classList.add('message');
                newMessageDiv.innerHTML = message;
                document.getElementById('messages').appendChild(newMessageDiv);

                let chatContainer = document.getElementById("chat-container");
                chatContainer.scrollTop = chatContainer.scrollHeight;


            }
        })


}

setInterval(checkMessage, 300)