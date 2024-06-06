import { render, screen, waitFor } from '@testing-library/react';

import Footer from "./Footer";

describe('Footer', () => {
    const defaultProps = {
        disclaimer: 'This project was conceived by the <a href="mcg.uva.nl">Music Cognition Gorup</a>',
        logos: [
            {
                'file': 'some/logo.jpg',
                'href': 'some.url.net',
                'alt': 'Our beautiful logo',
            },
            {
                'file': 'another/path.jpg',
                'href': 'another.url.net',
                'alt': 'And another logo',
            }
        ],
        privacy: 'Some privacy statement'
    }

    it('renders a disclaimer', async () => {
        render(
            <Footer {... defaultProps}></Footer>
        )
        expect(screen.findByText('project'));
    });

    it('renders the logos', async () => {
        render(
            <Footer {... defaultProps}></Footer>
        )
        expect(document.querySelectorAll('img').length).toEqual(2);
    });

    it('renders the disclaimer', async () => {
        render(
            <Footer {... defaultProps}></Footer>
        )
        expect(screen.getByText('Some privacy statement'));
    });
});