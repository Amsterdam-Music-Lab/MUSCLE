import { useEffect } from "react";

import { setPlaylist } from "@/API";
import { PlaylistAction, SharedActionProps, Playlist as IPlaylist } from "@/types/Action";
import useBoundStore from "@/util/stores";

/**
 * Playlist is a block view, that handles (auto)selection of a playlist
 */
const Playlist = ({ instruction, onNext, playlists, participant }: PlaylistAction & SharedActionProps) => {
    const session = useBoundStore((state) => state.session);
    const theme = useBoundStore((state) => state.theme);

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
                                setPlaylist({sessionID: session!.id, playlistID: playlistId, participant}).then( () => onNext() );
                            }}
                            delay={index * 250}
                            iconColor={theme!.colorPrimary}
                        />
                    ))}
                </ul>
            </div>
        );
    } else { return null };
};

interface PlaylistItemProps {
    delay: number;
    playlist: IPlaylist;
    onClick: (playlistId: number) => void;
    iconColor: string;
}

const PlaylistItem = ({ delay, playlist, onClick, iconColor }: PlaylistItemProps) => (
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
        <i className="icon" style={{backgroundColor: iconColor}}/>
        <span>{playlist.name}</span>
    </li>
);

export default Playlist;
