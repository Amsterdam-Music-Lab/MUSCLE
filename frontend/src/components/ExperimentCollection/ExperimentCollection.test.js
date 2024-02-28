import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';

import mockAxios from "jest-mock-axios";

import ExperimentCollection from './ExperimentCollection';


describe('ExperimentCollection', () => {
    const experiment1 = {
        slug: 'some_slug',
        name: 'Some Experiment'
    };
    const experiment2 = {
        slug: 'another_slug',
        name: 'Another Experiment'
    };

    afterEach(() => {
        mockAxios.reset();
    });

    it('shows a dashboard of multiple experiments if it receives an array', async () => {
        mockAxios.get.mockResolvedValueOnce({data: {dashboard: [experiment1, experiment2]}});
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        await screen.findByTestId('collection-dashboard');
    });

    it('forwards to a single experiment if it receives a single object', async () => {
        mockAxios.get.mockResolvedValueOnce({data: experiment1});
        render(<ExperimentCollection match={{params: {slug: 'some_collection'}}}/>);
        await screen.findByTestId('collection-redirect');
    });

    
})