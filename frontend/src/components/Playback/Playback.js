import React, { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { MEDIA_ROOT } from "../../config";

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
    preloadMessage,
    autoAdvance,
    responseTime,
    playConfig = {},
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
        if (playConfig.timeout_after_playback) {
            setTimeout(finishedPlaying, playConfig.timeout_after_playback);
        } else {
            finishedPlaying();
        }
    }, []);

    // Play audio
    const playAudio = useCallback(
        (index) => {
            let latency = 0;
            if (playConfig.play_method === 'BUFFER' && !playConfig.external_audio) {
                console.log('Play buffer (local)');                

                // Determine latency for current audio device
                latency = webAudio.getTotalLatency();

                // Store player index
                setPlayerIndex(index);

                // Determine if audio should be played
                if (playConfig.mute) {
                    setPlayerIndex(-1);
                    webAudio.stopBuffer();
                    return;
                }
    
                // Cancel active events
                cancelAudioListeners();           
                
                // Play audio
                webAudio.playBuffer(sections[index].id);

                // listen for active audio events
                activeAudioEndedListener.current = webAudio.listenOnce("ended", onAudioEnded);                
            } else {
                console.log('Play HTML audo')

                // Only initialize webaudio if section is local            
                if (!playConfig.external_audio) {                    
                    latency = webAudio.initWebAudio();
                }

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
            }
            // Compensate for audio latency and set state to playing
            setTimeout(startedPlaying && startedPlaying(), latency);            
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
            if (playConfig.play_method === 'BUFFER' && !playConfig.external_audio) {
                // Play section from buffer
                if (index !== lastPlayerIndex.current) {
                    // Load different audio
                    if (prevPlayerIndex.current !== -1) {
                        stopPlaying();
                    }                
                    playAudio(index);
                    return;
                }

                // Stop playback
                if (lastPlayerIndex.current === index) {
                    webAudio.suspend();
                    setPlayerIndex(-1);
                    return;
                }

                // Start playback
                playAudio(index);
            } else {
                if (playConfig.external_audio) {
                    // webAudio.closeWebAudio();
                }

                // Play section from <AUDIO> tag
                if (index !== lastPlayerIndex.current) {
                    // Load different audio
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

                // Start playback
                playAudio(index);
            }
            
        },
        [playAudio, sections]
    );

    const stopPlaying = () => {
        if (playConfig.play_method === 'BUFFER' && !playConfig.external_audio) {
            webAudio.stopBuffer();
        } else {
            audio.stop();
        }
    }

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
        setPlayerIndex(-1);
        stopPlaying();
        finishedPlaying && finishedPlaying();
    }, [finishedPlaying]);

    // Stop audio on unmount
    useEffect(
        () => () => {
            stopPlaying();
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
