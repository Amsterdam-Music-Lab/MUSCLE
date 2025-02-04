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
        is_skippable: false,
        submits: false,
        style: "boolean",
        choices: {
            yes: "fa-check",
            unsure: "fa-question",
            no: "fa-xmark",
        },
        min_values: 1,
    },
    {
        key: "like_song",
        view: "ICON_RANGE",
        explainer: "",
        question: "2. How much do you like this song?",
        is_skippable: false,
        submits: false,
        style: "gradient-7",
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
    submit_label: "Submit",
    skip_label: "Skip",
    is_skippable: true,
    is_profile: true,
    ...overrides,
});

const getDefaultPlayback = (overrides = {}) => ({
    play_method: "NOAUDIO",
    view: "BUTTON",
    instruction: "This is the instruction",
    preload_message: "This is the preload message",
    play_config: {
        autoplay: true,
        controls: true,
        loop: true,
        muted: true,
        playback_rate: 1,
        preload: "auto",
    },
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
    config: {
        style: "PRELOAD",
        auto_advance: true,
        response_time: 1000,
        continue_label: "Continue",
        show_continue_button: true,
    },
    playback: getDefaultPlayback(),
    feedback_form: getDefaultFeedbackForm(),
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
    args: getDefaultArgs({
        config: {
            style: "boolean",
            auto_advance: true,
            response_time: 1000,
            continue_label: "Continue",
            show_continue_button: true,
        },
    }),
    decorators: [getDecorator,],
};

export const BooleanNegativeFirstColorScheme = {
    args: getDefaultArgs({
        config: {
            style: "boolean-negative-first",
            auto_advance: true,
            response_time: 1000,
            continue_label: "Continue",
            show_continue_button: true,
        },
    }),
    decorators: [getDecorator,],
};

export const NeutralColorScheme = {
    args: getDefaultArgs({
        config: {
            style: "neutral",
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
                    is_skippable: false,
                    submits: false,
                    style: "neutral",
                    choices: {
                        yes: "fa-check",
                        unsure: "fa-question",
                        no: "fa-xmark",
                    },
                    min_values: 1,
                },
                {
                    key: "like_song",
                    view: "ICON_RANGE",
                    explainer: "",
                    question: "2. How much do you like this song?",
                    is_skippable: false,
                    submits: false,
                    style: "neutral",
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
            submit_label: "Submit",
            skip_label: "Skip",
            is_skippable: true,
            is_profile: true,
        },
    }),
    decorators: [getDecorator,],
};

export const NeutralInvertedColorScheme = {
    args: getDefaultArgs({
        config: {
            style: "neutral-inverted",
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
                    is_skippable: false,
                    submits: false,
                    style: "neutral-inverted",
                    choices: {
                        yes: "fa-check",
                        unsure: "fa-question",
                        no: "fa-xmark",
                    },
                    min_values: 1,
                },
                {
                    key: "like_song",
                    view: "ICON_RANGE",
                    explainer: "",
                    question: "2. How much do you like this song?",
                    is_skippable: false,
                    submits: false,
                    style: "neutral-inverted",
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
            submit_label: "Submit",
            skip_label: "Skip",
            is_skippable: true,
            is_profile: true,
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
            timeout_after_playback: null,
            stop_audio_after: 5,
            resume_play: false,
            style: {
                root: "neutral-inverted"
            },
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
                    is_skippable: false,
                    submits: true,
                    style: "neutral-inverted",
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

export const Gradient7ColorScheme = {
    args: getDefaultArgs({
        config: {
            style: "gradient-7",
            auto_advance: true,
            response_time: 1000,
            continue_label: "Continue",
            show_continue_button: true,
        },
    }),
    decorators: [getDecorator,],
};
