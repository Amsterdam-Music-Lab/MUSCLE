import { useState } from "react";
import Playback, { PlaybackProps } from "../components/Playback/Playback";
import { AUTOPLAY } from "../types/Playback";

import audio from "./assets/music.ogg";
import useBoundStore from "@/util/stores";
import { StoryFn } from "@storybook/react";

export default {
    title: "Playback/Playback",
    component: Playback,
    parameters: {
        layout: "fullscreen",
    },
};

// Create a decorator that dynamically accepts a play_method
const createCommonDecorator = (play_method: "BUFFER" | "EXTERNAL") => (Story: StoryFn) => {
    const [initialized, setInitialized] = useState(false);

    const setCurrentAction = useBoundStore((state) => state.setCurrentAction);
    setCurrentAction({
        view: "TRIAL_VIEW",
        playback: {
            view: AUTOPLAY,
            play_method,
            show_animation: true,
            preload_message: "Loading audio...",
            instruction: "Click the button to play the audio.",
            sections: [{ id: 0, url: audio }],
            play_from: 0.0,
            resume_play: false,
        }
    });

    if (!initialized) {
        return (
            <>
                <button onClick={() => setInitialized(true)}>
                    Initialize WebAudio
                </button>
            </>
        );
    }

    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    );
};

// Create playback arguments dynamically
const createPlaybackArgs = (play_method: "BUFFER" | "EXTERNAL"): PlaybackProps => ({
    playbackArgs: {
        view: AUTOPLAY,
        play_method,
        show_animation: true,
        preload_message: "Loading audio...",
        instruction: "Click the button to play the audio.",
        sections: [
            {
                id: 0,
                url: audio,
            }
        ],
        play_from: 0.0,
        resume_play: false,
    },
    onPreloadReady: () => { },
    autoAdvance: false,
    responseTime: 10,
    submitResult: () => { },
    finishedPlaying: () => { },
});

export const PlaybackAutoplayBuffer = {
    args: createPlaybackArgs("BUFFER"),
    decorators: [createCommonDecorator("BUFFER")],
};

export const PlaybackAutoplayExternal = {
    args: createPlaybackArgs("EXTERNAL"),
    decorators: [createCommonDecorator("EXTERNAL")],
};
