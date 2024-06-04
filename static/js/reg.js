document.getElementById('iconPassword').addEventListener('mousedown', function() {
    const passwordInput = document.getElementById('password');
    passwordInput.type = 'text';
    this.src = this.getAttribute('data-open')
});

document.getElementById('iconPassword').addEventListener('mouseup', function() {
    const passwordInput = document.getElementById('password');
    passwordInput.type = 'password';
    this.src = this.getAttribute('data-hidden')
});

document.getElementById('iconPassword').addEventListener('mouseleave', function() {
    const passwordInput = document.getElementById('password');
    passwordInput.type = 'password';
    this.src = this.getAttribute('data-hidden')
});


function displayPasswordError(message) {
    const passwordError = document.getElementById('password-error');
    const passwordInput = document.getElementById('password');
    const _window = document.querySelector('.container');

    passwordError.textContent = message;
    passwordInput.style.boxShadow = '0 0 5px red';
    passwordInput.style.borderColor = 'pink';
    _window.style.borderColor = 'pink';
    _window.style.boxShadow = '0 0 20px red';
    return false;
}

function displayEmailError(message) {
    const emailError = document.getElementById('email-error');
    const emailInput = document.getElementById('email');
    const _window = document.querySelector('.container');

    emailError.textContent = 'Некорректный адрес эл.почты';
    emailInput.style.boxShadow = '0 0 5px red';
    emailInput.style.borderColor = 'pink';
    _window.style.borderColor = 'pink';
    _window.style.boxShadow = '0 0 20px red';
    return false;
}

document.getElementById('form-main-button').addEventListener('click', function () {
    let isValid = true;

    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const _window = document.querySelector('.container');
    const form = document.getElementById('auth-form')
    const nameInput = document.getElementById('name')

    emailError.textContent = '';
    passwordError.textContent = '';
    emailInput.style.boxShadow = '0 0 5px aqua';
    emailInput.style.borderColor = 'white';
    passwordInput.style.boxShadow = '0 0 5px aqua';
    passwordInput.style.borderColor = 'white';
    _window.style.border = '2px solid whitesmoke';
    _window.style.boxShadow = '0 0 20px aqua';
    nameInput.style.boxShadow = '0 0 5px aqua';
        nameInput.style.borderColor = 'white';
    document.getElementById('head-h1').innerText = ''



    const emailValue = emailInput.value;
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    if (!emailPattern.test(emailValue)) {
        isValid = false;
        emailError.textContent = 'Некорректный адрес эл.почты';
        emailInput.style.boxShadow = '0 0 5px red';
        emailInput.style.borderColor = 'pink';
        _window.style.borderColor = 'pink';
        _window.style.boxShadow = '0 0 20px red';
    }

    const passwordValue = passwordInput.value;

    if (passwordValue.length < 8) {
        isValid = displayPasswordError('Пароль должен быть минимум из 8 символов');
    }
    if (!/[a-zA-Z]/.test(passwordValue)){
        isValid = displayPasswordError('В пароле должна быть минимум 1 буква');
    }
    if (!/\d/.test(passwordValue)){
        isValid = displayPasswordError('В пароле должна быть минимум 1 цифра');
    }
    if (/[^a-zA-Z0-9]/.test(passwordValue)) {
        isValid = displayPasswordError('Пароль может содержать буквы только латинского алфавита');
    }


    if (!/[а-яА-Яa-zA-Z]/.test(nameInput.value) || /[0-9]/.test(nameInput.value)) {
        document.getElementById('name-error').textContent = 'Поле не может быть пустым или быть числовым';
        nameInput.style.boxShadow = '0 0 5px red';
        nameInput.style.borderColor = 'pink';
        window.style.borderColor = 'pink';
        window.style.boxShadow = '0 0 20px red';
        isValid = false;
    }








    if (isValid) {
        const name = document.getElementById('name').value
        const email = emailValue;
        const password = passwordValue;
        const data = {
            name: name,
            email: email,
            password: password
        }

        fetch('/reg',{
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())

            .then(result => {
                if (result.result){
                    window.location.href = '/confirm_email'
                }
                else if(result.result == 'test'){
                    alert(1)
                }
                else {
                    emailValue.value = ''
                    passwordValue.value = ''
                    _window.style.borderColor = 'pink';
                    _window.style.boxShadow = '0 0 20px red';
                    document.getElementById('head-h1').innerText = 'Email уже используется'
                }
            })
    }
});
