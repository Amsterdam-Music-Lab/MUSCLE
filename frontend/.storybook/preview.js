import { initialize, mswLoader } from 'msw-storybook-addon'
import "../public/vendor/bootstrap/bootstrap.min.css";
import "../src/index.scss";
import { initAudioListener } from "../src/util/audio";
import { initWebAudioListener } from "../src/util/webAudio";

// Init audio listener
initAudioListener();
initWebAudioListener();

// Initialize MSW
initialize({
    serviceWorker: {
        url: './mockServiceWorker.js',
    },
});

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
    // Provide the MSW addon loader globally
    loaders: [mswLoader],
};



export default preview;
