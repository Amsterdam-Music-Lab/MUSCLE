import Question from "../components/Question/Question";

export default {
    title: "Question/Question",
    component: Question,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        question: {
            question: "This is the question",
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

export const WithOnChange = {
    args: {
        question: {
            question: "This is the question",
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

export const WithDisabledTrue = {
    args: {
        question: {
            question: "This is the question",
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

export const WithEmphasizeTitle = {
    args: {
        question: {
            question: "This is the question",
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

export const Checkboxes = {
    args: {
        question: {
            question: "This is the question",
            explainer: "This is the explainer",
            view: "CHECKBOXES",
            value: "",
            choices: [{value: 1, label: "Choice 1"}, {value: 2, label: "Choice 2"}, {value: 3, label: "Choice 3"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
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

export const Dropdown = {
    args: {
        question: {
            question: "This is the question",
            explainer: "This is the explainer",
            view: "DROPDOWN",
            value: "",
            choices: [{value: 1, label: "Choice 1"}, {value: 2, label: "Choice 2"}, {value: 3, label: "Choice 3"}],
            style: {},
        },
        onChange: () => { },
        id: 0,
        active: true,
    },
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

export const Autocomplete = {
    args: {
        question: {
            question: "This is the question",
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
            question: "This is the question",
            explainer: "This is the explainer",
            view: "RADIOS",
            value: "",
            choices: [{value: 1, label: "Choice 1"}, {value: 2, label: "Choice 2"}, {value: 3, label: "Choice 3"}],
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

export const Range = {
    args: {
        question: {
            question: "This is the question",
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
    decorators: [
        (Story) => {
            return (
                <div
                    style={{
                        width: "100%",
                        height: "100%",
                        backgroundColor: "#ddd",
                        padding: "3rem",
                        position: "relative",
                    }}
                >
                    <Story />
                </div>
            );
        },
    ],
};

export const TextRange = {
    args: {
        question: {
            question: "This is the question",
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
    decorators: [
        (Story) => {
            return (
                <div
                    style={{
                        width: "100%",
                        height: "100%",
                        backgroundColor: "#ddd",
                        padding: "3rem",
                        position: "relative",
                    }}
                >
                    <Story />
                </div>
            );
        },
    ],
};

export const IconRange = {
    args: {
        question: {
            question: "This is the question",
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
    decorators: [
        (Story) => {
            return (
                <div
                    style={{
                        width: "100%",
                        height: "100%",
                        backgroundColor: "#ddd",
                        padding: "3rem",
                        position: "relative",
                    }}
                >
                    <Story />
                </div>
            );
        },
    ],
};

export const Number = {
    args: {
        question: {
            question: "This is the question",
            explainer: "This is the explainer",
            view: "NUMBER",
            minValue: 1,
            maxValue: 42,
        },
        onChange: () => { },
        value: "",
    },
    decorators: [
        (Story) => {
            return (
                <div
                    style={{
                        width: "100%",
                        height: "100%",
                        backgroundColor: "#ddd",
                        padding: "3rem",
                        position: "relative",
                    }}
                >
                    <Story />
                </div>
            );
        },
    ],
};

export const String = {
    args: {
        question: {
            question: "This is the question",
            explainer: "This is the explainer",
            view: "STRING",
            maxLength: 9,
        },
        onChange: () => { },
        value: "",
    },
    decorators: [
        (Story) => {
            return (
                <div
                    style={{
                        width: "100%",
                        height: "100%",
                        backgroundColor: "#ddd",
                        padding: "3rem",
                        position: "relative",
                    }}
                >
                    <Story />
                </div>
            );
        },
    ],
};
