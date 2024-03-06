import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';

import Playlist from './Playlist';

vi.mock("../../util/stores");

describe('Playlist Component', () => {
    const playlist = { current: 25 };
    const experimentProp = { slug: 'test-experiment', playlists: [{id: 42}, {id: 43}] };
    const onNext = vi.fn();

    it('renders correctly with given props', () => {
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={onNext} playlist={playlist}/>
        )
        expect(screen.getByTestId('playlist-instruction')).to.exist;
        const playlistItems = screen.getAllByTestId('playlist-item');
        expect(playlistItems.length === 2);
    });

    it('calls onNext when playlist item is clicked', () => {
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={onNext} playlist={playlist}/>
        )
        fireEvent.click(screen.getAllByTestId('playlist-item')[0]);
        expect((onNext).toHaveBeenCalled);
    })

    it('does not render with less than 2 playlists', () => {
        experimentProp.playlists = [{id: 42}]
        render(
            <Playlist experiment={experimentProp} instruction="instruction" onNext={onNext} playlist={playlist}/>
        )
        expect((onNext).toHaveBeenCalled);
        expect(screen.queryByTestId('playlist-instruction')).not.to.exist;
    });
});