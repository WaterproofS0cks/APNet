(function() {

    function reportPost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id');
        var postType = postLayout.getAttribute('data-post-type');
        
        fetch("/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: postId, post_type: postType })
        });
    }

    function reportUser (button) {
        var postLayout = button.closest('.fm-post-layout');
        var userId = postLayout.getAttribute('data-user-id');

        fetch("/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: userId })
        });
    }

    function editPost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id');
        var postType = postLayout.getAttribute('data-post-type');
    
        fetch("/editpost", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ post_id: postId, post_type: postType })
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Error with the fetch request:', error);
        });
    }

    function deletePost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id');
        var postType = postLayout.getAttribute('data-post-type');
        
        fetch("/deletepost", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ post_id: postId, post_type: postType })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) postLayout.remove();
        })
        .catch(() => alert('Error deleting post.'));
    }

    window.reportPost = reportPost;
    window.reportUser = reportUser;
    window.editPost = editPost;
    window.deletePost = deletePost;

})();