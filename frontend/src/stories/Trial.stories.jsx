import Trial from "../components/Trial/Trial";
import useBoundStore from "@/util/stores";

export default {
    title: "Trial/Trial",
    component: Trial,
    parameters: {
        layout: "fullscreen",
    },
};

const getDefaultFeedbackForm = (overrides = {}) => ({
    form: [{
        key: "know_song",
        view: "BUTTON_ARRAY",
        explainer: "",
        question: "1. Do you know this song?",
        choices: [
            {value: "yes", label: "Yes", color: "colorPositive"},
            {value: "unsure", label: "Unsure", color: "colorNeutral1"},
            {value: "no", label: "No", color: "colorNegative"},
        ],
    },
    {
        key: "like_song",
        view: "ICON_RANGE",
        explainer: "",
        question: "2. How much do you like this song?",
        style: {"gradient-7": true},
        choices:  [
            {value: 1, label: "fa-face-grin-hearts"},
            {value: 2, label: "fa-face-grin"},
            {value: 3, label: "fa-face-smile"},
            {value: 4, label: "fa-face-meh"},
            {value: 5, label: "fa-face-frown"},
            {value: 6, label: "fa-face-frown-open"},
            {value: 7, label: "fa-face-angry"},
        ],
    }],
    submitButton: {
        label: "Submit",
    },
    skipButton: {
        label: "Skip",
    },
    ...overrides,
});

const getDefaultPlayback = (overrides = {}) => ({
    view: "BUTTON",
    instruction: "This is the instruction",
    preloadMessage: "This is the preload message",
    mute: false,
    sections: [
        {
            playFrom: 0,
            label: "This is the first section",
            playMethod: "NOAUDIO",
            color: "colorNeutral2"
        },
        {
            playFrom: 0,
            label: "This is the second section",
            link: "Placeholder",
            color: "colorPrimary",
            playMethod: "NOAUDIO",
        },
    ],
    ...overrides,
});

const getDefaultArgs = (overrides = {}) => ({
    html: {
        body: "<p>This is <u>the</u> <b>HTML</b> <i>body</i></p>",
    },
    autoAdvance: true,
    responseTime: 100,
    continueButton: {label: "Continue"},
    playback: getDefaultPlayback(),
    feedbackForm: getDefaultFeedbackForm(),
    onNext: () => { },
    onResult: () => { },
    ...overrides,
});

const getDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2', colorPositive: '#39d7b8', colorNeutral1: '#ffb14c', colorNegative: '#fa5577', colorNeutral2: "#0cc7f1"});
    return (
        <div style={{ width: "100%", height: "100%", backgroundColor: "#fff", padding: "1rem" }}>
            <Story />
        </div>
    )
};

export const Default = {
    args: getDefaultArgs(),
    decorators: [getDecorator,],
};

