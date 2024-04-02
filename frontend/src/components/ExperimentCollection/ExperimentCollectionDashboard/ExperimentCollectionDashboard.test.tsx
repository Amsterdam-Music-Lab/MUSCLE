import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';

import ExperimentCollectionDashboard from './ExperimentCollectionDashboard';

const getExperiment = (overrides = {}) => {
    return {
        slug: 'some_slug',
        name: 'Some Experiment',
        finished_session_count: 0,
        ...overrides
    };
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
            expect(counters).toHaveLength(2);
            expect(counters[1].innerHTML).toBe('2');
        })
    });
})