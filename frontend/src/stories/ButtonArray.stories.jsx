import ButtonArray from "../components/Question/_ButtonArray";

export default {
    title: "Question/ButtonArray",
    component: ButtonArray,
    parameters: {
        layout: "fullscreen",
    },
};

const defaultArgs = {
    question: {
        question: "This is the question",
        explainer: "This is the explainer",
        view: "BUTTON_ARRAY",
        value: "",
        choices: [{value: 1, label: "Choice 1", color: "colorNeutral1"}, {value: 2, label: "Choice 2", color: "colorNeutral2"}, {value: 3, label: "Choice 3", color: "colorNeutral3"}],
    },
    onChange: () => { },
    id: 0,
    active: true,
    style: {},
};

const getArgs = (args = {}) => ({ ...defaultArgs, ...args });

export const Default = {
    args: getArgs(),
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Disabled = {
    args: getArgs({ disabled: true }),
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const CategorizationWithHiddenText = {
    args: getArgs({
        question: {
            key: "choice",
            view: "BUTTON_ARRAY",
            explainer: "",
            question: "",
            resultId: 16549,
            style: {
                "invisible-text": true,
                "buttons-large-gap": true,
                "buttons-large-text": true,
                "neutral-inverted": true,
            },
            choices: {
                A: "___",
                B: "___",
            },
            minValues: 1,
            expectedResponse: "A",
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const CategorizationWithHiddenTextDisabled = {
    args: getArgs({
        disabled: true,
        question: {
            key: "choice",
            view: "BUTTON_ARRAY",
            explainer: "",
            question: "",
            style: {
                "invisible-text": true,
                "buttons-large-gap": true,
                "buttons-large-text": true,
                "neutral-inverted": true,
            },
            choices: {
                A: "___",
                B: "___",
            },
            minValues: 1,
            expectedResponse: "A",
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const BooleanColorScheme = {
    args: getArgs(),
    decorators: [
        (Story) => (
            <div
                className="boolean"
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const BooleanNegativeFirstColorScheme = {
    args: getArgs(),
    decorators: [
        (Story) => (
            <div
                className="boolean-negative-first"
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NeutralColorScheme = {
    args: getArgs(),
    decorators: [
        (Story) => (
            <div
                className="neutral"
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NeutralInvertedColorScheme = {
    args: getArgs(),
    decorators: [
        (Story) => (
            <div
                className="neutral-inverted"
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
