// Get rid off Sign in button from nav bar
document.querySelector('#nav-signin-button').hidden = true;


addEventListener('DOMContentLoaded', () => {
    const signIN_button = document.querySelector('#signin-button');
    const signUP_button = document.querySelector('#signup-button');
    const submit_button = document.querySelector('#submit-button');
    const auth_type = document.querySelector('#auth-type');
    const username_div = document.querySelector('#username-div');
    const password_confirm_div = document.querySelector('#password-confirm-div');

    function signIN() {
        signUP_button.classList.remove('bg-primary', 'text-white');
        signUP_button.classList.add('pointer');
        signIN_button.classList.add('bg-primary', 'text-white');
        signIN_button.classList.remove('pointer');
        submit_button.textContent = 'Login';
        auth_type.value = 'login';
        username_div.hidden = true;
        password_confirm_div.hidden = true;
    }

    function signUP() {
        signIN_button.classList.remove('bg-primary', 'text-white');
        signIN_button.classList.add('pointer');
        signUP_button.classList.add('bg-primary', 'text-white');
        signUP_button.classList.remove('pointer');
        submit_button.textContent = 'Register';
        auth_type.value = 'register';
        username_div.hidden = false;
        password_confirm_div.hidden = false;
        try {
            document.querySelector('.alert').hidden = true;
        }
        catch {}
    }

    signIN_button.addEventListener('click', () => signIN());
    signUP_button.addEventListener('click', () => signUP());
});