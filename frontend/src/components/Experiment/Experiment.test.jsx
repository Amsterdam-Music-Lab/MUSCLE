import React from 'react';
import { Route, MemoryRouter } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import Experiment from './Experiment';
import * as API from '../../API'; 

let mock = new MockAdapter(axios);

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
            setSession: vi.fn(),
        };
        
        return fn(state);
    },
    useBoundStore: vi.fn()
}));  

describe('Experiment Component', () => {

    afterEach(() => {
        mock.reset();
    });

    // fix/remove this implementation after merging #810
    test('renders with given props', async () => {
        mock.onGet().replyOnce(200, experimentObj);
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByText('Continue');
    });

    test('calls onNext', async () => {
        mock.onGet().replyOnce(200, experimentObj);
        const spy = vi.spyOn(API, 'getNextRound');

        render(
            <MemoryRouter initialEntries={['/test']}>
                <Route path="/:slug" component={Experiment} />
            </MemoryRouter>
        );
        const button = await screen.findByText('Continue');
        fireEvent.click(button);
        mock.onGet().replyOnce(200, nextRoundObj);
        await waitFor(() => expect(spy).toHaveBeenCalled());
    });

});