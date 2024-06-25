import Playback from "../components/Playback/Playback";

import audio from "./assets/audio.wav";

export default {
    title: "Playback",
    component: Playback,
    parameters: {
        layout: "fullscreen",
    },
};

export const Button = {
    args: {
        sections: [
            {
                id: 1,
                url: audio,
            },
        ],
        playerType: "BUTTON",
        onPreloadReady: () => {},
        instruction: "Click the button to play the audio.",
        preloadMessage: "Loading audio...",
        autoAdvance: false,
        responseTime: 5000,
        playConfig: {
            play_once: false,
            stop_audio_after: 0,
        },
        time: 0,
        submitResult: () => {},
        finishedPlaying: () => {},
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
