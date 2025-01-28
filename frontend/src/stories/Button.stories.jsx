import Button from "../components/Button/Button";

export default {
    title: "Button/Button",
    component: Button,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        title: "Click me",
        onClick: () => {},
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

export const Inactive = {
    args: {
        title: "Click me",
        onClick: () => {},
        active: false,
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

export const WithValue = {
    args: {
        title: "Click me",
        onClick: () => {},
        value: "value",
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

export const Primary = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-primary",
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

export const Secondary = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-secondary",
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

export const Success = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-success",
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

export const Danger = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-danger",
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

export const Warning = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-warning",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <div className="btn-group">
                    <Story />
                </div>
            </div>
        ),
    ],
};

export const Info = {
    args: {
        title: "Click me",
        onClick: () => {},
        className: "btn-info",
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

export const WithAlternativePadding = {
    args: {
        title: "Click me",
        onClick: () => {},
        padding: "px-2",
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

export const WithOnClick = {
    args: {
        title: "Click me",
        onClick: () => alert("Clicked!"),
    },
    decorators: [
        (Story) => (
            <div style={{ width: "100%", height: "100%", backgroundColor: "#ddd" }}>
                <Story />
            </div>
        ),
    ],
};
