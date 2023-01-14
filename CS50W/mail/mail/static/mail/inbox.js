document.addEventListener('DOMContentLoaded', function() {

  const email_view = document.createElement('div');
  document.querySelector('body').appendChild(email_view);
  email_view.setAttribute('id', 'email-view');
  email_view.classList.add("container")
  email_view.style.display = 'none';

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email("", "", ""));

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email(recipients, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  // Send email
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(() => {
        event.preventDefault();
        load_mailbox('sent');
      });
    });    
  }      
  

  function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Get emails for the chosen mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const div = document.createElement('div');
      document.querySelector('#emails-view').appendChild(div);
      div.classList.add('border', 'p-2');
      div.addEventListener('click', () => load_email(email.id));

      const pSubject = document.createElement('h3');
      const subject = document.createTextNode(email.subject);
      pSubject.appendChild(subject);
      div.appendChild(pSubject);
      pSubject.classList.add('m-0');
      
      const pSender = document.createElement('p');
      const sender = document.createTextNode(email.sender);
      pSender.appendChild(sender);
      div.appendChild(pSender);
      
      const pTimestamp = document.createElement('p');
      const timestamp = document.createTextNode(email.timestamp);
      pTimestamp.appendChild(timestamp);
      div.appendChild(pTimestamp);
      
      div.querySelectorAll('p').forEach(p => {
        p.classList.add('m-0');
      })  
      
      if (email.read === true) {
        div.classList.add("read")
      }  
    });        
});    
}

function load_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

      // Mark email as read
      if (email.read === false) {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });   
      }

      document.querySelector('#email-view').style.display = 'block';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';

      // Shows selected email
      const email_view = document.querySelector('#email-view');
      email_view.innerHTML = `<p class="m-0"><b>From: </b>${email.sender}</p>
                              <p class="m-0"><b>To: </b>${email.recipients}</p>
                              <p class="m-0"><b>Subject: </b>${email.subject}</p>
                              <p><b>Timestamp: </b>${email.timestamp}</p>
                              <hr>
                              <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                              <button class="btn btn-sm btn-outline-primary" id="archive">${email.archived ? 'Unarchive' : 'Archive'}</button>
                              <hr>
                              <p>${email.body}</p>`;

      // Pre-fill the composition form when reply
      document.querySelector('#reply').addEventListener('click', () => {
        let subject = '';
        if (email.subject.slice(0, 3) !== 'Re:') {
          subject = `Re: ${email.subject}`;
        } else {
          subject = email.subject;
          }
        compose_email(email.sender, subject, `On ${email.timestamp} ${email.sender} wrote: ${email.body}`);
      });

      // If the user is sender of a mail than don't show archive button
      const button = document.querySelector('#archive');
      if (document.querySelector('h2').innerHTML === email.sender) {
        button.style.display = 'none';
      }

      // Archive / Unarchive when button is pressed
      button.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => load_mailbox('inbox'));        
      });
  });

}