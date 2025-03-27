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

document.addEventListener("DOMContentLoaded", function() {
    let loggedInUserId;

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

    document.body.addEventListener("click", function(event) {
        const clickedDropdown = event.target.closest(".fms-dropdown");
        
        if (clickedDropdown) {
            const dropdownContent = clickedDropdown.querySelector(".fms-dropdown-content");
            document.querySelectorAll(".fms-dropdown-content").forEach(dropdown => {
                if (dropdown !== dropdownContent) {
                    dropdown.style.display = "none";
                }
            });
            dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
            event.stopPropagation();
        } else {
            document.querySelectorAll(".fms-dropdown-content").forEach(dropdown => {
                dropdown.style.display = "none";
            });
        }
    });

    document.body.addEventListener("click", function(event) {
        const targetId = event.target.id;
        let action = null;
    
        if (targetId === "fms-post-hearticon") {
            action = "liked";
        } else if (targetId === "fms-post-bookmarkicon") {
            action = "bookmark";
        }
    
        if (!action) return;
    
        const postElement = document.querySelector(".fms-post-layout");
        const postId = postElement.getAttribute("data-post-id"); 
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
    
    window.addEventListener("scroll", function() {
        if (window.innerHeight + window.scrollY < document.body.offsetHeight - 10) {
            document.querySelectorAll(".fms-dropdown-content").forEach(dropdown => {
                dropdown.style.display = "none";
            });
        }
    });

    const commentsList = document.querySelector('.fms-comments-list');

    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get("post_id");

    if (postId) {
        const url = `/comment?post_id=${postId}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                commentsList.innerHTML = data.html;
            })
            .catch(error => console.error('Error loading comments:', error));
    }
});