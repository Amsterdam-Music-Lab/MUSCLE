document.addEventListener("DOMContentLoaded", function() {
    // Function to update the preview image
    function updateImagePreview(inputId, imgPreviewId) {
      const input = document.getElementById(inputId);
      const preview = document.getElementById(imgPreviewId);
      if (input && preview) {
        input.addEventListener("change", function() {
          const url = input.value;
          preview.src = url;
          preview.style.display = url ? "block" : "none";
        });
      }
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
    addPreviewElement("id_logo", "logoPreview");
    addPreviewElement("id_background", "backgroundPreview");
  
    // Update previews on change
    updateImagePreview("id_logo", "logoPreview");
    updateImagePreview("id_background", "backgroundPreview");
  });
  