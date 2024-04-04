import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

import ExperimentCollectionDashboard from './ExperimentCollectionDashboard';
import Experiment from '@/types/Experiment';

const getExperiment = (overrides = {}) => {
    return {
        slug: 'some_slug',
        name: 'Some Experiment',
        started_session_count: 2,
        finished_session_count: 1,
        ...overrides
    } as Experiment
}

const experiment1 = getExperiment({
    slug: 'some_slug',
    name: 'Some Experiment'
});
const experiment2 = getExperiment({
    slug: 'another_slug',
    name: 'Another Experiment',
    finished_session_count: 2
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
})