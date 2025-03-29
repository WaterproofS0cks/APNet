const post_type = document.querySelector("script[data-type]")?.getAttribute("data-type") || "";
const page_type = document.querySelector("script[data-page]")?.getAttribute("data-page") || "";

let currentPage = 1;
let loadedPostIds = new Set();
const postContainer = document.getElementById('postContainer');
let isLoading = false;

function loadPosts(searchTerm = '') {
    if (isLoading) return;

    isLoading = true;

    const postIds = Array.from(postContainer.querySelectorAll('.fm-post-layout'))
        .map(post => post.getAttribute('data-post-id'))
        .filter(postId => postId && postId.trim() !== "");

    postIds.forEach(postId => loadedPostIds.add(postId));

    const url = '/load_more?page=' + currentPage + 
                '&loaded_ids=' + JSON.stringify(Array.from(loadedPostIds)) + 
                '&post_type=' + post_type +
                '&page_type=' + page_type +
                (searchTerm ? '&search=' + encodeURIComponent(searchTerm) : '');

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                postContainer.insertAdjacentHTML('beforeend', data.html);
                currentPage++;
                filter3DotMenu(data.user_id);
            }

            let noMorePostsMessage = document.getElementById('no-more-posts');
            if (noMorePostsMessage) {
                noMorePostsMessage.remove();
            }

            if (data.no_more_posts) {
                noMorePostsMessage = document.createElement('div');
                noMorePostsMessage.id = 'no-more-posts';
                noMorePostsMessage.style.textAlign = 'center';
                noMorePostsMessage.style.fontSize = '20px';
                noMorePostsMessage.textContent = 'No more posts to load';

                postContainer.appendChild(noMorePostsMessage);
            }

            isLoading = false;
        })
        .catch(error => {
            console.error('Error loading posts:', error);
            isLoading = false;
        });
}

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

function filter3DotMenu(sessionUserId) {
    document.querySelectorAll(".fm-post-layout").forEach(post => {
        const postUserId = post.getAttribute("data-user-id");
        const dropdown = post.querySelector(".fm-dropdown-content");

        if (dropdown) {
            const reportPost = dropdown.querySelector("#fm-reportposticon")?.parentElement;
            const reportUser = dropdown.querySelector("#fm-reportusericon")?.parentElement;
            const editPost = dropdown.querySelector("#fm-editicon")?.parentElement;
            const deletePost = dropdown.querySelector("#fm-deleteicon")?.parentElement;

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
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        // 3 Dot Menu
        const clickedDropdown = event.target.closest('.fm-dropdown');
        
        if (clickedDropdown) {
            const dropdownContent = clickedDropdown.querySelector('.fm-dropdown-content');
            
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
    });

    document.body.addEventListener("click", function (event) {
        let actionContainer = event.target.closest("[data-action]");

        if (!actionContainer && event.target.tagName === "IMG") {
            actionContainer = event.target.parentElement.closest("[data-action]");
        }

        if (!actionContainer) return;

        const postElement = actionContainer.closest(".fm-post-layout");
        if (!postElement) return;

        const postId = postElement.getAttribute("data-post-id");
        const action = actionContainer.getAttribute("data-action");

        if (!postId || !action) return;

        if (action === "liked" || action === "bookmark") {
            fetch("/engagement", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ post_id: postId, action: action, post_type: post_type }),
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
            .catch((error) => console.error("Error:", error));
        } else if (action === "specific") {

            if (post_type === "post") {
                window.location.href = "/specificpost?postid=" + encodeURIComponent(postId);
            } else if (post_type === "recruitment") {
                window.location.href = "/specificrecruitment?postid=" + encodeURIComponent(postId);
            }
        }
    });

    window.addEventListener('scroll', function() {
        if (isLoading) return;
        
        if (window.innerHeight + window.scrollY < document.body.offsetHeight - 10) {
            document.querySelectorAll('.fm-dropdown-content').forEach(function(dropdown) {
                dropdown.style.display = 'none';
            });
        }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('search') || '';
    loadPosts(searchTerm);

});

window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10 && !isLoading) {
        const urlParams = new URLSearchParams(window.location.search);
        const searchTerm = urlParams.get('search') || ''; 
        loadPosts(searchTerm);
    }
});  


function myFunction() {
  let person = prompt("Please enter your name", "Harry Potter");
  if (person != null) {
    document.getElementById("demo").innerHTML =
    "Hello " + person + "! How are you today?";
  }
}
