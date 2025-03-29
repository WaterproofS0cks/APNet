function engagement(action, postId, post_type) {
    
    if (!postId) return;

    fetch("/engagement", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ post_id: postId, action: action, post_type: post_type}),
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
}

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

function updateBookmarkUI(bookmark) {
    const bookmarkIcon = document.getElementById("fms-post-bookmarkicon");
    if (!bookmarkIcon) return;

    bookmarkIcon.src = bookmark
        ? "../static/src/icon/icons8-bookmark-evendarkergreen-500.png"
        : "../static/src/icon/icons8-bookmark-50.png";
}

function filter3DotMenu(sessionUserId) {
    const post = document.querySelector(".fms-post-layout");

    if (post) {
        const postUserId = post.getAttribute("data-user-id");
        const dropdown = post.querySelector(".fms-dropdown-content");

        if (dropdown) {
            const reportPost = dropdown.querySelector("#fms-reportposticon")?.parentElement;
            const reportUser = dropdown.querySelector("#fms-reportusericon")?.parentElement;
            const editPost = dropdown.querySelector("#fms-editicon")?.parentElement;
            const deletePost = dropdown.querySelector("#fms-deleteicon")?.parentElement;

            if (reportPost && reportUser && editPost && deletePost) {
                if (String(sessionUserId) === String(postUserId)) {
                    reportPost.style.display = "none";
                    reportUser.style.display = "none";
                    editPost.style.display = "block";
                    deletePost.style.display = "block";
                } else {
                    reportPost.style.display = "block";
                    reportUser.style.display = "block";
                    editPost.style.display = "none";
                    deletePost.style.display = "none";
                }
            }
        }
    }
}


document.addEventListener("DOMContentLoaded", function() {
    const post_type = document.querySelector("script[data-type]")?.getAttribute("data-type") || "";
    const postId = document.querySelector(".fms-post-layout").getAttribute("data-post-id");
    const commentsList = document.querySelector('.fms-comments-list');
    const commentInput = document.getElementById('commentInput');

    document.body.addEventListener("click", function(event) {
        const targetId = event.target.id;
        if (targetId === "fms-post-hearticon") {
            engagement("liked", postId, post_type);

        } else if (targetId === "fms-post-bookmarkicon") {
            engagement("bookmark", postId, post_type);

        } else if (targetId === "fms-moreicon") {
                
            const target = event.target;
            const clickedDropdown = target.closest('.fms-dropdown');
            
            if (clickedDropdown) {
                const dropdownContent = clickedDropdown.querySelector('.fms-dropdown-content');
                

                document.querySelectorAll('.fm-dropdown-content').forEach(function(dropdown) {
                    if (dropdown !== dropdownContent) { 
                        dropdown.style.display = 'none';
                    }
                });

                if (dropdownContent.style.display === "block") {
                    dropdownContent.style.display = "none"; 
                } else {
                    dropdownContent.style.display = "block";
                }

                event.stopPropagation();
            
            } else {
                document.querySelectorAll('.fm-dropdown-content').forEach(function(dropdown) {
                dropdown.style.display = 'none';
                });
            }
    
        }
    });

    commentInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const addCommentButton = document.getElementById('addCommentButton');
            if (addCommentButton) {
                addCommentButton.click();
            }
        }
    });

    if (addCommentButton) {
        addCommentButton.addEventListener('click', function(event) {
            const commentInput = document.getElementById('commentInput');
            const commentText = commentInput.value.trim();
            if (!commentText) return;

            fetch('/createcomment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment: commentText, post_type: post_type, id: postId })
            })
            .then(response => {
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
                newComment.id = 'comment-' + data.comment_id;
                console.log(newComment)

                const profileImg = document.createElement('img');
                profileImg.src = data.pfp;
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

                const deleteButton = document.createElement('button');
                deleteButton.className = 'delete-comment-btn';
                deleteButton.textContent = 'Delete';
                deleteButton.setAttribute('data-comment-id', data.comment_id);

                newComment.appendChild(profileImg);
                newComment.appendChild(usernameSpan);
                newComment.appendChild(commentSpan);
                newComment.appendChild(deleteButton);

                commentsList.insertBefore(newComment, commentsList.firstChild);
                commentInput.value = '';
            })
            .catch(error => console.error("Error posting comment:", error));
        });
    }


    if (postId) {
        fetch(`/comment?post_id=${postId}`)
            .then(response => response.json())  
            .then(data => {
                commentsList.innerHTML = data.html;
            })
            .catch(error => {
                console.error(error);
            });
    }

    commentsList.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('delete-comment-btn')) {
            const comment_id = event.target.getAttribute('data-comment-id');
            console.log(comment_id)
            console.log("deleting")
            fetch('/deletecomment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment_id: comment_id, post_type: post_type})
            })
            .then(response => response.json())
            .then(data => {
                if (data.delete) { 
                    const commentDiv = document.getElementById(`comment-${comment_id}`);
                    if (commentDiv) {
                        commentDiv.remove(); 
                        console.log("deleting now")
                    }
                } else {
                    console.error("Error deleting comment:", data.error);
                }
            })
            .catch(error => console.error("Error deleting comment:", error));
        }
    });

    fetch('/get_session')
        .then(response => response.json())
        .then(data => {
            if (data.session) {
                filter3DotMenu(data.session);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(console.error);

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