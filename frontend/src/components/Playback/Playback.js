import React, { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";
import SpectrogramPlayer from "./SpectrogramPlayer";
import MatchingPairs from "./MatchingPairs";
import Preload from "../Preload/Preload";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const SPECTROGRAM = "SPECTROGRAM";
export const MATCHINGPAIRS = "MATCHINGPAIRS";
export const PRELOAD = "PRELOAD";

const Playback = ({
    playerType,
    sections,
    instruction,
    onPreloadReady,
    preloadMessage = '',
    autoAdvance,
    responseTime,
    playConfig = {},
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
        if (playConfig.timeout_after_playback) {
            setTimeout(finishedPlaying, playConfig.timeout_after_playback);
        } else {
            finishedPlaying();
        }
    }, []);
    
    // Keep track of last player index
    useEffect(() => {
        lastPlayerIndex.current = playerIndex;
    }, [playerIndex]);

    if (playConfig.play_method === 'EXTERNAL') {                    
        webAudio.closeWebAudio();            
    }

    // Play section with given index
    const playSection = useCallback(
        (index = 0) => {
            
                if (index !== lastPlayerIndex.current) {
                    // Load different audio
                    if (prevPlayerIndex.current !== -1) {
                        pauseAudio(playConfig);
                    }                
                    // Store player index
                    setPlayerIndex(index);

                    // Determine if audio should be played
                    if (playConfig.mute) {
                        setPlayerIndex(-1);
                        pauseAudio(playConfig);
                        return;
                    }
                    const playheadShift = getPlayheadShift();
                    let latency = playAudio(playConfig, sections[index], playheadShift);

                    // Cancel active events
                    cancelAudioListeners();

                    // listen for active audio events
                    if (playConfig.play_method === 'BUFFER') {
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
                        pauseAudio(playConfig);                     
                        setPlayerIndex(-1);
                        return;
                    }
            },
            [playAudio, pauseAudio, sections, activeAudioEndedListener, cancelAudioListeners, startedPlaying, onAudioEnded]
    );

    const getPlayheadShift = () => {
        /* if the current Playback view has resume_play set to true,
        retrieve previous Playback view's decisionTime from sessionStorage
        */
        return playConfig.resume_play ? 
        parseFloat(window.sessionStorage.getItem('decisionTime')) : 0;
    }

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        pauseAudio(playConfig);
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying]);

    // Stop audio on unmount
    useEffect(
        () => () => {
            pauseAudio(playConfig);
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
            setView,
            instruction,
            preloadMessage,
            autoAdvance,
            responseTime,
            playConfig,
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
                    <Preload
                        instruction={preloadMessage}
                        duration={playConfig.ready_time}                        
                        sections={sections}
                        playConfig={playConfig}
                        onNext={() => {                        
                            setView(playerType);
                            onPreloadReady();
                        }}
                    />
            );
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
            case MATCHINGPAIRS:
                return (
                    <MatchingPairs
                        {...attrs}
                        stopAudioAfter={playConfig.stop_audio_after}
                        showAnimations={playConfig.show_animations}
                        histogramBars={playConfig.histogram_bars}
                        showTotalScore={playConfig.show_total_score}
                        showScoreMessage={playConfig.show_score_message}
                        showTurnFeedback={playConfig.show_turn_feedback}
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
