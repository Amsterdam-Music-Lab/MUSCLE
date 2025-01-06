import { Playlist as PlaylistAction } from "@/types/Action";
import Block from "@/types/Block";
import { useEffect } from "react";

export interface PlaylistProps extends PlaylistAction {
    block: Block;
    onNext: () => void;
}

/**
 * Playlist is a block view, that handles (auto)selection of a playlist
 */
const Playlist = ({ block, instruction, onNext, playlist }: PlaylistProps) => {
    const playlists = block.playlists;

    useEffect(() => {
        if (playlists.length < 2) {
            // silently proceed to next view
            onNext();
        }
    }, [playlists, onNext])

    // Handle playlist action
    if (playlists.length > 1) {
        return (
            <div className="aha__playlist">
                <h3 data-testid="playlist-instruction" className="title">{instruction}</h3>
                <ul>
                    {playlists.map((playlistItem, index) => (
                        <PlaylistItem
                            key={playlistItem.id}
                            playlist={playlistItem}
                            onClick={(playlistId) => {
                                playlist.current = playlistId;
                                onNext();
                            }}
                            delay={index * 250}
                        />
                    ))}
                </ul>
            </div>
        );
    } else { return null };
};

interface PlaylistItemProps {
    delay: number;
    playlist: { id: string, name: string };
    onClick: (playlistId: string) => void;
}

const PlaylistItem = ({ delay, playlist, onClick }: PlaylistItemProps) => (
    <li
        data-testid="playlist-item"
        onClick={() => {
            onClick(playlist.id);
        }}
        onKeyPress={() => {
            onClick(playlist.id);
        }}
        tabIndex={0}
        className="anim anim-fade-in-slide-left anim-speed-300"
        style={{ animationDelay: delay + "ms" }}
    >
        <i className="icon" />
        <span>{playlist.name}</span>
    </li>
);

export default Playlist;
