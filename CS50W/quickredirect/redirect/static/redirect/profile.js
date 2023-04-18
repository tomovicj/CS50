const popUp = new bootstrap.Modal('#popUp');
const popUpEl = document.querySelector('#popUp');

const form = document.querySelector('form[id="main"]');
const title = document.querySelector('#popUpLabel');
const error_msg = document.querySelector('#popup-message');
const username_div = document.querySelector('#username-div');
const email_div = document.querySelector('#email-div');
const password_div = document.querySelector('#password-div');
const type = form.querySelector('input[name="type"]');
const input = form.querySelector('#input-field');
const old_pass = form.querySelector('#old-password');
const lable = form.querySelector('[for="input-field"]');


document.querySelector('#username-edit').addEventListener('click', () => {
    title.textContent = 'Username Edit';
    username_div.hidden = false;
    lable.textContent = 'New username:';
    input.type = 'text';
    type.value = 'username';
    popUp.show();
})

document.querySelector('#email-edit').addEventListener('click', () => {
    title.textContent = 'Email Edit';
    email_div.hidden = false;
    lable.textContent = 'New email:';
    input.type = 'email';
    type.value = 'email';
    popUp.show();
})

document.querySelector('#password-edit').addEventListener('click', () => {
    title.textContent = 'Password Edit';
    password_div.hidden = false;
    old_pass.required = true;
    lable.textContent = 'New password:';
    input.type = 'password';
    type.value = 'password';
    popUp.show();
})

// After popup is closed, all divs will be hidden
popUpEl.addEventListener('hidden.bs.modal', () => {
    error_msg.hidden = true;
    username_div.hidden = true;
    email_div.hidden = true;
    password_div.hidden = true;
    old_pass.required = false;
    old_pass.value = '';
    input.value = '';
}) 

// Submit the form when edit button is clicked
document.querySelector('#edit-button').addEventListener('click', () => {
    const chosen_type = type.value;
    // If input field is empty
    if (input.value === '') {
        error_msg.textContent = 'Field is required';
        error_msg.hidden = false;
        return;
    }
    // Evaluate if inputted data is an email
    if (chosen_type === 'email') {
        const emailRegex = /^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$/;
        if (!emailRegex.test(input.value)) {
            error_msg.textContent = 'Looks like your email address is invalid';
            error_msg.hidden = false;
            return;
        }
    }
    // Chack if current password field is empty
    if (chosen_type === 'password') {
        if (old_pass.value === '') {
            error_msg.textContent = 'You did not entered the current password';
            error_msg.hidden = false;
            return;
        }
        if (old_pass.value === input.value) {
            error_msg.textContent = 'You can not set the new password to the current password';
            error_msg.hidden = false;
            return;
        }
    }
    form.submit();
})
