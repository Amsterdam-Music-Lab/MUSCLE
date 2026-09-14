import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, } from 'vitest';

import * as API from '@/API';
import Playlist from './Playlist';

vi.mock('@/util/stores', () => ({
    __esModule: true,
    default: (fn: (state: any) => any) => {
        const state = {
            theme: {
                colorPrimary: "#d843e2"
            }
        };

        return fn(state);
    },
    useBoundStore: vi.fn()
}));

describe('Playlist Component', () => {
    const playlists = [
        { id: 42, name: "Country" },
        { id: 43, name: "Pop" },
        { id: 44, name: "RnB" }
    ];
    const onNext = vi.fn();
    const mockParticipant = {id: 'participant-id'};

    it('renders correctly with given props', () => {
        render(
            <Playlist instruction="instruction" onNext={onNext} playlists={playlists} participant={mockParticipant} />
        )
        expect(screen.getByTestId('playlist-instruction')).toBeTruthy();
        const playlistItems = screen.getAllByTestId('playlist-item');
        expect(playlistItems.length === 2);
    });

    it('calls setPlaylist when playlist item is clicked', () => {
        const spy = vi.spyOn(API, 'setPlaylist');
        spy.mockImplementationOnce(() => Promise.resolve({status: "ok"}));

        render(
            <Playlist instruction="instruction" onNext={onNext} playlists={playlists} participant={mockParticipant} />
        )
        fireEvent.click(screen.getAllByTestId('playlist-item')[0]);
        waitFor(() => expect(spy).toHaveBeenCalled());
    })

    it('does not render with less than 2 playlists', () => {
        render(
            <Playlist instruction="instruction" onNext={onNext} playlists={playlists.slice(0, 1)} participant={mockParticipant} />
        )
        expect(onNext).toHaveBeenCalled();
        expect(screen.queryByTestId('playlist-instruction')).toBeNull();
    });
});
