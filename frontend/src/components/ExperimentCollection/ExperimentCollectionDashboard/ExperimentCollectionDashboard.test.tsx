import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

import ExperimentCollectionDashboard from './ExperimentCollectionDashboard';
import Experiment from '@/types/Experiment';

const getExperiment = (overrides = {}) => {
    return {
        id: 1,
        slug: 'some_slug',
        name: 'Some Experiment',
        description: 'Some description',
        image: {},
        ...overrides
    } as Experiment
}

const experiment1 = getExperiment({
    id: 1,
    slug: 'some_slug',
    name: 'Some Experiment',
    description: null,
});
const experiment2 = getExperiment({
    id: 2,
    slug: 'another_slug',
    name: 'Another Experiment',
    finished_session_count: 2,
    description: 'Some description',
});

const collectionWithDashboard = { dashboard: [experiment1, experiment2] }

const header = {
    nextExperimentButtonText: 'Next experiment',
    aboutButtonText: 'About us',
    showScore: true
}
const collectionWithTheme = {
    dashboard: [experiment1, experiment2],
    theme: {
        backgroundUrl: 'some/url.com',
        bodyFontUrl: 'font/url.com',
        description: 'description of the theme',
        headingFontUrl: 'another/font/url.com',
        logoUrl: 'where/is/the/logo.jpg',
        name: 'Collection name',
        header: header
    }
}

describe('ExperimentCollectionDashboard', () => {

    it('shows a dashboard of multiple experiments if it receives an array', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithDashboard} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
        });
    });

    it('shows a placeholder if an experiment has no image', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithDashboard} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            expect(screen.getByRole('menu').querySelector('.placeholder')).toBeTruthy();
        });
    });

    it('links to the experiment with the correct slug', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithDashboard} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            expect(screen.getByRole('menu').querySelector('a').getAttribute('href')).toBe('/some_slug');
        });
    });

    it('links to the experiment with the correct slug and participant id if the participand id url is present', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithDashboard} participantIdUrl="some_id" />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            expect(screen.getByRole('menu').querySelector('a').getAttribute('href')).toBe('/some_slug?participant_id=some_id');
        });
    });

    it('does not show a header if no theme.header is present', () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithDashboard} participantIdUrl="some_id" />
            </MemoryRouter>
        );
        const aboutButton = screen.queryByText('About us')
        expect(aboutButton).toBeFalsy();
    });

    it('shows a header if a theme.header is present', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={collectionWithTheme} participantIdUrl="some_id" />
            </MemoryRouter>
        );
        await screen.findByText('About us');
    });
})