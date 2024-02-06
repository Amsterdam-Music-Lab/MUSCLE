import React from 'react';
import { MemoryRouter } from 'react-router-dom/cjs/react-router-dom';
import { render, screen } from '@testing-library/react';

import Experiment from './Experiment';

jest.mock("../../util/stores");

// need to define the object returned by useExperiment, otherwise the mocked function 
// creates a different object every time, causing an infinite useEffect loop
const experimentObj = {id: 24, slug: 'test', name: 'Test', next_round: [
    {view: 'Playlist', playlists: [{id: 42, name: 'TestPlaylist'}]}
]};

jest.mock("../../API", () => ({
    useExperiment: () => [experimentObj, false],
    createSession: () => Promise.resolve({data: {session: {id: 1}}}),
    getNextRound: () => Promise.resolve({next_round: [{view: 'EXPLAINER'}]})
}));

describe('Experiment Component', () => {

    it('renders with given props', async () => {
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByTestId('experiment-wrapper');
        await screen.findByTestId('explainer');
    })

    it('renders with empty next_round array from useExperiment', async () => {
        const experimentObj = {id: 24, slug: 'test', name: 'Test', next_round: []};
        jest.mock("../../API", () => ({
            useExperiment: () => [experimentObj, false],
            createSession: () => Promise.resolve({data: {session: {id: 1}}}),
            getNextRound: () => Promise.resolve({next_round: [{view: 'EXPLAINER'}]})
        }));
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByTestId('experiment-wrapper');
        await screen.findByTestId('explainer');
    })



});