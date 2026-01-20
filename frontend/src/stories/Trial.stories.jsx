import Trial from "../components/Trial/Trial";

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
        style: {"boolean": true},
        choices: {
            yes: "fa-check",
            unsure: "fa-question",
            no: "fa-xmark",
        },
        minValues: 1,
    },
    {
        key: "like_song",
        view: "ICON_RANGE",
        explainer: "",
        question: "2. How much do you like this song?",
        style: {"gradient-7": true},
        choices: {
            1: "fa-face-grin-hearts",
            2: "fa-face-grin",
            3: "fa-face-smile",
            4: "fa-face-meh",
            5: "fa-face-frown",
            6: "fa-face-frown-open",
            7: "fa-face-angry",
        },
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
    playMethod: "NOAUDIO",
    view: "BUTTON",
    instruction: "This is the instruction",
    preloadMessage: "This is the preload message",
    mute: false,
    sections: [
        {
            start: 0,
            end: 10,
            text: "This is the first section",
        },
        {
            start: 10,
            end: 20,
            text: "This is the second section",
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

const getDecorator = (Story) => (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#fff", padding: "1rem" }}>
        <Story />
    </div>
);

export const Default = {
    args: getDefaultArgs(),
    decorators: [getDecorator,],
};

export const BooleanColorScheme = {
    args: getDefaultArgs(),
    decorators: [getDecorator,],
};

export const BooleanNegativeFirstColorScheme = {
    args: getDefaultArgs(),
    decorators: [getDecorator,],
};

export const NeutralColorScheme = {
    args: getDefaultArgs({
        feedbackForm: {
            form: [
                {
                    key: "know_song",
                    view: "BUTTON_ARRAY",
                    explainer: "",
                    question: "1. Do you know this song?",
                    style: {"neutral": true},
                    choices: {
                        yes: "fa-check",
                        unsure: "fa-question",
                        no: "fa-xmark",
                    },
                    minValues: 1,
                },
                {
                    key: "like_song",
                    view: "ICON_RANGE",
                    explainer: "",
                    question: "2. How much do you like this song?",
                    style: {"gradient-7": true},
                    choices: {
                        1: "fa-face-grin-hearts",
                        2: "fa-face-grin",
                        3: "fa-face-smile",
                        4: "fa-face-meh",
                        5: "fa-face-frown",
                        6: "fa-face-frown-open",
                        7: "fa-face-angry",
                    },
                }
            ],
            submitButton: {label: "Submit"},
            skipButton: {label: "Skip"},
        },
    }),
    decorators: [getDecorator,],
};

export const NeutralInvertedColorScheme = {
    args: getDefaultArgs({
        config: {
            auto_advance: true,
            response_time: 1000,
            continue_label: "Continue",
            show_continue_button: true,
        },
        feedback_form: {
            form: [
                {
                    key: "know_song",
                    view: "BUTTON_ARRAY",
                    explainer: "",
                    question: "1. Do you know this song?",
                    style: {"neutral-inverted": true},
                    choices: {
                        yes: "fa-check",
                        unsure: "fa-question",
                        no: "fa-xmark",
                    },
                    minValues: 1,
                },
                {
                    key: "like_song",
                    view: "ICON_RANGE",
                    explainer: "",
                    question: "2. How much do you like this song?",
                    style: {"gradient-7": true},
                    choices: {
                        1: "fa-face-grin-hearts",
                        2: "fa-face-grin",
                        3: "fa-face-smile",
                        4: "fa-face-meh",
                        5: "fa-face-frown",
                        6: "fa-face-frown-open",
                        7: "fa-face-angry",
                    },
                }
            ],
            submitButton: {
                label: "Submit"
            },
            skipButton: {
                label: "Skip"
            },
        },
    }),
    decorators: [getDecorator,],
};

export const ToontjeHoger4Absolute = {
    args: getDefaultArgs({
        config: {
            response_time: 5,
            auto_advance: false,
            listen_first: false,
            show_continue_button: true,
            continue_label: "Continue"
        },
        playback: {
            sections: [
                {
                    "id": 2,
                    "url": "http://localhost:8000/section/2/13319/",
                },
                {
                    "id": 3,
                    "url": "http://localhost:8000/section/3/94320/",
                }
            ],
            play_method: "EXTERNAL",
            show_animation: false,
            preload_message: "",
            instruction: "",
            play_from: 0,
            mute: false,
            resume_play: false,
            style: {"neutral-inverted": true},
            ID: "MULTIPLAYER",
            play_once: false,
            labels: [
                "A",
                "B"
            ],
            view: "MULTIPLAYER"
        },
        feedback_form: {
            form: [
                {
                    key: "pitch",
                    view: "BUTTON_ARRAY",
                    explainer: "",
                    question: "Welk fragment heeft de juiste toonhoogte?",
                    style: {"neutral-inverted": true},
                    choices: {
                        A: "A",
                        B: "B"
                    },
                    expected_response: "A"
                }
            ],
            submit_label: "Continue",
            skip_label: "Skip",
            is_skippable: false
        }
    }),
    decorators: [getDecorator,],
}
