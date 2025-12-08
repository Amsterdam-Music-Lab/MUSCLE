import { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import MultiPlayer from "./MultiPlayer";
import MatchingPairs from "../MatchingPairs/MatchingPairs";
import Preload from "../Preload/Preload";
import { AUTOPLAY, BUTTON, MATCHINGPAIRS, PRELOAD, PlaybackAction, PlaybackView } from "@/types/Playback";

export interface PlaybackProps extends PlaybackAction {
    onPreloadReady: () => void;
    autoAdvance: boolean;
    responseTime: number;
    submitResult: (result: any) => void;
    startedPlaying?: () => void;
    finishedPlaying: () => void;
}

interface PlaybackState {
    view: PlaybackView;
}

const Playback = ({
    sections,
    view,
    instruction,
    preloadMessage,
    playOnce,
    showAnimation,
    resumePlay=false,
    mute=false,
    scoreFeedbackDisplay,
    onPreloadReady,
    autoAdvance,
    responseTime,
    submitResult,
    startedPlaying,
    finishedPlaying,
}: PlaybackProps) => {
    const [playerIndex, setPlayerIndex] = useState(-1);
    const [hasPlayed, setHasPlayed] = useState<number[]>([]);
    const activeAudioEndedListener = useRef<() => void>();
    const [state, setState] = useState<PlaybackState>({ view: PRELOAD });

    const setView = (view: PlaybackView) => {
        setState({ view });
    }

    // check if the users device is webaudio compatible
    const playMethod = webAudio.compatibleDevice() ? sections[0].playMethod : 'EXTERNAL';

    useEffect(() => {
        if (playerIndex !== -1 && !hasPlayed.includes(playerIndex)) {
            setHasPlayed((prev) => [...prev, playerIndex]);
        }
    }, [playerIndex, hasPlayed]);

    // Cancel events
    const cancelAudioListeners = useCallback(() => {
        activeAudioEndedListener.current
            && activeAudioEndedListener.current();
    }, []);

    // Cancel all events when component unmounts
    useEffect(() => {
        return () => {
            cancelAudioListeners();
        };
    }, [cancelAudioListeners]);

    // Audio ended playing
    const onAudioEnded = useCallback((index: number) => {

        // If the player index is not the last player index, return
        if (playerIndex === index) {
            setPlayerIndex(-1);
        }

        finishedPlaying();
    }, [finishedPlaying]);

    if (playMethod === 'EXTERNAL') {
        webAudio.closeWebAudio();
    }

    const getPlayheadShift = useCallback(() => {
        /* if the current Playback view has resume_play set to true,
        retrieve previous Playback view's decisionTime from sessionStorage
        */
        return resumePlay ?
            parseFloat(window.sessionStorage.getItem('decisionTime')) : 0;
    }, [resumePlay]
    )

    // Play section with given index
    const playSection = useCallback((index = 0) => {
        if (playMethod === 'NOAUDIO') {
            return;
        }
        if (index !== playerIndex) {
            // Load different audio
            if (playerIndex !== -1) {
                pauseAudio(playMethod);
            }

            // Store player index
            setPlayerIndex(index);

            // Determine if audio should be played
            if (mute) {
                setPlayerIndex(-1);
                pauseAudio(playMethod);
                return;
            }
            const section = sections[index]

            let latency = playAudio(section, playMethod, getPlayheadShift() + section.playFrom);

            // Cancel active events
            cancelAudioListeners();

            // listen for active audio events
            if (playMethod === 'BUFFER') {
                activeAudioEndedListener.current = webAudio.listenOnce("ended", () => onAudioEnded(index));
            } else {
                activeAudioEndedListener.current = audio.listenOnce("ended", () => onAudioEnded(index));
            }

            // Compensate for audio latency and set state to playing
            if (startedPlaying) {
                setTimeout(startedPlaying, latency);
            }

            return;
        }
        // Stop playback
        if (playerIndex === index) {
            pauseAudio(playMethod);
            setPlayerIndex(-1);
            return;
        }
    }, [sections, activeAudioEndedListener, cancelAudioListeners, getPlayheadShift, playMethod, startedPlaying, onAudioEnded, mute, resumePlay]
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

    const render = (view: PlaybackView) => {
        const attrs = {
            autoAdvance,
            finishedPlaying: onFinishedPlaying,
            playSection,
            playing:playerIndex,
            hasPlayed,
            preloadMessage,
            instruction,
            playOnce,
            responseTime,
            scoreFeedbackDisplay,
            sections,
            setView,
            showAnimation,
            startedPlaying,
            submitResult,
            view,
        };

        switch (state.view) {
            case PRELOAD:
                return (
                    <Preload {...attrs}
                        playMethod={playMethod}
                        preloadMessage={preloadMessage}
                        onNext={() => {
                            setView(view);
                            onPreloadReady();
                        }}
                    />
                );
            case AUTOPLAY:
                return <AutoPlay {...attrs}
                    instruction={instruction}
                />;
            case BUTTON:
                return (
                    <MultiPlayer
                        {...attrs}
                    />
                );
            case MATCHINGPAIRS:
                return (
                    <MatchingPairs
                        {...attrs}
                        scoreFeedbackDisplay={scoreFeedbackDisplay}
                        view={playMethod === 'NOAUDIO' ? 'visual' : ''}
                    />
                );
            default:
                return <div> Unknown player view {view} </div>;
        }
    };

    return (
        <div className="aha__playback">
            <div className="playback"> {render(view)} </div>{" "}
        </div>
    );
};
export default Playback;
