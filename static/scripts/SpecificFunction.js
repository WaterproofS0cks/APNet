function updateLikeUI(container, liked, count) {
    const likeCountElement = container.querySelector("h4");
    const likeIcon = container.querySelector("img");

    likeIcon.src = liked
        ? "../static/src/icon/icons8-heart-red-50.png"
        : "../static/src/icon/icons8-heart-50.png";

    if (likeCountElement) {
        likeCountElement.textContent = `(${count})`;
    }
}

function updateBookmarkUI(container, bookmark) {
    const bookmarkIcon = container.querySelector("img");
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

            if (reportPost && reportUser && editPost && deletePost) {
                if (String(loggedInUserId) === String(postUserId)) {
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
    });
}

document.addEventListener("DOMContentLoaded", function() {
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
        let actionContainer = event.target.closest("[data-action]");
        if (!actionContainer && event.target.tagName === "IMG") {
            actionContainer = event.target.parentElement.closest("[data-action]");
        }
        if (!actionContainer) return;

        const postElement = actionContainer.closest(".fms-post-layout");
        if (!postElement) return;

        const postId = postElement.getAttribute("data-post-id");
        const action = actionContainer.getAttribute("data-action");
        if (!postId || !action) return;

        if (action === "liked" || action === "bookmark") {
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
                    updateLikeUI(actionContainer, data.liked, data.likes_count);
                } else if (action === "bookmark") {
                    updateBookmarkUI(actionContainer, data.bookmark);
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });

    window.addEventListener("scroll", function() {
        if (window.innerHeight + window.scrollY < document.body.offsetHeight - 10) {
            document.querySelectorAll(".fms-dropdown-content").forEach(dropdown => {
                dropdown.style.display = "none";
            });
        }
    });
});