document.addEventListener("DOMContentLoaded", function () {

    // Function to update the font preview
    function updateFontPreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        if (input && preview) {
            input.addEventListener("change", function () {
                const fontName = input.value.replace(/\s+/g, '+'); // Replace spaces with '+'
                if (fontName) {
                    // Load the font from Google Fonts
                    const link = document.createElement('link');
                    link.href = `https://fonts.googleapis.com/css?family=${encodeURIComponent(fontName)}:400,700`; // Escape meta-characters in font name
                    link.rel = 'stylesheet';
                    document.head.appendChild(link);

                    // Apply the font to the preview element
                    preview.style.fontFamily = `"${input.value}", sans-serif`;
                    preview.style.display = 'block';
                } else {
                    preview.style.display = 'none';
                }
            });
        }
    }

    // Add a preview element for the font
    function addFontPreviewElement(nextToElementId, previewId) {
        const element = document.getElementById(nextToElementId);
        if (element) {
            const preview = document.createElement("div");
            preview.id = previewId;
            preview.textContent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.";
            preview.style.display = "none"; // Hide initially
            preview.style.padding = "10px";
            preview.style.border = "1px solid #ccc";
            preview.style.marginTop = "10px";
            element.parentNode.insertBefore(preview, element.nextSibling);
        }
    }

    function loadAndPreviewFont(fontName, preview) {
        let fontUrl;
        const isUrl = /^(https?:\/\/)/.test(fontName); // Check if the input is a URL

        if (isUrl) {
            fontUrl = fontName; // Use the URL directly if it's a URL
        } else {
            const formattedFontName = fontName.replace(/\s+/g, '+'); // Replace spaces with '+' for Google Fonts
            fontUrl = `https://fonts.googleapis.com/css?family=${formattedFontName}:400,700`;
        }

        if (fontName) {
            // Load the font
            const link = document.createElement('link');
            link.href = fontUrl;
            link.rel = 'stylesheet';
            document.head.appendChild(link);

            // Apply the font to the preview element
            if (isUrl) {
                // Extract font-family name from URL
                const fontFamilyMatch = /family=([^&:]+)/.exec(fontUrl);
                const fontFamily = fontFamilyMatch ? fontFamilyMatch[1].replace(/\+/g, ' ') : "sans-serif";
                preview.style.fontFamily = `"${fontFamily}", sans-serif`;
            } else {
                preview.style.fontFamily = `"${fontName}", sans-serif`;
            }
            preview.style.display = 'block';
        } else {
            preview.style.display = 'none';
        }
    }


    // Function to update the font preview
    function updateFontPreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        if (input && preview) {
            input.addEventListener("change", function () {
                loadAndPreviewFont(input.value, preview);
            });

            // Preview the font if the input is pre-filled on page load
            loadAndPreviewFont(input.value, preview);
        }
    }

    // Setup font preview
    addFontPreviewElement("id_font", "fontPreview");

    // Update font preview on change
    updateFontPreview("id_font", "fontPreview");
});
