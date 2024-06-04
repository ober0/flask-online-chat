const userDivs = document.querySelectorAll('.user-div');

userDivs.forEach(div => {
    div.addEventListener('click', function() {
        let id = this.getAttribute('link')
        window.location.href = '/chat/'+id;
    });
});
