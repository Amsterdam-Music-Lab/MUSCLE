import React from 'react';
import { Route, MemoryRouter } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import mockAxios from "jest-mock-axios";
import * as API from '../../API';

import Experiment from './Experiment';

const experimentObj = {
    id: 24, slug: 'test', name: 'Test', playlists: [{ id: 42, name: 'TestPlaylist' }],
    next_round: [{ view: 'INFO', button_label: 'Continue' }]
};

const nextRoundObj = { next_round: [{ view: 'EXPLAINER', instruction: 'Instruction' }] };

jest.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn) => {
        const state = {
            session: 1,
            participant: 'participant-id',
        };
        
        return fn(state);
    },
    useBoundStore: jest.fn()
}));  

describe('Experiment Component', () => {

    afterEach(() => {
        mockAxios.reset();
    });

    it('renders with given props', async () => {
        mockAxios.get.mockResolvedValueOnce({ data: experimentObj });
        render((
            <MemoryRouter initialEntries={['/test']}>
                <Route path="/:slug" component={Experiment} />
            </MemoryRouter>
        ));
        await screen.findByText('Continue');
    });

    it('calls onNext', async () => {
        mockAxios.get.mockResolvedValueOnce({ data: experimentObj });
        render(
            <MemoryRouter initialEntries={['/test']}>
                <Route path="/:slug" component={Experiment} />
            </MemoryRouter>
        );
        const button = await screen.findByText('Continue');
        fireEvent.click(button);
        mockAxios.get.mockResolvedValueOnce({ data: nextRoundObj });
        jest.spyOn(API, 'getNextRound');
        await waitFor(() => expect(API.getNextRound).toHaveBeenCalled());
    });

});