import { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import MultiPlayer from "./MultiPlayer";
import MatchingPairs from "../MatchingPairs/MatchingPairs";
import Preload from "../Preload/Preload";
import { AUTOPLAY, BUTTON, MATCHINGPAIRS, PRELOAD, PlaybackAction, PlaybackView } from "@/types/Playback";
import { OnResultParams } from "@/hooks/useResultHandler";

export interface PlaybackProps extends PlaybackAction {
    onPreloadReady: () => void;
    autoAdvance: boolean;
    responseTime: number;
    submitResult: (result: OnResultParams) => void;
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
    const activeAudioEndedListener = useRef<() => void>();
    const [playingSections, setPlayingSections] = useState(sections)
    const [state, setState] = useState<PlaybackState>({ view: PRELOAD });

    const setView = (view: PlaybackView) => {
        setState({ view });
    }

    // check if the users device is webaudio compatible
    const playMethod = webAudio.compatibleDevice() ? sections[0].playMethod : 'EXTERNAL';

    // Cancel events
    const cancelAudioListeners = useCallback(() => {
        activeAudioEndedListener.current?.();
    }, []);

    // Cancel all events when component unmounts
    useEffect(() => {
        return () => {
            cancelAudioListeners();
        };
    }, [cancelAudioListeners]);

    // Audio ended playing
    const onAudioEnded = useCallback((index: number) => {
        setPlayingSections( prev => prev.map( (section, sectionIndex) => {
            if (index === sectionIndex) {
                return {
                    ...section,
                    playing: false,
                    hasPlayed: true
                }
            } else {
                return section
            }
        }))

        finishedPlaying();
    }, [finishedPlaying]);

    if (playMethod === 'EXTERNAL') {
        webAudio.closeWebAudio();
    }

    const getPlayheadShift = useCallback(() => {
        /* if the current Playback view has resumePlay set to true,
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

        // Determine if audio should be played
        if (index === -1 || mute) {
            pauseAudio(playMethod);
            return;
        }

        if (!playingSections[index].playing) {
            // only pause
            
            if (playingSections.filter(s => s.playing).length > 0) {
                // Load different audio if any other audio is playing
                pauseAudio(playMethod);
            }

            // set section as playing
            setPlayingSections( prev => prev.map((section, sectionIndex) => sectionIndex == index ? {...section, playing: true} : {...section, playing: false}) );

            const playheadShift = getPlayheadShift();
            const latency = playAudio(playingSections[index], playMethod, playheadShift + playingSections[index].playFrom);

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
        } else {
            pauseAudio(playMethod);
            setPlayingSections(prev => prev.map(section => {return { ...section, playing: false }}));
            return;
        }
    }, [playingSections, setPlayingSections, activeAudioEndedListener, cancelAudioListeners, getPlayheadShift, playMethod, startedPlaying, onAudioEnded, mute, resumePlay]
    );

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
            playSection,
            preloadMessage,
            instruction,
            playOnce,
            responseTime,
            scoreFeedbackDisplay,
            sections: playingSections,
            setView,
            showAnimation,
            startedPlaying,
            finishedPlaying,
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
