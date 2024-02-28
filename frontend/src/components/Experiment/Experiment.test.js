import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import mockAxios from "jest-mock-axios";
import { getNextRound } from '../../API';

import Experiment from './Experiment';

jest.mock("../../util/stores");

const experimentObj = {
    id: 24, slug: 'test', name: 'Test', playlists: [{id: 42, name: 'TestPlaylist'}],
    next_round: [{view: 'INFO', button_label: 'Continue'}]
};
const nextRoundObj = {next_round: [{view: 'EXPLAINER', instruction: 'Instruction'}]};


describe('Experiment Component', () => {
    afterEach(() => {
        mockAxios.reset();
    });
    

    it('renders with given props', async () => {
        mockAxios.get.mockResolvedValueOnce({data: experimentObj});
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        await screen.findByText('Continue');
    });

    xit('calls onNext', async () => {
        mockAxios.get.mockResolvedValueOnce({data: experimentObj});
        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        const button = await screen.findByText('Continue');
        fireEvent.click(button);
        mockAxios.get.mockResolvedValueOnce({data: nextRoundObj});
        await waitFor(() => expect(getNextRound).toHaveBeenCalled());
    });

});