import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';

import Experiment from './Experiment';

jest.mock("../../util/stores");

// need to define the returned objects, otherwise the mocked function 
// creates a different object every time, causing useEffect to trigger unnecessarily
const experimentObj = {
    id: 24, slug: 'test', name: 'Test', playlists: [{id: 42, name: 'TestPlaylist'}],
    next_round: [{view: 'PLAYLIST'}]
};
const sessionObj = {data: {session: {id: 1}}};
const nextRoundObj = {next_round: [{view: 'EXPLAINER'}]};

jest.mock("../../API", () => ({
    useExperiment: () => [experimentObj, false],
    createSession: () => Promise.resolve(sessionObj),
    getNextRound: () => Promise.resolve(nextRoundObj)
}));

describe('Experiment Component', () => {

    fit('renders with given props', async () => {
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByTestId('experiment-wrapper');
        await screen.findByTestId('explainer');
    });

});