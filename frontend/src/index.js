import "./index.css";
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App/App";
import { initSentry } from "./config/sentry";
import { initAudioListener } from "./util/audio";
import { initWebAudioListener } from "./util/webAudio";

// Init sentry
initSentry();

// Init audio listener
initAudioListener();
initWebAudioListener();


// Create app
ReactDOM.render(<App />, document.getElementById("root"));

// import * as serviceWorker from "./serviceWorker";
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
