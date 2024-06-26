import "./index.scss";
import { StrictMode } from "react";
import { createRoot } from 'react-dom/client';
import App from "./components/App/App.tsx";
import { initSentry } from "./config/sentry";
import { initAudioListener } from "./util/audio";
import { initWebAudioListener } from "./util/webAudio";

// Init sentry
initSentry();

// Init audio listener
initAudioListener();
initWebAudioListener();

// Create app
const container = document.getElementById("root");
const root = createRoot(container);
root.render(
    import.meta.env.VITE_STRICT === 'true' ? (
        <StrictMode>
            <App />
        </StrictMode>
    ) : (
        <App />
    )
);

// import * as serviceWorker from "./serviceWorker";
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
