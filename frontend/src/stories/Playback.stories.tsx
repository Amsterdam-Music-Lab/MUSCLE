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
const createCommonDecorator = (playMethod: "BUFFER" | "EXTERNAL") => (Story: StoryFn) => {

    const setCurrentAction = useBoundStore((state) => state.setCurrentAction);
    setCurrentAction({
        view: "TRIAL_VIEW",
        playback: {
            view: AUTOPLAY,
            showAnimation: true,
            preloadMessage: "Loading audio...",
            instruction: "Click the button to play the audio.",
            sections: [{ link: audio, color: 'colorPrimary', playMethod, playFrom: 0.0 }],
            mute: false,
            resumePlay: false,
        }
    });

    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    );
};

// Create playback arguments dynamically
const createPlaybackArgs = (playMethod: "BUFFER" | "EXTERNAL"): PlaybackProps => ({
    view: AUTOPLAY,
    showAnimation: true,
    preloadMessage: "Loading audio...",
    instruction: "Click the button to play the audio.",
    sections: [
        {
            link: audio,
            label: "",
            playMethod,
            playFrom: 0.0,
        }
    ],
    resumePlay: false,
    onPreloadReady: () => { },
    autoAdvance: false,
    responseTime: 10,
    submitResult: () => { },
    finishedPlaying: () => { },
    mute: false
});

export const PlaybackAutoplayBuffer = {
    args: createPlaybackArgs("BUFFER"),
    decorators: [createCommonDecorator("BUFFER")],
};

export const PlaybackAutoplayExternal = {
    args: createPlaybackArgs("EXTERNAL"),
    decorators: [createCommonDecorator("EXTERNAL")],
};
