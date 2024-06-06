const goBottom = document.getElementById('goBottom')
const exit = document.getElementById('goMenu')
const clear = document.getElementById('clear')

goBottom.addEventListener('click', function () {
    let chatContainer = document.getElementById("chat-container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
})


exit.addEventListener('click', function () {
    window.location.href = '/'
})


clear.addEventListener('click', function () {
    let user_id = this.getAttribute('user_id')
    console.log(user_id)
    let data = {
        chat: user_id
    }

    fetch('/clear', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const allMessages = document.querySelectorAll('.message');
                allMessages.forEach(message => {
                    message.remove();
                });
            }
        })
    })