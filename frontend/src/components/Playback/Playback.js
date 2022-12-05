import React, { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import { MEDIA_ROOT } from "../../config";

import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";
import SpectrogramPlayer from "./SpectrogramPlayer";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const SPECTROGRAM = "SPECTROGRAM";

const Playback = ({
    playerType,
    sections,
    instruction,
    onPreloadReady,
    preloadMessage,
    autoAdvance,
    decisionTime,
    playConfig = {},
    time,
    makeResult,
    startedPlaying,
    finishedPlaying,
}) => {
    const [playerIndex, setPlayerIndex] = useState(-1);
    const lastPlayerIndex = useRef(-1);
    const activeAudioEndedListener = useRef(null);
    const xPosition = useRef(-1);
    const yPosition = useRef(-1);

    const resultBuffer = [];

    // Keep track of which player has played, in a an array of player indices
    const [hasPlayed, setHasPlayed] = useState([]);
    const prevPlayerIndex = useRef(-1);

    useEffect(() => {
        const index = prevPlayerIndex.current;
        if (index !== -1) {
            setHasPlayed((hasPlayed) =>
                index === -1 || hasPlayed.includes(index) ? hasPlayed : [...hasPlayed, index]
            );
        }
        prevPlayerIndex.current = parseInt(playerIndex);
    }, [playerIndex]);

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
        return () => {
            cancelAudioListeners();
        };
    }, [cancelAudioListeners]);

    // Audio ended playing
    const onAudioEnded = useCallback(() => {
        setPlayerIndex(-1);

        //AJ: added for categorization experiment for form activation after playback and auto_advance to work properly
        if (playConfig.timeout_after_playback) {
            setTimeout(finishedPlaying, playConfig.timeout_after_playback);
        } else {
            finishedPlaying();
        }

    }, []);

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
            activeAudioEndedListener.current = audio.listenOnce("ended", onAudioEnded);

            // Play audio
            audio.playFrom(Math.max(0, playConfig.playhead || 0));
            startedPlaying && startedPlaying();
        },
        [cancelAudioListeners, playConfig.mute, playConfig.playhead, startedPlaying, onAudioEnded]
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
<<<<<<< HEAD
                audio.loadUntilAvailable(
                    MEDIA_ROOT + sections[index].url,
                    () => { 
                        playAudio(index);
                    }
                );
                checkMatchingPairs(index);
                
=======
                audio.loadUntilAvailable(MEDIA_ROOT + sections[index].url, () => {
                    playAudio(index);
                });
>>>>>>> develop
                return;
            }

            // Stop playback
            if (lastPlayerIndex.current === index) {
                audio.pause();
                setPlayerIndex(-1);
                return;
            }

            // Start playback
            playAudio(index);
        },
        [playAudio, sections]
    );

    const registerUserClicks = (posX, posY) => {
        xPosition.current = posX;
        yPosition.current = posY;
    }

    const checkMatchingPairs = (index) => {
        resultBuffer.push({
            selectedSection: sections[index],
            xPosition: xPosition.current,
            yPosition: yPosition.current
        })
        
        if (sections.filter(s => s.turned).length < 2) {
            sections[index].turned = true;
        } else {
            sections.forEach(section => section.turned = false);
            sections[index].turned = true;
            return;
        }

        if (lastPlayerIndex.current >=0 && sections[lastPlayerIndex.current].id === sections[index].id) {
            // match
            sections[lastPlayerIndex.current].inactive = true;
            sections[index].inactive = true;
            if (sections.filter(s => s.inactive).length === sections.length) {
                // all cards have been turned
                makeResult(resultBuffer);
            }
        }
        return;
    }

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying]);

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
            startedPlaying,
            playerIndex,
            finishedPlaying: onFinishedPlaying,
            playSection,
            registerUserClicks
        };

        switch (view) {
            case AUTOPLAY:
                return <AutoPlay {...attrs} onPreloadReady={onPreloadReady} />;
            case BUTTON:
                return (
                    <PlayButton
                        {...attrs}
                        isPlaying={playerIndex > -1}
                        disabled={playConfig.play_once && hasPlayed.includes(0)}
                    />
                );
            case MULTIPLAYER:
                return (
                    <MultiPlayer
                        {...attrs}
                        disabledPlayers={playConfig.play_once ? hasPlayed : undefined}
                    />
                );
            case SPECTROGRAM:
                return (
                    <SpectrogramPlayer
                        {...attrs}
                        disabledPlayers={playConfig.play_once ? hasPlayed : undefined}
                    />
                );
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
