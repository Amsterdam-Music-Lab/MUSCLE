import React from 'react';
import { Route, MemoryRouter, Routes } from 'react-router-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, vi } from 'vitest';
import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import Block from './Block';
import * as API from '../../API';

let mock = new MockAdapter(axios);

vi.mock("../../util/stores");

let mockUseParams = vi.fn();

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useParams: () => mockUseParams()
    };
});

const experimentObj = {
    id: 24, slug: 'test', name: 'Test', playlists: [{ id: 42, name: 'TestPlaylist' }],
    next_round: [{ view: 'INFO', button_label: 'Continue' }]
};

const nextRoundObj = { next_round: [{ view: 'EXPLAINER', instruction: 'Instruction' }] };

const mockSessionStore = { id: 1 };
const mockParticipantStore = {
    id: 1,
    hash: '00000000-0000-0000-0000-000000000000',
    csrf_token: 'auSoWt7JA9fYyGE0Cc51tlYDnvGGxwo1HqVBsQHQ8dUE7QJZAjYZIieJc4kdYB4r',
    participant_id_url: 'url',
    country: 'nl',
};

vi.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn) => {
        const state = {
            session: mockSessionStore,
            participant: mockParticipantStore,
            setSession: vi.fn(),
            setHeadData: vi.fn(),
            resetHeadData: vi.fn(),
            setBlock: vi.fn(),
        };

        return fn(state);
    },
    useBoundStore: vi.fn()
}));

describe('Block Component', () => {

    beforeEach(() => {
        mockUseParams.mockReturnValue({ slug: 'test' });
    });

    afterEach(() => {
        mock.reset();
    });

    // fix/remove this implementation after merging #810
    test('renders with given props', async () => {
        mock.onGet().replyOnce(200, experimentObj);
        render(
            <MemoryRouter>
                <Block />
            </MemoryRouter>
        );
        await screen.findByText('Continue');
    });

    test('calls onNext', async () => {
        mock.onGet().replyOnce(200, experimentObj);
        const spy = vi.spyOn(API, 'getNextRound');

        render(
            <MemoryRouter initialEntries={['/block/test']}>
                <Routes>
                    <Route path="/block/:slug" element={<Block />} />
                </Routes>
            </MemoryRouter>
        );
        const button = await screen.findByText('Continue');
        fireEvent.click(button);
        mock.onGet().replyOnce(200, nextRoundObj);
        await waitFor(() => expect(spy).toHaveBeenCalled());
    });

});
