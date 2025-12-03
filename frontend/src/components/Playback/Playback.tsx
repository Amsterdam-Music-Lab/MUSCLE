import { useState, useEffect, useRef, useCallback } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { playAudio, pauseAudio } from "../../util/audioControl";

import AutoPlay from "./Autoplay";
import PlayButton from "./PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";
import ImagePlayer from "./ImagePlayer";
import MatchingPairs from "../MatchingPairs/MatchingPairs";
import Preload from "../Preload/Preload";
import { AUTOPLAY, BUTTON, IMAGE, MATCHINGPAIRS, MULTIPLAYER, PRELOAD, PlaybackArgs, PlaybackView } from "@/types/Playback";

export interface PlaybackProps {
    playbackArgs: PlaybackArgs;
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
    playbackArgs,
    onPreloadReady,
    autoAdvance,
    responseTime,
    submitResult,
    startedPlaying,
    finishedPlaying,
}: PlaybackProps) => {
    const [playerIndex, setPlayerIndex] = useState(-1);
    const lastPlayerIndex = useRef(-1);
    const activeAudioEndedListener = useRef<() => void>();
    const [state, setState] = useState<PlaybackState>({ view: PRELOAD });

    const setView = (view: PlaybackView) => {
        setState({ view });
    }

    // check if the users device is webaudio compatible
    const playMethod = webAudio.compatibleDevice() ? playbackArgs.play_method : 'EXTERNAL';

    const { sections, style } = playbackArgs;

    // Keep track of which player has played, in a an array of player indices
    const [hasPlayed, setHasPlayed] = useState<number[]>([]);
    const prevPlayerIndex = useRef(-1);

    useEffect(() => {
        const index = prevPlayerIndex.current;
        if (index !== -1) {
            setHasPlayed((hasPlayed) =>
                index === -1 || hasPlayed.includes(index) ? hasPlayed : [...hasPlayed, index]
            );
        }
        prevPlayerIndex.current = parseInt(playerIndex, 10);
    }, [playerIndex]);

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
        if (lastPlayerIndex.current === index) {
            setPlayerIndex(-1);
        }

        finishedPlaying();
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
        if (playMethod === 'NOAUDIO') {
            return;
        }
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
            let latency = playAudio(sections[index], playMethod, playheadShift + playbackArgs.play_from);

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

    const render = (view: PlaybackView) => {
        const attrs = {
            autoAdvance,
            finishedPlaying: onFinishedPlaying,
            labels: playbackArgs.labels,
            lastPlayerIndex,
            playSection,
            playerIndex,
            responseTime,
            sections,
            setPlayerIndex,
            setView,
            style,
            showAnimation: playbackArgs.show_animation,
            startedPlaying,
            submitResult,
            view,
        };

        switch (state.view) {
            case PRELOAD:
                return (
                    <Preload {...attrs}
                        playMethod={playMethod}
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
                        images={playbackArgs.images}
                        image_labels={playbackArgs.image_labels}
                        disabledPlayers={playbackArgs.play_once ? hasPlayed : undefined}
                    />
                );
            case MATCHINGPAIRS:
                return (
                    <MatchingPairs
                        {...attrs}
                        showAnimation={playbackArgs.show_animation}
                        scoreFeedbackDisplay={playbackArgs.score_feedback_display}
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
