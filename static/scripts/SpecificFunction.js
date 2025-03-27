document.addEventListener("DOMContentLoaded", function() {
    let loggedInUserId;

    // Fetch session data
    fetch('/get_session')
        .then(response => response.json())
        .then(data => {
            if (data.session) {
                loggedInUserId = data.session_id;
                filter3DotMenu(loggedInUserId);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(error => console.error("Error fetching session:", error));

    document.body.addEventListener("click", function(event) {
        const targetId = event.target.id;
        let action = null;

        if (targetId === "fms-post-hearticon") {
            action = "liked";
        } else if (targetId === "fms-post-bookmarkicon") {
            action = "bookmark";
        } else if (targetId === "addCommentButton") {
            const commentInput = document.getElementById('commentInput');
            const commentText = commentInput.value.trim();
            if (!commentText) return;

            const postElement = document.querySelector(".fms-post-layout");
            const postId = postElement?.getAttribute("data-post-id");
            const postType = document.querySelector("script[data-type]")?.getAttribute("data-type") || "";

            if (!postId) {
                console.error("Post ID not found.");
                return;
            }

            fetch('/createcomment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment: commentText, page_type: postType, id: postId })
            })
            .then(response => {
                if (response.status === 204) {
                    return null;  // No content to parse
                }
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (!data) return;

                const commentsList = document.querySelector('.fms-comments-list');
                const newComment = document.createElement('div');
                newComment.className = 'fms-comment';

                const profileImg = document.createElement('img');
                profileImg.src = '../static/src/img/default-pfp.png';
                profileImg.alt = 'Profile Picture';
                profileImg.className = 'fms-pfp-placeholder';
                profileImg.style.width = '40px';
                profileImg.style.height = '40px';
                profileImg.style.borderRadius = '50%';

                const usernameSpan = document.createElement('span');
                usernameSpan.className = 'fms-username-placeholder';
                usernameSpan.textContent = data.username + ': ';

                const commentSpan = document.createElement('span');
                commentSpan.className = 'fms-comment-text';
                commentSpan.textContent = commentText;

                newComment.appendChild(profileImg);
                newComment.appendChild(usernameSpan);
                newComment.appendChild(commentSpan);

                commentsList.appendChild(newComment);
                commentInput.value = '';
            })
            .catch(error => console.error("Error posting comment:", error));

            return; // Prevent further processing
        }

        if (!action) return;

        const postElement = document.querySelector(".fms-post-layout");
        const postId = postElement?.getAttribute("data-post-id");
        if (!postId) return;

        fetch("/engagement", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ post_id: postId, action: action }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
                return;
            }

            if (action === "liked") {
                updateLikeUI(data.liked, data.likes_count);
            } else if (action === "bookmark") {
                updateBookmarkUI(data.bookmark);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Fetch and load comments
    const commentsList = document.querySelector('.fms-comments-list');
    const postId = document.querySelector(".fms-post-layout").getAttribute("data-post-id");

    if (postId) {
        fetch(`/comment?post_id=${postId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                commentsList.innerHTML = data.html;
            })
            .catch(error => console.error('Error loading comments:', error));
    }

    // Function to update like UI
    function updateLikeUI(liked, count) {
        const likeCountElement = document.getElementById("likeCount");
        const likeIcon = document.getElementById("fms-post-hearticon");

        likeIcon.src = liked
            ? "../static/src/icon/icons8-heart-red-50.png"
            : "../static/src/icon/icons8-heart-50.png";

        if (likeCountElement) {
            likeCountElement.textContent = `(${count})`;
        }
    }

    // Function to update bookmark UI
    function updateBookmarkUI(bookmark) {
        const bookmarkIcon = document.getElementById("fms-post-bookmarkicon");
        if (!bookmarkIcon) return;

        bookmarkIcon.src = bookmark
            ? "../static/src/icon/icons8-bookmark-evendarkergreen-500.png"
            : "../static/src/icon/icons8-bookmark-50.png";
    }

    // Function to filter 3-dot menu based on user ID
    function filter3DotMenu(loggedInUserId) {
        document.querySelectorAll(".fms-post-layout").forEach(post => {
            const postUserId = post.getAttribute("data-user-id");
            const dropdown = post.querySelector(".fms-dropdown-content");

            if (dropdown) {
                const reportPost = dropdown.querySelector("#fms-reportposticon")?.parentElement;
                const reportUser  = dropdown.querySelector("#fms-reportusericon")?.parentElement;
                const editPost = dropdown.querySelector("#fms-editicon")?.parentElement;
                const deletePost = dropdown.querySelector("#fms-deleteicon")?.parentElement;

                if (reportPost && reportUser  && editPost && deletePost) {
                    if (String(loggedInUserId) === String(postUserId)) {
                        reportPost.style.display = "none";
                        reportUser .style.display = "none";
                        editPost.style.display = "block";
                        deletePost.style.display = "block";
                    } else {
                        reportPost.style.display = "block";
                        reportUser .style.display = "block";
                        editPost.style.display = "none";
                        deletePost.style.display = "none";
                    }
                }
            }
        });
    }

    // Header profile picture dropdown functionality
    const profileImg = document.getElementById('hb-pfp-img');
    const popupMenu = document.getElementById('hb-popup-menu');

    if (profileImg && popupMenu) {
        profileImg.addEventListener('click', function(event) {
            popupMenu.style.display = popupMenu.style.display === "block" ? "none" : "block";
            event.stopPropagation();
        });

        document.addEventListener('click', function(event) {
            if (!profileImg.contains(event.target) && !popupMenu.contains(event.target)) {
                popupMenu.style.display = "none";
            }
        });
    }
});