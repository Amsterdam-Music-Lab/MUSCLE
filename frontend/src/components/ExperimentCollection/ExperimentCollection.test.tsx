import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import MockAdapter from "axios-mock-adapter";
import axios from 'axios';

import ExperimentCollection from './ExperimentCollection';
let mock = new MockAdapter(axios);

const getBlock = (overrides = {}) => {
    return {
        slug: 'some_slug',
        name: 'Some Block',
        ...overrides
    };
}

const block1 = getBlock({
    slug: 'some_slug',
    name: 'Some Block'
});

const theme = {
    backgroundUrl: 'someurl.com',
    bodyFontUrl: 'bodyFontUrl.com',
    description: 'Description of the theme',
    headingFontUrl: 'headingFontUrl.com',
    logo: {
        title: 'Logo title',
        description: 'Logo description',
        file: 'logo.jpg',
        alt: 'Logo alt',
        href: 'https://www.example.com',
        rel: 'noopener noreferrer',
        target: '_blank'
    },
    name: 'Awesome theme',
    footer: {
        disclaimer: 'disclaimer',
        logos: [
            {
                'file': 'some/logo.jpg',
                'href': 'some.url.net',
                'alt': 'Our beautiful logo',
            }
        ],
        privacy: 'privacy'
    }
}

const blockWithAllProps = getBlock({ image: 'some_image.jpg', description: 'Some description' });

describe('ExperimentCollection', () => {

    it('forwards to a single block if it receives an empty dashboard array', async () => {
        mock.onGet().replyOnce(200, { dashboard: [], nextExperiment: block1 });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>);
        await waitFor(() => {
            expect(screen.queryByRole('menu')).toBeFalsy();
        })
    });

    it('shows a loading spinner while loading', () => {
        mock.onGet().replyOnce(200, new Promise(() => { }));
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('.loader-container')).not.toBeNull();
        })
    });

    it('shows a placeholder if no image is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [block1], nextExperiment: block1 });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('.loader-container')).not.toBeNull();
        })
    });

    it('shows the image if it is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [blockWithAllProps], nextExperiment: block1 });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('img')).not.toBeNull();
        })
    });

    it('shows the description if it is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [blockWithAllProps], nextExperiment: block1 });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        waitFor(() => {
            expect(screen.getByText('Some description')).toBeInTheDocument();
        })
    });

    it('shows consent first if available', async () => {
        mock.onGet().replyOnce(200, { consent: '<p>This is our consent form!</p>', dashboard: [blockWithAllProps], nextExperiment: block1 });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(document.querySelector('.consent-text')).not.toBeNull();
        })
    });

    it('shows a footer if a theme with footer is available', async () => {
        mock.onGet().replyOnce(200, { dashboard: [blockWithAllProps], nextExperiment: block1, theme });
        render(
            <MemoryRouter>
                <ExperimentCollection match={{ params: { slug: 'some_collection' } }} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(document.querySelector('.aha__footer')).not.toBeNull();
        })
    })
})
