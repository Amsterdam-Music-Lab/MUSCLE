import React, { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import { MEDIA_ROOT } from "../../config";

import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";

const Playback = ({
    playerType,
    sections,
    instruction,
    onPreloadReady,
    preloadMessage,
    autoAdvance,
    decisionTime,
    playConfig,
    time,
    submitResult,
    startedPlaying,
    finishedPlaying,
}) => {
    const [playerIndex, setPlayerIndex] = useState(-1);
    const lastPlayerIndex = useRef(-1);
    const activeAudioEndedListener = useRef(null);

    // Preload first section
    useEffect(() => {
        return audio.loadUntilAvailable(MEDIA_ROOT + sections[0].url, () => {});
    }, [sections]);

    // Cancel events
    const cancelAudioListeners = useCallback(() => {
        activeAudioEndedListener.current && activeAudioEndedListener.current();
    }, []);

    // Cancel all events when component unmounts
    useEffect(() => {
        cancelAudioListeners();
    }, [cancelAudioListeners]);

    // Play audio
    const playAudio = useCallback(
        (index) => {
            // Store player index
            setPlayerIndex(index);

            // Determine if audio should be played
            if (playConfig.mute) {
                setPlayerIndex(-1);
                audio.pause();
                return;
            }
            // Volume 1
            audio.setVolume(1);

            // Cancel active events
            cancelAudioListeners();

            // listen for active audio events
            activeAudioEndedListener.current = audio.listenOnce(
                "ended",
                onAudioEnded
            );

            // Play audio
            audio.playFrom(Math.max(0, playConfig.playhead));
            startedPlaying();
        },
        [
            cancelAudioListeners,
            playConfig.mute,
            playConfig.playhead,
            startedPlaying,
        ]
    );

    // Keep track of last player index
    useEffect(() => {
        lastPlayerIndex.current = playerIndex;
    }, [playerIndex]);

    // Play section with given index
    const playSection = useCallback(
        (index = 0) => {
            // Load different audio
            if (index !== lastPlayerIndex.current) {
                audio.loadUntilAvailable(
                    MEDIA_ROOT + sections[index].url,
                    () => {
                        playAudio(index);
                    }
                );
                return;
            }

            // Stop playback
            if (lastPlayerIndex.current === index) {
                audio.pause();
                setPlayerIndex(-1);
                return;
            }

            // Start plback
            playAudio(index);
        },
        [playAudio, sections]
    );

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying]);

    // Audio ended playing
    const onAudioEnded = useCallback(() => {
        setPlayerIndex(-1);
    }, []);

    // Stop audio on unmount
    useEffect(
        () => () => {
            audio.stop();
        },
        []
    );

    // Autoplay
    useEffect(() => {
        playConfig.auto_play && playSection(0);
    }, [playConfig.auto_play, playSection]);

    const render = (view) => {
        const attrs = {
            sections,
            instruction,
            preloadMessage,
            autoAdvance,
            decisionTime,
            playConfig,
            time,
            submitResult,
            startedPlaying,
            playerIndex,
            finishedPlaying: onFinishedPlaying,
            playSection,
        };

        switch (view) {
            case AUTOPLAY:
                return <AutoPlay {...attrs} onPreloadReady={onPreloadReady} />;
            case BUTTON:
                return <PlayButton {...attrs} isPlaying={playerIndex > -1} />;
            case MULTIPLAYER:
                return <MultiPlayer {...attrs} />;
            default:
                return <div> Unknown player view {view} </div>;
        }
    };

    return (
        <div className="aha__playback">
            <div className="playback"> {render(playerType)} </div>{" "}
        </div>
    );
};
export default Playback;
