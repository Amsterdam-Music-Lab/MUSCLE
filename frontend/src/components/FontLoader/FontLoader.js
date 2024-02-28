import React, { useEffect } from 'react';
import useBoundStore from 'util/stores';

const FontLoader = () => {
    const theme = useBoundStore(state => state.theme);
    const fontUrl = theme?.font_url;
    const fontFamilyMatch = /family=([^&:]+)/.exec(fontUrl);
    const fontFamily = fontFamilyMatch ? fontFamilyMatch[1].replace(/\+/g, ' ') : "sans-serif";


    useEffect(() => {
        // Dynamically load the font
        const link = document.createElement('link');
        link.href = fontUrl;
        link.rel = 'stylesheet';
        document.head.appendChild(link);

        // Set the global font style
        const style = document.createElement('style');
        style.innerHTML = `
            body {
                font-family: "${fontFamily}", sans-serif;
            }
        `;
        document.head.appendChild(style);

        return () => {
            document.head.removeChild(link);
            document.head.removeChild(style);
        };
    }, [theme]);

    return null;
}

export default FontLoader;