import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';

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

    it('forwards to a single experiment if it receives a single object', () => {
        mockAxios.get.mockResolvedValueOnce({data: experiment1});
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>);
        waitFor(() => {
            expect(screen.getByTestId('collection-redirect')).toBeInTheDocument();
        })
    });

    it('shows a dashboard of multiple experiments if it receives an array', () => {
        mockAxios.get.mockResolvedValueOnce({data: {dashboard: [experiment1, experiment2]}});
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
        </MemoryRouter>
        );
        waitFor(() => {
            expect(screen.getByTestId('collection-dashboard')).toBeInTheDocument();
        }) 
    });

    
})