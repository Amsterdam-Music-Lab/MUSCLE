import Trial from '../components/Trial/Trial';

export default {
    title: 'Trial',
    component: Trial,
    parameters: {
        layout: 'fullscreen',
    },
};

export const Default = {
    args: {
        html: {
            body: "<p>This is <u>the</u> <b>HTML</b> <i>body</i></p>",
        },
        config: {
            style: "AUTOPLAY",
            auto_advance: true,
            response_time: 1000,
            continue_label: "Continue",
            show_continue_button: true,
        },
        playback: {
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
        },
        feedback_form: {
            form: [{
                key: "msi_14_never_complimented",
                view: "TEXT_RANGE",
                value: "",
                question: "Ik heb nog nooit complimenten gekregen voor mijn talenten als muzikant.",
                explainer: "In hoeverre ben je het hiermee eens of oneens?",
                result_id: 18,
                style: "neutral",
                scoring_rule: "LIKERT",
                scale_steps: 7,
                choices: {
                    "1": "Helemaal mee oneens",
                    "2": "Zeer mee oneens",
                    "3": "Mee oneens",
                    "4": "Niet mee eens of oneens",
                    "5": "Mee eens",
                    "6": "Zeer mee eens",
                    "7": "Helemaal mee eens"
                }
            }],
            submit_label: "Submit",
            skip_label: "Skip",
            is_skippable: true,
            is_profile: true,
        },
        onNext: () => { },
        onResult: () => { },
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#fff', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};
