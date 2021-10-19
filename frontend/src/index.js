import "./index.css";
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App/App";
import { initAudioListener } from "./util/audio";

// Init audio listener
initAudioListener();

// Create app
ReactDOM.render(<App />, document.getElementById("root"));

// import * as serviceWorker from "./serviceWorker";
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
