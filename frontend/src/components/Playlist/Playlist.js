import React, { useEffect } from "react";

// Playlist is an experiment view, that handles (auto)selection of a playlist
const Playlist = ({ experiment, instruction, onNext, playlist }) => {
    const playlists = experiment.playlists;

    useEffect(() => {
        if (playlists.length < 2) {
            console.error("This experiment defines a playlist view, but only has one playlist registered");
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

const PlaylistItem = ({ delay, playlist, onClick }) => (
    <li
        data-testid="playlist-item"
        onClick={() => {
            onClick(playlist.id);
        }}
        onKeyPress={() => {
            onClick(playlist.id);
        }}
        tabIndex="0"
        className="anim anim-fade-in-slide-left anim-speed-300"
        style={{ animationDelay: delay + "ms" }}
    >
        <i className="icon" />
        <span>{playlist.name}</span>
    </li>
);

export default Playlist;
