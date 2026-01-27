import Question from "../components/Question/Question";
import useBoundStore from "@/util/stores";

export default {
    title: "Question/Question",
    component: Question,
    parameters: {
        layout: "fullscreen",
    },
};

const getDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPositive: '#39d7b8', colorNegative: '#fa5577', colorNeutral1: '#ffb14c', colorNeutral2: "#0cc7f1", colorNeutral3: "#2b2bee"});
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    )
}

export const Default = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            value: "",
            style: {},
            maxLength: 42,
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const WithOnChange = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            value: "",
            style: {},
            maxLength: 42
        },
        onChange: (value, id) => alert(`Question ${id} changed to ${value}`),
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const WithDisabledTrue = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            value: "",
            style: {},
            maxLength: 42
        },
        onChange: () => { },
        id: 0,
        disabled: true,
    },
    decorators: [getDecorator],
};

export const WithEmphasizeTitle = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            value: "",
            style: {"emphasize-title": true},
            maxLength: 42
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const Checkboxes = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "CHECKBOXES",
            value: "",
            choices: [{value: "1", label: "Choice 1"}, {value: "2", label: "Choice 2"}, {value: "3", label: "Choice 3"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const Dropdown = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "DROPDOWN",
            value: "",
            choices: [{value: "1", label: "Choice 1"}, {value: "2", label: "Choice 2"}, {value: "3", label: "Choice 3"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const Autocomplete = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "AUTOCOMPLETE",
            value: "",
            choices: [
                {value: "br", label: "Brazil"},
                {value: "cn", label: "China"},
                {value: "de", label: "Germany"},
                {value: "jp", label: "Japan"},
                {value: "nl", label: "Netherlands"},
                {value: "tr", label: "Turkey"},
                {value: "us", label: "United States"},
            ],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "100%",
                    height: "100%",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                    position: "relative",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Radios = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "RADIOS",
            value: "",
            choices: [{value: 1, label: "Choice 1", color: "colorPositive"}, {value: 2, label: "Choice 2", color: "colorNeutral1"}, {value: 3, label: "Choice 3", color: "colorNeutral2"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const Range = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "RANGE",
            value: "",
            choices: [{value: 1, label: "Choice 1"}, {value: 2, label: "Choice 2"}, {value: 3, label: "Choice 3"}],
            minValue: 1,
            maxValue: 42,
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const TextRange = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "TEXT_RANGE",
            value: "",
            choices: [{value: 1, label: "Choice 1"}, {value: 2, label: "Choice 2"}, {value: 3, label: "Choice 3"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const IconRange = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            icon: "🌎",
            view: "ICON_RANGE",
            value: "",
            choices: [{value: "globe", label: "fa-globe"}, {value: "pencil", label: "fa-pencil"}, {value: "bike", label: "fa-bicycle"}],
            minValue: 1,
            maxValue: 42,
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
    decorators: [getDecorator],
};

export const Number = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "NUMBER",
            minValue: 1,
            maxValue: 42,
        },
        onChange: () => { },
        value: "",
    },
    decorators: [getDecorator],
};

export const String = {
    args: {
        question: {
            text: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            maxLength: 9,
        },
        onChange: () => { },
        value: "",
    },
    decorators: [getDecorator],
};
