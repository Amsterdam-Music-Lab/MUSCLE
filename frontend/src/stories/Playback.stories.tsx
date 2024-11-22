import { useState } from "react";
import Playback, { PlaybackProps } from "../components/Playback/Playback";
import { AUTOPLAY } from "../types/Playback";

import audio from "./assets/music.ogg";

export default {
    title: "Playback",
    component: Playback,
    parameters: {
        layout: "fullscreen",
    },
};

export const Button = {
    args: {
        playbackArgs: {
            view: AUTOPLAY,
            play_method: "BUFFER",
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
    } as PlaybackProps,
    decorators: [
        (Story) => {

            const [initialized, setInitialized] = useState(false);


            if (!initialized) {
                return (
                    <>
                        <button onClick={() => {
                            setInitialized(true);
                        }
                        }>
                            Initialize WebAudio
                        </button>
                    </>
                )
            }

            return (
                <div
                    style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
                >
                    <Story />
                </div>
            )
        }
    ],
};
