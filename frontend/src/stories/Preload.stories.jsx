import Playback from "../components/Preload/Preload";

import audio from "./assets/audio.wav";

export default {
    title: "Playback/Preload",
    component: Playback,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        instruction: "Click the button to play the audio.",
        pageTitle: "Listen to the audio",
        duration: 0,
        sections: [
            {
                link: audio,
                playMethod: "EXTERNAL"
            },
        ],
        onNext: () => {},
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
