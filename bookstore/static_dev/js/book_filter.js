document.addEventListener("DOMContentLoaded", function() {
    const genreSelect = document.getElementById("genre-filter");
    
    if (genreSelect) {
        genreSelect.addEventListener("change", function() {
            const form = document.getElementById("filter-form");
            if (form) {
                form.submit();
            }
        });
    }
});