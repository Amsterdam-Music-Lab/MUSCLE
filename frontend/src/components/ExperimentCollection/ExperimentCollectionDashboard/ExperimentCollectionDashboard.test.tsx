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
        image: '',
        started_session_count: 2,
        finished_session_count: 1,
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

const experimentWithAllProps = getExperiment({ image: 'some_image.jpg', description: 'Some description' });

describe('ExperimentCollectionDashboard', () => {

    it('shows a dashboard of multiple experiments if it receives an array', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={{ dashboard: [experiment1, experiment2] }} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            const counters = screen.getAllByRole('status');
            expect(counters).toHaveLength(4);
            expect(counters[0].innerHTML).toBe(experiment1.started_session_count.toString());
            expect(counters[1].innerHTML).toBe(experiment1.finished_session_count.toString());
        })
    });

    it('shows a placeholder if an experiment has no image', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={{ dashboard: [experiment1] }} />
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
                <ExperimentCollectionDashboard experimentCollection={{ dashboard: [experiment1] }} />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            expect(screen.getByRole('menu').querySelector('a').getAttribute('href')).toBe('/some_slug/');
        });
    });

    it('links to the experiment with the correct slug and participant id', async () => {
        render(
            <MemoryRouter>
                <ExperimentCollectionDashboard experimentCollection={{ dashboard: [experiment1] }} participantId="123" />
            </MemoryRouter>
        );
        await waitFor(() => {
            expect(screen.getByRole('menu')).toBeTruthy();
            expect(screen.getByRole('menu').querySelector('a').getAttribute('href')).toBe('/some_slug/?participant_id=123');
        });
    });
})