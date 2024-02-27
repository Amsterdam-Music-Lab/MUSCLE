document.addEventListener("DOMContentLoaded", function () {
    // Function to update the preview image
    function updateImagePreview(inputId, imgPreviewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(imgPreviewId);
        if (input && preview) {
            input.addEventListener("change", function () {
                const url = input.value;
                const escapedUrl = escapeHtml(url); // Escape the meta-characters in the URL
                preview.src = escapedUrl;
                preview.style.display = url ? "block" : "none";
            });
        }
    }

    // Function to escape meta-characters in a string
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function (m) { return map[m]; });
    }

    // Add previews next to the input fields
    function addPreviewElement(nextToElementId, previewId) {
        const element = document.getElementById(nextToElementId);
        if (element) {
            const preview = document.createElement("img");
            preview.id = previewId;
            preview.style.maxWidth = "200px";
            preview.style.marginTop = "1rem";
            element.parentNode.insertBefore(preview, element.nextSibling);

            const url = element.value;
            preview.src = url;
            preview.style.display = url ? "block" : "none";
        }
    }

    // Setup previews
    addPreviewElement("id_logo_url", "logoPreview");
    addPreviewElement("id_background_url", "backgroundPreview");

    // Update previews on change
    updateImagePreview("id_logo_url", "logoPreview");
    updateImagePreview("id_background_url", "backgroundPreview");
});
