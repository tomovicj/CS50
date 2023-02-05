document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('nav');
    const create_new = document.querySelector('#new');
    const feed = document.querySelector('#feed');
    const profile_div = document.querySelector('#profile');
    

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
                post_button.setAttribute('listener', 'true');
                post_button.addEventListener('click', function (event) {
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
            profile_div.style.display = 'none';
            create_new.style.display = 'block';
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
                edit_button.setAttribute('listener', 'true');
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

    function pagination(type, num_pages, on_page, additionally) {
        const pagination = document.createElement('ul');
        pagination.classList.add('pagination', 'justify-content-center', 'mt-3');
        feed.appendChild(pagination);

        const previous = document.createElement('li');
        previous.classList.add('page-item');
        previous.style.cursor = 'pointer';
        pagination.appendChild(previous);
        if (!(on_page > 1)) {
            previous.classList.add('disabled');
            previous.style.cursor = 'default';
        }
        else {
            if (type === 'profile') {
                previous.addEventListener('click', () => load_feed(type, on_page - 1, additionally));
            }
            else {
                previous.addEventListener('click', () => load_feed(type, on_page - 1));
            }
        }

        let span = document.createElement('span');
        span.classList.add('page-link');
        span.textContent = 'Previous';
        previous.appendChild(span);

        for (let i = 1; i < num_pages + 1; i++) {
            const page = document.createElement('li');
            page.classList.add('page-item');
            page.style.cursor = 'pointer';
            pagination.appendChild(page);

            const span = document.createElement('span');
            span.classList.add('page-link');
            span.textContent = i;
            page.appendChild(span);

            if (i === on_page) {
                page.classList.add('active');
            }

            page.addEventListener('click', () => {
                load_feed(type, i, additionally);
            })
        }

        const next = document.createElement('li');
        next.classList.add('page-item');
        next.style.cursor = 'pointer';
        pagination.appendChild(next);
        if (!(on_page < num_pages)) {
            next.classList.add('disabled');
            next.style.cursor = 'default';
        }
        else {
            if (type === 'profile') {
                next.addEventListener('click', () => load_feed(type, on_page + 1, additionally));
            }
            else {
                next.addEventListener('click', () => load_feed(type, on_page + 1));
            }
        }
        
        span = document.createElement('span');
        span.classList.add('page-link');
        span.textContent = 'Next';
        next.appendChild(span);

    }


    function profile(username) {
        window.history.pushState({}, `Social Network | ${username}`, `/@${username}`);
        document.title = `Social Network | ${username}`;
        window.onpopstate = (event) => {
            window.history.pushState({}, 'Social Network', '/');
            document.title = 'Social Network';
            load_feed();
        };

        if (create_new) {
            create_new.style.display = 'none';
        }
        profile_div.style.display = 'block';

        document.querySelector('#place-for-follow-btn').innerHTML = '';
        const username_palce = document.querySelector('#username');
        const followers_count = document.querySelector('#followers-count');
        const following_count = document.querySelector('#following-count');
        username_palce.textContent = '';
        followers_count.textContent = '';
        following_count.textContent = '';
        fetch(`/profile/${username}`)
        .then(response => response.json())
        .then(data => {
            username_palce.textContent = data.username;
            followers_count.textContent = data.followers_count;
            following_count.textContent = data.following_count;
            if (data.authenticated & !data.mine) {
                const follow_btn = document.createElement('span');
                follow_btn.classList.add('btn', 'w-100', data.following_status ? 'btn-outline-primary' : 'btn-primary');
                follow_btn.textContent = data.following_status ? 'Unfollow' : 'Follow';
                document.querySelector('#place-for-follow-btn').appendChild(follow_btn);

                follow_btn.addEventListener('click', () => {
                    fetch('/follow', {
                        method: 'PUT',
                        body: JSON.stringify({
                            user_id: data.id
                        })
                    })
                    .then(response => {
                        profile(username);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        load_feed('profile', 1, `username=${username}`);
    }


    function load_feed(type = 'all', page = 1, additionally = null) {
        // Don't show form for new post on profile page
        if (type !== 'profile') {
            profile_div.style.display = 'none';
            new_form();
        }

        // Clear previous feed posts
        feed.innerHTML = '';
    
        fetch(`/feed/${type}?page=${page}&${additionally}`)
        .then(response => response.json())
        .then(data => {
            data['posts'].forEach(post => {
                const row = document.createElement('div');
                row.setAttribute('id',`post-${post.id}`);
                row.classList.add('row', 'border', 'p-2', 'mb-1');
                row.style.display = 'block';
                feed.appendChild(row);
    
                const author = document.createElement('h3');
                author.textContent = post.author;
                author.style.cursor = 'pointer';
                row.appendChild(author);
                author.addEventListener('click', () => profile(post.author))
    
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
            if (data.posts.length === 0){
                const text = document.createElement('h2');
                text.textContent = 'Sorry, there are no posts yet :(';
                text.classList.add('text-center', 'mt-2');
                feed.appendChild(text);
            }
            else {
                pagination(type, data["num_pages"], data["on_page"], additionally);
            }
            
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    
    // When clicked on All Posts load all posts
    document.querySelector('#all-posts').addEventListener('click', () => load_feed('all'));
    // When clicked on Following load following page
    try {
        document.querySelector('#following').addEventListener('click', () => load_feed('following'));
        const username_nav = nav.querySelector('#username-nav');
        username_nav.addEventListener('click', () => profile(username_nav.textContent));
    } catch {}
    nav.querySelectorAll('span').forEach((link) => {
        link.addEventListener('click', (event) => {
            if (link.id !== 'username-nav') {
                window.history.pushState({}, 'Social Network', '/');
                document.title = 'Social Network';
            }
        });
    })

    // Load profile if page ends with '/@{username}'
    if (window.location.pathname.slice(0, 2) === '/@') {
        const username = window.location.pathname.substring(2);
        profile(username);
    }
    else {
        load_feed();
    }
});


