import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import Playlist from './Playlist';

jest.mock("../../util/stores");

jest.mock('../../API', () => ({
    registerPlaylist: jest.fn(),
}));

describe('Playlist Component', () => {
    const experimentProp = { slug: 'test-experiment', playlists: [{id: 42}, {id: 43}] };
    it('renders correctly with given props', () => {
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={jest.fn()}/>
        )
        expect(screen.getByTestId('playlist-instruction')).toBeInTheDocument();
        const playlistItems = screen.getAllByTestId('playlist-item');
        expect(playlistItems.length === 2);
    });

    it('calls registerPlaylist when playlist item is clicked', async () => {
        const { registerPlaylist } = require('../../API');
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={jest.fn()}/>
        )
        registerPlaylist.mockResolvedValueOnce({});
        fireEvent.click(screen.getAllByTestId('playlist-item')[0]);
        await waitFor(() => expect(registerPlaylist).toHaveBeenCalled);
    })

    it('does not render with less than 2 playlists', () => {
        const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        experimentProp.playlists = [{id: 42}]
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={jest.fn()}/>
        )
        expect(consoleSpy).toHaveBeenCalled();
        expect(screen.queryByTestId('playlist-instruction')).not.toBeInTheDocument();
    });
});