import "../public/vendor/bootstrap/bootstrap.min.css";
import "../src/index.css";
import { initAudioListener } from "../src/util/audio";
import { initWebAudioListener } from "../src/util/webAudio";

// Init audio listener
initAudioListener();
initWebAudioListener();

/** @type { import('@storybook/react').Preview } */
const preview = {
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
    },
};



export default preview;
