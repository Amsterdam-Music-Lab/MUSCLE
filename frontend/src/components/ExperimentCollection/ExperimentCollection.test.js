import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import MockAdapter from "axios-mock-adapter";
import axios from 'axios';

import ExperimentCollection from './ExperimentCollection';

let mock = new MockAdapter(axios);

describe('ExperimentCollection', () => {
    const experiment1 = getExperiment({
        slug: 'some_slug',
        name: 'Some Experiment'
    });
    const experiment2 = getExperiment({
        slug: 'another_slug',
        name: 'Another Experiment'
    });
    const experimentWithAllProps = getExperiment({ image: 'some_image.jpg', description: 'Some description' });

    it('forwards to a single experiment if it receives a single object', () => {
        mock.onGet().replyOnce(200, experiment1);
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>);
        waitFor(() => {
            expect(screen.getByTestId('collection-redirect')).toBeInTheDocument();
        })
    });

    it('shows a dashboard of multiple experiments if it receives an array', () => {
        mock.onGet().replyOnce(200, {dashboard: [experiment1, experiment2]});
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(document.querySelector('[data-testid="collection-dashboard"]')).not.toBeNull();
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
        mock.onGet().replyOnce(200, new Promise(() => {
            dashboard: [experiment1]
        }));
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
        mock.onGet().replyOnce(200, new Promise(() => {
            dashboard: [experimentWithAllProps]
        }));
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
        mock.onGet().replyOnce(200, new Promise(() => {
            dashboard: [experimentWithAllProps]
        }));
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

const getExperiment = (overrides = {}) => {
    return {
        slug: 'some_slug',
        name: 'Some Experiment',
        ...overrides
    }
}