import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import MockAdapter from "axios-mock-adapter";
import axios from 'axios';

import ExperimentCollection from './ExperimentCollection';

let mock = new MockAdapter(axios);

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

const experimentWithAllProps = getExperiment({ image: 'some_image.jpg', description: 'Some description' });

describe('ExperimentCollection', () => {

    it('forwards to a single experiment if it receives a single object', async () => {
        mock.onGet().replyOnce(200, experiment1);
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>);
        await waitFor(() => {
            expect(screen.queryByRole('menu')).toBeFalsy();
        })
    });

    it('shows a loading spinner while loading', () => {
        mock.onGet().replyOnce(200, new Promise(() => {}));
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('.loader-container')).not.toBeNull();
        })
    });

    it('shows a placeholder if no image is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [experiment1] });
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('.loader-container')).not.toBeNull();
        })
    });

    it('shows the image if it is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [experimentWithAllProps] });
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('img')).not.toBeNull();
        })
    });

    it('shows the description if it is available', () => {
        mock.onGet().replyOnce(200, { dashboard: [experimentWithAllProps] });
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(screen.getByText('Some description')).toBeInTheDocument();
        })
    });
})