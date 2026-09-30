import { cleanup, render } from '@testing-library/react';
import FontLoader from './FontLoader';
import { describe, it, expect } from 'vitest';

describe('FontLoader', () => {

    it('renders without crashing', () => {
        const { container } = render(<FontLoader />);
        expect(container.innerHTML).toBe('');
    });

    it('loads the font and sets the global font style', async () => {
        const fontUrl = 'https://fonts.googleapis.com/css?family=Roboto';
        const fontType = 'heading';

        render(<FontLoader fontUrl={fontUrl} fontType={fontType} />);

        const linkElement = document.querySelector('link[href="' + fontUrl + '"]');
        const styleElement = document.querySelector('style');

        expect(linkElement).not.toBeNull();
        expect(styleElement).not.toBeNull();
        expect(styleElement!.innerHTML).toContain('font-family: "Roboto", sans-serif;');
        
        cleanup();

        const removedLinkElement = document.querySelector('link[href="' + fontUrl + '"]');
        const removedStyleElement = document.querySelector('style');

        expect(removedLinkElement).toBeNull();
        expect(removedStyleElement).toBeNull();
    });

    it('does not load the font if fontUrl is not provided', async () => {
        render(<FontLoader />);

        const linkElement = document.querySelector('link');
        const styleElement = document.querySelector('style');

        expect(linkElement).toBeNull();
        expect(styleElement).toBeNull();
    });
});
