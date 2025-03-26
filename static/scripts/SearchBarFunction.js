document.addEventListener('DOMContentLoaded', function() {
    const searchContainer = document.getElementById('ha-searchbar');
    searchContainer.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); 

            const searchTerm = searchContainer.value.trim();

            if (searchTerm) {
                const baseUrl = window.location.href.split('?')[0]; 
                window.location.href = baseUrl + "?search=" + encodeURIComponent(searchTerm);
            }
        }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('search') || '';
    loadPosts(searchTerm);
});