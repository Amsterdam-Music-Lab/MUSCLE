import React from 'react';
import { Route, MemoryRouter } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { getNextRound } from '../../API';

import Experiment from './Experiment';

vi.mock("../../util/stores");

const experimentObj = {
    id: 24, slug: 'test', name: 'Test', playlists: [{ id: 42, name: 'TestPlaylist' }],
    next_round: [{ view: 'INFO', button_label: 'Continue' }]
};

const nextRoundObj = { next_round: [{ view: 'EXPLAINER', instruction: 'Instruction' }] };

vi.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn) => {
        const state = {
            session: 1,
            participant: 'participant-id',
        };
        
        return fn(state);
    },
    useBoundStore: vi.fn()
}));  

describe('Experiment Component', () => {

    afterEach(() => {
        // mockAxios.reset();
    });

    // fix/remove this implementation after merging #810
    test.skip('renders with given props', async () => {
        // mockAxios.get.mockResolvedValueOnce({data: experimentObj});
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByText('Continue');
    });

    // fix/remove this implementation after merging #810
    test.skip('calls onNext', async () => {
        // mockAxios.get.mockResolvedValueOnce({data: experimentObj});
        render(
            <MemoryRouter initialEntries={['/test']}>
                <Route path="/:slug" component={Experiment} />
            </MemoryRouter>
        );
        const button = await screen.findByText('Continue');
        fireEvent.click(button);
        // mockAxios.get.mockResolvedValueOnce({data: nextRoundObj});
        await waitFor(() => expect(getNextRound).toHaveBeenCalled());
    });

});