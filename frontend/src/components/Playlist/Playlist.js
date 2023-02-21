import React, { useEffect } from "react";
import Loading from "../Loading/Loading";

// Playlist is an experiment view, that handles (auto)selection of a playlist
const Playlist = ({ experiment, instruction, setPlaylist, onNext, setError }) => {
    const playlists = experiment.playlists;

    // Handle empty or single playlist
    useEffect(() => {
        if (playlists.length === 0) {
            setError("No playlist available");
        }

        if (playlists.length === 1) {
            // Only one playlist: advance
            setPlaylist(playlists[0].id);
            onNext();
        }
    }, [playlists, setError, setPlaylist, onNext]);

    // Handle playlist action
    switch (playlists.length) {
        case 0:
        case 1:
            return <Loading loadingText={experiment.loading_text} />;
        default:
            return (
                <div className="aha__playlist">
                    <h3 className="title">{instruction}</h3>

                    <ul>
                        {playlists.map((playlist, index) => (
                            <PlaylistItem
                                key={playlist.id}
                                playlist={playlist}
                                onClick={(playlistId) => {
                                    setPlaylist(playlistId);
                                    onNext();
                                }}
                                delay={index * 250}
                            />
                        ))}
                    </ul>
                </div>
            );
    }
};

const PlaylistItem = ({ delay, playlist, onClick }) => (
    <li
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
