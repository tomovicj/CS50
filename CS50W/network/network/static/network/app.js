document.addEventListener('DOMContentLoaded', () => {
    const create_new = document.querySelector('#new');
    const feed = document.querySelector('#feed');


    function new_form() {
        if (create_new !== null) {
            const alert = create_new.querySelector('.alert-danger');
            const post_button = create_new.querySelector('#post_button');

            alert.style.display = 'none';
            create_new.querySelector('h3').textContent = 'New post:';
            create_new.querySelector('#new_content').value = '';
            post_button.style.display = 'block';
            document.querySelector('#edit_button').style.display = 'none';
        
            // Add event listener ONLY if there is no listener added before
            if (post_button.getAttribute('listener') !== 'true') {
                post_button.addEventListener('click', function (event) {
                    const elementClicked = event.target;
                    elementClicked.setAttribute('listener', 'true');
                    // Send post to the server
                    event.preventDefault();
                    fetch('/post', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': create_new.querySelector('input[name="csrfmiddlewaretoken"]').value
                        },
                        body: JSON.stringify({
                            content: create_new.querySelector('#new_content').value
                        })
                    })
                    .then(response => {
                        if (response.ok) {
                            load_feed();
                        }
                        else {
                            alert.textContent = 'Unsuccessfully posted!';
                            alert.style.display = 'block';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            }
        }
    }

    function like(post_id) {
        const like_section = document.querySelector(`#post-${post_id}`).querySelector('#like-section');

        const liked_img = '/static/network/img/liked.png';
        const unliked_img = '/static/network/img/unliked.png';
        const like_button = like_section.querySelector('img');
        const like_count = like_section.querySelector('p');

        fetch('/like', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: post_id,
            })
        })
        .then(response => response.json())
        .then(data => {
            like_button.src = data.liked ? liked_img : unliked_img;
            if (typeof data.likes == 'number') {
                like_count.textContent = data.likes;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function edit(post_id) {
        const start_text = document.querySelector(`#post-${post_id}`).querySelector('.content').textContent;
        const edit_button = document.querySelector('#edit_button');
        const alert = create_new.querySelector('.alert-danger');

        alert.style.display = 'none';
        create_new.querySelector('h3').textContent = 'Edit post:';
        create_new.querySelector('#new_content').value = start_text;
        document.querySelector('#post_button').style.display = 'none';
        edit_button.style.display = 'block';

        // Add event listener ONLY if there is no listener added before    
        if (edit_button.getAttribute('listener') !== 'true') {
            edit_button.addEventListener('click', function (event) {
                const elementClicked = event.target;
                elementClicked.setAttribute('listener', 'true');
                // Send post to the server
                event.preventDefault();
                fetch(`/edit/${post_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': create_new.querySelector('input[name="csrfmiddlewaretoken"]').value
                    },
                    body: JSON.stringify({
                        content: create_new.querySelector('#new_content').value
                    })
                })
                .then(response => {
                    if (response.ok) {
                        load_feed();
                    }
                    else {
                        alert.textContent = 'Unsuccessfully edited post!';
                        alert.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
           });
       }
    }


    function load_feed(type = 'all') {
        new_form();
        feed.innerHTML = '';
    
        fetch(`/feed/${type}`)
        .then(response => response.json())
        .then(posts => {
            posts['posts'].forEach(post => {
                const row = document.createElement('div');
                row.setAttribute('id',`post-${post.id}`);
                row.classList.add('row', 'border', 'p-2', 'mb-1');
                row.style.display = 'block';
                feed.appendChild(row);
    
                const author = document.createElement('h3');
                author.textContent = post.author;
                row.appendChild(author);
    
                const content = document.createElement('p');
                content.textContent = post.content;
                content.classList.add('content');
                row.appendChild(content);
    
                const post_time = document.createElement('p');
                const datetime = new Date(post.time);
                post_time.textContent = datetime.toLocaleString();
                post_time.classList.add('text-muted', 'mb-1');
                row.appendChild(post_time);

                // Like section
                const like_section = document.createElement('div');
                like_section.setAttribute('id', 'like-section');
                like_section.classList.add('d-flex', 'align-items-center');
                row.appendChild(like_section);


                const liked = '/static/network/img/liked.png';
                const unliked = '/static/network/img/unliked.png';
                const like_button = document.createElement('img');
                like_button.src = post.liked ? liked : unliked;
                like_button.classList.add('like-button', 'mr-1');
                like_section.appendChild(like_button);

                like_button.addEventListener('click', () => like(post.id))

                const likes = document.createElement('p');
                likes.textContent = post.likes;
                likes.classList.add('mb-0');
                like_section.appendChild(likes);

                if (post.mine) {
                    const edit_link = document.createElement('a');
                    edit_link.href = '#';
                    edit_link.textContent = 'Edit';
                    // edit_link.classList.add();
                    row.appendChild(edit_link);

                    edit_link.addEventListener('click', () => edit(post.id))
                }
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    
    // Reload page when 'logo' is clicked
    document.querySelector('.navbar-brand').addEventListener('click', () => location.reload());
    // When clicked on All Posts load all posts
    document.querySelector('#all-posts').addEventListener('click', () => load_feed('all'));
    // When clicked on Following load following page
    try {
        document.querySelector('#following').addEventListener('click', () => load_feed('following'));
    } catch {}
    load_feed();
});


