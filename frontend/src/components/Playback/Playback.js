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
    const playMethod = playbackArgs.play_method;
    const sections = playbackArgs.sections;

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

    if (playMethod === 'EXTERNAL') {                    
        webAudio.closeWebAudio();            
    }

    const getPlayheadShift = useCallback(() => {
        /* if the current Playback view has resume_play set to true,
        retrieve previous Playback view's decisionTime from sessionStorage
        */
        return playbackArgs.resume_play ? 
        parseFloat(window.sessionStorage.getItem('decisionTime')) : 0;
    }, [playbackArgs]
    )

    // Play section with given index
    const playSection = useCallback((index = 0) => {
        if (index !== lastPlayerIndex.current) {
            // Load different audio
            if (prevPlayerIndex.current !== -1) {
                pauseAudio(playMethod);
            }                
            // Store player index
            setPlayerIndex(index);
            // Determine if audio should be played
            if (playbackArgs.mute) {
                setPlayerIndex(-1);
                pauseAudio(playMethod);
                return;
            }
                
            const playheadShift = getPlayheadShift();
            let latency = playAudio(playMethod, sections[index], playheadShift);
            // Cancel active events
            cancelAudioListeners();
            // listen for active audio events
            if (playMethod === 'BUFFER') {
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
                pauseAudio(playMethod);                     
                setPlayerIndex(-1);
                return;
        }
    }, [sections, activeAudioEndedListener, cancelAudioListeners, getPlayheadShift, playbackArgs, playMethod, startedPlaying, onAudioEnded]
    );

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        pauseAudio(playMethod);
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying, playMethod]);

    // Stop audio on unmount
    useEffect(
        () => {
            return () => pauseAudio(playMethod);
        },
        [playMethod]
    );

    const render = (view) => {
        const attrs = {
            sections,
            showAnimation: playbackArgs.show_animation,
            setView,
            autoAdvance,
            responseTime,
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
                        playMethod={playbackArgs.play_method}
                        duration={playbackArgs.ready_time}
                        preloadMessage={playbackArgs.preload_message}
                        onNext={() => {                        
                            setView(playbackArgs.view);
                            onPreloadReady();
                        }}
                    />
            );
            case AUTOPLAY:
                return <AutoPlay {...attrs}
                        instruction={playbackArgs.instruction}
                />;
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
                        labels={playbackArgs.labels}
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
