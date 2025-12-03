import { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import MultiPlayer from "./MultiPlayer";
import MatchingPairs from "../MatchingPairs/MatchingPairs";
import Preload from "../Preload/Preload";
import { AUTOPLAY, BUTTON, MATCHINGPAIRS, PRELOAD, PlaybackAction, PlaybackView } from "@/types/Playback";
import PlaybackSection from "@/types/Section";

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
    sections: initialSections,
    showAnimation,
    preloadMessage,
    instruction,
    view,
    mute,
    resumePlay,
    playOnce=false,
    scoreFeedbackDisplay,
    onPreloadReady,
    autoAdvance,
    responseTime,
    submitResult,
    startedPlaying,
    finishedPlaying,
}: PlaybackProps) => {
    const activeAudioEndedListener = useRef<() => void>();
    const [state, setState] = useState<PlaybackState>({ view: PRELOAD });

    const setView = (view: PlaybackView) => {
        setState({ view });
    }

    // check if the users device is webaudio compatible
    const playMethod = webAudio.compatibleDevice() ? initialSections[0].playMethod : 'EXTERNAL';

    // Keep track of which section has played
    const [sections, setSections] = useState(() => initialSections.map(section => ({
        ...section,
        hasPlayed: false,
        playing: false
    })));

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
    const onAudioEnded = useCallback((section: PlaybackSection) => {
        // If the player index is not the last player index, return
        setSections(currentSections => currentSections.map(currentSection => {
            section.playing = false;
            if (currentSection.link === section.link) {
                return {...section, hasPlayed:true};
            } else {
                return section
            }
        }))
        finishedPlaying();
    }, [finishedPlaying]);

    if (playMethod === 'EXTERNAL') {
        webAudio.closeWebAudio();
    }

    const getPlayheadShift = () => {
        return resumePlay ? parseFloat(window.sessionStorage.getItem('decisionTime')) : 0
    }

    // Play section with given index
    const playSection = useCallback((section: PlaybackSection) => {
        if (section.playMethod === 'NOAUDIO') {
            return;
        }
        if (!section.playing) {
            // Load different audio
            pauseAudio(playMethod);

            // Change the playing state
            setSections(currentSections => currentSections.map(currentSection => {
                if (currentSection.link === section.link) {
                    return {...currentSection, playing: true}
                } else {
                    return {...currentSection, playing: false}
                }
            }))

            // Determine if audio should be played
            if (mute) {
                pauseAudio(playMethod);
                return;
            }

            const playheadShift = getPlayheadShift() + section.playFrom | 0;
            let latency = playAudio(section, playMethod, playheadShift);

            // Cancel active events
            cancelAudioListeners();

            // listen for active audio events
            if (playMethod === 'BUFFER') {
                activeAudioEndedListener.current = webAudio.listenOnce("ended", () => onAudioEnded(section));
            } else {
                activeAudioEndedListener.current = audio.listenOnce("ended", () => onAudioEnded(section));
            }

            // Compensate for audio latency and set state to playing
            if (startedPlaying) {
                setTimeout(startedPlaying, latency);
            }

            return;
        }
        // Stop playback
        if (section.playing) {
            pauseAudio(playMethod);
            return;
        }
    }, [sections, activeAudioEndedListener, cancelAudioListeners, getPlayheadShift, startedPlaying, onAudioEnded]
    );

    // Local logic for onfinished playing
    const onFinishedPlaying = useCallback(() => {
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
            responseTime,
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
                        playOnce={playOnce}
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
            <div className="playback"> {render(playbackArgs.view)} </div>{" "}
        </div>
    );
};
export default Playback;
