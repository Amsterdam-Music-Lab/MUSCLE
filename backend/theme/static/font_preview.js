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
            // preview texts in various languages, each on a new line
            const texts = [
                "This is an experiment to test the font.",
                "這是一個測試字體的實驗。",
                "これはフォントをテストする実験です。",
                "이것은 글꼴을 테스트하는 실험입니다.",
                "Это эксперимент для тестирования шрифта.",
                "هذه تجربة لاختبار الخط.",
                "Это эксперымент для тэставання шрыфтаў.",
                "এটা ফন্ট পরীক্ষা করার একটি প্রয়োগ।",
                "این یک آزمایش برای تست فونت است.",
                "இது எழுத்துருவை சோதிக்க ஒரு சோதனை ஆகும்."
            ];
            preview.innerHTML = texts.join("<br>"); // Use <br> to render new lines
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
            fontUrl = `https://fonts.googleapis.com/css?family=${encodeURIComponent(formattedFontName)}:400,700`; // Escape meta-characters in font name
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

    // Setup heading font preview
    addFontPreviewElement("id_heading_font_url", "fontPreview");

    // Update heading font preview on change
    updateFontPreview("id_heading_font_url", "fontPreview");

    // Setup body font preview
    addFontPreviewElement("id_body_font_url", "bodyFontPreview");

    // Update body font preview on change
    updateFontPreview("id_body_font_url", "bodyFontPreview");
});