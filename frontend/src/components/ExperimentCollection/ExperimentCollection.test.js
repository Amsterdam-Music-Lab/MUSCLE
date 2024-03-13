import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import MockAdapter from "axios-mock-adapter";
import axios from 'axios';

import ExperimentCollection from './ExperimentCollection';

let mock = new MockAdapter(axios);

describe('ExperimentCollection', () => {
    const experiment1 = {
        slug: 'some_slug',
        name: 'Some Experiment'
    };
    const experiment2 = {
        slug: 'another_slug',
        name: 'Another Experiment'
    };

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

    
})