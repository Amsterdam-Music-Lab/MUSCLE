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
        name: 'Some Experiment',
        finished_session_count: 0
    };
    const experiment2 = {
        slug: 'another_slug',
        name: 'Another Experiment',
        finished_session_count: 2
    };

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

    it('shows a dashboard of multiple experiments if it receives an array', async () => {
        mock.onGet().replyOnce(200, {dashboard: [experiment1, experiment2]});
        render(
        <MemoryRouter>
            <ExperimentCollection match={{params: {slug: 'some_collection'}}}/>
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