document.getElementById('add-chat').addEventListener('click', function () {
    const id = this.getAttribute('user-id');
    const message = document.getElementById('message');
    let data;


    if (this.getAttribute('do') == 'add') {
        data = {
            command: 'add_user',
            user_id: id
        };
    } else if (this.getAttribute('do') == 'remove') {
        data = {
            command: 'remove_user',
            user_id: id
        };
    } else {
        data = {
            command: 'unknown',
            user_id: id
        };
    }



    fetch('/user/' + id, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
            if (result.result){
                message.innerText = 'Успешно!'
                message.style.color = 'green'
                setTimeout(3000, function () {
                    message.innerText = ''
                })
            }
            if (!result.result){
                message.innerText = result.message
                message.style.color = 'red'
            }
        })
});
