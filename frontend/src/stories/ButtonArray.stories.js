
import ButtonArray from '../components/Question/_ButtonArray';

export default {
    title: 'ButtonArray',
    component: ButtonArray,
    parameters: {
        layout: 'fullscreen',
    },
};


export const Default = {
    args: {
        question: {
            question: "This is the question",
            explainer: "This is the explainer",
            view: "BUTTON_ARRAY",
            value: "",
            choices: [
                "Choice 1",
                "Choice 2",
                "Choice 3",
            ],
        },
        onChange: () => { },
        id: 0,
        active: true,
        style: {},
        emphasizeTitle: false,
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const CategorizationWithHiddenText = {
    args: {
        question: {
            "key": "choice",
            "view": "BUTTON_ARRAY",
            "explainer": "",
            "question": "",
            "result_id": 16549,
            "is_skippable": false,
            "submits": true,
            "style": {
                "invisible-text": true,
                "buttons-large-gap": true,
                "buttons-large-text": true,
                "neutral-inverted": true
            },
            "choices": {
                "A": "___",
                "B": "___"
            },
            "min_values": 1,
            "expected_response": "A"
        },
        onChange: () => { },
        id: 0,
        active: true,
        style: {},
        emphasizeTitle: false,
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
}
