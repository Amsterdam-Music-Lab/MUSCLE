import ButtonArray from "../components/Question/_ButtonArray";
import useBoundStore from "@/util/stores";

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

const ButtonArrayDecorator = (Story) => {
    StoreDecorator();
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    );
}

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPositive: '#39d7b8', colorNegative: '#fa5577', colorNeutral1: '#ffb14c', colorNeutral2: "#0cc7f1", colorNeutral3: "#2b2bee"});
};

export const Default = {
    args: getArgs(),
    decorators: [ButtonArrayDecorator],
};

export const Disabled = {
    args: getArgs({ disabled: true }),
    decorators: [ButtonArrayDecorator],
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
            },
            choices: [
                {value: "A", label: "   ", color: "colorNeutral1"},
                {value: "B", label: "   ", color: "colorNeutral2"},
            ],
            expectedResponse: "A",
        },
    }),
    decorators: [ButtonArrayDecorator],
};

export const CategorizationWithHiddenTextDisabled = {
    args: getArgs({
        disabled: true,
        question: {
            key: "choice",
            view: "BUTTON_ARRAY",
            explainer: "",
            text: "",
            choices: [
                {value: "A", label: "   ", color: "colorNeutral1"},
                {value: "B", label: "   ", color: "colorNeutral2"},
            ],
            expectedResponse: "A",
            style: {
                "invisible-text": true,
                "buttons-large-gap": true,
                "buttons-large-text": true,
            }
        },
    }),
    decorators: [ButtonArrayDecorator],
};

export const BooleanColorScheme = {
    args: getArgs({question: {
        key: "truth",
        choices: [
            {value: "true", label: "True", color: "colorPositive"},
            {value: "false", label: "False", color: "colorNegative"}
        ]
    }}),
    decorators: [ButtonArrayDecorator],
};
