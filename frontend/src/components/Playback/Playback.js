import React, { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";
import ImagePlayer from "./ImagePlayer";
import MatchingPairs from "./MatchingPairs";
import Preload from "../Preload/Preload";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const IMAGE = "IMAGE";
export const MATCHINGPAIRS = "MATCHINGPAIRS";
export const PRELOAD = "PRELOAD";

const Playback = ({
    playbackArgs,
    onPreloadReady,
    autoAdvance,
    responseTime,
    time,
    submitResult,
    startedPlaying,
    finishedPlaying,
}) => {
    const [playerIndex, setPlayerIndex] = useState(-1);
    const lastPlayerIndex = useRef(-1);
    const activeAudioEndedListener = useRef(null);
    const [state, setState] = useState({ view: PRELOAD });
    const setView = (view, data = {}) => {
        setState({ view, ...data });
    }

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
        if (playbackArgs.timeout_after_playback) {
            setTimeout(finishedPlaying, playbackArgs.timeout_after_playback);
        } else {
            finishedPlaying();
        }
    }, [playbackArgs, finishedPlaying]);
    
    // Keep track of last player index
    useEffect(() => {
        lastPlayerIndex.current = playerIndex;
    }, [playerIndex]);

    if (playbackArgs.play_method === 'EXTERNAL') {                    
        webAudio.closeWebAudio();            
    }

    // Play section with given index
    const playSection = useCallback((index = 0) => {
        if (index !== lastPlayerIndex.current) {
            // Load different audio
            if (prevPlayerIndex.current !== -1) {
                pauseAudio(playbackArgs);
            }                
            // Store player index
            setPlayerIndex(index);
            // Determine if audio should be played
            if (playbackArgs.play_from) {
                setPlayerIndex(-1);
                pauseAudio(playbackArgs);
                return;
            }
            let latency = playAudio(playbackArgs, playbackArgs.sections[index]);
            // Cancel active events
            cancelAudioListeners();
            // listen for active audio events
            if (playbackArgs.play_method === 'BUFFER') {
                activeAudioEndedListener.current = webAudio.listenOnce("ended", onAudioEnded);
            } else {
                activeAudioEndedListener.current = audio.listenOnce("ended", onAudioEnded);
            }                    
            // Compensate for audio latency and set state to playing
            setTimeout(startedPlaying && startedPlaying(), latency);
            return;
        }
        // Stop playback
        if (lastPlayerIndex.current === index) {
                pauseAudio(playbackArgs);                     
                setPlayerIndex(-1);
                return;
        }
    },[playbackArgs, activeAudioEndedListener, cancelAudioListeners, startedPlaying, onAudioEnded]
    );

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        pauseAudio(playbackArgs);
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying, playbackArgs]);

    // Stop audio on unmount
    useEffect(
        () => {
            return pauseAudio(playbackArgs);
        },
        [playbackArgs]
    );

    // // Autoplay
    // useEffect(() => {
    //     playbackArgs.view === 'AUTOPLAY' && playSection(0);
    // }, [playbackArgs, playSection]);

    const render = (view) => {
        const attrs = {
            playbackArgs,
            setView,
            autoAdvance,
            responseTime,
            time,
            startedPlaying,
            playerIndex,
            finishedPlaying: onFinishedPlaying,
            playSection,
            lastPlayerIndex,
            setPlayerIndex,
            submitResult
        };

        switch (state.view) {
            case PRELOAD:
                return (
                    <Preload {...attrs}
                        onNext={() => {                        
                            setView(playbackArgs.view);
                            onPreloadReady();
                        }}
                    />
            );
            case AUTOPLAY:
                return <AutoPlay {...attrs} />;
            case BUTTON:
                return (
                    <PlayButton
                        {...attrs}
                        isPlaying={playerIndex > -1}
                        disabled={playbackArgs.play_once && hasPlayed.includes(0)}
                    />
                );
            case MULTIPLAYER:
                return (
                    <MultiPlayer
                        {...attrs}
                        disabledPlayers={playbackArgs.play_once ? hasPlayed : undefined}
                    />
                );
            case IMAGE:
                return (
                    <ImagePlayer
                        {...attrs}
                        disabledPlayers={playbackArgs.play_once ? hasPlayed : undefined}
                    />
                );
            case MATCHINGPAIRS:
                return (
                    <MatchingPairs
                        {...attrs}
                        stopAudioAfter={playbackArgs.stop_audio_after}
                    />
                );
            default:
                return <div> Unknown player view {view} </div>;
        }
    };
    
    return (
        <div className="aha__playback">
            <div className="playback"> {render(playbackArgs.view)} </div>{" "}
        </div>
    );
};
export default Playback;
