import { useEffect } from 'react';

const FontLoader = ({ fontUrl, fontType = 'heading' }) => {
    const fontMatch = /family=([^&:]+)/.exec(fontUrl);
    const font = fontMatch ? fontMatch[1].replace(/\+/g, ' ') : "sans-serif";
    const selector = fontType === 'heading' ? 'h1, h2, h3, h4, h5, h6, .btn' : 'body';

    useEffect(() => {
        if (!fontUrl) {
            return;
        }

        const linkId = `dynamic-font-link-${fontType}`
        let link = document.getElementById(linkId);
        if (!link) {
            link = document.createElement('link');
            link.id = linkId;
            link.href = fontUrl;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }

        const styleId = `dynamic-font-style-${fontType}`;
        let style = document.getElementById(styleId);
        if (!style) {
            style = document.createElement('style');
            style.id = styleId;
            style.innerHTML = `${selector} { font-family: "${font}", sans-serif; }`;
            document.head.appendChild(style);
        }

        return () => {
            // Remove the link and style elements during cleanup
            link && document.head.removeChild(link);
            style && document.head.removeChild(style);
        };
    }, [fontUrl, font, selector]);

    return null;
};

export default FontLoader;
