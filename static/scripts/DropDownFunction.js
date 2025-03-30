const scriptTag = document.currentScript;
const post_type = scriptTag.getAttribute("data-type") || "";

(function() {

    function reportPost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id');
        
        fetch("/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ Id: postId, post_type: post_type })
        });
    }

    function reportUser (button) {
        var postLayout = button.closest('.fm-post-layout');
        var userId = postLayout.getAttribute('data-user-id');

        fetch("/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ Id: userId })
        });
    }

    function editPost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id'); 
        
        fetch("/editpost", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ postId: postId, post_type: post_type })
        });
    }

    function deletePost(button) {
        var postLayout = button.closest('.fm-post-layout');
        var postId = postLayout.getAttribute('data-post-id');
        
        fetch("/delete-post", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ postId: postId, post_type: post_type })
        });
    }

    window.reportPost = reportPost;
    window.reportUser  = reportUser ;
    window.editPost = editPost;
    window.deletePost = deletePost;

})();