import { fireEvent, render, screen } from '@testing-library/react';
import { vi, describe, it, expect, } from 'vitest';

import Playlist from './Playlist';

vi.mock("../../util/stores");

describe('Playlist Component', () => {
    const playlist = { current: '42' };
    const block = {
        slug: 'test-experiment',
        playlists: [
            { id: '42', name: 'Playlist A' },
            { id: '43', name: 'Playlist B' }
        ]
    };
    const onNext = vi.fn();

    it('renders correctly with given props', () => {
        render(
            <Playlist block={block} instruction="instruction" onNext={onNext} playlist={playlist} />
        )
        expect(screen.getByTestId('playlist-instruction')).toBeTruthy();
        const playlistItems = screen.getAllByTestId('playlist-item');
        expect(playlistItems.length === 2);
    });

    it('calls onNext when playlist item is clicked', () => {
        render(
            <Playlist block={block} instruction="instruction" onNext={onNext} playlist={playlist} />
        )
        fireEvent.click(screen.getAllByTestId('playlist-item')[0]);
        expect(onNext).toHaveBeenCalled();
    })

    it('does not render with less than 2 playlists', () => {
        block.playlists = [{ id: '42', name: 'Playlist A' }];
        render(
            <Playlist block={block} instruction="instruction" onNext={onNext} playlist={playlist} />
        )
        expect(onNext).toHaveBeenCalled();
        expect(screen.queryByTestId('playlist-instruction')).toBeNull();
    });
});
