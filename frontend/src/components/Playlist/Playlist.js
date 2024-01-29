import React, { useEffect } from "react";

import { registerPlaylist } from "API";
import { useErrorStore, useParticipantStore, useSessionStore } from "util/stores";

// Playlist is an experiment view, that handles (auto)selection of a playlist
const Playlist = ({ experiment, instruction, onNext }) => {
    const playlists = experiment.playlists;
    const session = useSessionStore(state => state.session);
    const participant = useParticipantStore(state => state.participant);
    const setError = useErrorStore(state => state.setError);

    useEffect(() => {
        if (playlists.length < 2) {
            console.error("This experiment defines a playlist view, but only has one playlist registered");
        }
    }, [playlists])

    // Handle playlist action
    return (
        <div className="aha__playlist">
            <h3 className="title">{instruction}</h3>
            <ul>
                {playlists.map((playlist, index) => (
                    <PlaylistItem
                        key={playlist.id}
                        playlist={playlist}
                        onClick={(playlistId) => {
                            registerPlaylist(playlistId, participant, session).then(response => {
                                if (response) {
                                    onNext();
                                }
                                else {
                                    setError("Could not set playlist");
                                }
                            });
                        }}
                        delay={index * 250}
                    />
                ))}
            </ul>
        </div>
    );
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
