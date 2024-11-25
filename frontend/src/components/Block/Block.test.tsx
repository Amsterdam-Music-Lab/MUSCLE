import { Route, MemoryRouter, Routes } from 'react-router-dom';
import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Block from './Block';
import * as API from '../../API';

vi.mock("../../util/stores");

let mockUseParams = vi.fn();

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useParams: () => mockUseParams()
    };
});

const blockObj = {
    id: 24, slug: 'test', name: 'Test',
    playlists: [{ id: 42, name: 'TestPlaylist' }],
    session_id: 42,
    loadingText: 'Patience!'
};

const nextRoundObj = { next_round: [{ view: 'EXPLAINER', instruction: 'Instruction', title: 'Some title' }] };

const mockSessionStore = { id: 1 };
const mockParticipantStore = {
    id: 1,
    hash: '00000000-0000-0000-0000-000000000000',
    csrf_token: 'auSoWt7JA9fYyGE0Cc51tlYDnvGGxwo1HqVBsQHQ8dUE7QJZAjYZIieJc4kdYB4r',
    participant_id_url: 'url',
    country: 'nl',
};

vi.mock('../../API', () => ({
    useBlock: () => [Promise.resolve(blockObj), false],
    getNextRound: () => Promise.resolve(nextRoundObj)
}));


vi.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn: any) => {
        const state = {
            session: mockSessionStore,
            participant: mockParticipantStore,
            setError: vi.fn(),
            setSession: vi.fn(),
            setHeadData: vi.fn(),
            resetHeadData: vi.fn(),
            setBlock: vi.fn(),
            setRound: vi.fn(),
            setCurrentAction: vi.fn(),
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
        vi.clearAllMocks();
    });

    it('renders with given props', async () => {
        // Mock the useParticipantLink hook

        render(
            <MemoryRouter>
                <Block />
            </MemoryRouter>
        );
        await screen.findByText('Instruction');
    });

    it('calls onNext', async () => {
        const spy = vi.spyOn(API, 'getNextRound');
        spy.mockImplementationOnce(() => Promise.resolve(nextRoundObj))

        render(
            <MemoryRouter initialEntries={['/block/test']}>
                <Routes>
                    <Route path="/block/:slug" element={<Block />} />
                </Routes>
            </MemoryRouter>
        );
        await waitFor(() => expect(spy).toHaveBeenCalled());
    });

});
