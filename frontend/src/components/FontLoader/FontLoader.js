import { useEffect } from 'react';

const FontLoader = ({fontUrl, fontType = 'heading'}) => {
    const fontMatch = /family=([^&:]+)/.exec(fontUrl);
    const font = fontMatch ? fontMatch[1].replace(/\+/g, ' ') : "sans-serif";
    const selector = fontType === 'heading' ? 'h1, h2, h3, h4, h5, h6, .btn' : 'body';

    useEffect(() => {

        if (!fontUrl) {
            return;
        }

        // Dynamically load the font
        const link = document.createElement('link');
        link.href = fontUrl;
        link.rel = 'stylesheet';
        document.head.appendChild(link);

        // Set the global font style
        const style = document.createElement('style');
        style.innerHTML = `
    ${selector} {
        font-family: "${font}", sans-serif;
    }
`;
        document.head.appendChild(style);

        return () => {
            document.head.removeChild(link);
            document.head.removeChild(style);
        };
    }, [fontUrl]);

    return null;
}

export default FontLoader;